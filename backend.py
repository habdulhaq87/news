import streamlit as st
import json
import os
import requests

# GitHub Configuration
GITHUB_USER = "habdulhaq87"
GITHUB_REPO = "news"
NEWS_FILE_PATH = "news.json"  # Path to the file in the repo
GITHUB_PAT = st.secrets["github"]["personal_access_token"]

# GitHub API URL
GITHUB_API_URL = f"https://api.github.com/repos/{GITHUB_USER}/{GITHUB_REPO}/contents/{NEWS_FILE_PATH}"

# Paths
PHOTO_DIR = "photo"
os.makedirs(PHOTO_DIR, exist_ok=True)

# Load news data from local
def load_news_data():
    if os.path.exists(NEWS_FILE_PATH):
        with open(NEWS_FILE_PATH, "r", encoding="utf-8") as file:
            return json.load(file)
    return []

# Save uploaded image to the photo directory
def save_uploaded_image(uploaded_file):
    file_path = os.path.join(PHOTO_DIR, uploaded_file.name)
    with open(file_path, "wb") as file:
        file.write(uploaded_file.getbuffer())
    return file_path

# Upload news.json to GitHub
def upload_to_github(news_data):
    # Get the current file SHA (needed for updates)
    headers = {"Authorization": f"token {GITHUB_PAT}"}
    response = requests.get(GITHUB_API_URL, headers=headers)
    if response.status_code == 200:
        sha = response.json()["sha"]  # Get file's SHA
    elif response.status_code == 404:
        sha = None  # File doesn't exist yet
    else:
        st.error(f"Error fetching file SHA: {response.status_code}")
        return False

    # Prepare the payload
    payload = {
        "message": "Update news.json",
        "content": json.dumps(news_data, ensure_ascii=False, indent=4),
        "sha": sha,
    }

    # Make the PUT request
    response = requests.put(GITHUB_API_URL, headers=headers, json=payload)
    if response.status_code in [200, 201]:
        st.success("news.json successfully updated on GitHub!")
        return True
    else:
        st.error(f"Error uploading file to GitHub: {response.status_code} - {response.text}")
        return False

# Initialize Streamlit app
st.set_page_config(page_title="News Backend", layout="wide")

# Load existing news data
news_data = load_news_data()

# Header
st.title("News Backend")
st.write("Manage your news articles dynamically. Add, edit, or delete articles from the JSON file.")

# Add new article
st.header("Add New Article")
with st.form("add_article_form", clear_on_submit=True):
    new_title = st.text_input("Title", key="new_title")
    new_subtitle = st.text_input("Subtitle", key="new_subtitle")
    new_content = st.text_area("Content (Markdown supported)", key="new_content")
    new_takeaway = st.text_area("Takeaway (Markdown supported)", key="new_takeaway")
    uploaded_image = st.file_uploader("Upload Image (jpg, png)", type=["jpg", "png"], key="new_image")

    submitted = st.form_submit_button("Add Article")

    if submitted:
        if new_title and new_subtitle and new_content and uploaded_image:
            image_path = save_uploaded_image(uploaded_image)
            relative_path = os.path.relpath(image_path, PHOTO_DIR)
            new_article = {
                "id": new_title.replace(" ", "_").lower(),
                "title": new_title,
                "subtitle": new_subtitle,
                "content": new_content,
                "takeaway": new_takeaway,
                "image_url": os.path.join(PHOTO_DIR, relative_path),
            }
            news_data.append(new_article)
            upload_to_github(news_data)
        else:
            st.error("All fields are required except Takeaway.")

# Manage existing articles
st.header("Manage Existing Articles")
for i, article in enumerate(news_data):
    st.subheader(f"Article {i+1}: {article['title']}")
    with st.expander("View / Edit Article"):
        edit_title = st.text_input("Title", value=article["title"], key=f"edit_title_{i}")
        edit_subtitle = st.text_input("Subtitle", value=article["subtitle"], key=f"edit_subtitle_{i}")
        edit_content = st.text_area("Content (Markdown supported)", value=article["content"], key=f"edit_content_{i}")
        edit_takeaway = st.text_area("Takeaway (Markdown supported)", value=article["takeaway"], key=f"edit_takeaway_{i}")
        st.image(article["image_url"], caption="Current Image", use_column_width=True)
        uploaded_image = st.file_uploader(f"Replace Image for Article {i+1} (jpg, png)", type=["jpg", "png"], key=f"edit_image_{i}")

        if uploaded_image:
            image_path = save_uploaded_image(uploaded_image)
            relative_path = os.path.relpath(image_path, PHOTO_DIR)
            article["image_url"] = os.path.join(PHOTO_DIR, relative_path)

        if st.button("Save Changes", key=f"save_{i}"):
            news_data[i] = {
                "id": edit_title.replace(" ", "_").lower(),
                "title": edit_title,
                "subtitle": edit_subtitle,
                "content": edit_content,
                "takeaway": edit_takeaway,
                "image_url": article["image_url"],
            }
            upload_to_github(news_data)

        if st.button("Delete Article", key=f"delete_{i}"):
            del news_data[i]
            upload_to_github(news_data)
            st.experimental_rerun()
