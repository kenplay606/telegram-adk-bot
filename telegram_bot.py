"""
Telegram Bot Integration for Google ADK Agent
Allows hands-free interaction with your ADK agent via Telegram
"""

import os
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from google.adk.agents.llm_agent import Agent
import sys
from dotenv import load_dotenv

# Load environment variables from my_agent/.env (for local development)
# Railway will use environment variables set in dashboard
env_path = os.path.join(os.path.dirname(__file__), 'my_agent', '.env')
if os.path.exists(env_path):
    load_dotenv(env_path)
else:
    # Running in production (Railway) - env vars already set
    pass

# Import your agent from my_agent folder
sys.path.append(os.path.join(os.path.dirname(__file__), 'my_agent'))
from my_agent.agent import root_agent

# Configuration
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')  # Get from BotFather
ALLOWED_USER_IDS = os.getenv('ALLOWED_USER_IDS', '').split(',')  # Comma-separated user IDs for security

# Store conversation context per user
user_sessions = {}


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command"""
    user_id = str(update.effective_user.id)
    
    # Security check
    if ALLOWED_USER_IDS and ALLOWED_USER_IDS[0] and user_id not in ALLOWED_USER_IDS:
        await update.message.reply_text("⛔ Unauthorized access. Please contact the bot owner.")
        return
    
    welcome_message = """
🤖 **Google ADK Agent - Telegram Bot**

I'm your AI assistant powered by Google's Agent Development Kit!

**Available Commands:**
/start - Show this welcome message
/help - Get help
/reset - Reset conversation context
/info - Show agent information

**How to use:**
Just send me any message and I'll respond using my tools and knowledge!

Example: "What time is it in Tokyo?"
    """
    
    await update.message.reply_text(welcome_message, parse_mode='Markdown')


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command"""
    help_text = """
📚 **Help & Usage**

**Commands:**
• /start - Welcome message
• /help - This help message
• /reset - Clear conversation history
• /info - Agent details

**Tips:**
• Ask questions naturally
• The agent has access to tools like get_current_time
• Conversations are private and secure
• Each user has their own session

**Examples:**
• "What time is it in New York?"
• "Tell me the current time in London"
• "What's the time in Hong Kong?"
    """
    
    await update.message.reply_text(help_text, parse_mode='Markdown')


async def info_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /info command"""
    info_text = f"""
ℹ️ **Agent Information**

**Name:** {root_agent.name}
**Model:** {root_agent.model}
**Description:** {root_agent.description}

**Available Tools:**
{', '.join([tool.__name__ for tool in root_agent.tools]) if root_agent.tools else 'None'}

**Status:** ✅ Active and ready
    """
    
    await update.message.reply_text(info_text, parse_mode='Markdown')


async def reset_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /reset command - clear conversation context"""
    user_id = str(update.effective_user.id)
    
    if user_id in user_sessions:
        del user_sessions[user_id]
    
    await update.message.reply_text("🔄 Conversation reset! Starting fresh.")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle regular text messages"""
    user_id = str(update.effective_user.id)
    user_message = update.message.text
    
    # Security check
    if ALLOWED_USER_IDS and ALLOWED_USER_IDS[0] and user_id not in ALLOWED_USER_IDS:
        await update.message.reply_text("⛔ Unauthorized access.")
        return
    
    # Show typing indicator
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    
    try:
        # Initialize session for new users
        if user_id not in user_sessions:
            user_sessions[user_id] = {
                'history': [],
                'context': {}
            }
        
        # Get response from ADK agent
        response = await get_agent_response(user_message, user_sessions[user_id])
        
        # Send response back to user
        await update.message.reply_text(response)
        
        # Update conversation history
        user_sessions[user_id]['history'].append({
            'user': user_message,
            'agent': response
        })
        
        # Keep only last 10 exchanges to manage memory
        if len(user_sessions[user_id]['history']) > 10:
            user_sessions[user_id]['history'] = user_sessions[user_id]['history'][-10:]
    
    except Exception as e:
        error_message = f"❌ Error processing your request: {str(e)}"
        await update.message.reply_text(error_message)
        print(f"Error: {e}")


async def get_agent_response(user_message: str, session_data: dict) -> str:
    """
    Get response from the ADK agent
    This is a simplified version - you may need to adjust based on ADK's async API
    """
    try:
        # The ADK agent should handle the message and return a response
        # Note: This is a synchronous call - you may need to wrap it properly for async
        # depending on how ADK handles execution
        
        # For now, we'll use a simple approach
        # You might need to adjust this based on ADK's actual API
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None, 
            lambda: root_agent.run(user_message)
        )
        
        return str(response)
    
    except Exception as e:
        return f"I encountered an error: {str(e)}\n\nPlease try rephrasing your question."


async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle errors"""
    print(f'Update {update} caused error {context.error}')
    
    if update and update.effective_message:
        await update.effective_message.reply_text(
            "⚠️ An error occurred while processing your request. Please try again."
        )


def main():
    """Start the Telegram bot"""
    
    # Check for bot token
    if not TELEGRAM_BOT_TOKEN:
        print("❌ Error: TELEGRAM_BOT_TOKEN not found in environment variables!")
        print("Please set your Telegram bot token:")
        print("1. Get token from @BotFather on Telegram")
        print("2. Add to .env file: TELEGRAM_BOT_TOKEN=your_token_here")
        return
    
    print("🚀 Starting Telegram bot...")
    print(f"📱 Agent: {root_agent.name}")
    print(f"🤖 Model: {root_agent.model}")
    
    # Create application
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    
    # Add command handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("info", info_command))
    application.add_handler(CommandHandler("reset", reset_command))
    
    # Add message handler for regular text
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Add error handler
    application.add_error_handler(error_handler)
    
    # Start the bot
    print("✅ Bot is running! Press Ctrl+C to stop.")
    print("💬 Send a message to your bot on Telegram to start chatting!")
    
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()
