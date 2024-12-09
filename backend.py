import streamlit as st
import json
import os
import requests
import base64
import time
from view import view_articles  # Import view_articles function
from bot import post_to_telegram  # Import Telegram posting functionality
from style import apply_styles, footer  # Import styles and footer functions
from style_page import style_page  # Import style management page

# Constants for GitHub integration
GITHUB_USER = "habdulhaq87"
GITHUB_REPO = "news"
GITHUB_PAT = st.secrets["github_pat"]

JSON_FILE = "news.json"
PHOTO_DIR = "photo"

# GitHub API URLs
GITHUB_API_URL_JSON = f"https://api.github.com/repos/{GITHUB_USER}/{GITHUB_REPO}/contents/{JSON_FILE}"
GITHUB_API_URL_PHOTO = f"https://api.github.com/repos/{GITHUB_USER}/{GITHUB_REPO}/contents/{PHOTO_DIR}"

# Upload a file to GitHub
def upload_to_github(file_path, github_path, commit_message):
    with open(file_path, "rb") as file:
        content = file.read()

    base64_content = base64.b64encode(content).decode("utf-8")
    response = requests.get(github_path, headers={"Authorization": f"token {GITHUB_PAT}"})
    sha = response.json().get("sha") if response.status_code == 200 else None

    payload = {
        "message": commit_message,
        "content": base64_content,
        "sha": sha
    }

    response = requests.put(
        github_path,
        headers={"Authorization": f"token {GITHUB_PAT}"},
        json=payload
    )

    return response.status_code in [200, 201]

# Save uploaded image to GitHub and return its GitHub URL
def save_uploaded_image_to_github(uploaded_file):
    if not uploaded_file:
        return None

    timestamp = int(time.time())
    filename = f"{timestamp}_{uploaded_file.name}"
    file_path = os.path.join("/tmp", filename)

    with open(file_path, "wb") as file:
        file.write(uploaded_file.getbuffer())

    github_path = f"{GITHUB_API_URL_PHOTO}/{filename}"
    if upload_to_github(file_path, github_path, f"Add image {filename}"):
        return f"https://raw.githubusercontent.com/{GITHUB_USER}/{GITHUB_REPO}/main/{PHOTO_DIR}/{filename}"
    return None

# Load existing news data
def load_news_data():
    response = requests.get(GITHUB_API_URL_JSON, headers={"Authorization": f"token {GITHUB_PAT}"})
    if response.status_code == 200:
        content = base64.b64decode(response.json().get("content")).decode("utf-8")
        return json.loads(content)
    return []

# Save news data to GitHub
def save_news_data(news_data):
    content = json.dumps(news_data, ensure_ascii=False, indent=4)
    content_encoded = base64.b64encode(content.encode("utf-8")).decode("utf-8")

    response = requests.get(GITHUB_API_URL_JSON, headers={"Authorization": f"token {GITHUB_PAT}"})
    sha = response.json().get("sha") if response.status_code == 200 else None

    payload = {
        "message": "Update news data via Streamlit app",
        "content": content_encoded,
        "sha": sha,
    }

    response = requests.put(
        GITHUB_API_URL_JSON,
        headers={"Authorization": f"token {GITHUB_PAT}"},
        json=payload,
    )

    if response.status_code not in [200, 201]:
        st.error("Failed to update news data on GitHub. Please check your permissions or the repository.")

# Initialize the Streamlit app
st.set_page_config(page_title="News Backend", layout="wide")  # Called once here

# Apply styles globally
apply_styles()

# Sidebar Navigation as Buttons
st.sidebar.title("Navigation")
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

# Page: Add New Article
if st.session_state["current_page"] == "add":
    from add import main as add_main  # Importing here to avoid circular import
    add_main(news_data, save_news_data, save_uploaded_image_to_github)

# Page: View Articles
elif st.session_state["current_page"] == "view":
    view_articles(news_data, save_news_data, save_uploaded_image_to_github, post_to_telegram)

# Page: Style Page
elif st.session_state["current_page"] == "style":
    style_page()

