# news.py

# A dictionary to store news articles
news_storage = {}

def add_news(news_id, title, short_title, photo_url, bullets, takeaway):
    """
    Adds a new news article to the storage.

    Args:
        news_id (str): Unique identifier for the news article.
        title (str): Full title of the article.
        short_title (str): Shortened title of the article.
        photo_url (str): URL to the article's image.
        bullets (list): Key points of the article.
        takeaway (str): Takeaway message for the article.

    Returns:
        bool: True if the article was added successfully, False otherwise.
    """
    if news_id in news_storage:
        return False  # News ID already exists

    news_storage[news_id] = {
        "title": title,
        "short_title": short_title,
        "photo_url": photo_url,
        "bullets": bullets,
        "takeaway": takeaway,
    }
    return True

def get_news(news_id):
    """
    Retrieves a news article by its ID.

    Args:
        news_id (str): Unique identifier for the news article.

    Returns:
        dict: The news article if found, None otherwise.
    """
    return news_storage.get(news_id)

def get_all_news():
    """
    Retrieves all news articles.

    Returns:
        dict: All stored news articles.
    """
    return news_storage
