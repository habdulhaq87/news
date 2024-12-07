import streamlit as st
import json
import os
import requests
import base64
import time
from streamlit_quill import st_quill
from view import view_articles
from bot import post_to_telegram

# Your existing backend code...
# Constants, loading news, GitHub integration, etc.

# Sidebar navigation
st.sidebar.title("Navigation")
pages = {
    "Add New Article": "add",
    "View Articles": "view",
}
page_selection = st.sidebar.radio("Go to", list(pages.keys()))
st.session_state["current_page"] = pages[page_selection]

# Page routing
if st.session_state["current_page"] == "add":
    # Add new article functionality
    # Your add article form logic
    pass
elif st.session_state["current_page"] == "view":
    view_articles(news_data, save_news_data, save_uploaded_image_to_github, post_to_telegram)
