import streamlit as st
import json
import os

# Path to the JSON file
JSON_FILE = "news.json"

# Load news data from the JSON file
def load_news_data():
    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    return []

# Save news data to the JSON file
def save_news_data(news_data):
    with open(JSON_FILE, "w", encoding="utf-8") as file:
        json.dump(news_data, file, ensure_ascii=False, indent=4)

# Initialize the Streamlit app
st.set_page_config(page_title="News Backend", layout="wide")

# Load existing news data
news_data = load_news_data()

# Header
st.title("News Backend")
st.write("Manage your news articles dynamically. Add, edit, or delete articles from the JSON file.")

# Add a new article
st.header("Add New Article")
with st.form("add_article_form", clear_on_submit=True):
    new_title = st.text_input("Title", key="new_title")
    new_subtitle = st.text_input("Subtitle", key="new_subtitle")
    new_content = st.text_area("Content", key="new_content")
    new_takeaway = st.text_area("Takeaway", key="new_takeaway")
    new_image_url = st.text_input("Image Path (e.g., photo/1.jpg)", key="new_image_url")
    submitted = st.form_submit_button("Add Article")

    if submitted:
        if new_title and new_subtitle and new_content and new_image_url:
            new_article = {
                "id": new_title.replace(" ", "_").lower(),
                "title": new_title,
                "subtitle": new_subtitle,
                "content": new_content,
                "takeaway": new_takeaway,
                "image_url": new_image_url,
            }
            news_data.append(new_article)
            save_news_data(news_data)
            st.success("Article added successfully!")
        else:
            st.error("All fields are required except Takeaway.")

# Edit or delete existing articles
st.header("Manage Existing Articles")
for i, article in enumerate(news_data):
    st.subheader(f"Article {i+1}: {article['title']}")
    with st.expander("View / Edit Article"):
        # Display existing details
        edit_title = st.text_input("Title", value=article["title"], key=f"edit_title_{i}")
        edit_subtitle = st.text_input("Subtitle", value=article["subtitle"], key=f"edit_subtitle_{i}")
        edit_content = st.text_area("Content", value=article["content"], key=f"edit_content_{i}")
        edit_takeaway = st.text_area("Takeaway", value=article["takeaway"], key=f"edit_takeaway_{i}")
        edit_image_url = st.text_input("Image Path", value=article["image_url"], key=f"edit_image_url_{i}")

        # Save changes
        if st.button("Save Changes", key=f"save_{i}"):
            news_data[i] = {
                "id": edit_title.replace(" ", "_").lower(),
                "title": edit_title,
                "subtitle": edit_subtitle,
                "content": edit_content,
                "takeaway": edit_takeaway,
                "image_url": edit_image_url,
            }
            save_news_data(news_data)
            st.success("Article updated successfully!")
        
        # Delete article
        if st.button("Delete Article", key=f"delete_{i}"):
            del news_data[i]
            save_news_data(news_data)
            st.success("Article deleted successfully!")
            st.experimental_rerun()  # Refresh the app to reflect changes
