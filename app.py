import streamlit as st
import json
import requests
from urllib.parse import urlencode, quote
from markdown import markdown  # For converting Markdown to HTML
from style import apply_styles, footer  # Import styles and footer
import re  # For parsing image URLs in Markdown

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

# Function to process and encode image URLs in Markdown
def process_markdown_with_images(content):
    """
    Parse and process Markdown content to ensure URLs are encoded.
    """
    image_pattern = r"!\[.*?\]\((.*?)\)"  # Matches Markdown image syntax
    def encode_image_url(match):
        url = match.group(1)
        encoded_url = encode_url(url)
        return f"![Image]({encoded_url})"
    
    # Replace all image URLs with encoded versions
    content = re.sub(image_pattern, encode_image_url, content)
    return markdown(content)  # Convert processed Markdown to HTML

# Helper function to generate a shareable link
def generate_shareable_link(news_id):
    base_url = "https://habdulhaqnews.streamlit.app"  # Replace with your Streamlit URL
    params = {"news_id": news_id}
    return f"{base_url}?{urlencode(params)}"

# Check if the app is accessed with a query parameter
query_params = st.experimental_get_query_params()
selected_news_id = query_params.get("news_id", [None])[0]

# Find and display the specific news article if news_id is provided
if selected_news_id:
    selected_news = next((news for news in news_data if news["id"] == selected_news_id), None)
    if selected_news:
        # Display the main image
        encoded_image_url = encode_url(selected_news["image_url"])
        st.image(encoded_image_url, use_column_width=True, caption=selected_news["title"])

        # Display the title and subtitle
        st.markdown(f"""
            <div class="news-container">
                <div class="news-title">{selected_news["title"]}</div>
                <div class="news-subtitle">{selected_news["subtitle"]}</div>
            </div>
        """, unsafe_allow_html=True)

        # Process and render the content
        html_content = process_markdown_with_images(selected_news["content"])
        st.components.v1.html(html_content, height=500, scrolling=True)

        # Display the takeaway
        st.markdown(f"""
            <div class="news-takeaway">📌 : {selected_news["takeaway"]}</div>
        """, unsafe_allow_html=True)
    else:
        st.warning("The specified news article could not be found.")
else:
    st.warning("No specific article selected. Please use a valid link.")

# Add footer
footer()
