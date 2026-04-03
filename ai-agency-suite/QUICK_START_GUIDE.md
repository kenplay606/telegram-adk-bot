# 🚀 Quick Start Guide - AI Agency Suite

## 📍 Access Your Dashboard

**Dashboard URL:** http://localhost:8501

## 👥 Step 1: Add a Client

1. Click **"👥 Clients"** in the left sidebar
2. Click the **"➕ Add Client"** tab
3. Fill in the form:
   - **Client Name:** e.g., "Acme Restaurant"
   - **Business Type:** e.g., "Restaurant"
   - **Contact Email:** e.g., "owner@acme.com"
   - **Description:** Brief business description
4. Click **"Add Client"**

## 🤖 Step 2: Generate AI Website

### Using the API (PowerShell):

```powershell
# Build a website for client ID 1
$body = @{
    client_id = 1
    business_name = "Acme Restaurant"
    business_type = "Restaurant"
    description = "Modern Italian restaurant serving authentic pasta and pizza"
    features = @("Online reservations", "Menu showcase", "Contact form")
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/api/marketing/website/build" -Method POST -Body $body -ContentType "application/json"
```

### Using cURL:

```bash
curl -X POST "http://localhost:8000/api/marketing/website/build" \
  -H "Content-Type: application/json" \
  -d '{
    "client_id": 1,
    "business_name": "Acme Restaurant",
    "business_type": "Restaurant",
    "description": "Modern Italian restaurant serving authentic pasta and pizza",
    "features": ["Online reservations", "Menu showcase", "Contact form"]
  }'
```

## 📱 Step 3: Generate Personal Content (Videos)

1. Click **"📱 Personal Content"** in the sidebar
2. Use the tabs:
   - **💡 Ideas** - Generate viral video ideas
   - **✍️ Scripts** - Write video scripts
   - **🎬 Videos** - Create videos with AI voiceover
   - **📤 Post** - Post to social media

### Generate Video Ideas:

In the **💡 Ideas** tab:
- **Topic:** e.g., "AI automation tips"
- **Platform:** Choose YouTube Shorts, Instagram Reels, or TikTok
- Click **"Generate Ideas"**

### Write a Script:

In the **✍️ Scripts** tab:
- **Video Idea:** Paste your idea
- **Duration:** e.g., 30 seconds
- **Style:** Choose tone (energetic, professional, etc.)
- Click **"Generate Script"**

## 🎨 Step 4: Create Ad Campaigns

### Generate Ad Campaign Strategy:

```powershell
$body = @{
    client_id = 1
    campaign_type = "brand_awareness"
    platform = "facebook"
    target_audience = "Food enthusiasts aged 25-45"
    budget = 1000
    goals = @("Increase reservations", "Build brand awareness")
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/api/marketing/ads/campaign" -Method POST -Body $body -ContentType "application/json"
```

### Generate Ad Copy:

```powershell
$body = @{
    client_id = 1
    product_service = "Italian Restaurant Dining Experience"
    platform = "facebook"
    tone = "warm"
    length = "short"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/api/marketing/ads/copy" -Method POST -Body $body -ContentType "application/json"
```

## 📊 Available API Endpoints

### Marketing Agents:
- `POST /api/marketing/website/build` - Build complete website
- `POST /api/marketing/website/seo` - Get SEO optimization tips
- `POST /api/marketing/ads/campaign` - Create ad campaign strategy
- `POST /api/marketing/ads/copy` - Generate ad copy variations

### Personal Content:
- `POST /api/personal/ideas/generate` - Generate video ideas
- `POST /api/personal/ideas/trending` - Analyze trending topics
- `POST /api/personal/script/write` - Write video script
- `POST /api/personal/video/create` - Create video with TTS
- `POST /api/personal/post/youtube` - Post to YouTube
- `POST /api/personal/post/instagram` - Post to Instagram
- `POST /api/personal/post/facebook` - Post to Facebook

### Clients:
- `GET /api/clients/` - List all clients
- `POST /api/clients/` - Create new client
- `GET /api/clients/{id}` - Get client details
- `PUT /api/clients/{id}` - Update client
- `DELETE /api/clients/{id}` - Delete client

## 🔑 API Documentation

Full interactive API docs available at:
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

## 💡 Tips

1. **Always add a client first** before using marketing features
2. **Check the Settings page** to verify OpenRouter is configured
3. **Use the API docs** at http://localhost:8000/docs for interactive testing
4. **Generated websites** are saved in the `output/websites/` directory
5. **Generated videos** are saved in the `output/videos/` directory

## 🆘 Need Help?

- Check logs in the terminal where services are running
- Visit Settings page to verify system status
- Use the interactive API docs for testing endpoints
