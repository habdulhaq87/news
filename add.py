import streamlit as st
from streamlit_quill import st_quill  # Rich text editor
from backend import save_uploaded_image_to_github, save_news_data  # Import backend functions

def main(news_data):
    st.title("Add New Article")  # Relying on backend.py's st.set_page_config
    with st.form("add_article_form", clear_on_submit=True):
        new_title = st.text_input("Title", key="new_title")
        new_subtitle = st.text_input("Subtitle", key="new_subtitle")
        new_content = st_quill("Write your content here", key="new_content")  # Initialize blank editor
        new_takeaway = st.text_area("Takeaway (Markdown supported)", key="new_takeaway")
        uploaded_image = st.file_uploader("Upload Image (jpg, png)", type=["jpg", "png"], key="new_image")

        submitted = st.form_submit_button("Add Article")

        if submitted:
            if new_title and new_subtitle and new_content and uploaded_image:
                image_url = save_uploaded_image_to_github(uploaded_image)
                if image_url:
                    new_article = {
                        "id": new_title.replace(" ", "_").lower(),
                        "title": new_title,
                        "subtitle": new_subtitle,
                        "content": new_content,
                        "takeaway": new_takeaway,
                        "image_url": image_url,
                    }
                    news_data.append(new_article)
                    save_news_data(news_data)
                    st.success("Article added successfully!")
            else:
                st.error("All fields are required except Takeaway.")
