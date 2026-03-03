# 🤖 AI-Powered Telegram Prompter Bot

A free, AI-powered Telegram bot that sends you daily learning prompts, accepts Word document uploads to build question banks, and uses Google Gemini AI to generate intelligent questions.

## ✨ Features

- 📅 **Daily Prompts** - Scheduled questions at your preferred time
- 📤 **Word File Upload** - Upload .docx files to automatically generate questions
- 🤖 **AI-Powered** - Uses Groq (Llama 3.1) to create thoughtful questions
- 💾 **Question Bank** - Stores all questions in a local database
- 📊 **Progress Tracking** - Monitor your responses over time
- 🆓 **100% Free** - Uses free tiers of Render.com and Groq AI
- 🌍 **Available Worldwide** - Works in all countries

## 🚀 Quick Start Guide

### Step 1: Get Your API Keys

#### A. Create Telegram Bot
1. Open Telegram and search for [@BotFather](https://t.me/botfather)
2. Send `/newbot` command
3. Choose a name for your bot (e.g., "My Prompter Bot")
4. Choose a username (must end in 'bot', e.g., "myprompt_bot")
5. **Copy the token** - it looks like: `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz`

#### B. Get Google Gemini API Key (Free)
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click **"Get API Key"** or **"Create API Key"**
4. **Copy the API key** - it looks like: `AIzaSyABCD1234...`

### Step 2: Deploy to Render.com

#### A. Prepare Your Code
1. **Fork this repository** or create a new GitHub repository
2. Upload all these files to your GitHub repo:
   - `bot.py`
   - `requirements.txt`
   - `render.yaml`

#### B. Deploy on Render
1. Go to [Render.com](https://render.com) and sign up (free)
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub account
4. Select your repository
5. Render will auto-detect settings from `render.yaml`
6. Click **"Advanced"** and add environment variables:
   - `TELEGRAM_BOT_TOKEN` = (paste your token from BotFather)
   - `GROQ_API_KEY` = (paste your Groq API key)
   - `PROMPT_TIME` = `09:00` (or your preferred time in HH:MM format)
   - `TIMEZONE` = `UTC` (or your timezone like `Asia/Jakarta`)
7. Click **"Create Web Service"**

#### C. Wait for Deployment
- First deployment takes 3-5 minutes
- Watch the logs for "Bot started" message
- Your bot is now running 24/7! 🎉

### Step 3: Start Using Your Bot

1. Open Telegram and search for your bot username
2. Send `/start` to begin
3. Upload a Word file (.docx) to build your question bank
4. Use `/prompt` to get a question immediately
5. Wait for your daily scheduled prompt!

## 📱 Bot Commands

| Command | Description |
|---------|-------------|
| `/start` | Initialize the bot and register |
| `/help` | Show help message |
| `/prompt` | Get a question right now |
| `/stats` | View your statistics |
| `/stop` | Pause daily prompts |
| `/resume` | Resume daily prompts |

## 🎯 How It Works

1. **Upload Documents**: Send .docx files containing your study materials
2. **AI Extracts Questions**: Gemini analyzes the content and generates questions
3. **Question Bank**: All questions are stored in SQLite database
4. **Daily Prompts**: Bot sends you a question every day at your scheduled time
5. **Mix of Questions**: 70% from your uploaded materials, 30% AI-generated new questions
6. **Track Progress**: Your responses are saved for review

## ⚙️ Configuration

### Change Prompt Time
In Render dashboard, update the `PROMPT_TIME` environment variable:
- Format: `HH:MM` (24-hour format)
- Examples: `08:30`, `14:00`, `20:15`

### Change Timezone
Update the `TIMEZONE` environment variable:
- Examples: `America/New_York`, `Europe/London`, `Asia/Jakarta`, `Asia/Tokyo`
- [List of timezones](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones)

### Database
- SQLite database file: `prompter_bot.db`
- Automatically created on first run
- Stored on Render's disk (persists between deployments)

## 🔧 Local Development

If you want to test locally before deploying:

```bash
# Clone the repository
git clone <your-repo-url>
cd telegram-prompter-bot

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env and add your tokens

# Run the bot
python bot.py
```

## 💰 Cost Breakdown

| Service | Free Tier | Usage |
|---------|-----------|-------|
| **Render.com** | 750 hours/month | ~720 hours (24/7) ✅ |
| **Groq AI** | 14,400 requests/day | ~10-50/day ✅ |
| **Telegram Bot API** | Unlimited | Free forever ✅ |
| **Total Cost** | **$0.00/month** | 🎉 |

## 🐛 Troubleshooting

### Bot doesn't respond
- Check Render logs for errors
- Verify environment variables are set correctly
- Make sure bot is running (check Render dashboard)

### API errors
- Verify your Groq API key is valid
- Check you haven't exceeded free tier limits (14,400/day)
- Ensure API key has proper permissions

### Daily prompts not working
- Verify `PROMPT_TIME` is in correct format (HH:MM)
- Check `TIMEZONE` is a valid timezone
- Look at Render logs during scheduled time

### Can't upload Word files
- Ensure file is .docx format (not .doc)
- File should contain readable text
- Maximum file size: 20MB

## 🔐 Security Notes

- Never commit `.env` file to GitHub
- Store API keys only in Render environment variables
- Database is private to your Render instance
- Bot only responds to users who start it

## 📈 Future Enhancements

Want to add features? Ideas:
- Spaced repetition algorithm
- Multiple choice questions
- Progress charts
- Export to Anki
- Group study mode
- Voice note prompts

## 🤝 Contributing

Feel free to fork and improve! This is a learning project.

## 📄 License

MIT License - free to use and modify

## 🆘 Support

If you run into issues:
1. Check the troubleshooting section above
2. Review Render deployment logs
3. Verify all environment variables are set
4. Test API keys independently

## 🎓 Educational Use

This bot is perfect for:
- Students building study materials
- Teachers creating review questions
- Self-learners building knowledge bases
- Anyone using spaced repetition for learning

---

**Made with ❤️ using Python, Telegram Bot API, and Groq AI**

**100% Free Forever • Works Worldwide** 🎉
