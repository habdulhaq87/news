import requests

# Telegram bot token and chat ID
TELEGRAM_BOT_TOKEN = "7553058540:AAFphfdsbYV6En1zCmPM4LeKuTYT65xJmkc"
TELEGRAM_CHAT_ID = "@hawkartest"  # Replace with your Telegram channel username or ID

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
        bool: True if posted successfully, False otherwise.
    """
    # Format the message
    message = f"""
🌟 **{title}**
_{subtitle}_

{content[:200]}...  *(Read more in the full article)*

🔗 [Read more]({link})

📌 **Takeaway**:
{takeaway}
    """
    # Construct the payload for Telegram API
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "photo": image_url,
        "caption": message,
        "parse_mode": "Markdown",
    }

    # Telegram API endpoint
    telegram_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto"

    try:
        # Send the POST request to Telegram API
        response = requests.post(telegram_url, data=payload)
        if response.status_code == 200:
            print("Posted successfully to Telegram!")
            return True
        else:
            # Log failure details
            print(f"Failed to post to Telegram. Status code: {response.status_code}")
            try:
                print(f"Response: {response.json()}")
            except Exception as json_error:
                print(f"Error parsing JSON response: {json_error}")
            return False
    except requests.exceptions.RequestException as req_error:
        # Handle network-related errors
        print(f"Request error while posting to Telegram: {req_error}")
        return False
    except Exception as e:
        # Log any unexpected exceptions
        print(f"Unexpected error posting to Telegram: {e}")
        return False

# Example usage for testing
if __name__ == "__main__":
    # Sample data
    sample_title = "Test Title"
    sample_subtitle = "This is a subtitle"
    sample_content = "This is the content of the article. It's quite engaging and informative."
    sample_takeaway = "Key takeaways are essential for summaries."
    sample_image_url = "https://via.placeholder.com/800x400.png"
    sample_link = "https://example.com/full-article"

    # Post to Telegram
    result = post_to_telegram(
        title=sample_title,
        subtitle=sample_subtitle,
        content=sample_content,
        takeaway=sample_takeaway,
        image_url=sample_image_url,
        link=sample_link,
    )

    if result:
        print("Article posted successfully.")
    else:
        print("Failed to post the article.")
