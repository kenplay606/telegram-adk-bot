# Telegram Bot Setup for Google ADK Agent

This guide shows you how to connect your Google ADK agent to Telegram for hands-free interaction.

## Prerequisites

- Google ADK agent already set up (`my_agent/`)
- Telegram account
- Python virtual environment activated

## Step 1: Create a Telegram Bot

1. **Open Telegram** and search for `@BotFather`
2. **Start a chat** with BotFather
3. **Send command:** `/newbot`
4. **Choose a name** for your bot (e.g., "My ADK Assistant")
5. **Choose a username** (must end in 'bot', e.g., "my_adk_assistant_bot")
6. **Copy the bot token** - You'll receive something like:
   ```
   123456789:ABCdefGHIjklMNOpqrsTUVwxyz
   ```

## Step 2: Install Telegram Dependencies

Activate your virtual environment and install the required packages:

**PowerShell:**
```powershell
.venv\Scripts\Activate.ps1
pip install -r requirements-telegram.txt
```

**Command Prompt:**
```console
.venv\Scripts\activate.bat
pip install -r requirements-telegram.txt
```

This installs:
- `python-telegram-bot` - Telegram bot framework
- `python-dotenv` - Environment variable management
- `google-adk` - Already installed

## Step 3: Configure Environment Variables

Add your Telegram bot token to the `.env` file:

1. **Open or create** `my_agent/.env`
2. **Add these lines:**
   ```env
   TELEGRAM_BOT_TOKEN=your_bot_token_here
   ALLOWED_USER_IDS=your_telegram_user_id
   ```

### How to Get Your Telegram User ID

1. Search for `@userinfobot` on Telegram
2. Start a chat and send `/start`
3. Copy your user ID (e.g., `123456789`)
4. Add it to `.env` file

**Example `.env` file:**
```env
GOOGLE_API_KEY=AIzaSyAbiZMAhtUWUznC-7E4tPXZb2fIn8MTHyQ
GOOGLE_GENAI_USE_VERTEXAI=0
TELEGRAM_BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz
ALLOWED_USER_IDS=987654321
```

**For multiple users:**
```env
ALLOWED_USER_IDS=987654321,123456789,555555555
```

## Step 4: Run the Telegram Bot

With your virtual environment activated:

```powershell
python telegram_bot.py
```

You should see:
```
🚀 Starting Telegram bot...
📱 Agent: root_agent
🤖 Model: gemini-2.5-flash
✅ Bot is running! Press Ctrl+C to stop.
💬 Send a message to your bot on Telegram to start chatting!
```

## Step 5: Test Your Bot

1. **Open Telegram** and search for your bot by username
2. **Start a chat** and send `/start`
3. **Try asking a question:**
   - "What time is it in Tokyo?"
   - "Tell me the current time in New York"

## Available Commands

| Command | Description |
|---------|-------------|
| `/start` | Welcome message and instructions |
| `/help` | Show help and usage tips |
| `/info` | Display agent information |
| `/reset` | Clear conversation history |

## Features

✅ **Hands-free interaction** - Chat with your ADK agent via Telegram  
✅ **Secure** - Only authorized users can access (via ALLOWED_USER_IDS)  
✅ **Persistent sessions** - Each user has their own conversation context  
✅ **Tool support** - Agent can use tools like `get_current_time`  
✅ **Error handling** - Graceful error messages  
✅ **Typing indicators** - Shows when agent is processing  

## Running in Background

### Windows (PowerShell)

**Option 1: Keep terminal open**
```powershell
python telegram_bot.py
```

**Option 2: Run as background job**
```powershell
Start-Process python -ArgumentList "telegram_bot.py" -WindowStyle Hidden
```

**Option 3: Use Windows Task Scheduler**
1. Open Task Scheduler
2. Create Basic Task
3. Set trigger (e.g., "At startup")
4. Action: Start a program
5. Program: `C:\Users\ching\CascadeProjects\Ai Agent\.venv\Scripts\python.exe`
6. Arguments: `telegram_bot.py`
7. Start in: `C:\Users\ching\CascadeProjects\Ai Agent`

### Linux/Mac

**Run in background with nohup:**
```bash
nohup python telegram_bot.py > telegram_bot.log 2>&1 &
```

**Or use screen/tmux:**
```bash
screen -S telegram_bot
python telegram_bot.py
# Press Ctrl+A, then D to detach
```

## Troubleshooting

### Bot doesn't respond

**Check:**
- ✅ Bot token is correct in `.env`
- ✅ Virtual environment is activated
- ✅ Script is running (check terminal output)
- ✅ Your user ID is in ALLOWED_USER_IDS

**Test:**
```powershell
python -c "import os; from dotenv import load_dotenv; load_dotenv('my_agent/.env'); print(os.getenv('TELEGRAM_BOT_TOKEN'))"
```

### "Unauthorized access" message

**Solution:**
- Add your Telegram user ID to ALLOWED_USER_IDS in `.env`
- Get your ID from @userinfobot
- Restart the bot after updating `.env`

### Import errors

**Solution:**
```powershell
pip install -r requirements-telegram.txt --upgrade
```

### Agent errors

**Check:**
- ✅ `my_agent/agent.py` exists and is valid
- ✅ GOOGLE_API_KEY is set in `.env`
- ✅ Google ADK is installed: `pip install google-adk`

## Customization

### Add More Commands

Edit `telegram_bot.py` and add new command handlers:

```python
async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Your custom response")

# In main():
application.add_handler(CommandHandler("custom", custom_command))
```

### Modify Agent Behavior

Edit `my_agent/agent.py` to:
- Add more tools
- Change instructions
- Update the model
- Modify behavior

### Change Response Format

Edit the `get_agent_response()` function in `telegram_bot.py` to format responses differently.

## Security Best Practices

⚠️ **Important Security Tips:**

1. **Never share your bot token** - Keep it secret
2. **Use ALLOWED_USER_IDS** - Restrict access to authorized users only
3. **Don't commit `.env` to git** - Already in `.gitignore`
4. **Regenerate token if compromised** - Use BotFather's `/revoke` command
5. **Monitor bot usage** - Check logs regularly

## Advanced: Deploy to Cloud

### Deploy to Heroku

1. Create `Procfile`:
   ```
   worker: python telegram_bot.py
   ```

2. Create `runtime.txt`:
   ```
   python-3.10
   ```

3. Deploy:
   ```bash
   heroku create
   git push heroku main
   heroku ps:scale worker=1
   ```

### Deploy to Railway

1. Connect GitHub repo
2. Add environment variables in Railway dashboard
3. Set start command: `python telegram_bot.py`

### Deploy to Google Cloud Run

1. Create `Dockerfile`
2. Build and push to Container Registry
3. Deploy to Cloud Run

## Stopping the Bot

**If running in terminal:**
- Press `Ctrl+C`

**If running as background process:**
```powershell
# Find the process
Get-Process python

# Stop it
Stop-Process -Name python
```

## Next Steps

- ✅ Customize agent tools in `my_agent/agent.py`
- ✅ Add more Telegram commands
- ✅ Deploy to cloud for 24/7 availability
- ✅ Add logging and monitoring
- ✅ Create custom keyboards and buttons

## Support

For issues:
1. Check bot is running: Look for "Bot is running!" message
2. Verify `.env` configuration
3. Check terminal for error messages
4. Test with `/start` command first
5. Review ADK agent logs

---

**Enjoy your hands-free AI assistant on Telegram! 🤖📱**
