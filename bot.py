from telegram import Bot, InputMediaPhoto
from telegram.ext import Updater, CommandHandler
import json
import requests

# Bot token
BOT_TOKEN = "7553058540:AAFphfdsbYV6En1zCmPM4LeKuTYT65xJmkc"

# Path to the JSON file
NEWS_JSON = "news.json"

# Load news data from JSON
def load_news():
    with open(NEWS_JSON, "r", encoding="utf-8") as file:
        return json.load(file)

# Helper to shorten a URL using TinyURL API
def shorten_url(long_url):
    try:
        response = requests.get(f"http://tinyurl.com/api-create.php?url={long_url}")
        if response.status_code == 200:
            return response.text.strip()
        else:
            return long_url  # Fallback to long URL if TinyURL fails
    except Exception as e:
        return long_url

# Command to share the latest news
def share_news(update, context):
    chat_id = update.effective_chat.id
    bot = context.bot

    # Load the news data
    news_data = load_news()

    # Loop through the latest news and send them
    for news in news_data:
        # Generate the shareable link
        base_url = "https://habdulhaqnews.streamlit.app"
        long_url = f"{base_url}?news_id={news['id']}"
        short_url = shorten_url(long_url)

        # Create the message
        message = f"""
🌟 **{news['title']}**
_{news['subtitle']}_

{news['content'][:200]}...

🔗 [View Full Article]({short_url})
        """

        # Send the article with an image
        bot.send_photo(
            chat_id=chat_id,
            photo=news["image_url"],
            caption=message,
            parse_mode="Markdown",
        )

# Command to start the bot
def start(update, context):
    welcome_message = """
👋 Welcome to Hawkar Abdulhaq News Bot!

Use the command /share_news to share the latest news articles with a visually appealing format.
"""
    context.bot.send_message(chat_id=update.effective_chat.id, text=welcome_message)

# Main function to start the bot
def main():
    updater = Updater(token=BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # Add command handlers
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("share_news", share_news))

    # Start polling
    updater.start_polling()
    print("Bot is running...")
    updater.idle()

if __name__ == "__main__":
    main()
