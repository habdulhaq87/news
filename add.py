import streamlit as st
from streamlit_quill import st_quill  # Rich text editor
import json
import base64
import requests
import time  # For generating unique timestamps for filenames


# Constants for GitHub integration
GITHUB_USER = "habdulhaq87"
GITHUB_REPO = "news"
GITHUB_PAT = st.secrets["github_pat"]
JSON_FILE = "news.json"
GITHUB_API_URL_JSON = f"https://api.github.com/repos/{GITHUB_USER}/{GITHUB_REPO}/contents/{JSON_FILE}"


def main(news_data, save_news_data, save_uploaded_image_to_github):
    """
    Main function to add a new article.
    Allows users to upload an image, embed it in the content, and save the article.

    Args:
        news_data (list): The existing news data.
        save_news_data (function): Function to save updated news data.
        save_uploaded_image_to_github (function): Function to upload an image to GitHub and return its URL.
    """
    # Page Title
    st.title("Add New Article")

    # Form to collect article details
    with st.form("add_article_form", clear_on_submit=True):
        # Article Title
        new_title = st.text_input("Title", key="new_title")
        
        # Article Subtitle
        new_subtitle = st.text_input("Subtitle", key="new_subtitle")
        
        # Content Editor Section
        st.markdown("### Content Editor")
        new_content = st_quill("Write your content here", key="new_content")  # Rich text editor

        # Image Upload for Embedding in Content
        uploaded_image = st.file_uploader(
            "Upload Image to Embed (jpg, png)", 
            type=["jpg", "png"], 
            key="new_image_embed"
        )

        # Initialize variables to store image information
        image_url = None
        if uploaded_image:
            # Save uploaded image and get the URL
            image_url = save_uploaded_image_to_github(uploaded_file=uploaded_image)
            if image_url:
                # Automatically embed the image in the content
                new_content += f'\n\n![Image Description]({image_url})'
                st.success("Image uploaded and embedded in the content!")
            else:
                st.error("Failed to upload image. Please try again.")

        # Article Takeaway
        new_takeaway = st.text_area("Takeaway (Markdown supported)", key="new_takeaway")

        # Submit Button
        submitted = st.form_submit_button("Add Article")

        # Form Submission Logic
        if submitted:
            if new_title and new_subtitle and new_content:
                # Create the new article dictionary
                new_article = {
                    "id": new_title.replace(" ", "_").lower(),
                    "title": new_title,
                    "subtitle": new_subtitle,
                    "content": new_content,  # Content now includes embedded image URLs
                    "takeaway": new_takeaway,
                    "image_url": image_url,  # Save the image URL separately
                }
                # Append the new article to the news data
                news_data.append(new_article)
                # Save updated news data to GitHub
                save_news_data(news_data)
                st.success("Article added successfully!")
            else:
                st.error("All fields are required except Takeaway.")
