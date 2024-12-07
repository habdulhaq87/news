import streamlit as st
from urllib.parse import urlencode, parse_qs

# Set up page configuration
st.set_page_config(page_title="Instant News", page_icon="⚡", layout="wide")

# Placeholder for stored news (replace with a database in production)
news_storage = {
    "breaking_news": {
        "title": "Breaking News: Instant Pages Achieved!",
        "content": "With the power of Streamlit and query parameters, instant pages are now possible without external hosting!",
    },
    "climate_update": {
        "title": "Climate Update: New Initiatives Announced",
        "content": "Governments worldwide are joining hands to implement large-scale climate resilience programs.",
    },
}

# Helper function to generate a shareable link
def generate_shareable_link(news_id):
    base_url = "https://q5c32sstqku8zyyrmxtcil.streamlit.app"
    params = {"news_id": news_id}
    return f"{base_url}?{urlencode(params)}"

# Check if the app is accessed with a query parameter
query_params = st.experimental_get_query_params()
news_id = query_params.get("news_id", [None])[0]

if news_id and news_id in news_storage:
    # Load the specific news article
    news = news_storage[news_id]
    st.title(news["title"])
    st.write(news["content"])
else:
    # Display default news list
    st.title("Instant News Dashboard")
    st.write("Welcome to the Instant News Dashboard. Click on any news below to read and share!")

    for news_id, news in news_storage.items():
        with st.container():
            st.subheader(news["title"])
            st.write(news["content"][:100] + "...")
            shareable_link = generate_shareable_link(news_id)
            if st.button(f"Read & Share '{news['title']}'", key=news_id):
                st.write("Share this link:")
                st.markdown(f"[{shareable_link}]({shareable_link})")
