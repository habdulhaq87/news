import streamlit as st
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
    Allows users to manage content blocks dynamically and save the article.

    Args:
        news_data (list): The existing news data.
        save_news_data (function): Function to save updated news data.
        save_uploaded_image_to_github (function): Function to upload an image to GitHub and return its URL.
    """
    # Page Title
    st.title("Add New Article")

    # Collect article metadata
    new_title = st.text_input("Title")
    new_subtitle = st.text_input("Subtitle")
    new_takeaway = st.text_area("Takeaway (Markdown supported)")

    # Initialize a list to store content blocks
    content_blocks = []

    # Add a new content block
    st.markdown("### Add Content Blocks")
    if st.button("Add Text Block"):
        new_text = st.text_area("Text Block Content", key=f"text_block_{len(content_blocks)}")
        content_blocks.append({"type": "text", "value": new_text})

    uploaded_image = st.file_uploader("Upload Image", type=["jpg", "png"])
    if uploaded_image:
        # Save the uploaded image to GitHub
        image_url = save_uploaded_image_to_github(uploaded_image)
        if image_url:
            image_caption = st.text_input("Image Caption", key=f"caption_{len(content_blocks)}")
            content_blocks.append({
                "type": "image",
                "value": image_url,
                "alt": "Image description",
                "caption": image_caption
            })
            st.success("Image uploaded successfully and added to content blocks!")
        else:
            st.error("Failed to upload image. Please try again.")

    # Preview current content blocks
    st.markdown("### Content Preview")
    for block in content_blocks:
        if block["type"] == "text":
            st.markdown(block["value"])
        elif block["type"] == "image":
            st.image(block["value"], caption=block.get("caption", ""))

    # Submit the article
    if st.button("Save Article"):
        if new_title and new_subtitle and content_blocks:
            # Create the new article structure
            new_article = {
                "id": new_title.replace(" ", "_").lower(),
                "title": new_title,
                "subtitle": new_subtitle,
                "content": content_blocks,
                "takeaway": new_takeaway,
                "image_url": content_blocks[0]["value"] if content_blocks and content_blocks[0]["type"] == "image" else None  # Use the first image as main if available
            }
            # Append the article to the news data and save it
            news_data.append(new_article)
            save_news_data(news_data)
            st.success("Article added successfully!")
        else:
            st.error("Title, Subtitle, and at least one content block are required.")
