# 🤖 AI Agency Suite

**Complete Multi-Client Marketing Agency + Personal Content Automation Platform**

A comprehensive AI-powered system that combines:
- **Marketing Agency**: Manage multiple clients, create campaigns, build websites, automate Instagram DMs
- **Personal Content Creator**: Generate viral video ideas, write scripts, create videos, auto-post to social media

## 🔐 Security First

**This project follows strict security practices:**
- ✅ **No hardcoded secrets** - All API keys loaded from environment variables
- ✅ **`.env` never committed** - Included in `.gitignore`
- ✅ **`.env.example` provided** - Template with placeholders
- ✅ **No logging of secrets** - Sensitive data never logged
- ✅ **Local-first** - Works completely offline with Ollama

## ✨ Features

### Marketing Agency (Multi-Client)
- 👥 **Client Management** - Manage multiple clients with separate memories
- 🎨 **Ad Designer** - Create advertising campaigns and copy
- 🌐 **Website Builder** - Generate complete HTML/CSS/JS websites
- 📈 **SEO Optimizer** - Optimize content for search engines
- 📱 **Instagram Automation** - Auto-respond to DMs for each client
- 📊 **Analytics** - Track campaign performance
- 📧 **Lead Capture** - Collect and manage leads
- 🗓️ **Content Strategist** - Plan content calendars

### Personal Content Agency (For You)
- 💡 **Content Ideas** - Generate viral video concepts
- ✍️ **Script Writer** - Write engaging video scripts
- 🎬 **Video Assembler** - Create videos with TTS + subtitles
- 🖼️ **Thumbnail Generator** - Design eye-catching thumbnails
- 📤 **Social Poster** - Auto-upload to YouTube, Instagram, Facebook

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Ollama (will be installed during setup)

### Installation

1. **Clone or navigate to the project:**
```bash
cd ai-agency-suite
```

2. **Run setup (installs everything):**
```bash
python setup.py
```

This will:
- ✅ Check Python version
- ✅ Install dependencies
- ✅ Install Ollama (if needed)
- ✅ Pull AI model (llama3.1)
- ✅ Initialize database
- ✅ Create `.env` file
- ✅ Create necessary directories

3. **Configure API keys (optional):**

Edit `.env` and add your keys:
```env
# Optional - for social media posting
INSTAGRAM_ACCESS_TOKEN=your_token_here
YOUTUBE_API_KEY=your_key_here
FACEBOOK_ACCESS_TOKEN=your_token_here

# Optional - for cloud AI (free tier available)
GROQ_API_KEY=your_key_here
```

**The system works 100% locally without these keys!**

4. **Start the system:**
```bash
python run.py
```

5. **Access the platform:**
- 📊 **Dashboard**: http://localhost:8501
- 🔌 **API Docs**: http://localhost:8000/docs

## 📖 Usage

### Marketing Agency

#### Add a Client
```python
# Via Dashboard: Clients → Add Client
# Or via API:
import requests

client_data = {
    "name": "Joe's Pizza",
    "email": "joe@joespizza.com",
    "company": "Joe's Pizza",
    "industry": "restaurant",
    "instagram_username": "joespizza",
    "brand_voice": "Friendly, casual, family-oriented",
    "target_audience": "Local families and food lovers"
}

response = requests.post("http://localhost:8000/api/clients/", json=client_data)
```

#### Build a Website
```python
# Via Dashboard: Use the marketing tools
# Or via API:
website_request = {
    "client_id": 1,
    "business_name": "Joe's Pizza",
    "business_type": "restaurant",
    "description": "Family-owned pizza restaurant",
    "features": ["menu", "contact", "gallery", "reviews"]
}

response = requests.post("http://localhost:8000/api/marketing/website/build", json=website_request)
```

#### Auto-Respond to Instagram DMs
The system automatically responds when configured:
1. Set up Instagram webhook (see deployment docs)
2. Add client's Instagram account ID
3. Messages are auto-processed and responded to

### Personal Content Creation

#### Generate Video Ideas
```python
# Via Dashboard: Personal Content → Ideas
# Or via API:
ideas_request = {
    "niche": "finance",
    "platform": "youtube_shorts",
    "count": 10,
    "trending_topics": ["passive income", "investing"]
}

response = requests.post("http://localhost:8000/api/personal/ideas/generate", json=ideas_request)
```

#### Create a Complete Video
```python
# 1. Generate ideas
# 2. Write script
script_request = {
    "title": "5 Ways to Make Money Online",
    "main_points": [
        "Start affiliate marketing",
        "Create digital products",
        "Freelance your skills",
        "Build a YouTube channel",
        "Invest in dividend stocks"
    ],
    "duration": 60,
    "style": "educational"
}

script_response = requests.post("http://localhost:8000/api/personal/script/write", json=script_request)

# 3. Create video
video_request = {
    "script": script_response.json()["full_script"],
    "title": "5 Ways to Make Money Online",
    "add_subtitles": True
}

video_response = requests.post("http://localhost:8000/api/personal/video/create", json=video_request)

# 4. Post to social media
post_request = {
    "video_path": video_response.json()["video_path"],
    "platform": "youtube_shorts",
    "title": "5 Ways to Make Money Online",
    "description": "Learn how to make money online with these proven methods",
    "tags": ["money", "finance", "passive income"]
}

post_response = requests.post("http://localhost:8000/api/personal/post/youtube", json=post_request)
```

## 🗂️ Project Structure

```
ai-agency-suite/
├── backend/
│   ├── agents/
│   │   ├── marketing/          # Client marketing agents
│   │   │   ├── ad_designer.py
│   │   │   ├── website_builder.py
│   │   │   └── instagram_messaging.py
│   │   └── personal/           # Personal content agents
│   │       ├── content_ideas.py
│   │       ├── script_writer.py
│   │       ├── video_assembler.py
│   │       └── social_poster.py
│   ├── api/                    # FastAPI routes
│   ├── core/                   # Core utilities
│   ├── models/                 # Database models
│   └── memory/                 # Memory management
├── dashboard/                  # Streamlit UI
├── docker/                     # Docker deployment
├── .env.example               # Environment template
├── requirements.txt
├── setup.py                   # One-command setup
└── run.py                     # Start everything
```

## 🔧 Configuration

All configuration is in `.env`:

```env
# Core
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=llama3.1

# Optional Cloud AI
GROQ_API_KEY=                  # Free tier: https://console.groq.com

# Social Media (Optional)
INSTAGRAM_ACCESS_TOKEN=        # https://developers.facebook.com/
YOUTUBE_API_KEY=               # https://console.cloud.google.com/
FACEBOOK_ACCESS_TOKEN=         # https://developers.facebook.com/

# Video Settings
VIDEO_RESOLUTION=1080x1920     # Vertical video for Shorts/Reels
VIDEO_FPS=30
TTS_ENGINE=gtts                # or pyttsx3 for offline
```

## 🐳 Docker Deployment

### Local Docker
```bash
cd docker
docker-compose up -d
```

### Cloud Deployment (Render, Fly.io, Railway)

1. **Push to GitHub** (`.env` is gitignored)

2. **Deploy to Render:**
   - Connect GitHub repo
   - Add environment variables from `.env.example`
   - Deploy

3. **Deploy to Fly.io:**
```bash
fly launch
fly secrets set OLLAMA_MODEL=llama3.1
fly secrets set GROQ_API_KEY=your_key
fly deploy
```

## 📊 API Documentation

Once running, visit:
- **Interactive API Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Key Endpoints

**Clients:**
- `POST /api/clients/` - Create client
- `GET /api/clients/` - List clients
- `GET /api/clients/{id}/stats` - Get client stats

**Marketing:**
- `POST /api/marketing/website/build` - Build website
- `POST /api/marketing/ads/campaign` - Create ad campaign
- `POST /api/marketing/instagram/respond` - Process Instagram DM

**Personal Content:**
- `POST /api/personal/ideas/generate` - Generate video ideas
- `POST /api/personal/script/write` - Write script
- `POST /api/personal/video/create` - Create video
- `POST /api/personal/post/youtube` - Post to YouTube

## 🔒 Security Best Practices

1. **Never commit `.env`** - It's in `.gitignore`
2. **Use environment variables** - All secrets from env
3. **Rotate API keys regularly**
4. **Use HTTPS in production**
5. **Enable API authentication** - Set `API_KEY` in `.env`
6. **Limit CORS origins** - Update in `backend/main.py`

## 🆓 Free Tier Resources

- **Ollama**: 100% free, runs locally
- **Groq API**: 30 requests/min free
- **YouTube API**: 10,000 units/day free
- **Instagram API**: Free tier available
- **Facebook API**: Free tier available

## 🛠️ Development

### Run in Development Mode
```bash
# Backend only
python backend/main.py

# Dashboard only
streamlit run dashboard/streamlit_app.py

# Both
python run.py
```

### Run Tests
```bash
pytest
```

### Code Formatting
```bash
black .
flake8 .
```

## 📝 Troubleshooting

### Ollama Not Found
```bash
# Install Ollama
# Windows: Download from https://ollama.ai/download/windows
# Mac: brew install ollama
# Linux: curl -fsSL https://ollama.ai/install.sh | sh

# Pull model
ollama pull llama3.1
```

### Database Issues
```bash
# Reinitialize database
python -c "from backend.core.db_client import init_db; init_db()"
```

### API Connection Error
- Ensure backend is running: `python backend/main.py`
- Check port 8000 is not in use

### Video Creation Fails
- Check FFmpeg is installed: `ffmpeg -version`
- Ensure TTS engine is configured in `.env`

## 🤝 Contributing

This is a complete, production-ready system. Feel free to:
- Add new agents
- Enhance existing features
- Improve UI/UX
- Add integrations

## 📄 License

MIT License - Use freely for personal or commercial projects

## 🙏 Acknowledgments

Built with:
- **Ollama** - Local AI models
- **FastAPI** - Backend API
- **Streamlit** - Dashboard UI
- **ChromaDB** - Vector memory
- **MoviePy** - Video processing
- **SQLAlchemy** - Database ORM

---

**🚀 Ready to build your AI agency empire!**

For questions or issues, check the documentation or API docs at `/docs`.
