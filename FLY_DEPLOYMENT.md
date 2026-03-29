# Deploy Telegram Bot to Fly.io

This guide shows you how to deploy your Google ADK Telegram bot to Fly.io for 24/7 availability.

## Why Fly.io?

✅ **Free tier available** - Free allowances for small apps  
✅ **Always-on** - No spin down like other free tiers  
✅ **Global deployment** - Deploy close to your users  
✅ **Simple CLI** - Easy deployment with flyctl  
✅ **Docker-based** - Reliable containerized deployment  

## Prerequisites

- Fly.io account (free)
- Flyctl CLI installed
- Your code already on GitHub (✅ Done!)

## Step 1: Install Flyctl CLI

### Windows (PowerShell)

```powershell
iwr https://fly.io/install.ps1 -useb | iex
```

### Verify Installation

```powershell
flyctl version
```

## Step 2: Sign Up / Login to Fly.io

### Create Account

```powershell
flyctl auth signup
```

This will open your browser to create a Fly.io account.

### Or Login (if you already have an account)

```powershell
flyctl auth login
```

## Step 3: Launch Your App

Navigate to your project directory and launch:

```powershell
cd "C:\Users\ching\CascadeProjects\Ai Agent"
flyctl launch
```

**During launch, answer these prompts:**

1. **App name:** Press Enter to use `telegram-adk-bot` (or choose your own)
2. **Region:** Choose closest to you (e.g., `sin` for Singapore)
3. **Would you like to set up a Postgresql database?** → **No**
4. **Would you like to set up an Upstash Redis database?** → **No**
5. **Would you like to deploy now?** → **No** (we need to add secrets first)

This creates a `fly.toml` configuration file (already created for you).

## Step 4: Set Environment Variables (Secrets)

Add your credentials as secrets:

```powershell
flyctl secrets set GOOGLE_API_KEY="AIzaSyAbiZMAhtUWUznC-7E4tPXZb2fIn8MTHyQ"
flyctl secrets set GOOGLE_GENAI_USE_VERTEXAI="0"
flyctl secrets set TELEGRAM_BOT_TOKEN="8237861648:AAFm4Z0Pv15zTNTyUITa7dmxNtnlKBeefew"
flyctl secrets set ALLOWED_USER_IDS="7020223466"
```

**Note:** Secrets are encrypted and secure.

## Step 5: Deploy Your Bot

```powershell
flyctl deploy
```

This will:
1. Build Docker image from your `Dockerfile`
2. Push to Fly.io registry
3. Deploy to your chosen region
4. Start your bot

**Deployment takes 2-5 minutes.**

## Step 6: Verify Deployment

### Check Status

```powershell
flyctl status
```

You should see your app running.

### View Logs

```powershell
flyctl logs
```

Look for:
```
🚀 Starting Telegram bot...
📱 Agent: root_agent
🤖 Model: gemini-2.5-flash
✅ Bot is running!
```

### Test Your Bot

1. Open Telegram
2. Send a message to your bot
3. Bot should respond!

## Fly.io Free Tier

### What You Get (Free)

- **3 shared-cpu-1x VMs** with 256MB RAM each
- **160GB outbound data transfer/month**
- **Always-on** (no spin down!)
- **Automatic HTTPS**

### Estimated Cost

- **Free tier:** $0/month for small bots
- **If you exceed:** ~$2-5/month
- **Monitor usage:** `flyctl dashboard`

## Managing Your Bot

### View Dashboard

```powershell
flyctl dashboard
```

Opens web dashboard in browser.

### View Logs (Real-time)

```powershell
flyctl logs -f
```

Press Ctrl+C to stop.

### Restart Bot

```powershell
flyctl apps restart telegram-adk-bot
```

### Scale Resources (if needed)

```powershell
# Increase memory
flyctl scale memory 512

# Increase CPU
flyctl scale vm shared-cpu-2x
```

## Updating Your Bot

When you make code changes:

### 1. Commit and Push to GitHub

```powershell
git add .
git commit -m "Update bot features"
git push
```

### 2. Deploy Updated Code

```powershell
flyctl deploy
```

Fly.io will rebuild and redeploy automatically.

## Monitoring

### Check App Status

```powershell
flyctl status
```

### View Metrics

```powershell
flyctl dashboard
```

Then go to **Metrics** tab.

### Set Up Alerts

In Fly.io dashboard:
- Configure email alerts
- Set up monitoring for crashes
- Track resource usage

## Troubleshooting

### Bot Not Starting

**Check logs:**
```powershell
flyctl logs
```

**Common issues:**
- Missing secrets (environment variables)
- Invalid bot token
- Dependency installation failed

**Solution:**
```powershell
# Verify secrets are set
flyctl secrets list

# Re-set if needed
flyctl secrets set TELEGRAM_BOT_TOKEN="your_token"
```

### Bot Crashes

**View crash logs:**
```powershell
flyctl logs --app telegram-adk-bot
```

**Common causes:**
- Python import errors
- API key issues
- Memory limit exceeded

**Solution:**
- Fix code errors
- Verify API keys
- Scale up memory if needed

### Deployment Failed

**Check build logs:**
```powershell
flyctl logs
```

**Common issues:**
- Dockerfile syntax errors
- Missing dependencies in requirements.txt
- Build timeout

**Solution:**
- Fix Dockerfile
- Update requirements.txt
- Retry deployment

### Out of Free Tier

**Check usage:**
```powershell
flyctl dashboard
```

**Solutions:**
- Add payment method (pay only for overages)
- Optimize bot to use less resources
- Scale down if over-provisioned

## Advanced Configuration

### Custom Domain

```powershell
flyctl certs add yourdomain.com
```

Then configure DNS as instructed.

### Multiple Regions

Deploy to multiple regions for redundancy:

```powershell
flyctl regions add nrt  # Tokyo
flyctl regions add lax  # Los Angeles
flyctl scale count 2
```

### Health Checks

Already configured in `fly.toml`:
- Fly.io monitors your app
- Auto-restarts on crashes
- Email alerts on failures

### Persistent Storage (if needed)

```powershell
flyctl volumes create data --size 1
```

Then mount in `fly.toml`.

## Useful Commands

```powershell
# SSH into your app
flyctl ssh console

# Open app in browser (if it had a web interface)
flyctl open

# View app info
flyctl info

# List all apps
flyctl apps list

# Destroy app (careful!)
flyctl apps destroy telegram-adk-bot
```

## Cost Optimization

### Stay Within Free Tier

- **1 VM with 256MB RAM** - Free
- **Monitor usage** - `flyctl dashboard`
- **Set billing alerts** - In dashboard

### If You Need More

- **Upgrade to 512MB RAM:** ~$2/month
- **Add second VM:** ~$2/month
- **Still very affordable!**

## Security Best Practices

⚠️ **Important:**

1. **Never commit secrets to GitHub**
   - Use `flyctl secrets` only
   - Already protected by `.gitignore`

2. **Rotate tokens if exposed**
   - Get new token from @BotFather
   - Update: `flyctl secrets set TELEGRAM_BOT_TOKEN="new_token"`

3. **Use ALLOWED_USER_IDS**
   - Restrict bot access
   - Already configured

4. **Monitor logs regularly**
   - Check for unauthorized access
   - Review error patterns

5. **Keep dependencies updated**
   - Update `requirements.txt`
   - Redeploy regularly

## Comparing Platforms

| Feature | Fly.io Free | Render Free | Railway Free |
|---------|-------------|-------------|--------------|
| **Always-on** | ✅ Yes | ❌ Spins down | ✅ Yes |
| **Free tier** | 3 VMs | 750 hrs/month | $5 credit |
| **Memory** | 256MB | 512MB | 512MB |
| **Deployment** | CLI | GitHub auto | GitHub auto |
| **Best for** | Always-on bots | Testing | Production |

**Recommendation:** Fly.io is great for always-on free tier!

## Next Steps

After deployment:

- ✅ Bot runs 24/7 automatically
- ✅ No spin down (unlike Render free tier)
- ✅ Survives computer shutdowns
- ✅ Auto-restarts on crashes
- ✅ Monitor via Fly.io dashboard

### Optional Improvements

1. **Add more tools** to your agent (`my_agent/agent.py`)
2. **Customize bot commands** (`telegram_bot.py`)
3. **Set up monitoring** alerts
4. **Deploy to multiple regions** for redundancy
5. **Add persistent storage** if needed

## Support

**Fly.io Documentation:** https://fly.io/docs  
**Fly.io Community:** https://community.fly.io  
**Telegram Bot API:** https://core.telegram.org/bots/api

---

**Your bot is now deployed to Fly.io! 🚀**

Always-on, no spin down, runs 24/7 in the cloud!
