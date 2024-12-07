import streamlit as st
from urllib.parse import urlencode

# Set up page configuration
st.set_page_config(page_title="Instant News", page_icon="⚡", layout="wide")

# Single news article
news_id = "breaking_news"
news_title = "Breaking News: Instant Pages Achieved!"
news_content = """
With the power of Streamlit and query parameters, instant pages are now possible without external hosting!
Streamlit allows dynamic content delivery, making it easier to share and consume news instantly.
"""

# Helper function to generate a shareable link
def generate_shareable_link(news_id):
    base_url = "https://q5c32sstqku8zyyrmxtcil.streamlit.app"  # Replace with your Streamlit URL
    params = {"news_id": news_id}
    return f"{base_url}?{urlencode(params)}"

# Check if the app is accessed with a query parameter
query_params = st.experimental_get_query_params()
if query_params.get("news_id", [None])[0] == news_id:
    # Display the specific news article
    st.title(news_title)
    st.write(news_content)
else:
    # Display default news content
    st.title(news_title)
    st.write(news_content[:150] + "...")
    
    # Generate shareable link
    shareable_link = generate_shareable_link(news_id)
    if st.button("Read & Share This News"):
        st.success("Shareable Link Generated!")
        st.write("Click the link below to share:")
        st.markdown(f"[{shareable_link}]({shareable_link})")
