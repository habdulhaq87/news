import streamlit as st
import json
import os
import requests
import base64
import time
from streamlit_quill import st_quill  # Rich text editor

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

# AI Suggestions for Writing Content
def suggest_content(text):
    api_url = "https://api.openai.com/v1/completions"
    headers = {
        "Authorization": f"Bearer {st.secrets['openai_api_key']}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "text-davinci-003",
        "prompt": f"Improve the following content: {text}",
        "max_tokens": 150,
        "temperature": 0.7
    }
    response = requests.post(api_url, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json().get("choices")[0].get("text").strip()
    return "No suggestions available."

# Initialize the Streamlit app
st.set_page_config(page_title="News Backend", layout="wide")

# Load existing news data
news_data = load_news_data()

# Header
st.title("News Backend")
st.write("Manage your news articles dynamically. Add, edit, or delete articles from the JSON file.")

# Add a new article
st.header("Add New Article")

# Separate AI suggestions outside the form
content_for_suggestions = st_quill("Write your content here and get suggestions", key="content_suggestions")
if st.button("Get Suggestions for Content"):
    suggestions = suggest_content(content_for_suggestions or "")
    st.write(f"Suggestions: {suggestions}")

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
        else:
            st.error("All fields are required except Takeaway.")

# Edit or delete existing articles
st.header("Manage Existing Articles")
for i, article in enumerate(news_data):
    st.subheader(f"Article {i+1}: {article['title']}")
    with st.expander("View / Edit Article"):
        edit_title = st.text_input("Title", value=article["title"], key=f"edit_title_{i}")
        edit_subtitle = st.text_input("Subtitle", value=article["subtitle"], key=f"edit_subtitle_{i}")
        edit_content = st_quill("Edit your content here", key=f"edit_content_{i}")  # No direct `value`
        edit_takeaway = st.text_area("Takeaway (Markdown supported)", value=article["takeaway"], key=f"edit_takeaway_{i}")
        st.image(article["image_url"], caption="Current Image", use_container_width=True)
        uploaded_image = st.file_uploader(f"Replace Image for Article {i+1} (jpg, png)", type=["jpg", "png"], key=f"edit_image_{i}")

        if uploaded_image:
            image_url = save_uploaded_image_to_github(uploaded_image)
            if image_url:
                article["image_url"] = image_url

        if st.button("Save Changes", key=f"save_{i}"):
            news_data[i] = {
                "id": edit_title.replace(" ", "_").lower(),
                "title": edit_title,
                "subtitle": edit_subtitle,
                "content": edit_content or article["content"],
                "takeaway": edit_takeaway,
                "image_url": article["image_url"],
            }
            save_news_data(news_data)

        if st.button("Delete Article", key=f"delete_{i}"):
            del news_data[i]
            save_news_data(news_data)
            st.experimental_rerun()
