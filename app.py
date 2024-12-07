import streamlit as st
from urllib.parse import urlencode

# Set up page configuration
st.set_page_config(page_title="Instant News", page_icon="📰", layout="centered")

# Single news article
news_id = "breaking_news"
news_title = "Breaking News: Instant Pages Achieved!"
news_content = """
With the power of Streamlit and query parameters, instant pages are now possible without external hosting!
Streamlit allows dynamic content delivery, making it easier to share and consume news instantly.
"""
news_image_url = "https://via.placeholder.com/800x400?text=Breaking+News"  # Replace with an actual news-related image

# Helper function to generate a shareable link
def generate_shareable_link(news_id):
    base_url = "https://q5c32sstqku8zyyrmxtcil.streamlit.app"  # Replace with your Streamlit URL
    params = {"news_id": news_id}
    return f"{base_url}?{urlencode(params)}"

# Add custom CSS for better styling
st.markdown("""
    <style>
        .news-container {
            background-color: #f9f9f9;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
        }
        .news-title {
            font-size: 32px;
            font-weight: bold;
            color: #333333;
        }
        .news-content {
            font-size: 18px;
            line-height: 1.6;
            color: #555555;
        }
        .share-button {
            margin-top: 20px;
        }
    </style>
""", unsafe_allow_html=True)

# Check if the app is accessed with a query parameter
query_params = st.experimental_get_query_params()
if query_params.get("news_id", [None])[0] == news_id:
    # Display the specific news article
    st.image(news_image_url, use_column_width=True)
    st.markdown(f"<div class='news-container'><div class='news-title'>{news_title}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='news-content'>{news_content}</div></div>", unsafe_allow_html=True)
else:
    # Display default news content with improved UI
    st.image(news_image_url, use_column_width=True)
    st.markdown(f"<div class='news-container'><div class='news-title'>{news_title}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='news-content'>{news_content[:150]}...</div></div>", unsafe_allow_html=True)
    
    # Generate shareable link
    shareable_link = generate_shareable_link(news_id)
    if st.button("🔗 Read & Share This News", key="share_button", help="Click to generate a shareable link"):
        st.success("Shareable Link Generated!")
        st.write("Click the link below to share:")
        st.markdown(f"[{shareable_link}]({shareable_link})")

# Add a footer for branding or additional links
st.markdown("""
    <hr>
    <div style='text-align: center; font-size: 14px; color: #888888;'>
        Powered by <strong>Streamlit</strong> | <a href="https://streamlit.io" target="_blank">Learn More</a>
    </div>
""", unsafe_allow_html=True)
