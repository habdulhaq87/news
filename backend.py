import streamlit as st
import json
import os
import requests

# Constants for GitHub integration
GITHUB_USER = "habdulhaq87"  # Your GitHub username
GITHUB_REPO = "news"         # Your repository name
GITHUB_PAT = st.secrets["github_pat"]  # Personal Access Token from Streamlit secrets

JSON_FILE = "news.json"
PHOTO_DIR = "photo"

# GitHub API URL for the news.json file
GITHUB_API_URL = f"https://api.github.com/repos/{GITHUB_USER}/{GITHUB_REPO}/contents/{JSON_FILE}"

# Ensure the photo directory exists
os.makedirs(PHOTO_DIR, exist_ok=True)

# Load news data from the JSON file (local)
def load_news_data():
    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    return []

# Save news data locally
def save_news_data_local(news_data):
    with open(JSON_FILE, "w", encoding="utf-8") as file:
        json.dump(news_data, file, ensure_ascii=False, indent=4)

# Upload news data to GitHub
def upload_to_github(file_path):
    # Read file content
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()
    
    # Get the current file SHA (required for updates)
    response = requests.get(GITHUB_API_URL, headers={"Authorization": f"token {GITHUB_PAT}"})
    if response.status_code == 200:
        sha = response.json().get("sha")
    elif response.status_code == 404:
        sha = None  # File doesn't exist yet
    else:
        st.error(f"Error fetching file information from GitHub: {response.status_code}")
        return False

    # Prepare the payload
    payload = {
        "message": "Update news.json via Streamlit backend",
        "content": content.encode("utf-8").decode("utf-8"),  # Base64 encoding handled by GitHub API
        "sha": sha
    }

    # Make the API request
    response = requests.put(
        GITHUB_API_URL,
        headers={"Authorization": f"token {GITHUB_PAT}"},
        json=payload
    )

    if response.status_code in [200, 201]:
        st.success("news.json successfully updated on GitHub!")
        return True
    else:
        st.error(f"Error uploading file to GitHub: {response.status_code} - {response.text}")
        return False

# Save and upload news data
def save_news_data(news_data):
    save_news_data_local(news_data)  # Save locally first
    upload_to_github(JSON_FILE)     # Then upload to GitHub

# Save uploaded image to the photo directory
def save_uploaded_image(uploaded_file):
    file_path = os.path.join(PHOTO_DIR, uploaded_file.name)
    with open(file_path, "wb") as file:
        file.write(uploaded_file.getbuffer())
    return file_path

# Initialize the Streamlit app
st.set_page_config(page_title="News Backend", layout="wide")

# Load existing news data
news_data = load_news_data()

# Header
st.title("News Backend")
st.write("Manage your news articles dynamically. Add, edit, or delete articles from the JSON file.")

# Add a new article
st.header("Add New Article")
with st.form("add_article_form", clear_on_submit=True):
    new_title = st.text_input("Title", key="new_title")
    new_subtitle = st.text_input("Subtitle", key="new_subtitle")
    new_content = st.text_area("Content (Markdown supported)", key="new_content", 
                                help="Use Markdown syntax for text styling. E.g., **bold**, *italic*, [link](http://example.com)")
    new_takeaway = st.text_area("Takeaway (Markdown supported)", key="new_takeaway", 
                                 help="Use Markdown syntax for text styling.")
    uploaded_image = st.file_uploader("Upload Image (jpg, png)", type=["jpg", "png"], key="new_image")

    submitted = st.form_submit_button("Add Article")

    if submitted:
        if new_title and new_subtitle and new_content and uploaded_image:
            image_path = save_uploaded_image(uploaded_image)
            relative_path = os.path.relpath(image_path, PHOTO_DIR)  # Save relative path to JSON
            new_article = {
                "id": new_title.replace(" ", "_").lower(),
                "title": new_title,
                "subtitle": new_subtitle,
                "content": new_content,
                "takeaway": new_takeaway,
                "image_url": os.path.join(PHOTO_DIR, relative_path),
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
        # Display existing details
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

        # Save changes
        if st.button("Save Changes", key=f"save_{i}"):
            news_data[i] = {
                "id": edit_title.replace(" ", "_").lower(),
                "title": edit_title,
                "subtitle": edit_subtitle,
                "content": edit_content,
                "takeaway": edit_takeaway,
                "image_url": article["image_url"],
            }
            save_news_data(news_data)
        
        # Delete article
        if st.button("Delete Article", key=f"delete_{i}"):
            del news_data[i]
            save_news_data(news_data)
            st.experimental_rerun()  # Refresh the app to reflect changes
