"""
Client management page
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
    st.title("👥 Client Management")
    
    tab1, tab2 = st.tabs(["📋 Client List", "➕ Add Client"])
    
    with tab1:
        st.subheader("Your Clients")
        
        try:
            response = requests.get(f"{API_URL}/clients/")
            if response.status_code == 200:
                clients = response.json()
                
                if clients:
                    for client in clients:
                        with st.expander(f"**{client['name']}** - {client['company'] or 'No company'}"):
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                st.write(f"**Email:** {client['email']}")
                                st.write(f"**Industry:** {client['industry'] or 'Not specified'}")
                                st.write(f"**Instagram:** @{client['instagram_username'] or 'Not connected'}")
                            
                            with col2:
                                st.write(f"**Status:** {'🟢 Active' if client['is_active'] else '🔴 Inactive'}")
                                st.write(f"**Created:** {client['created_at'][:10]}")
                            
                            if st.button(f"View Stats", key=f"stats_{client['id']}"):
                                stats_response = requests.get(f"{API_URL}/clients/{client['id']}/stats")
                                if stats_response.status_code == 200:
                                    stats = stats_response.json()
                                    st.json(stats)
                else:
                    st.info("No clients yet. Add your first client in the 'Add Client' tab!")
            else:
                st.error("Failed to load clients")
        
        except Exception as e:
            st.error(f"Error connecting to API: {e}")
            st.info("Make sure the backend server is running: `python backend/main.py`")
    
    with tab2:
        st.subheader("Add New Client")
        
        with st.form("add_client_form"):
            name = st.text_input("Client Name*")
            email = st.text_input("Email*")
            company = st.text_input("Company")
            industry = st.text_input("Industry")
            
            st.markdown("**Social Media Accounts**")
            instagram_username = st.text_input("Instagram Username")
            instagram_account_id = st.text_input("Instagram Account ID")
            
            st.markdown("**Brand Information**")
            brand_voice = st.text_area("Brand Voice (tone, style, keywords)")
            target_audience = st.text_area("Target Audience")
            
            submitted = st.form_submit_button("Add Client")
            
            if submitted:
                if not name or not email:
                    st.error("Name and Email are required!")
                else:
                    client_data = {
                        "name": name,
                        "email": email,
                        "company": company,
                        "industry": industry,
                        "instagram_username": instagram_username,
                        "instagram_account_id": instagram_account_id,
                        "brand_voice": brand_voice,
                        "target_audience": target_audience
                    }
                    
                    try:
                        response = requests.post(f"{API_URL}/clients/", json=client_data)
                        if response.status_code == 200:
                            st.success(f"✅ Client '{name}' added successfully!")
                            st.balloons()
                        else:
                            st.error(f"Failed to add client: {response.json().get('detail', 'Unknown error')}")
                    except Exception as e:
                        st.error(f"Error: {e}")
