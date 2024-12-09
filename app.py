import streamlit as st
import json
import requests
from urllib.parse import urlencode, quote
from markdown import markdown  # Import markdown for HTML rendering
from style import apply_styles, footer  # Import styles and footer
import re  # For parsing image URLs from Markdown

# Set up page configuration
st.set_page_config(page_title="هەواڵی نوێ", page_icon="📰", layout="wide")

# Apply custom styles
apply_styles()

# Load news from the JSON file
def load_news_data():
    with open("news.json", "r", encoding="utf-8") as file:
        return json.load(file)

news_data = load_news_data()

# Helper function to encode URLs
def encode_url(url):
    """
    Ensure the URL is properly encoded to handle spaces and special characters.
    """
    return quote(url, safe=":/")

# Function to process Markdown content into HTML
def render_content_as_html(content):
    """
    Convert Markdown content to HTML and explicitly encode image URLs.
    """
    # Regex to find Markdown image syntax: ![Alt Text](URL)
    image_pattern = r"!\[.*?\]\((.*?)\)"

    def encode_url_in_markdown(match):
        encoded_url = encode_url(match.group(1))
        return f"![Alt Text]({encoded_url})"

    # Encode URLs in Markdown
    content = re.sub(image_pattern, encode_url_in_markdown, content)

    # Convert Markdown to HTML
    html_content = markdown(content)
    return html_content

# Check if the app is accessed with a query parameter
query_params = st.experimental_get_query_params()
selected_news_id = query_params.get("news_id", [None])[0]

# Find and display the specific news article if news_id is provided
if selected_news_id:
    selected_news = next((news for news in news_data if news["id"] == selected_news_id), None)
    if selected_news:
        # Ensure the main image URL is encoded
        encoded_image_url = encode_url(selected_news["image_url"])
        st.image(encoded_image_url, use_column_width=True, caption=selected_news["title"])

        st.markdown(f"""
            <div class="news-container">
                <div class="news-title">{selected_news["title"]}</div>
                <div class="news-subtitle">{selected_news["subtitle"]}</div>
            </div>
        """, unsafe_allow_html=True)

        # Convert content to HTML and display it explicitly
        html_content = render_content_as_html(selected_news["content"])
        st.components.v1.html(html_content, height=500, scrolling=True)

        st.markdown(f"""
            <div class="news-takeaway">📌 : {selected_news["takeaway"]}</div>
        """, unsafe_allow_html=True)
    else:
        st.warning("The specified news article could not be found.")
else:
    st.warning("No specific article selected. Please use a valid link.")

# Add footer
footer()
