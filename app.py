import streamlit as st
from urllib.parse import urlencode
import news  # Import the backend

# Set up page configuration
st.set_page_config(page_title="Instant News", page_icon="⚡", layout="wide")

# Add sample news to the backend (if not already added)
if not news.get_all_news():
    news.add_news(
        news_id="breaking_news",
        title="Breaking News: Instant Pages Achieved!",
        short_title="Instant Pages with Streamlit",
        photo_url="https://i.imgur.com/8XXoUSs.png",
        bullets=[
            "Streamlit now supports creating shareable, instant pages.",
            "No external hosting is required; everything is dynamic.",
            "Easily integrate with query parameters to make content shareable.",
        ],
        takeaway="Streamlit makes content sharing faster and more interactive with minimal setup.",
    )

# Helper function to generate a shareable link
def generate_shareable_link(news_id):
    base_url = "https://q5c32sstqku8zyyrmxtcil.streamlit.app"  # Replace with your Streamlit URL
    params = {"news_id": news_id}
    return f"{base_url}?{urlencode(params)}"

# Check if the app is accessed with a query parameter
query_params = st.experimental_get_query_params()
news_id = query_params.get("news_id", [None])[0]

if news_id:
    # Display specific news if the ID is in the query parameter
    article = news.get_news(news_id)
    if article:
        st.title(article["title"])
        st.subheader(article["short_title"])
        st.image(article["photo_url"], use_column_width=True)
        st.write("### Key Points:")
        for bullet in article["bullets"]:
            st.write(f"- {bullet}")
        st.write("### Takeaway Message:")
        st.success(article["takeaway"])
    else:
        st.error("News not found!")
else:
    # Display all news articles
    st.title("Instant News Dashboard")
    st.write("Welcome to the Instant News Dashboard. Click on any news below to read and share!")

    all_news = news.get_all_news()
    for news_id, article in all_news.items():
        with st.container():
            st.subheader(article["short_title"])
            st.image(article["photo_url"], use_column_width=True)
            st.write(article["bullets"][0] + "...")
            shareable_link = generate_shareable_link(news_id)
            if st.button(f"Read & Share '{article['short_title']}'", key=news_id):
                st.write("Share this link:")
                st.markdown(f"[{shareable_link}]({shareable_link})")
