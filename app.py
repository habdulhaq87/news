import streamlit as st
from urllib.parse import urlencode
import json
import os

# Set up page configuration (must be the first Streamlit command)
st.set_page_config(page_title="News App", page_icon="📰", layout="wide")

# File path for the JSON file
NEWS_FILE = "news.json"

def load_news():
    """Load the news from the JSON file."""
    if os.path.exists(NEWS_FILE):
        with open(NEWS_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    return []

def save_news(news_list):
    """Save the news list to the JSON file."""
    with open(NEWS_FILE, "w", encoding="utf-8") as file:
        json.dump(news_list, file, ensure_ascii=False, indent=4)

# Load existing news
news_list = load_news()

# Sidebar for adding new articles
st.sidebar.header("Add a New News Article")
with st.sidebar.form("add_news_form"):
    new_id = st.text_input("Unique ID", "")
    new_title = st.text_input("Title", "")
    new_subtitle = st.text_input("Subtitle", "")
    new_content = st.text_area("Content", "")
    new_takeaway = st.text_input("Takeaway Message", "")
    new_image_url = st.text_input("Image URL", "")
    submit_button = st.form_submit_button("Add News")

if submit_button:
    if new_id and new_title and new_subtitle and new_content and new_takeaway and new_image_url:
        # Add the new article
        news_list.insert(0, {
            "id": new_id,
            "title": new_title,
            "subtitle": new_subtitle,
            "content": new_content,
            "takeaway": new_takeaway,
            "image_url": new_image_url
        })
        save_news(news_list)
        st.sidebar.success("✅ News article added successfully!")
        st.experimental_rerun()  # Refresh the page to load the new article
    else:
        st.sidebar.error("❌ All fields are required!")

# Check if there is news to display
if news_list:
    news = news_list[0]
else:
    st.error("No news articles available.")
    st.stop()

# Helper function to generate a shareable link
def generate_shareable_link(news_id):
    base_url = "https://q5c32sstqku8zyyrmxtcil.streamlit.app"  # Replace with your Streamlit URL
    params = {"news_id": news_id}
    return f"{base_url}?{urlencode(params)}"

# Add custom CSS for enhanced styling with custom font
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
            font-size: 24px;
            font-weight: 500;
            color: #555555;
            margin-bottom: 20px;
        }

        .news-content {
            font-size: 20px;
            line-height: 1.8;
            color: #555555;
            direction: rtl;
        }

        .telegram-logo {
            width: 24px;  /* Reduced size */
            height: 24px; /* Reduced size */
            vertical-align: middle;
            margin-right: 8px;
        }

        .takeaway {
            font-size: 18px;
            font-style: italic;
            color: #007BFF;
            margin-top: 20px;
        }
    </style>
""", unsafe_allow_html=True)

# Display the latest article
st.image(news["image_url"], use_column_width=True, caption=news["subtitle"])
st.markdown(f"""
    <div class="news-container">
        <div class="news-title">{news["title"]}</div>
        <div class="news-subtitle">{news["subtitle"]}</div>
        <div class="news-content">{news["content"]}</div>
        <div class="takeaway">Takeaway: {news["takeaway"]}</div>
    </div>
""", unsafe_allow_html=True)

# Generate and display the shareable link
shareable_link = generate_shareable_link(news["id"])
if st.button("🔗 هاوکاری بکە و هەواڵەکەی بڵاو بکە", key="share_button", help="کرتە بکە بۆ هاوکاری کردن"):
    st.success("بەستەرەکە دروست کرا!")
    st.write("کرتە بکە لە بەستەرەکە بۆ هاوکاری:")
    st.markdown(f'<a class="share-button" href="{shareable_link}" target="_blank">بڵاوکردنەوە</a>', unsafe_allow_html=True)

# Footer with Telegram and contact info
st.markdown(f"""
    <div class="footnote-container">
        فەرەی <strong>ھەوکەر علی عبدولحق</strong> لە تێلەگرام:
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
