import streamlit as st
import json
from datetime import datetime

# Path to save the news data
news_file = "news.json"

# Load existing news if available
try:
    with open(news_file, "r") as file:
        news_data = json.load(file)
except FileNotFoundError:
    news_data = []

# Streamlit inputs
st.title("📰 Add News to JSON")
st.write("Fill out the form below to create a news entry:")

title = st.text_input("Title:")
subtitle = st.text_input("Subtitle:")
content = st.text_area("Content:", height=200)
takeaway = st.text_input("Takeaway Message:")
image_file = st.file_uploader("Upload a photo for the news:", type=["png", "jpg", "jpeg"])

# Generate a unique ID and timestamp
news_id = f"news_{len(news_data) + 1}"
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

if st.button("Save News"):
    if not (title and content and takeaway):
        st.error("Title, content, and takeaway message are required!")
    else:
        # Save the image if uploaded
        image_path = None
        if image_file:
            image_path = f"images/{image_file.name}"
            with open(image_path, "wb") as img_file:
                img_file.write(image_file.read())

        # Append the new news item
        new_news = {
            "id": news_id,
            "title": title,
            "subtitle": subtitle,
            "content": content,
            "takeaway": takeaway,
            "image": image_path,
            "timestamp": timestamp,
        }
        news_data.append(new_news)

        # Save to JSON
        with open(news_file, "w") as file:
            json.dump(news_data, file, indent=4)

        st.success("News saved successfully!")
        st.balloons()
