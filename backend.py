import streamlit as st
import json
import os

# Paths
JSON_FILE = "news.json"
PHOTO_DIR = "photo"

# Ensure the photo directory exists
os.makedirs(PHOTO_DIR, exist_ok=True)

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

# Save uploaded image to the photo directory
def save_uploaded_image(uploaded_file):
    file_path = os.path.join(PHOTO_DIR, uploaded_file.name)
    with open(file_path, "wb") as file:
        file.write(uploaded_file.getbuffer())
    return file_path

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
    new_content = st.text_area("Content (Markdown supported)", key="new_content", 
                                help="Use Markdown syntax for text styling. E.g., **bold**, *italic*, [link](http://example.com)")
    new_takeaway = st.text_area("Takeaway (Markdown supported)", key="new_takeaway", 
                                 help="Use Markdown syntax for text styling.")
    uploaded_image = st.file_uploader("Upload Image (jpg, png)", type=["jpg", "png"], key="new_image")

    submitted = st.form_submit_button("Add Article")

    if submitted:
        if new_title and new_subtitle and new_content and uploaded_image:
            image_path = save_uploaded_image(uploaded_image)
            relative_path = os.path.relpath(image_path, PHOTO_DIR)  # Save relative path to JSON
            new_article = {
                "id": new_title.replace(" ", "_").lower(),
                "title": new_title,
                "subtitle": new_subtitle,
                "content": new_content,
                "takeaway": new_takeaway,
                "image_url": os.path.join(PHOTO_DIR, relative_path),
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
        edit_content = st.text_area("Content (Markdown supported)", value=article["content"], key=f"edit_content_{i}")
        edit_takeaway = st.text_area("Takeaway (Markdown supported)", value=article["takeaway"], key=f"edit_takeaway_{i}")
        current_image = os.path.basename(article["image_url"])
        st.image(article["image_url"], caption="Current Image", use_column_width=True)
        uploaded_image = st.file_uploader(f"Replace Image for Article {i+1} (jpg, png)", type=["jpg", "png"], key=f"edit_image_{i}")

        if uploaded_image:
            image_path = save_uploaded_image(uploaded_image)
            relative_path = os.path.relpath(image_path, PHOTO_DIR)
            article["image_url"] = os.path.join(PHOTO_DIR, relative_path)

        # Save changes
        if st.button("Save Changes", key=f"save_{i}"):
            news_data[i] = {
                "id": edit_title.replace(" ", "_").lower(),
                "title": edit_title,
                "subtitle": edit_subtitle,
                "content": edit_content,
                "takeaway": edit_takeaway,
                "image_url": article["image_url"],
            }
            save_news_data(news_data)
            st.success("Article updated successfully!")
        
        # Delete article
        if st.button("Delete Article", key=f"delete_{i}"):
            del news_data[i]
            save_news_data(news_data)
            st.success("Article deleted successfully!")
            st.experimental_rerun()  # Refresh the app to reflect changes
