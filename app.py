import streamlit as st
from backend import (
    save_uploaded_image_to_github,
    save_news_data,
    load_news_data,
    upload_to_github,
)  # Import necessary functions from backend
from view import view_articles  # Import the article viewing module
from bot import post_to_telegram  # Import Telegram posting functionality
from style import apply_styles  # Apply global styles
from style_page import style_page  # Import style management functionality
from add import main as add_main  # Import add module main function

# Initialize the Streamlit app
st.set_page_config(page_title="News Management App", layout="wide")

# Apply global styles
apply_styles()

# Sidebar Navigation
st.sidebar.title("Navigation")
if "current_page" not in st.session_state:
    st.session_state["current_page"] = "view"  # Default page

if st.sidebar.button("Add New Article"):
    st.session_state["current_page"] = "add"
if st.sidebar.button("View Articles"):
    st.session_state["current_page"] = "view"
if st.sidebar.button("Style Page"):
    st.session_state["current_page"] = "style"

# Load the existing news data from GitHub
news_data = load_news_data()

# Page: Add New Article
if st.session_state["current_page"] == "add":
    add_main(news_data, save_news_data, save_uploaded_image_to_github)

# Page: View Articles
elif st.session_state["current_page"] == "view":
    view_articles(news_data, save_news_data, save_uploaded_image_to_github, post_to_telegram)

# Page: Style Page
elif st.session_state["current_page"] == "style":
    style_page()
