import requests
import streamlit as st

# Telegram bot token and chat ID
TELEGRAM_BOT_TOKEN = "7553058540:AAFphfdsbYV6En1zCmPM4LeKuTYT65xJmkc"
TELEGRAM_CHAT_ID = "@hawkartest"  # Replace with your Telegram channel username

def post_to_telegram(title, subtitle, content, takeaway, image_url, link):
    """
    Post a news article to Telegram.
    
    Args:
        title (str): Title of the article.
        subtitle (str): Subtitle of the article.
        content (str): Content of the article.
        takeaway (str): Takeaway or key points.
        image_url (str): URL of the image to post.
        link (str): Link to the full article.
    
    Returns:
        None
    """
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
            print("Posted successfully to Telegram!")
        else:
            print(f"Failed to post to Telegram. Status code: {response.status_code}")
            print(response.json())
    except Exception as e:
        print(f"Error posting to Telegram: {e}")
