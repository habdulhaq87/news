import streamlit as st
import json
import requests
from urllib.parse import urlencode

# Set up page configuration
st.set_page_config(page_title="هەواڵی نوێ", page_icon="📰", layout="wide")

# Telegram bot token and chat ID
TELEGRAM_BOT_TOKEN = "7553058540:AAFphfdsbYV6En1zCmPM4LeKuTYT65xJmkc"
TELEGRAM_CHAT_ID = "@habdulaq"  # Replace with your Telegram channel username

# Load news from the JSON file
def load_news_data():
    with open("news.json", "r", encoding="utf-8") as file:
        return json.load(file)

news_data = load_news_data()

# Helper function to shorten a URL using TinyURL API
def shorten_url(long_url):
    try:
        response = requests.get(f"http://tinyurl.com/api-create.php?url={long_url}")
        if response.status_code == 200:
            return response.text.strip()
        else:
            st.warning(f"TinyURL API failed with status code {response.status_code}. Using the long URL instead.")
            return long_url
    except Exception as e:
        st.error(f"Error generating short URL: {e}")
        return long_url

# Helper function to generate a shareable link
def generate_shareable_link(news_id):
    base_url = "https://habdulhaqnews.streamlit.app"  # Replace with your Streamlit URL
    params = {"news_id": news_id}
    long_url = f"{base_url}?{urlencode(params)}"
    return shorten_url(long_url)

# Function to post to Telegram
def post_to_telegram(title, subtitle, content, takeaway, image_url, link):
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
        "caption": message,
        "photo": image_url,
        "parse_mode": "Markdown",
    }
    telegram_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto"
    try:
        response = requests.post(telegram_url, data=payload)
        if response.status_code == 200:
            st.success("Posted successfully to Telegram!")
        else:
            st.error(f"Failed to post to Telegram. Status code: {response.status_code}")
    except Exception as e:
        st.error(f"Error posting to Telegram: {e}")

# Add custom CSS for enhanced styling
st.markdown("""
    <style>
        @font-face {
            font-family: 'SpedaBold';
            src: url('font/Speda-Bold.eot');
            src: url('font/Speda-Bold.eot?#iefix') format('embedded-opentype'),
                 url('font/Speda-Bold.woff') format('woff'),
                 url('font/Speda-Bold.ttf') format('truetype'),
                 url('font/Speda-Bold.svg#SpedaBold') format('svg');
            font-weight: normal;
            font-style: normal;
        }

        body {
            background-color: #f4f4f4;
            font-family: 'SpedaBold', Arial, sans-serif;
            direction: rtl;
        }

        .news-container {
            background-color: #ffffff;
            padding: 30px;
            border-radius: 12px;
            box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1);
            max-width: 800px;
            margin: 0 auto;
            direction: rtl;
        }

        .news-title {
            font-size: 36px;
            font-weight: bold;
            color: #333333;
            margin-bottom: 10px;
        }

        .news-subtitle {
            font-size: 20px;
            color: #777777;
            margin-bottom: 20px;
        }

        .news-content {
            font-size: 20px;
            line-height: 1.8;
            color: #555555;
            margin-bottom: 20px;
        }

        .news-takeaway {
            font-size: 18px;
            font-style: italic;
            color: #007BFF;
            margin-top: 20px;
        }

        .telegram-logo {
            width: 24px;
            height: 24px;
            vertical-align: middle;
            margin-right: 8px;
        }
    </style>
""", unsafe_allow_html=True)

# Display all news articles with previews
for news in news_data:
    short_url = generate_shareable_link(news["id"])  # Generate the TinyURL
    st.image(news["image_url"], use_column_width=True, caption=news["title"])
    st.markdown(f"""
        <div class="news-container">
            <div class="news-title">{news["title"]}</div>
            <div class="news-subtitle">{news["subtitle"]}</div>
            <div class="news-content">{news["content"][:250]}...</div>
        </div>
    """, unsafe_allow_html=True)

    # Display Tiny URL in a read-only text input
    st.text_input(f"Tiny URL for {news['title']}", value=short_url, key=f"tiny_url_{news['id']}")

    # Add button to post to Telegram
    if st.button(f"Post '{news['title']}' to Telegram", key=f"post_{news['id']}"):
        post_to_telegram(
            title=news["title"],
            subtitle=news["subtitle"],
            content=news["content"],
            takeaway=news["takeaway"],
            image_url=news["image_url"],
            link=short_url,
        )

# Footer with contact info
st.markdown(f"""
    <div class="footnote-container">
        فەرەی <strong>هاوکار علی عبدالحق</strong> لە تێلەگرام:
        <a href="https://t.me/habdulaq" target="_blank"><img src="https://i.imgur.com/Hxr3jCj.png" class="telegram-logo"></a>
        <br>
        <a href="https://www.habdulhaq.com" target="_blank">www.habdulhaq.com</a><br>
        <a href="mailto:connect@habdulhaq.com">connect@habdulhaq.com</a>
    </div>
""", unsafe_allow_html=True)

st.markdown("""
    <div class="footer">
        پەروەردەکراو بە <strong>Streamlit</strong> | <a href="https://streamlit.io" target="_blank">فێرببە</a>
    </div>
""", unsafe_allow_html=True)
