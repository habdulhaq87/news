import streamlit as st
from urllib.parse import urlencode

# Set up page configuration
st.set_page_config(page_title="Instant News", page_icon="⚡", layout="wide")

# News content template
news_id = "breaking_news"
news = {
    "title": "Breaking News: Instant Pages Achieved!",
    "short_title": "Instant Pages with Streamlit",
    "photo_url": "https://i.imgur.com/8XXoUSs.png",  # Direct image link
    "bullets": [
        "Streamlit now supports creating shareable, instant pages.",
        "No external hosting is required; everything is dynamic.",
        "Easily integrate with query parameters to make content shareable.",
    ],
    "takeaway": "Streamlit makes content sharing faster and more interactive with minimal setup."
}

# Helper function to generate a shareable link
def generate_shareable_link(news_id):
    base_url = "https://q5c32sstqku8zyyrmxtcil.streamlit.app"  # Replace with your Streamlit URL
    params = {"news_id": news_id}
    return f"{base_url}?{urlencode(params)}"

# Check if the app is accessed with a query parameter
query_params = st.experimental_get_query_params()
if query_params.get("news_id", [None])[0] == news_id:
    # Display the news using the template
    st.title(news["title"])
    st.subheader(news["short_title"])
    st.image(news["photo_url"], use_column_width=True)
    st.write("### Key Points:")
    for bullet in news["bullets"]:
        st.write(f"- {bullet}")
    st.write("### Takeaway Message:")
    st.success(news["takeaway"])
else:
    # Display the default news card
    st.title(news["title"])
    st.subheader(news["short_title"])
    st.image(news["photo_url"], use_column_width=True)
    st.write(news["bullets"][0] + "...")
    
    # Generate shareable link
    shareable_link = generate_shareable_link(news_id)
    if st.button("Read & Share This News"):
        st.success("Shareable Link Generated!")
        st.write("Click the link below to share:")
        st.markdown(f"[{shareable_link}]({shareable_link})")
