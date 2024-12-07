import streamlit as st
from urllib.parse import urlencode

# Set the page configuration
st.set_page_config(page_title="Instant News", page_icon="📰", layout="wide")

# Get query parameters from the URL
query_params = st.experimental_get_query_params()

# Check if there's a shared article to display
if "title" in query_params and "content" in query_params:
    # Display shared news
    st.title(query_params["title"][0])
    st.write(query_params["content"][0])
else:
    # Default news content
    st.title("Breaking News: Streamlit Makes Sharing Easy!")
    news_content = """
    Streamlit has released a new feature allowing users to create dynamic, shareable links.
    Now, you can easily share your news content and make it appear instantly with minimal effort!
    """
    st.write(news_content)

    # Shareable link generation
    if st.button("Share this news"):
        base_url = "https://q5c32sstqku8zyyrmxtcil.streamlit.app"  # Your deployed Streamlit app URL
        share_params = {
            "title": "Breaking News: Streamlit Makes Sharing Easy!",
            "content": news_content,
        }
        share_url = f"{base_url}?{urlencode(share_params)}"
        st.success("Shareable Link Generated!")
        st.write("Click the link below to share:")
        st.markdown(f"[{share_url}]({share_url})")
