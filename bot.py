import requests

# Telegram bot token and chat ID
TELEGRAM_BOT_TOKEN = "7553058540:AAFphfdsbYV6En1zCmPM4LeKuTYT65xJmkc"
TELEGRAM_CHAT_ID = "@1239693460"  # Replace with your Telegram channel username or ID

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
    # Validate the image URL
    if not (image_url.startswith("http://") or image_url.startswith("https://")):
        return False, f"Invalid image URL: {image_url}. It must be an HTTP/HTTPS URL."

    message = f"""
🌟 **{title}**
_{subtitle}_

{content[:200]}... *(Read more in the full article)*

🔗 [Read more]({link})

📌 **بە کورتی**:
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
        # Post to Telegram
        response = requests.post(telegram_url, data=payload)
        debug_message = (
            f"Attempting to post to Telegram:\n"
            f"Chat ID: {TELEGRAM_CHAT_ID}\n"
            f"Payload: {payload}\n"
            f"Response Status Code: {response.status_code}\n"
            f"Response Text: {response.text}\n"
        )
        
        if response.status_code == 200:
            debug_message += "Success: Article posted to Telegram."
            return True, debug_message
        else:
            debug_message += f"Error: Failed to post to Telegram. Status code: {response.status_code}."
            return False, debug_message
    except Exception as e:
        debug_message = f"Exception occurred: {e}"
        return False, debug_message
