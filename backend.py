import streamlit as st
import json
import os
import requests
import base64
import time

# Constants for GitHub integration
GITHUB_USER = "habdulhaq87"
GITHUB_REPO = "news"
GITHUB_PAT = st.secrets["github_pat"]

JSON_FILE = "news.json"
PHOTO_DIR = "photo"

# Telegram bot token and chat ID
TELEGRAM_BOT_TOKEN = "7553058540:AAFphfdsbYV6En1zCmPM4LeKuTYT65xJmkc"
TELEGRAM_CHAT_ID = "@habdulaq"

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

# Function to post to Telegram
def post_to_telegram(article):
    title = article["title"]
    subtitle = article["subtitle"]
    content = article["content"]
    takeaway = article["takeaway"]
    image_url = article["image_url"]
    link = article.get("short_url", "")

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
        if response.status_code == 200:
            st.success(f"Posted successfully to Telegram: {title}")
        else:
            st.error(f"Failed to post to Telegram. Status code: {response.status_code}")
            st.error(response.json())
    except Exception as e:
        st.error(f"Error posting to Telegram: {e}")

# Initialize the Streamlit backend app
st.set_page_config(page_title="News Backend", layout="wide")

# Load existing news data
news_data = load_news_data()

# Header
st.title("News Backend")
st.write("Manage your news articles dynamically. Add, edit, delete, or post articles to Telegram.")

# Manage existing articles with Telegram posting option
st.header("Manage Articles")
for i, article in enumerate(news_data):
    st.subheader(f"Article {i+1}: {article['title']}")
    with st.expander("View / Edit / Post Article"):
        st.write(f"**Subtitle:** {article['subtitle']}")
        st.write(f"**Content:** {article['content']}")
        st.write(f"**Takeaway:** {article['takeaway']}")
        st.image(article["image_url"], caption="Article Image", use_container_width=True)

        # Add button to post to Telegram
        if st.button(f"Post '{article['title']}' to Telegram", key=f"post_{i}"):
            post_to_telegram(article)
