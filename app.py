import streamlit as st
from urllib.parse import urlencode

# Set up page configuration
st.set_page_config(page_title="Instant News", page_icon="📰", layout="wide")

# Single news article
news_id = "ai_and_streaming"
news_title = "AI and Streaming: Key Updates"
news_content = """
AI and streaming services are undergoing big changes. OpenAI’s CEO Sam Altman now believes AGI (Artificial General Intelligence) might have less impact than expected, even as OpenAI introduces a $200/month subscription for its latest model. Google and Amazon are ramping up their AI efforts, but generative AI still struggles with inaccuracies.

In streaming, platforms are becoming more like cable. Disney bundled ESPN with Disney Plus, and Max launched always-on HBO channels. Meanwhile, Bitcoin hit $100,000, Spotify Wrapped added an AI podcast, and The Verge launched a new subscription service.

Tech and media are changing fast—more to come!
"""
news_image_url = "https://i.imgur.com/38GVvtY.jpg"  # News banner image

# Helper function to generate a shareable link
def generate_shareable_link(news_id):
    base_url = "https://q5c32sstqku8zyyrmxtcil.streamlit.app"  # Replace with your Streamlit URL
    params = {"news_id": news_id}
    return f"{base_url}?{urlencode(params)}"

# Add custom CSS for enhanced styling
st.markdown("""
    <style>
        body {
            background-color: #f4f4f4;
            font-family: "Arial", sans-serif;
        }
        .news-container {
            background-color: #ffffff;
            padding: 30px;
            border-radius: 12px;
            box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1);
            max-width: 800px;
            margin: 0 auto;
        }
        .news-title {
            font-size: 36px;
            font-weight: bold;
            color: #333333;
            margin-bottom: 10px;
        }
        .news-subtitle {
            font-size: 18px;
            font-weight: 500;
            color: #777777;
            margin-bottom: 20px;
        }
        .news-content {
            font-size: 20px;
            line-height: 1.8;
            color: #555555;
        }
        .share-button {
            display: inline-block;
            margin-top: 20px;
            padding: 10px 20px;
            background-color: #007BFF;
            color: white;
            font-size: 16px;
            font-weight: bold;
            border-radius: 5px;
            text-decoration: none;
            transition: background-color 0.3s ease;
        }
        .share-button:hover {
            background-color: #0056b3;
        }
        .footer {
            text-align: center;
            margin-top: 50px;
            font-size: 14px;
            color: #888888;
        }
        .footer a {
            color: #007BFF;
            text-decoration: none;
        }
        .footer a:hover {
            text-decoration: underline;
        }
    </style>
""", unsafe_allow_html=True)

# Check if the app is accessed with a query parameter
query_params = st.experimental_get_query_params()
if query_params.get("news_id", [None])[0] == news_id:
    # Display the specific news article
    st.image(news_image_url, use_column_width=True, caption="AI and Streaming: Transforming Industries")
    st.markdown(f"""
        <div class="news-container">
            <div class="news-title">{news_title}</div>
            <div class="news-subtitle">Latest updates in AI and the streaming world.</div>
            <div class="news-content">{news_content}</div>
        </div>
    """, unsafe_allow_html=True)
else:
    # Display default news content
    st.image(news_image_url, use_column_width=True, caption="AI and Streaming: Transforming Industries")
    st.markdown(f"""
        <div class="news-container">
            <div class="news-title">{news_title}</div>
            <div class="news-subtitle">Latest updates in AI and the streaming world.</div>
            <div class="news-content">{news_content[:250]}...</div>
        </div>
    """, unsafe_allow_html=True)
    
    # Generate shareable link
    shareable_link = generate_shareable_link(news_id)
    if st.button("🔗 Read & Share This News", key="share_button", help="Click to generate a shareable link"):
        st.success("Shareable Link Generated!")
        st.write("Click the link below to share:")
        st.markdown(f'<a class="share-button" href="{shareable_link}" target="_blank">Share Now</a>', unsafe_allow_html=True)

# Add a footer
st.markdown("""
    <div class="footer">
        Powered by <strong>Streamlit</strong> | <a href="https://streamlit.io" target="_blank">Learn More</a>
    </div>
""", unsafe_allow_html=True)
