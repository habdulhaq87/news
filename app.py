import streamlit as st
import json
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
    """Load news data from the local JSON file."""
    with open("news.json", "r", encoding="utf-8") as file:
        return json.load(file)

news_data = load_news_data()

# Helper function to encode URLs
def encode_url(url):
    """Ensure the URL is properly encoded to handle spaces and special characters."""
    return quote(url, safe=":/")

# Function to process Markdown content and encode image URLs
def process_markdown_with_images(content):
    """
    Process Markdown content to ensure URLs are encoded.
    Convert processed Markdown to HTML for rendering.
    """
    # Encode image URLs in Markdown
    image_pattern = r"!\[.*?\]\((.*?)\)"  # Matches Markdown image syntax
    def encode_image_url(match):
        url = match.group(1)
        return f"![Image]({encode_url(url)})"

    # Replace image URLs with encoded versions
    content = re.sub(image_pattern, encode_image_url, content)

    # Convert Markdown to HTML
    return markdown(content)

# Helper function to generate a shareable link
def generate_shareable_link(news_id):
    """Generate a shareable link for a specific news article."""
    base_url = "https://habdulhaqnews.streamlit.app"  # Replace with your Streamlit URL
    params = {"news_id": news_id}
    return f"{base_url}?{urlencode(params)}"

# Check if the app is accessed with a query parameter
query_params = st.experimental_get_query_params()
selected_news_id = query_params.get("news_id", [None])[0]

# Display the selected news article if a valid ID is provided
if selected_news_id:
    selected_news = next((news for news in news_data if news["id"] == selected_news_id), None)
    if selected_news:
        # Display debug info (optional, remove if not needed)
        st.write("### Selected News Debug Info")
        st.json(selected_news)

        # Display the main image
        if selected_news.get("image_url"):
            encoded_image_url = encode_url(selected_news["image_url"])
            st.image(encoded_image_url, use_column_width=True, caption=selected_news["title"])

        # Display the title and subtitle
        st.markdown(f"""
            <div class="news-container">
                <div class="news-title">{selected_news["title"]}</div>
                <div class="news-subtitle">{selected_news["subtitle"]}</div>
            </div>
        """, unsafe_allow_html=True)

        # Process and display the content
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
