import streamlit as st
from urllib.parse import urlencode

# Set up page configuration
st.set_page_config(page_title="Instant News", page_icon="⚡", layout="wide")

# Predefined news articles (simulating a database)
news_storage = {
    "breaking_news": {
        "title": "Breaking News: Instant Pages Achieved!",
        "content": "With the power of Streamlit and query parameters, instant pages are now possible without external hosting!",
    },
    "climate_update": {
        "title": "Climate Update: New Initiatives Announced",
        "content": "Governments worldwide are joining hands to implement large-scale climate resilience programs, focusing on renewable energy and sustainable infrastructure.",
    },
    "tech_innovation": {
        "title": "Tech Innovation: AI Shapes the Future",
        "content": "Artificial Intelligence continues to revolutionize industries, from healthcare to finance, promising new levels of efficiency and innovation.",
    },
    "health_alert": {
        "title": "Health Alert: Flu Season Tips",
        "content": "As flu season approaches, experts advise staying up to date on vaccinations, practicing good hygiene, and maintaining a healthy lifestyle.",
    },
    "sports_highlight": {
        "title": "Sports Highlight: Historic Football Win",
        "content": "In an unforgettable match, the underdog team triumphed in the final moments, sparking celebrations across the nation.",
    },
}

# Helper function to generate a shareable link
def generate_shareable_link(news_id):
    base_url = "https://q5c32sstqku8zyyrmxtcil.streamlit.app"  # Replace with your Streamlit URL
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
