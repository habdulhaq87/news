import json
import os

# Path to the news JSON file
NEWS_FILE = "news.json"

def get_existing_news():
    """Load existing news from the JSON file."""
    if os.path.exists(NEWS_FILE):
        with open(NEWS_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    return []

def save_news(news_list):
    """Save the updated news list to the JSON file."""
    with open(NEWS_FILE, "w", encoding="utf-8") as file:
        json.dump(news_list, file, ensure_ascii=False, indent=4)

def add_news():
    """Prompt user to add a news article."""
    print("=== Add a New News Article ===")
    title = input("Title: ").strip()
    subtitle = input("Subtitle: ").strip()
    content = input("Content: ").strip()
    takeaway = input("Takeaway Message: ").strip()
    image_url = input("Image URL (or upload later): ").strip()

    # Add the new news article
    news_list = get_existing_news()
    news_list.append({
        "title": title,
        "subtitle": subtitle,
        "content": content,
        "takeaway": takeaway,
        "image_url": image_url
    })
    save_news(news_list)
    print("✅ News article added successfully!")

def main():
    """Main menu for managing news."""
    while True:
        print("\n=== News Management ===")
        print("1. Add a new news article")
        print("2. View existing news articles")
        print("3. Exit")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            add_news()
        elif choice == "2":
            news_list = get_existing_news()
            if not news_list:
                print("No news articles found.")
            else:
                for idx, news in enumerate(news_list, start=1):
                    print(f"\n{idx}. {news['title']}")
                    print(f"   Subtitle: {news['subtitle']}")
                    print(f"   Takeaway: {news['takeaway']}")
        elif choice == "3":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
