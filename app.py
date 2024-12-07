import streamlit as st
import json
from urllib.parse import urlencode

# Load news from JSON file
NEWS_FILE = "news.json"

def load_news():
    """Load news articles from the JSON file."""
    try:
        with open(NEWS_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

# Load all news articles
news_list = load_news()

# Set up page configuration
st.set_page_config(page_title="هەواڵی نوێ", page_icon="📰", layout="wide")

# Display the latest news article
if news_list:
    latest_news = news_list[-1]  # Show the latest news first
    news_title = latest_news["title"]
    news_subtitle = latest_news["subtitle"]
    news_content = latest_news["content"]
    news_takeaway = latest_news["takeaway"]
    news_image_url = latest_news["image_url"]
else:
    st.error("No news articles available. Please add news via `news.py`.")

# Helper function to generate a shareable link
def generate_shareable_link(news_id):
    base_url = "https://q5c32sstqku8zyyrmxtcil.streamlit.app"  # Replace with your Streamlit URL
    params = {"news_id": news_id}
    return f"{base_url}?{urlencode(params)}"

# Add custom CSS for styling
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
            font-size: 18px;
            color: #666666;
            margin-bottom: 20px;
        }

        .news-content {
            font-size: 20px;
            line-height: 1.8;
            color: #555555;
            direction: rtl;
        }

        .takeaway {
            font-size: 18px;
            font-style: italic;
            color: #444444;
            margin-top: 30px;
        }

        .telegram-logo {
            width: 24px;
            height: 24px;
            vertical-align: middle;
            margin-right: 8px;
        }
    </style>
""", unsafe_allow_html=True)

if news_list:
    st.image(news_image_url, use_column_width=True, caption=news_subtitle)
    st.markdown(f"""
        <div class="news-container">
            <div class="news-title">{news_title}</div>
            <div class="news-subtitle">{news_subtitle}</div>
            <div class="news-content">{news_content}</div>
            <div class="takeaway">📌 {news_takeaway}</div>
        </div>
    """, unsafe_allow_html=True)

    # Generate and display shareable link
    shareable_link = generate_shareable_link(news_id="latest")
    st.markdown(f"""
        <div style="margin-top: 20px;">
            <a class="share-button" href="{shareable_link}" target="_blank">🔗 هاوکاری بکە و هەواڵەکەی بڵاو بکە</a>
        </div>
    """, unsafe_allow_html=True)

st.markdown(f"""
    <div class="footnote-container">
        فەرەی <strong>ھەوکەر علی عبدولحق</strong> لە تێلەگرام:
        <a href="https://t.me/habdulaq" target="_blank"><img src="{telegram_logo_url}" class="telegram-logo"></a>
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
