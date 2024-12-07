import json
import os

# Path to the JSON file for storing news
NEWS_FILE = "news_data.json"

# Initialize the JSON file if it doesn't exist
if not os.path.exists(NEWS_FILE):
    with open(NEWS_FILE, "w") as f:
        json.dump({}, f)

# Function to load all news
def load_news():
    with open(NEWS_FILE, "r") as f:
        return json.load(f)

# Function to save all news
def save_news(news_data):
    with open(NEWS_FILE, "w") as f:
        json.dump(news_data, f, indent=4)

# Function to add a new news entry
def add_news(news_id, title, short_title, photo_url, bullets, takeaway):
    news_data = load_news()
    news_data[news_id] = {
        "title": title,
        "short_title": short_title,
        "photo_url": photo_url,
        "bullets": bullets,
        "takeaway": takeaway,
    }
    save_news(news_data)
