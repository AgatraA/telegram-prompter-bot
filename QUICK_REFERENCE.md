# 📋 Quick Reference Card

## 🔑 Your API Keys

### Telegram Bot Token
- Get from: @BotFather on Telegram
- Command: `/newbot`
- Format: `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz`

### Groq API Key
- Get from: https://console.groq.com/
- Format: `gsk_abcdefghijk...`
- Free tier: 14,400 requests/day
- **Available worldwide!**

---

## 🤖 Bot Commands

| Command | What It Does |
|---------|--------------|
| `/start` | Register with the bot |
| `/help` | Show all commands |
| `/prompt` | Get a question now |
| `/stats` | View your progress |
| `/stop` | Pause daily prompts |
| `/resume` | Resume daily prompts |

---

## 📤 How to Use

1. **Upload Word Files**: Just drag and drop .docx files into the chat
2. **Wait for AI**: Bot extracts text and generates ~10 questions
3. **Get Daily Prompts**: Automatic at your scheduled time
4. **Answer Anytime**: Reply to questions whenever convenient

---

## ⚙️ Environment Variables

Set these in Render.com dashboard:

| Variable | Example | Description |
|----------|---------|-------------|
| `TELEGRAM_BOT_TOKEN` | `123:ABC...` | Your bot token |
| `GROQ_API_KEY` | `gsk_...` | Your Groq key |
| `PROMPT_TIME` | `09:00` | Daily prompt time (24hr) |
| `TIMEZONE` | `UTC` | Your timezone |

### Common Timezones:
- `UTC` - Coordinated Universal Time
- `America/New_York` - Eastern Time
- `America/Los_Angeles` - Pacific Time
- `Europe/London` - UK Time
- `Asia/Tokyo` - Japan Time
- `Asia/Jakarta` - Indonesia Time
- `Australia/Sydney` - Australia Time

---

## 🎯 How Questions Work

**70% from your uploads** - Random selection from question bank
**30% AI-generated** - New questions based on your content

---

## 💡 Pro Tips

1. **Build your bank first**: Upload 5-10 Word files before enabling daily prompts
2. **Various content**: Mix different topics for diverse questions
3. **Quality input**: Well-written documents = better questions
4. **Respond thoughtfully**: Your answers are saved for review
5. **Check stats**: Use `/stats` to track progress

---

## 🆓 Free Forever

| Service | Limit | Your Usage |
|---------|-------|------------|
| Render.com | 750 hrs/mo | ~720 hrs ✅ |
| Groq API | 14,400/day | ~10-50/day ✅ |
| Telegram | Unlimited | Free ✅ |

---

## 🔧 Quick Fixes

**Bot not responding?**
→ Check Render dashboard (service running?)

**Upload fails?**
→ Use .docx format (not .doc or PDF)

**No daily prompts?**
→ Verify `PROMPT_TIME` and `TIMEZONE`

**API errors?**
→ Check Groq API key is valid

---

## 📱 Access Anywhere

- Telegram Web: https://web.telegram.org
- Telegram Desktop: Download for your OS
- Mobile Apps: iOS/Android
- Your bot works on ALL platforms!

---

## 🎓 Perfect For

✅ Students studying for exams
✅ Language learners
✅ Professional certifications
✅ Book clubs / reading groups
✅ Interview preparation
✅ Spaced repetition learning

---

**Need detailed help? Check DEPLOYMENT_GUIDE.md**
**Need full documentation? Check README.md**
