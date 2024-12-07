import json
import os

# File path for the JSON file
NEWS_FILE = "news.json"

def load_news():
    """Load the news from the JSON file."""
    if os.path.exists(NEWS_FILE):
        with open(NEWS_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    return []

def save_news(news_list):
    """Save the news list to the JSON file."""
    with open(NEWS_FILE, "w", encoding="utf-8") as file:
        json.dump(news_list, file, ensure_ascii=False, indent=4)

def add_news():
    """Prompt the user to add a new article."""
    print("Add a New News Article")
    id = input("Enter a unique ID for the article: ")
    title = input("Enter the news title: ")
    subtitle = input("Enter the news subtitle: ")
    content = input("Enter the full news content: ")
    takeaway = input("Enter the takeaway message: ")
    image_url = input("Enter the URL of the image: ")

    # Load the existing news
    news_list = load_news()

    # Add the new article
    news_list.insert(0, {
        "id": id,
        "title": title,
        "subtitle": subtitle,
        "content": content,
        "takeaway": takeaway,
        "image_url": image_url
    })

    # Save the updated list
    save_news(news_list)
    print("✅ News article added successfully!")

if __name__ == "__main__":
    add_news()
