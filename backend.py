import streamlit as st
import json
from add import add_article_page  # Import the add article page
from view import view_articles  # Import the view articles page
from style_page import style_page  # Import the style management page
from backend_utils import load_news_data  # Import utility functions

# Initialize the Streamlit app
st.set_page_config(page_title="News Backend", layout="wide")

# Sidebar Navigation as Buttons
st.sidebar.title("Navigation")
st.sidebar.markdown(
    """
    <style>
        .stButton>button {
            background-color: #007BFF;
            color: white;
            border-radius: 8px;
            border: none;
            padding: 8px 16px;
            margin: 4px 0;
            font-size: 16px;
            font-weight: bold;
        }
        .stButton>button:hover {
            background-color: #0056b3;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Session state for current page
if "current_page" not in st.session_state:
    st.session_state["current_page"] = "view"  # Default page

if st.sidebar.button("Add New Article"):
    st.session_state["current_page"] = "add"
if st.sidebar.button("View Articles"):
    st.session_state["current_page"] = "view"
if st.sidebar.button("Style Page"):
    st.session_state["current_page"] = "style"

# Load existing news data
news_data = load_news_data()

# Route to the appropriate page
if st.session_state["current_page"] == "add":
    add_article_page(news_data)
elif st.session_state["current_page"] == "view":
    view_articles(news_data)
elif st.session_state["current_page"] == "style":
    style_page()
