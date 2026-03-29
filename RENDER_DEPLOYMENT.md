# Deploy Telegram Bot to Render.com

This guide shows you how to deploy your Google ADK Telegram bot to Render.com for 24/7 availability.

## Why Render.com?

✅ **Free tier available** - 750 hours/month free  
✅ **Easy deployment** - Deploy from GitHub in minutes  
✅ **Automatic restarts** - Bot stays running 24/7  
✅ **Environment variables** - Secure credential management  
✅ **Logs & monitoring** - Track bot activity  
✅ **No credit card required** for free tier  

## Prerequisites

- GitHub account
- Render.com account (free)
- Your Telegram bot token and user ID

## Step 1: Create GitHub Repository

### Option A: Using GitHub Desktop (Easiest)

1. **Download GitHub Desktop** (if not installed): https://desktop.github.com
2. **Install and sign in** with your GitHub account
3. **Add this project:**
   - File → Add Local Repository
   - Choose: `C:\Users\ching\CascadeProjects\Ai Agent`
   - Click "Add Repository"
4. **Create repository on GitHub:**
   - Click "Publish repository"
   - Name: `telegram-adk-bot`
   - Description: "Google ADK Agent with Telegram Bot"
   - **Uncheck** "Keep this code private" (or keep private if you prefer)
   - Click "Publish repository"
5. **Commit and push:**
   - Write commit message: "Initial commit - Telegram bot setup"
   - Click "Commit to main"
   - Click "Push origin"

### Option B: Using Git Command Line

```powershell
# Navigate to project
cd "C:\Users\ching\CascadeProjects\Ai Agent"

# Initialize git repository
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit - Telegram bot setup"

# Create repository on GitHub (do this manually on github.com first)
# Then connect and push:
git remote add origin https://github.com/YOUR_USERNAME/telegram-adk-bot.git
git branch -M main
git push -u origin main
```

## Step 2: Sign Up for Render.com

1. **Go to:** https://render.com
2. **Click:** "Get Started" or "Sign Up"
3. **Sign up with GitHub** (recommended for easy deployment)
4. **Authorize Render** to access your GitHub account

## Step 3: Create New Web Service

1. **Click:** "New +" button (top right)
2. **Select:** "Background Worker"
3. **Connect your repository:**
   - Click "Connect account" if needed
   - Select `telegram-adk-bot` repository
   - Click "Connect"

## Step 4: Configure Service

### Basic Settings

| Setting | Value |
|---------|-------|
| **Name** | `telegram-adk-bot` |
| **Region** | Choose closest to you |
| **Branch** | `main` |
| **Runtime** | `Python 3` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `python telegram_bot.py` |

### Instance Type

- **Select:** "Free" (750 hours/month)
- **Note:** Free tier spins down after 15 min of inactivity
- **For 24/7:** Upgrade to Starter ($7/month) - optional

## Step 5: Add Environment Variables

**Critical:** Add your credentials as environment variables.

Click "Advanced" → "Add Environment Variable"

Add these variables:

| Key | Value |
|-----|-------|
| `GOOGLE_API_KEY` | `AIzaSyAbiZMAhtUWUznC-7E4tPXZb2fIn8MTHyQ` |
| `GOOGLE_GENAI_USE_VERTEXAI` | `0` |
| `TELEGRAM_BOT_TOKEN` | `8237861648:AAFm4Z0Pv15zTNTyUITa7dmxNtnlKBeefew` |
| `ALLOWED_USER_IDS` | `7020223466` |

**Important:** Click "Add" after each variable.

## Step 6: Deploy

1. **Click:** "Create Background Worker"
2. **Render will:**
   - Clone your repository
   - Install dependencies
   - Start your bot
3. **Wait for deployment** (2-5 minutes)

## Step 7: Verify Deployment

### Check Logs

1. **In Render dashboard**, click on your service
2. **Click:** "Logs" tab
3. **You should see:**
   ```
   🚀 Starting Telegram bot...
   📱 Agent: root_agent
   🤖 Model: gemini-2.5-flash
   ✅ Bot is running!
   ```

### Test Your Bot

1. **Open Telegram**
2. **Send a message** to your bot
3. **Bot should respond!**

## Free Tier Limitations

### What You Get

- ✅ **750 hours/month** free
- ✅ **512 MB RAM**
- ✅ **0.1 CPU**
- ✅ **Automatic deploys** from GitHub

### Important Note: Spin Down

⚠️ **Free tier services spin down after 15 minutes of inactivity**

**What this means:**
- Bot stops after 15 min of no messages
- First message after spin down takes 30-60 seconds to wake up
- Subsequent messages are instant

**Solutions:**
1. **Accept the delay** (free option)
2. **Upgrade to Starter** ($7/month for 24/7 uptime)
3. **Use a ping service** to keep it awake (see below)

### Keep Bot Awake (Optional)

Use a free service to ping your bot every 14 minutes:

**Option 1: UptimeRobot**
1. Sign up at https://uptimerobot.com (free)
2. Add monitor with your Render service URL
3. Set interval to 5 minutes

**Option 2: Cron-job.org**
1. Sign up at https://cron-job.org (free)
2. Create job to ping your service every 14 minutes

**Note:** This keeps the service awake but uses your 750 free hours faster.

## Updating Your Bot

When you make changes to your code:

### Using GitHub Desktop

1. **Make changes** to your code locally
2. **Open GitHub Desktop**
3. **Review changes** in the left panel
4. **Write commit message** (e.g., "Add new feature")
5. **Click:** "Commit to main"
6. **Click:** "Push origin"
7. **Render automatically redeploys!**

### Using Git Command Line

```powershell
git add .
git commit -m "Your change description"
git push
```

Render will automatically detect the push and redeploy.

## Monitoring & Logs

### View Logs

- Render Dashboard → Your Service → Logs
- See real-time bot activity
- Filter by log level (info, error, etc.)

### Check Status

- **Live** = Bot is running
- **Deploying** = Updating with new code
- **Failed** = Check logs for errors

### Restart Service

- Click "Manual Deploy" → "Deploy latest commit"
- Or click "Restart" button

## Troubleshooting

### Bot Not Starting

**Check logs for errors:**
- Render Dashboard → Logs

**Common issues:**
- Missing environment variables
- Invalid bot token
- Dependency installation failed

**Solution:**
- Verify all environment variables are set
- Check token is correct with @BotFather
- Review build logs for pip errors

### Bot Crashes After Starting

**Check logs for:**
- Import errors (missing dependencies)
- API key issues
- Telegram token errors

**Solution:**
- Add missing packages to `requirements.txt`
- Verify Google API key is valid
- Check Telegram bot token

### Environment Variables Not Loading

**Issue:** Bot can't find credentials

**Solution:**
- Verify variables are set in Render dashboard
- Check variable names match exactly (case-sensitive)
- Redeploy after adding variables

### Bot Stops Responding (Free Tier)

**Issue:** Service spun down after 15 minutes

**Solution:**
- Send another message (will wake up in 30-60 sec)
- Upgrade to Starter plan for 24/7 uptime
- Use ping service to keep awake

### Deployment Failed

**Check:**
- Build logs for errors
- Python version compatibility
- requirements.txt syntax

**Solution:**
- Fix errors in code
- Push changes to GitHub
- Render will auto-redeploy

## Cost & Pricing

### Free Tier

- **750 hours/month** (enough for ~31 days if always on)
- **Spins down after 15 min inactivity**
- **No credit card required**
- **Perfect for testing**

### Starter Plan ($7/month)

- **Always on** (no spin down)
- **Better performance**
- **Priority support**
- **Recommended for production**

### Estimated Usage

- **Free tier:** $0/month (with spin down)
- **Starter:** $7/month (24/7 uptime)
- **Most personal bots:** Free tier is sufficient

## Security Best Practices

⚠️ **Important Security Tips:**

1. **Never commit `.env` file to GitHub**
   - Already in `.gitignore`
   - Use Render environment variables instead

2. **Keep repository private** (optional but recommended)
   - GitHub Settings → Danger Zone → Change visibility

3. **Rotate tokens if exposed**
   - Get new token from @BotFather
   - Update in Render environment variables

4. **Use ALLOWED_USER_IDS**
   - Restrict bot access to authorized users only
   - Already configured with your user ID

5. **Review Render logs regularly**
   - Check for unauthorized access attempts
   - Monitor error patterns

## Advanced Configuration

### Custom Domain (Paid Plans)

- Add custom domain in Render dashboard
- Configure DNS settings
- Enable HTTPS automatically

### Auto-Deploy from GitHub

- **Already enabled by default**
- Push to main branch = automatic deployment
- Disable in Settings if needed

### Health Checks

Add to your bot for better monitoring:

```python
# Add health check endpoint (optional)
from flask import Flask
app = Flask(__name__)

@app.route('/health')
def health():
    return 'OK', 200
```

### Scaling (Paid Plans)

- Increase instance size for better performance
- Add more instances for redundancy
- Configure auto-scaling rules

## Comparing Render vs Railway

| Feature | Render Free | Railway Free |
|---------|-------------|--------------|
| **Free hours** | 750/month | $5 credit |
| **Spin down** | Yes (15 min) | No |
| **Credit card** | Not required | Not required |
| **Deployment** | GitHub auto | GitHub auto |
| **Logs** | Yes | Yes |
| **Best for** | Testing | Production |

**Recommendation:**
- **Render Free:** Good for testing, accepts 15-min delay
- **Render Starter ($7):** 24/7 uptime, no delays
- **Railway:** Better for production if you need always-on free tier

## Next Steps

After deployment:

- ✅ Bot runs automatically in the cloud
- ✅ Survives computer shutdowns
- ✅ Auto-restarts on crashes
- ✅ Monitor via Render dashboard
- ✅ Update by pushing to GitHub

### Optional Improvements

1. **Add more tools** to your agent (`my_agent/agent.py`)
2. **Customize bot commands** (`telegram_bot.py`)
3. **Add logging** for better debugging
4. **Set up monitoring** alerts
5. **Upgrade to Starter** for 24/7 uptime

## Support

**Render Documentation:** https://render.com/docs  
**Render Community:** https://community.render.com  
**Telegram Bot API:** https://core.telegram.org/bots/api

---

**Your bot is now deployed to Render! 🚀**

Free tier: Bot runs when active, spins down after 15 min.  
Starter plan: Bot runs 24/7 without interruption.

Choose based on your needs!
