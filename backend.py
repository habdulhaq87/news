import streamlit as st
from view import view_articles  # Import view_articles function
from style import apply_styles, footer  # Import styles and footer functions
from style_page import style_page  # Import style management page
from add import add_article_page  # Import add article page

# Initialize the Streamlit app
st.set_page_config(page_title="News Backend", layout="wide")

# Apply styles globally
apply_styles()

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

if "current_page" not in st.session_state:
    st.session_state["current_page"] = "view"  # Default page

if st.sidebar.button("Add New Article"):
    st.session_state["current_page"] = "add"
if st.sidebar.button("View Articles"):
    st.session_state["current_page"] = "view"
if st.sidebar.button("Style Page"):
    st.session_state["current_page"] = "style"

# Page Navigation
if st.session_state["current_page"] == "add":
    add_article_page()
elif st.session_state["current_page"] == "view":
    view_articles()
elif st.session_state["current_page"] == "style":
    style_page()
