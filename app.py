import streamlit as st
from urllib.parse import urlencode
from news import load_news, add_news

# Set up page configuration
st.set_page_config(page_title="Instant News", page_icon="⚡", layout="wide")

# Load all news
news_data = load_news()

# Helper function to generate a shareable link
def generate_shareable_link(news_id):
    base_url = "https://q5c32sstqku8zyyrmxtcil.streamlit.app"  # Replace with your Streamlit URL
    params = {"news_id": news_id}
    return f"{base_url}?{urlencode(params)}"

# Check if the app is accessed with a query parameter
query_params = st.experimental_get_query_params()
news_id = query_params.get("news_id", [None])[0]

if news_id and news_id in news_data:
    # Display the news using the template
    news = news_data[news_id]
    st.title(news["title"])
    st.subheader(news["short_title"])
    st.image(news["photo_url"], use_column_width=True)
    st.write("### Key Points:")
    for bullet in news["bullets"]:
        st.write(f"- {bullet}")
    st.write("### Takeaway Message:")
    st.success(news["takeaway"])
else:
    # Default news dashboard
    st.title("Instant News Dashboard")
    st.write("Welcome to the Instant News Dashboard. Click on any news below to read and share!")

    for news_id, news in news_data.items():
        with st.container():
            st.subheader(news["title"])
            st.image(news["photo_url"], use_column_width=True)
            st.write(news["bullets"][0] + "...")
            shareable_link = generate_shareable_link(news_id)
            if st.button(f"Read & Share '{news['title']}'", key=news_id):
                st.write("Share this link:")
                st.markdown(f"[{shareable_link}]({shareable_link})")

# Section to add new news
st.sidebar.title("Add New News")
with st.sidebar.form("add_news_form"):
    new_news_id = st.text_input("News ID (unique)", value="")
    new_title = st.text_input("Title", value="")
    new_short_title = st.text_input("Short Title", value="")
    new_photo_url = st.text_input("Photo URL", value="")
    new_bullets = st.text_area("Bullet Points (separate by line)").split("\n")
    new_takeaway = st.text_area("Takeaway Message", value="")
    submitted = st.form_submit_button("Add News")

    if submitted:
        if new_news_id and new_title and new_short_title:
            add_news(
                new_news_id,
                new_title,
                new_short_title,
                new_photo_url,
                new_bullets,
                new_takeaway,
            )
            st.success(f"News '{new_title}' added successfully!")
        else:
            st.error("Please fill out all required fields!")
