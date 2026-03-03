# 🚀 Step-by-Step Deployment Guide

Follow these exact steps to get your bot running on Render.com (free forever!)

## Part 1: Get Your API Keys (10 minutes)

### Step 1: Create Telegram Bot Token

1. **Open Telegram** on your phone or desktop
2. **Search for** `@BotFather` (official bot with blue checkmark)
3. **Start chat** and send: `/newbot`
4. **Bot will ask for a name**. Reply with something like: `My Daily Prompter`
5. **Bot will ask for username**. Reply with something ending in `bot`, like: `mydaily_prompter_bot`
6. **BotFather gives you a token** - looks like:
   ```
   1234567890:ABCdefGHIjklMNOpqrsTUVwxyz-123456
   ```
7. **COPY THIS TOKEN** - you'll need it soon!

### Step 2: Get Groq API Key (Available Worldwide!)

1. **Go to**: https://console.groq.com/
2. **Sign up** with Google, GitHub, or email (free account)
3. **Click** your profile icon (top right) → "API Keys"
4. **Click** "Create API Key"
5. **Name it**: "Telegram Bot" (or anything you like)
6. **Copy the key** - looks like:
   ```
   gsk_abcdefghijklmnopqrstuvwxyz1234567890ABCDEFGHIJK
   ```
6. **Save this key** - you'll need it soon!

**Note:** Groq is available worldwide and has a generous free tier:
- 14,400 requests per day
- Ultra-fast responses
- High-quality Llama 3.1 model

---

## Part 2: Prepare Your Code (5 minutes)

### Option A: Use GitHub (Recommended)

1. **Create GitHub account** if you don't have one: https://github.com/signup
2. **Create new repository**:
   - Go to: https://github.com/new
   - Repository name: `telegram-prompter-bot`
   - Make it **Public**
   - Click **"Create repository"**

3. **Upload files**:
   - Click **"uploading an existing file"**
   - Drag and drop ALL these files:
     - `bot.py`
     - `requirements.txt`
     - `render.yaml`
     - `README.md`
     - `.gitignore`
   - Click **"Commit changes"**

### Option B: GitHub Desktop (Easier if not familiar with Git)

1. Download GitHub Desktop: https://desktop.github.com/
2. Install and sign in
3. Create new repository (File → New Repository)
4. Copy all the bot files into that folder
5. Commit and push to GitHub

---

## Part 3: Deploy to Render.com (10 minutes)

### Step 1: Sign Up for Render

1. **Go to**: https://render.com
2. **Click** "Get Started for Free"
3. **Sign up with GitHub** (easiest option - links your repos automatically)
4. **Authorize Render** to access your GitHub

### Step 2: Create Web Service

1. **Click** "New +" (top right)
2. **Select** "Web Service"
3. **Connect your repository**:
   - Find `telegram-prompter-bot` in the list
   - Click **"Connect"**

### Step 3: Configure the Service

Render will auto-detect settings from `render.yaml`, but verify:

- **Name**: `telegram-prompter-bot` (or anything you like)
- **Environment**: `Python 3`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `python bot.py`

### Step 4: Add Environment Variables

Scroll down to **"Environment Variables"** section:

**Add these 4 variables:**

1. **Variable 1:**
   - Key: `TELEGRAM_BOT_TOKEN`
   - Value: (paste the token from BotFather)

2. **Variable 2:**
   - Key: `GROQ_API_KEY`
   - Value: (paste your Groq API key)

3. **Variable 3:**
   - Key: `PROMPT_TIME`
   - Value: `09:00` (or your preferred time, like `07:30` or `20:00`)

4. **Variable 4:**
   - Key: `TIMEZONE`
   - Value: `UTC` (or your timezone like `Asia/Jakarta`, `America/New_York`, etc.)

### Step 5: Deploy!

1. **Scroll down** and click **"Create Web Service"**
2. **Wait 3-5 minutes** while it deploys
3. **Watch the logs** - you'll see:
   ```
   Installing dependencies...
   Starting bot...
   Bot started. Daily prompts scheduled for 09:00 UTC
   ```

4. **Success!** When you see "Bot started", it's live! 🎉

---

## Part 4: Test Your Bot (5 minutes)

### Step 1: Find Your Bot

1. **Open Telegram**
2. **Search** for your bot's username (e.g., `@mydaily_prompter_bot`)
3. **Click** on it and press **"Start"**

### Step 2: Test Commands

1. Send: `/start` - should get welcome message
2. Send: `/help` - should see command list
3. Send: `/prompt` - should get a question (might say "no questions yet")

### Step 3: Upload a Word File

1. **Create a simple Word document** (.docx) with some text like:
   ```
   Machine Learning Basics
   
   Machine learning is a subset of artificial intelligence that enables 
   systems to learn from data. Key concepts include supervised learning, 
   unsupervised learning, and reinforcement learning.
   
   Neural networks are computing systems inspired by biological neural 
   networks. They consist of layers of interconnected nodes.
   ```

2. **Send the file** to your bot in Telegram
3. **Wait ~30 seconds** - bot will:
   - Download the file
   - Extract text
   - Generate 10 questions using AI
   - Save them to database

4. **Success!** You should see:
   ```
   ✅ Success! Generated and saved 10 questions from your document.
   
   📝 Sample questions:
   • What is machine learning?
   • Explain the difference between supervised and unsupervised learning
   • How are neural networks inspired by biological systems?
   ```

5. **Test daily prompt**: Send `/prompt` - should now get a real question!

---

## Part 5: Verify Daily Prompts Are Scheduled

### Check the Logs

1. **Go back to Render dashboard**
2. **Click on your service** (telegram-prompter-bot)
3. **Click "Logs"** tab
4. **Look for**: `Bot started. Daily prompts scheduled for 09:00 UTC`

This confirms your bot will send daily prompts!

### Customize Your Schedule

Want to change the time?

1. Go to Render dashboard
2. Click your service → "Environment" tab
3. Edit `PROMPT_TIME` variable (e.g., change to `07:30`)
4. Edit `TIMEZONE` variable (e.g., change to `Asia/Jakarta`)
5. Click "Save Changes"
6. Render will auto-redeploy

---

## 🎉 You're Done!

Your bot is now:
- ✅ Running 24/7 on Render.com
- ✅ Will send you daily prompts at your scheduled time
- ✅ Accepts Word files and generates AI questions
- ✅ Completely free

### What Happens Next?

1. **Tomorrow at your scheduled time**, you'll receive your first daily prompt
2. **Upload more Word files** to build your question bank
3. **Reply to questions** - your responses are saved
4. **Use `/stats`** to track your progress

---

## 🆘 Troubleshooting

### "Bot doesn't respond in Telegram"

1. Check Render logs for errors
2. Make sure service is running (green status in Render dashboard)
3. Verify environment variables are set correctly
4. Try redeploying: Manual Deploy → "Deploy latest commit"

### "Can't upload Word files"

1. Make sure file is `.docx` format (not `.doc`)
2. File should have readable text content
3. Check Render logs for error messages

### "Daily prompts not working"

1. Wait until scheduled time passes
2. Check Render logs at that time for activity
3. Verify timezone is correct
4. Make sure you ran `/start` to register

### "AI question generation fails"

1. Check Groq API key is correct
2. Verify you haven't exceeded 14,400 requests/day (very unlikely)
3. Try with a different Word file
4. Check Render logs for specific error messages

---

## 📞 Need Help?

1. Check README.md for more details
2. Review Render logs for specific errors
3. Verify all steps were followed exactly
4. Test API keys independently

---

**Congratulations! You now have a free, AI-powered learning assistant! 🎓**
