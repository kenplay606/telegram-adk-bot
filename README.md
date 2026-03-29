# Google ADK Agent with Telegram Bot Integration

This project contains a Google Agent Development Kit (ADK) agent that can be accessed via:
- **Command-line interface** (CLI)
- **Web interface** (browser-based)
- **Telegram bot** (hands-free mobile access) 🤖📱

## Prerequisites

- Python 3.10 or later
- `pip` for installing packages
- Telegram account (for bot integration)

## Installation

This project has already been set up with:
- ✅ Python virtual environment (`.venv`)
- ✅ `google-adk` package installed
- ✅ Agent project created (`my_agent/`)
- ✅ API key configured
- ✅ Telegram bot integration ready

### Activate the Virtual Environment

Before running any commands, activate the virtual environment:

**PowerShell:**
```powershell
.venv\Scripts\Activate.ps1
```

**Command Prompt:**
```console
.venv\Scripts\activate.bat
```

**Bash/Git Bash:**
```bash
source .venv/bin/activate
```

## Project Structure

```text
my_agent/
    agent.py      # main agent code with get_current_time tool
    .env          # API keys (GOOGLE_API_KEY already configured)
    __init__.py
```

## Agent Overview

The `agent.py` file contains a `root_agent` with a `get_current_time` tool that returns the current time in a specified city.

## Run Your Agent

### Option 1: Telegram Bot (Recommended for Hands-Free Use) 🤖

Chat with your agent via Telegram on your phone or desktop:

```powershell
python telegram_bot.py
```

**Setup required:** See `TELEGRAM_SETUP.md` for complete instructions.

**Features:**
- 📱 Access from anywhere via Telegram
- 🔒 Secure (user ID authentication)
- 💬 Persistent conversations
- 🚀 Easy to use with commands like `/start`, `/help`

### Option 2: Command-Line Interface

Run your agent using the `adk run` command:

```console
adk run my_agent
```

### Option 3: Web Interface

Start the ADK web interface for testing and interaction:

```console
adk web --port 8000
```

**Note:** Run this command from the **parent directory** that contains your `my_agent/` folder.

Access the web interface at [http://localhost:8000](http://localhost:8000). Select the agent at the upper left corner and type a request.

⚠️ **Caution:** ADK Web is for development only, not for production deployments.

## API Key

Your Google API key is already configured in `my_agent/.env`. If you need to update it:

1. Get your API key from [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Update the `.env` file:

```console
echo 'GOOGLE_API_KEY="YOUR_API_KEY"' > my_agent/.env
```

## Using Other AI Models

ADK supports many generative AI models. For more information on configuring other models, see the [Models & Authentication documentation](https://ai.google.dev/adk-docs/agents/models).

## Telegram Bot Setup (Quick Start)

1. **Get a bot token from @BotFather on Telegram**
2. **Get your user ID from @userinfobot on Telegram**
3. **Add to `my_agent/.env`:**
   ```env
   TELEGRAM_BOT_TOKEN=your_token_here
   ALLOWED_USER_IDS=your_user_id_here
   ```
4. **Install dependencies:**
   ```powershell
   pip install -r requirements-telegram.txt
   ```
5. **Run the bot:**
   ```powershell
   python telegram_bot.py
   ```

📖 **Full guide:** See `TELEGRAM_SETUP.md` for detailed instructions.

## Next Steps

Now that you have ADK installed and your first agent running, try:

- **Set up Telegram bot** for hands-free mobile access (see `TELEGRAM_SETUP.md`)
- Customizing the `get_current_time` tool
- Adding new tools to your agent
- Building more complex agents with the [ADK tutorials](https://ai.google.dev/adk-docs/tutorials/)
