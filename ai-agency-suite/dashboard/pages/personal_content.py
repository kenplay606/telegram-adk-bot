"""
Personal content creation page
"""
import streamlit as st
import requests
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from backend.config import settings

# Use localhost instead of 0.0.0.0 for Windows compatibility
API_URL = f"http://localhost:{settings.API_PORT}/api"


def show():
    st.title("📱 Personal Content Creation")
    
    tab1, tab2, tab3, tab4 = st.tabs(["💡 Ideas", "✍️ Scripts", "🎬 Videos", "📤 Post"])
    
    with tab1:
        st.subheader("Generate Video Ideas")
        
        col1, col2 = st.columns(2)
        
        with col1:
            niche = st.text_input("Content Niche", "finance")
            platform = st.selectbox("Platform", ["youtube_shorts", "instagram_reels", "tiktok"])
        
        with col2:
            count = st.slider("Number of Ideas", 1, 20, 10)
        
        trending_topics = st.text_input("Trending Topics (comma-separated, optional)")
        
        if st.button("🚀 Generate Ideas"):
            with st.spinner("Generating viral video ideas..."):
                try:
                    payload = {
                        "niche": niche,
                        "platform": platform,
                        "count": count
                    }
                    
                    if trending_topics:
                        payload["trending_topics"] = [t.strip() for t in trending_topics.split(",")]
                    
                    response = requests.post(f"{API_URL}/personal/ideas/generate", json=payload)
                    
                    if response.status_code == 200:
                        result = response.json()
                        ideas = result.get("ideas", [])
                        
                        st.success(f"✅ Generated {len(ideas)} video ideas!")
                        
                        for i, idea in enumerate(ideas, 1):
                            with st.expander(f"💡 Idea {i}: {idea.get('title', 'Untitled')}"):
                                st.markdown(f"**Hook:** {idea.get('hook', 'N/A')}")
                                st.markdown(f"**Main Points:**")
                                for point in idea.get('main_points', []):
                                    st.markdown(f"- {point}")
                                st.markdown(f"**CTA:** {idea.get('cta', 'N/A')}")
                                st.markdown(f"**Duration:** {idea.get('duration', 'N/A')}s")
                                st.markdown(f"**Viral Score:** {idea.get('viral_score', 'N/A')}/10")
                    else:
                        st.error("Failed to generate ideas")
                
                except Exception as e:
                    st.error(f"Error: {e}")
    
    with tab2:
        st.subheader("Write Video Script")
        
        title = st.text_input("Video Title", "How to Make Money Online")
        
        main_points = st.text_area(
            "Main Points (one per line)",
            "Start with affiliate marketing\nCreate valuable content\nBuild an audience\nMonetize multiple ways"
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            duration = st.slider("Duration (seconds)", 15, 90, 60)
        
        with col2:
            style = st.selectbox("Style", ["educational", "entertaining", "storytelling", "motivational"])
        
        if st.button("✍️ Write Script"):
            with st.spinner("Writing script..."):
                try:
                    points_list = [p.strip() for p in main_points.split("\n") if p.strip()]
                    
                    payload = {
                        "title": title,
                        "main_points": points_list,
                        "duration": duration,
                        "style": style
                    }
                    
                    response = requests.post(f"{API_URL}/personal/script/write", json=payload)
                    
                    if response.status_code == 200:
                        script = response.json()
                        
                        st.success("✅ Script written!")
                        
                        st.markdown("### 🎬 Full Script")
                        st.text_area("Script", script.get("full_script", ""), height=300)
                        
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.markdown("**Hook:**")
                            st.info(script.get("hook", "N/A"))
                        
                        with col2:
                            st.markdown("**CTA:**")
                            st.info(script.get("cta", "N/A"))
                        
                        # Store script in session state for video creation
                        st.session_state['last_script'] = script.get("full_script", "")
                        st.session_state['last_title'] = title
                    else:
                        st.error("Failed to write script")
                
                except Exception as e:
                    st.error(f"Error: {e}")
    
    with tab3:
        st.subheader("Create Video")
        
        # Use script from previous tab if available
        if 'last_script' in st.session_state:
            script = st.text_area("Script", st.session_state['last_script'], height=200)
            video_title = st.text_input("Title", st.session_state.get('last_title', ''))
        else:
            script = st.text_area("Script", height=200)
            video_title = st.text_input("Title")
        
        add_subtitles = st.checkbox("Add Subtitles", value=True)
        
        if st.button("🎬 Create Video"):
            if not script or not video_title:
                st.error("Please provide both script and title")
            else:
                with st.spinner("Creating video... This may take a few minutes"):
                    try:
                        payload = {
                            "script": script,
                            "title": video_title,
                            "add_subtitles": add_subtitles
                        }
                        
                        response = requests.post(f"{API_URL}/personal/video/create", json=payload)
                        
                        if response.status_code == 200:
                            result = response.json()
                            
                            st.success("✅ Video created successfully!")
                            
                            st.markdown(f"**Video Path:** `{result.get('video_path')}`")
                            st.markdown(f"**Thumbnail:** `{result.get('thumbnail_path')}`")
                            st.markdown(f"**Duration:** {result.get('duration', 0):.1f}s")
                            st.markdown(f"**File Size:** {result.get('file_size', 0) / 1024 / 1024:.1f} MB")
                            
                            # Store for posting
                            st.session_state['last_video'] = result.get('video_path')
                            st.session_state['last_video_title'] = video_title
                        else:
                            st.error("Failed to create video")
                    
                    except Exception as e:
                        st.error(f"Error: {e}")
    
    with tab4:
        st.subheader("Post to Social Media")
        
        # Use video from previous tab if available
        if 'last_video' in st.session_state:
            video_path = st.text_input("Video Path", st.session_state['last_video'])
            post_title = st.text_input("Title/Caption", st.session_state.get('last_video_title', ''))
        else:
            video_path = st.text_input("Video Path")
            post_title = st.text_input("Title/Caption")
        
        platform = st.selectbox("Platform", ["youtube_shorts", "instagram_reels", "facebook"])
        
        description = st.text_area("Description (YouTube only)")
        tags = st.text_input("Tags/Hashtags (comma-separated)")
        
        if st.button("📤 Post"):
            if not video_path:
                st.error("Please provide video path")
            else:
                with st.spinner(f"Posting to {platform}..."):
                    try:
                        payload = {
                            "video_path": video_path,
                            "platform": platform,
                            "title": post_title,
                            "description": description,
                            "caption": post_title,
                            "tags": [t.strip() for t in tags.split(",") if t.strip()],
                            "hashtags": [t.strip() for t in tags.split(",") if t.strip()]
                        }
                        
                        if platform == "youtube_shorts":
                            response = requests.post(f"{API_URL}/personal/post/youtube", json=payload)
                        elif platform == "instagram_reels":
                            response = requests.post(f"{API_URL}/personal/post/instagram", json=payload)
                        else:
                            response = requests.post(f"{API_URL}/personal/post/facebook", json=payload)
                        
                        if response.status_code == 200:
                            result = response.json()
                            
                            if result.get('status') == 'saved_locally':
                                st.warning("⚠️ Video saved locally (API credentials not configured)")
                                st.info(result.get('note', ''))
                                st.code(f"Saved to: {result.get('path')}")
                            else:
                                st.success(f"✅ Posted to {platform}!")
                                if result.get('url'):
                                    st.markdown(f"**URL:** {result['url']}")
                        else:
                            st.error("Failed to post")
                    
                    except Exception as e:
                        st.error(f"Error: {e}")
