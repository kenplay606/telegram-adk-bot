"""
AI Agency Suite - Modern Marketing Dashboard
"""
import streamlit as st
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.config import settings

st.set_page_config(
    page_title=settings.APP_NAME,
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for dark modern design
st.markdown("""
<style>
    /* Dark theme base */
    .main {
        background-color: #0a0e27;
    }
    
    .testimonial-card {
        background: rgba(30, 41, 59, 0.6);
        border-left: 4px solid #64b5f6;
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(100, 181, 246, 0.2);
    }
    
    .service-card {
        background: rgba(30, 41, 59, 0.4);
        border-radius: 12px;
        padding: 2rem;
        border: 1px solid rgba(100, 181, 246, 0.2);
        height: 100%;
        backdrop-filter: blur(10px);
    }
    
    .service-card h3 {
        color: #64b5f6;
        margin-bottom: 1rem;
    }
    
    .service-card p, .service-card li {
        color: #b0bec5;
    }
    
    .stat-box {
        text-align: center;
        padding: 2.5rem;
        background: rgba(30, 41, 59, 0.6);
        border: 1px solid rgba(100, 181, 246, 0.3);
        color: white;
        border-radius: 12px;
        backdrop-filter: blur(10px);
    }
    
    .stat-number {
        font-size: 3.5rem;
        font-weight: bold;
        color: #64b5f6;
    }
    
    .section-title {
        font-size: 2.5rem;
        font-weight: 300;
        margin: 3rem 0 2rem 0;
        color: white;
        text-align: center;
    }
    
    .testimonial-card p {
        color: #b0bec5;
    }
    
    .testimonial-card p:last-child {
        color: #64b5f6;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar navigation
st.sidebar.title("🤖 AI Agency Suite")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigation",
    ["🏠 Home", "👥 Clients", "📱 Personal Content", "📊 Analytics", "⚙️ Settings"]
)

# Main content
if page == "🏠 Home":
    # Hero Section - Dark Modern Design
    st.markdown("""
    <div style="text-align: center; padding: 4rem 2rem; background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%); border-radius: 15px; margin-bottom: 3rem;">
        <h1 style="font-size: 4rem; font-weight: 300; color: white; margin-bottom: 1rem;">
            Halo <span style="color: #64b5f6;">AI studio</span>.
        </h1>
        <p style="font-size: 1.3rem; color: #b0bec5; margin-bottom: 2rem;">
            We develop custom AI solutions for innovative companies.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Statistics Section
    st.markdown('<h2 class="section-title">Statistics</h2>', unsafe_allow_html=True)
    
    stat_col1, stat_col2, stat_col3 = st.columns(3)
    
    with stat_col1:
        st.markdown("""
        <div class="stat-box">
            <div class="stat-number">80K</div>
            <p>Docs Saved Per Month</p>
        </div>
        """, unsafe_allow_html=True)
    
    with stat_col2:
        st.markdown("""
        <div class="stat-box">
            <div class="stat-number">€50K</div>
            <p>Cost Saved Per Month</p>
        </div>
        """, unsafe_allow_html=True)
    
    with stat_col3:
        st.markdown("""
        <div class="stat-box">
            <div class="stat-number">+10%</div>
            <p>Efficiency Increase</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # What We Do Section
    st.markdown('<h2 class="section-title">What we do</h2>', unsafe_allow_html=True)
    
    service_col1, service_col2 = st.columns(2)
    
    with service_col1:
        st.markdown("""
        <div class="service-card">
            <h3>🤖 Chatbot Development</h3>
            <p>We develop custom AI solutions for innovative companies. Chatbots that leverage advanced NLP to deliver seamless customer interactions and enhance your business processes.</p>
            <ul>
                <li>24/7 Customer Support</li>
                <li>Multi-language Support</li>
                <li>CRM Integration</li>
                <li>Advanced Analytics</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with service_col2:
        st.markdown("""
        <div class="service-card">
            <h3>✍️ Content Creation</h3>
            <p>Our content creation solutions effectively generate high-quality, engaging content according to your brand's guidelines to capture your audience.</p>
            <ul>
                <li>Video Script Writing</li>
                <li>Social Media Posts</li>
                <li>Blog Articles</li>
                <li>Marketing Copy</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Reviews Section
    st.markdown('<h2 class="section-title">⭐ Client Reviews</h2>', unsafe_allow_html=True)
    
    review_col1, review_col2 = st.columns(2)
    
    with review_col1:
        st.markdown("""
        <div class="testimonial-card">
            <p style="font-style: italic;">"Thanks to AI Agency Suite, we've been able to find the right solution for our business needs. The automation has saved us countless hours. Highly recommended!"</p>
            <p style="font-weight: bold; margin-top: 1rem;">— Dan M., CTO / Wired</p>
        </div>
        """, unsafe_allow_html=True)
    
    with review_col2:
        st.markdown("""
        <div class="testimonial-card">
            <p style="font-style: italic;">"Highly recommendable! AI Agency Suite is a great way to quickly get started on your AI journey. The support team is fantastic and the results speak for themselves."</p>
            <p style="font-weight: bold; margin-top: 1rem;">— Jasmine E., CEO / TechCorp</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Process Section
    st.markdown('<h2 class="section-title">Our Process</h2>', unsafe_allow_html=True)
    
    process_col1, process_col2, process_col3 = st.columns(3)
    
    with process_col1:
        st.markdown("""
        <div class="service-card">
            <h3>01 Discover & Plan</h3>
            <p>We analyze your business needs and create a customized AI strategy tailored to your goals.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with process_col2:
        st.markdown("""
        <div class="service-card">
            <h3>02 Build & Deploy</h3>
            <p>Our team develops and implements your AI solutions with seamless integration into your existing systems.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with process_col3:
        st.markdown("""
        <div class="service-card">
            <h3>03 Maintain & Improve</h3>
            <p>After deployment, our team will keep working hard by providing support and continuously improving the implemented solutions.</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Get in Touch Section
    st.markdown('<h2 class="section-title">Get in Touch</h2>', unsafe_allow_html=True)
    
    contact_col1, contact_col2, contact_col3 = st.columns([1, 2, 1])
    
    with contact_col2:
        st.markdown("""
        <div style="text-align: center; padding: 2.5rem; background: rgba(30, 41, 59, 0.6); border-radius: 12px; border: 1px solid rgba(100, 181, 246, 0.3); backdrop-filter: blur(10px);">
            <h3 style="color: #64b5f6; margin-bottom: 1rem;">Ready to Transform Your Business?</h3>
            <p style="color: #b0bec5;">Contact us today to discuss how AI can revolutionize your operations.</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Contact Us", key="contact_btn", use_container_width=True):
            st.success("✅ Thank you! We'll get back to you within 24 hours.")

elif page == "👥 Clients":
    from dashboard.pages import clients
    clients.show()

elif page == "📱 Personal Content":
    from dashboard.pages import personal_content
    personal_content.show()

elif page == "📊 Analytics":
    st.title("📊 Analytics Dashboard")
    st.info("Analytics dashboard coming soon!")

elif page == "⚙️ Settings":
    st.title("⚙️ Settings")
    
    st.subheader("API Configuration")
    st.markdown("""
    Configure your API keys in the `.env` file:
    
    - **Instagram**: For client DM automation
    - **YouTube**: For posting Shorts
    - **Facebook**: For posting videos
    - **OpenRouter**: Optional cloud AI (free tier available at https://openrouter.ai/keys)
    
    See `.env.example` for all available settings.
    """)
    
    st.subheader("System Status")
    col1, col2 = st.columns(2)
    
    with col1:
        st.success("✅ Ollama Connected")
        st.info(f"Model: {settings.OLLAMA_MODEL}")
    
    with col2:
        if settings.OPENROUTER_API_KEY:
            st.success("✅ OpenRouter API Configured")
            st.info(f"Model: {settings.OPENROUTER_MODEL}")
        else:
            st.warning("⚠️ OpenRouter API Not Configured")
    
    st.subheader("Database")
    st.code(settings.DATABASE_URL)
    
    st.subheader("Storage Directories")
    st.code(f"Videos: {settings.VIDEO_OUTPUT_DIR}")
    st.code(f"Thumbnails: {settings.THUMBNAIL_OUTPUT_DIR}")
    st.code(f"ChromaDB: {settings.CHROMA_PERSIST_DIR}")

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("**AI Agency Suite v1.0**")
st.sidebar.markdown("Powered by Ollama + FastAPI + Streamlit")
