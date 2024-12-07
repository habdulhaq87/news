import streamlit as st
import json
import os
import requests
import base64
import time
from urllib.parse import urlencode

# Constants for GitHub integration
GITHUB_USER = "habdulhaq87"
GITHUB_REPO = "news"
GITHUB_PAT = st.secrets["github_pat"]

JSON_FILE = "news.json"
PHOTO_DIR = "photo"

# GitHub API URLs
GITHUB_API_URL_JSON = f"https://api.github.com/repos/{GITHUB_USER}/{GITHUB_REPO}/contents/{JSON_FILE}"
GITHUB_API_URL_PHOTO = f"https://api.github.com/repos/{GITHUB_USER}/{GITHUB_REPO}/contents/{PHOTO_DIR}"

# Telegram bot token and chat ID
TELEGRAM_BOT_TOKEN = st.secrets.get("telegram_bot_token", "YOUR_BOT_TOKEN")
TELEGRAM_CHAT_ID = st.secrets.get("telegram_chat_id", "@YOUR_CHANNEL_USERNAME")


# Load existing news data from GitHub
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


# Helper function to shorten a URL using TinyURL API
def shorten_url(long_url):
    try:
        response = requests.get(f"http://tinyurl.com/api-create.php?url={long_url}")
        if response.status_code == 200:
            return response.text.strip()
        return long_url
    except Exception as e:
        print(f"Error generating short URL: {e}")
        return long_url


# Helper function to generate a shareable link
def generate_shareable_link(news_id):
    base_url = "https://habdulhaqnews.streamlit.app"  # Replace with your Streamlit URL
    params = {"news_id": news_id}
    long_url = f"{base_url}?{urlencode(params)}"
    return shorten_url(long_url)


# Function to post to Telegram
def post_to_telegram(news):
    title = news.get("title", "Untitled")
    subtitle = news.get("subtitle", "")
    content = news.get("content", "")
    takeaway = news.get("takeaway", "")
    image_url = news.get("image_url", "")
    link = generate_shareable_link(news.get("id", ""))

    message = f"""
🌟 **{title}**
_{subtitle}_

{content[:200]}...

🔗 [Read more]({link})

📌 **Takeaway**:
{takeaway}
    """

    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "photo": image_url,
        "caption": message,
        "parse_mode": "Markdown",
    }
    telegram_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto"
    try:
        response = requests.post(telegram_url, data=payload)
        return response.status_code == 200, response.json()
    except Exception as e:
        return False, {"error": str(e)}


# Function to handle Telegram posting from app
def handle_post_to_telegram(news_id):
    news_data = load_news_data()
    news_item = next((news for news in news_data if news["id"] == news_id), None)
    if not news_item:
        return False, {"error": "News article not found."}

    success, response = post_to_telegram(news_item)
    return success, response
