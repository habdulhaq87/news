import requests

# Telegram bot token and chat ID
TELEGRAM_BOT_TOKEN = "7553058540:AAFphfdsbYV6En1zCmPM4LeKuTYT65xJmkc"
TELEGRAM_CHAT_ID = "@habdulaq"  # Replace with your Telegram channel username or ID

def post_to_telegram(title, subtitle, content, takeaway, image_url, link):
    """
    Post a news article to Telegram with detailed debugging.

    Args:
        title (str): Title of the article.
        subtitle (str): Subtitle of the article.
        content (str): Content of the article.
        takeaway (str): Takeaway or key points.
        image_url (str): URL of the image to post.
        link (str): Link to the full article.

    Returns:
        tuple: (bool, str) - Success status and debug message.
    """
    message = f"""
🌟 **{title}**
_{subtitle}_

{content[:200]}... *(Read more in the full article)*

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
        debug_message = f"Payload: {payload}\nResponse: {response.text}\n"
        
        if response.status_code == 200:
            debug_message += "Success: Article posted to Telegram."
            return True, debug_message
        else:
            debug_message += f"Error: Failed to post to Telegram. Status code: {response.status_code}."
            return False, debug_message
    except Exception as e:
        debug_message = f"Exception occurred: {e}"
        return False, debug_message
