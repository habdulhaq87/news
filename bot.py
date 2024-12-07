import requests
import logging

# Configure logging
logging.basicConfig(
    level=logging.DEBUG, 
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.FileHandler("telegram_debug.log"), logging.StreamHandler()]
)

# Telegram bot token and chat ID
TELEGRAM_BOT_TOKEN = "7553058540:AAFphfdsbYV6En1zCmPM4LeKuTYT65xJmkc"
TELEGRAM_CHAT_ID = "@hawkartest"  # Replace with your Telegram channel username or ID

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
        bool: True if posted successfully, False otherwise.
    """
    try:
        # Create the message body
        message = f"""
🌟 **{title}**
_{subtitle}_

{content[:200]}... *(Read more in the full article)*

🔗 [Read more]({link})

📌 **Takeaway**:
{takeaway}
        """
        logging.debug("Message constructed for Telegram: %s", message)
        
        # Define the payload for the Telegram API
        payload = {
            "chat_id": TELEGRAM_CHAT_ID,
            "photo": image_url,
            "caption": message,
            "parse_mode": "Markdown",
        }
        logging.debug("Payload constructed: %s", payload)
        
        # Construct the Telegram API URL
        telegram_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto"
        logging.debug("Telegram API URL: %s", telegram_url)
        
        # Send the POST request to Telegram
        response = requests.post(telegram_url, data=payload)
        logging.debug("Response received: %s", response.text)
        
        # Check the response status
        if response.status_code == 200:
            logging.info("Posted successfully to Telegram!")
            return True
        else:
            logging.error(
                "Failed to post to Telegram. Status code: %d. Response: %s",
                response.status_code,
                response.json(),
            )
            return False
    except Exception as e:
        logging.exception("Error posting to Telegram: %s", e)
        return False

# Example usage for testing
if __name__ == "__main__":
    # Sample article data
    sample_title = "Test Article Title"
    sample_subtitle = "A sample subtitle for the article."
    sample_content = "This is a brief snippet of the article content, highlighting the main points of the news."
    sample_takeaway = "Key insights or takeaways from the article."
    sample_image_url = "https://via.placeholder.com/800x400.png"
    sample_link = "https://example.com/full-article"

    # Call the function to post to Telegram
    result = post_to_telegram(
        title=sample_title,
        subtitle=sample_subtitle,
        content=sample_content,
        takeaway=sample_takeaway,
        image_url=sample_image_url,
        link=sample_link,
    )

    if result:
        print("Article posted to Telegram successfully.")
    else:
        print("Failed to post the article.")
