import os
import logging
import sqlite3
import random
from datetime import datetime, time
from io import BytesIO
from groq import Groq
from telegram import Update, ForceReply
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from docx import Document
import pytz

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Configuration from environment variables
TELEGRAM_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
GROQ_API_KEY = os.getenv('GROQ_API_KEY')
PROMPT_TIME = os.getenv('PROMPT_TIME', '09:00')  # Default 9 AM
TIMEZONE = os.getenv('TIMEZONE', 'UTC')

# Initialize Groq
client = Groq(api_key=GROQ_API_KEY)

# Database setup
def init_db():
    """Initialize SQLite database"""
    conn = sqlite3.connect('prompter_bot.db')
    c = conn.cursor()
    
    # Questions table
    c.execute('''CREATE TABLE IF NOT EXISTS questions
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  question TEXT NOT NULL,
                  source TEXT,
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                  times_asked INTEGER DEFAULT 0,
                  last_asked TIMESTAMP)''')
    
    # Responses table
    c.execute('''CREATE TABLE IF NOT EXISTS responses
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  user_id INTEGER,
                  question_id INTEGER,
                  response TEXT,
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                  FOREIGN KEY (question_id) REFERENCES questions(id))''')
    
    # User settings
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (user_id INTEGER PRIMARY KEY,
                  chat_id INTEGER,
                  username TEXT,
                  prompt_time TEXT,
                  timezone TEXT,
                  active BOOLEAN DEFAULT 1,
                  joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    
    conn.commit()
    conn.close()

# Database functions
def add_question(question, source="manual"):
    """Add a question to the database"""
    conn = sqlite3.connect('prompter_bot.db')
    c = conn.cursor()
    c.execute('INSERT INTO questions (question, source) VALUES (?, ?)', (question, source))
    conn.commit()
    conn.close()

def get_random_question():
    """Get a random question from the database"""
    conn = sqlite3.connect('prompter_bot.db')
    c = conn.cursor()
    c.execute('SELECT id, question FROM questions ORDER BY RANDOM() LIMIT 1')
    result = c.fetchone()
    conn.close()
    return result

def update_question_asked(question_id):
    """Update when a question was last asked"""
    conn = sqlite3.connect('prompter_bot.db')
    c = conn.cursor()
    c.execute('''UPDATE questions 
                 SET times_asked = times_asked + 1, 
                     last_asked = CURRENT_TIMESTAMP 
                 WHERE id = ?''', (question_id,))
    conn.commit()
    conn.close()

def save_response(user_id, question_id, response):
    """Save user's response"""
    conn = sqlite3.connect('prompter_bot.db')
    c = conn.cursor()
    c.execute('INSERT INTO responses (user_id, question_id, response) VALUES (?, ?, ?)',
              (user_id, question_id, response))
    conn.commit()
    conn.close()

def add_or_update_user(user_id, chat_id, username):
    """Add or update user in database"""
    conn = sqlite3.connect('prompter_bot.db')
    c = conn.cursor()
    c.execute('''INSERT OR REPLACE INTO users (user_id, chat_id, username, prompt_time, timezone)
                 VALUES (?, ?, ?, ?, ?)''',
              (user_id, chat_id, username, PROMPT_TIME, TIMEZONE))
    conn.commit()
    conn.close()

def get_all_active_users():
    """Get all active users for daily prompts"""
    conn = sqlite3.connect('prompter_bot.db')
    c = conn.cursor()
    c.execute('SELECT user_id, chat_id FROM users WHERE active = 1')
    results = c.fetchall()
    conn.close()
    return results

def extract_text_from_docx(file_bytes):
    """Extract text from Word document"""
    doc = Document(BytesIO(file_bytes))
    text = '\n'.join([paragraph.text for paragraph in doc.paragraphs if paragraph.text.strip()])
    return text

async def generate_questions_from_text(text, num_questions=5):
    """Use Groq AI to generate questions from document text"""
    prompt = f"""You are an educational question generator. Based on the following text, generate {num_questions} thoughtful questions that would help someone learn and review this material.

Make the questions:
- Clear and specific
- Thought-provoking
- Varied in difficulty
- Focused on key concepts

Text:
{text[:3000]}

Return ONLY the questions, one per line, numbered 1-{num_questions}."""

    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="llama-3.1-70b-versatile",  # Fast and high quality
            temperature=0.7,
        )
        
        response_text = chat_completion.choices[0].message.content
        questions = response_text.strip().split('\n')
        
        # Clean up the questions
        cleaned = []
        for q in questions:
            q = q.strip()
            # Remove numbering
            if q and len(q) > 3:
                # Remove leading numbers and dots
                q = q.lstrip('0123456789.)-• ').strip()
                if q:
                    cleaned.append(q)
        return cleaned[:num_questions]
    except Exception as e:
        logger.error(f"Error generating questions: {e}")
        return []

async def generate_new_question():
    """Use Groq AI to generate a completely new question based on question bank context"""
    conn = sqlite3.connect('prompter_bot.db')
    c = conn.cursor()
    c.execute('SELECT question FROM questions ORDER BY RANDOM() LIMIT 5')
    sample_questions = [row[0] for row in c.fetchall()]
    conn.close()
    
    if not sample_questions:
        return None
    
    prompt = f"""Based on these example questions from a learning question bank, generate 1 NEW thoughtful question in a similar style and topic area:

Examples:
{chr(10).join(f"- {q}" for q in sample_questions)}

Generate 1 new question that:
- Is related to similar topics
- Has similar depth and style
- Would help with learning/review
- Is clear and specific

Return ONLY the new question, no explanation."""

    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="llama-3.1-70b-versatile",
            temperature=0.8,
        )
        
        new_question = chat_completion.choices[0].message.content.strip()
        return new_question
    except Exception as e:
        logger.error(f"Error generating new question: {e}")
        return None

# Bot command handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command"""
    user = update.effective_user
    add_or_update_user(user.id, update.effective_chat.id, user.username)
    
    await update.message.reply_html(
        f"👋 Hi {user.mention_html()}!\n\n"
        f"I'm your AI-powered daily prompter bot!\n\n"
        f"📝 <b>What I can do:</b>\n"
        f"• Send you daily prompts at {PROMPT_TIME} ({TIMEZONE})\n"
        f"• Accept Word files (.docx) to build your question bank\n"
        f"• Generate AI questions from your documents\n"
        f"• Track your responses over time\n\n"
        f"📤 <b>Upload a Word file</b> to get started!\n"
        f"Or use /help to see all commands."
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command"""
    help_text = """
🤖 <b>Available Commands:</b>

/start - Start the bot
/help - Show this help message
/prompt - Get a question now
/stats - See your statistics
/stop - Pause daily prompts
/resume - Resume daily prompts

📤 <b>Upload Word Files:</b>
Just send me a .docx file and I'll:
1. Extract the content
2. Generate questions using AI
3. Add them to your question bank

💡 <b>How it works:</b>
Every day at your scheduled time, I'll send you a question. You can answer right away or whenever you have time. Your responses are saved for tracking progress!
"""
    await update.message.reply_html(help_text)

async def prompt_now(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /prompt command - send a question immediately"""
    await send_daily_prompt(update.effective_chat.id, context.application)

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show user statistics"""
    user_id = update.effective_user.id
    
    conn = sqlite3.connect('prompter_bot.db')
    c = conn.cursor()
    
    # Get total questions in bank
    c.execute('SELECT COUNT(*) FROM questions')
    total_questions = c.fetchone()[0]
    
    # Get user's response count
    c.execute('SELECT COUNT(*) FROM responses WHERE user_id = ?', (user_id,))
    response_count = c.fetchone()[0]
    
    # Get recent responses
    c.execute('''SELECT r.created_at, q.question, r.response 
                 FROM responses r 
                 JOIN questions q ON r.question_id = q.id 
                 WHERE r.user_id = ? 
                 ORDER BY r.created_at DESC 
                 LIMIT 5''', (user_id,))
    recent = c.fetchall()
    
    conn.close()
    
    stats_text = f"""
📊 <b>Your Statistics</b>

🏦 Question Bank: {total_questions} questions
✅ Your Responses: {response_count}
📅 Active since: {datetime.now().strftime('%Y-%m-%d')}

<b>Recent Activity:</b>
"""
    
    if recent:
        for created, question, response in recent:
            date = datetime.fromisoformat(created).strftime('%m/%d')
            stats_text += f"\n📌 {date}: {question[:50]}..."
    else:
        stats_text += "\nNo responses yet! Use /prompt to get started."
    
    await update.message.reply_html(stats_text)

async def stop_prompts(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Pause daily prompts"""
    user_id = update.effective_user.id
    conn = sqlite3.connect('prompter_bot.db')
    c = conn.cursor()
    c.execute('UPDATE users SET active = 0 WHERE user_id = ?', (user_id,))
    conn.commit()
    conn.close()
    
    await update.message.reply_text("⏸ Daily prompts paused. Use /resume to start again.")

async def resume_prompts(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Resume daily prompts"""
    user_id = update.effective_user.id
    conn = sqlite3.connect('prompter_bot.db')
    c = conn.cursor()
    c.execute('UPDATE users SET active = 1 WHERE user_id = ?', (user_id,))
    conn.commit()
    conn.close()
    
    await update.message.reply_text(f"▶️ Daily prompts resumed! You'll receive prompts at {PROMPT_TIME} ({TIMEZONE}).")

async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle Word document uploads"""
    document = update.message.document
    
    if not document.file_name.endswith('.docx'):
        await update.message.reply_text("❌ Please send a .docx file (Word document).")
        return
    
    await update.message.reply_text("📥 Processing your document...")
    
    # Download file
    file = await context.bot.get_file(document.file_id)
    file_bytes = await file.download_as_bytearray()
    
    # Extract text
    text = extract_text_from_docx(bytes(file_bytes))
    
    if not text or len(text) < 50:
        await update.message.reply_text("❌ Could not extract enough text from the document. Please check the file.")
        return
    
    await update.message.reply_text("🤖 Generating questions with AI... This may take a moment.")
    
    # Generate questions using AI
    questions = await generate_questions_from_text(text, num_questions=10)
    
    if not questions:
        await update.message.reply_text("❌ Could not generate questions. Please try again.")
        return
    
    # Save questions to database
    for question in questions:
        add_question(question, source=document.file_name)
    
    await update.message.reply_html(
        f"✅ <b>Success!</b> Generated and saved {len(questions)} questions from your document.\n\n"
        f"📝 <b>Sample questions:</b>\n"
        + "\n".join(f"• {q}" for q in questions[:3])
        + f"\n\n💡 Use /prompt to get a question now!"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle text messages (save as responses to last question)"""
    user_id = update.effective_user.id
    response_text = update.message.text
    
    # Check if there's a recent question for this user
    conn = sqlite3.connect('prompter_bot.db')
    c = conn.cursor()
    c.execute('''SELECT question_id FROM responses 
                 WHERE user_id = ? 
                 ORDER BY created_at DESC LIMIT 1''', (user_id,))
    result = c.fetchone()
    conn.close()
    
    if result:
        # This might be a response to the last question
        # For now, just acknowledge
        await update.message.reply_text(
            "📝 Response noted! Use /prompt to get another question."
        )
    else:
        await update.message.reply_text(
            "👋 Send me a Word file (.docx) to build your question bank, or use /prompt to get a question!"
        )

async def send_daily_prompt(chat_id, application):
    """Send a daily prompt to a user"""
    # Randomly choose between existing question or AI-generated new question
    use_ai = random.random() < 0.3  # 30% chance of AI-generated question
    
    question_text = None
    question_id = None
    
    if use_ai:
        question_text = await generate_new_question()
        if question_text:
            # Save the new AI-generated question
            add_question(question_text, source="AI-generated")
            conn = sqlite3.connect('prompter_bot.db')
            c = conn.cursor()
            c.execute('SELECT id FROM questions WHERE question = ? ORDER BY id DESC LIMIT 1', (question_text,))
            result = c.fetchone()
            if result:
                question_id = result[0]
            conn.close()
    
    if not question_text:
        # Fallback to random question from bank
        result = get_random_question()
        if result:
            question_id, question_text = result
    
    if not question_text:
        await application.bot.send_message(
            chat_id=chat_id,
            text="⚠️ No questions in your bank yet! Upload a Word file to get started."
        )
        return
    
    # Update question stats
    if question_id:
        update_question_asked(question_id)
    
    # Send the question
    await application.bot.send_message(
        chat_id=chat_id,
        text=f"💭 <b>Daily Prompt</b>\n\n{question_text}\n\n<i>Reply with your answer anytime!</i>",
        parse_mode='HTML'
    )

async def scheduled_daily_prompt(context: ContextTypes.DEFAULT_TYPE):
    """Scheduled function to send daily prompts to all active users"""
    users = get_all_active_users()
    logger.info(f"Sending daily prompts to {len(users)} active users")
    
    for user_id, chat_id in users:
        try:
            await send_daily_prompt(chat_id, context.application)
        except Exception as e:
            logger.error(f"Error sending prompt to user {user_id}: {e}")

def main():
    """Start the bot"""
    # Initialize database
    init_db()
    
    # Create application
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("prompt", prompt_now))
    application.add_handler(CommandHandler("stats", stats))
    application.add_handler(CommandHandler("stop", stop_prompts))
    application.add_handler(CommandHandler("resume", resume_prompts))
    application.add_handler(MessageHandler(filters.Document.ALL, handle_document))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Setup scheduler for daily prompts
    scheduler = AsyncIOScheduler(timezone=pytz.timezone(TIMEZONE))
    hour, minute = map(int, PROMPT_TIME.split(':'))
    scheduler.add_job(
        scheduled_daily_prompt,
        CronTrigger(hour=hour, minute=minute),
        args=[application]
    )
    scheduler.start()
    
    logger.info(f"Bot started. Daily prompts scheduled for {PROMPT_TIME} {TIMEZONE}")
    
    # Start the bot
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
