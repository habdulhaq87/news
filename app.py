import streamlit as st
import json
from urllib.parse import urlencode

# Path to the news data
news_file = "news.json"

# Load the news data
try:
    with open(news_file, "r") as file:
        news_data = json.load(file)
except FileNotFoundError:
    st.error("No news available! Add news using the `news.py` tool.")
    st.stop()

# Set up page configuration
st.set_page_config(page_title="هەواڵی نوێ", page_icon="📰", layout="wide")

# Helper function to generate a shareable link
def generate_shareable_link(news_id):
    base_url = "https://q5c32sstqku8zyyrmxtcil.streamlit.app"  # Replace with your Streamlit URL
    params = {"news_id": news_id}
    return f"{base_url}?{urlencode(params)}"

# Check if the app is accessed with a query parameter
query_params = st.experimental_get_query_params()
news_id = query_params.get("news_id", [None])[0]

if news_id:
    # Show the specific news article
    news_item = next((news for news in news_data if news["id"] == news_id), None)
    if not news_item:
        st.error("News not found!")
        st.stop()

    st.image(news_item["image"], use_column_width=True, caption=news_item["title"])
    st.markdown(f"""
        <div class="news-container">
            <div class="news-title">{news_item["title"]}</div>
            <div class="news-subtitle">{news_item["subtitle"]}</div>
            <div class="news-content">{news_item["content"]}</div>
            <div class="news-takeaway"><strong>Takeaway:</strong> {news_item["takeaway"]}</div>
            <div class="news-timestamp"><small>Published on: {news_item["timestamp"]}</small></div>
        </div>
    """, unsafe_allow_html=True)
else:
    # Display all news
    st.title("📰 Latest News")
    for news_item in news_data:
        with st.container():
            st.image(news_item["image"], width=200, caption=news_item["title"])
            st.subheader(news_item["title"])
            st.write(news_item["subtitle"])
            st.write(news_item["content"][:250] + "...")
            shareable_link = generate_shareable_link(news_item["id"])
            st.markdown(f"[🔗 Read More & Share]({shareable_link})")

# Add footer
st.markdown("""
    <div class="footer">
        پەروەردەکراو بە <strong>Streamlit</strong> | <a href="https://streamlit.io" target="_blank">فێرببە</a>
    </div>
""", unsafe_allow_html=True)
