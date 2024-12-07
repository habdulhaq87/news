import streamlit as st
import json
import requests
from urllib.parse import urlencode
from style import apply_styles, footer  # Import styles and footer

# Set up page configuration
st.set_page_config(page_title="هەواڵی نوێ", page_icon="📰", layout="wide")

# Apply custom styles
apply_styles()

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

# Check if the app is accessed with a query parameter
query_params = st.experimental_get_query_params()
selected_news_id = query_params.get("news_id", [None])[0]

# Find and display the specific news article if `news_id` is provided
if selected_news_id:
    selected_news = next((news for news in news_data if news["id"] == selected_news_id), None)
    if selected_news:
        st.image(selected_news["image_url"], use_container_width=True, caption=selected_news["title"])
        st.markdown(f"""
            <div class="news-container">
                <div class="news-title">{selected_news["title"]}</div>
                <div class="news-subtitle">{selected_news["subtitle"]}</div>
                <div class="news-content">{selected_news["content"]}</div>
                <div class="news-takeaway">📌 : {selected_news["takeaway"]}</div>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.warning("The specified news article could not be found.")
else:
    st.warning("No specific article selected. Please use a valid link.")

# Add footer
footer()
