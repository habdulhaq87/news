import streamlit as st
import json
import os
import requests
import base64
import time
from streamlit_quill import st_quill  # Rich text editor
from view import view_articles  # Import view_articles function
from bot import post_to_telegram  # Import Telegram posting functionality

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
    with open(JSON_FILE, "w", encoding="utf-8") as file:
        json.dump(news_data, file, ensure_ascii=False, indent=4)
    upload_to_github(JSON_FILE, GITHUB_API_URL_JSON, "Update news.json via Streamlit backend")

# Initialize the Streamlit app
st.set_page_config(page_title="News Backend", layout="wide")

# Sidebar Navigation
st.sidebar.title("Navigation")
navigation = st.sidebar.radio(
    "Select Page",
    options=["Add New Article", "View Articles"]
)

# Load existing news data
news_data = load_news_data()

# Page: Add New Article
if navigation == "Add New Article":
    st.title("Add New Article")
    with st.form("add_article_form", clear_on_submit=True):
        new_title = st.text_input("Title", key="new_title")
        new_subtitle = st.text_input("Subtitle", key="new_subtitle")
        new_content = st_quill("Write your content here", key="new_content")  # Initialize blank editor
        new_takeaway = st.text_area("Takeaway (Markdown supported)", key="new_takeaway")
        uploaded_image = st.file_uploader("Upload Image (jpg, png)", type=["jpg", "png"], key="new_image")

        submitted = st.form_submit_button("Add Article")

        if submitted:
            if new_title and new_subtitle and new_content and uploaded_image:
                image_url = save_uploaded_image_to_github(uploaded_image)
                if image_url:
                    new_article = {
                        "id": new_title.replace(" ", "_").lower(),
                        "title": new_title,
                        "subtitle": new_subtitle,
                        "content": new_content,
                        "takeaway": new_takeaway,
                        "image_url": image_url,
                    }
                    news_data.append(new_article)
                    save_news_data(news_data)
                    st.success("Article added successfully!")
            else:
                st.error("All fields are required except Takeaway.")

# Page: View Articles
elif navigation == "View Articles":
    view_articles(news_data, save_news_data, save_uploaded_image_to_github, post_to_telegram)
