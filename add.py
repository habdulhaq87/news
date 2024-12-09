import streamlit as st
from streamlit_quill import st_quill  # Rich text editor
import json
import requests
import time
import os
import zipfile
from docx import Document

# GitHub Constants
GITHUB_USER = "habdulhaq87"
GITHUB_REPO = "news"
GITHUB_PAT = st.secrets["github_pat"]
JSON_FILE = "news.json"
GITHUB_API_URL_JSON = f"https://api.github.com/repos/{GITHUB_USER}/{GITHUB_REPO}/contents/{JSON_FILE}"

def extract_content_from_docx(docx_file, save_uploaded_image_to_github):
    """
    Extract content and images from a .docx file.

    Args:
        docx_file: The uploaded .docx file.
        save_uploaded_image_to_github: Function to upload images to GitHub.

    Returns:
        str: The extracted content in Markdown format.
    """
    from pathlib import Path

    # Load the .docx file
    document = Document(docx_file)
    content = ""

    # Ensure the "photo" directory exists
    photo_dir = Path(os.getcwd()) / "photo"
    photo_dir.mkdir(parents=True, exist_ok=True)

    # Extract text paragraphs
    for paragraph in document.paragraphs:
        if paragraph.text.strip():
            content += f"{paragraph.text}\n\n"

    # Extract images from the .docx file
    for rel_id, rel in document.part.rels.items():
        if "image" in rel.target_ref:
            try:
                # Access the binary data of the image
                image_part = document.part.related_parts[rel.target_ref]
                image_data = image_part.blob

                # Save the image to the photo directory
                timestamp = int(time.time())
                filename = f"{timestamp}_{Path(rel.target_ref).name}"
                file_path = photo_dir / filename

                with open(file_path, "wb") as img_file:
                    img_file.write(image_data)

                # Upload the image to GitHub
                with open(file_path, "rb") as img_file:
                    image_url = save_uploaded_image_to_github(img_file)

                if image_url:
                    content += f"![Image Description]({image_url})\n\n"
            except Exception as e:
                st.error(f"Error processing image: {rel.target_ref} - {e}")

    return content.strip()

def main(news_data, save_news_data, save_uploaded_image_to_github):
    """
    Main function to add a new article with styled content and images.

    Args:
        news_data (list): The existing news data.
        save_news_data (function): Function to save updated news data.
        save_uploaded_image_to_github (function): Function to upload an image to GitHub and return its URL.
    """
    st.title("Add New Article")

    # Form to collect article details
    with st.form("add_article_form", clear_on_submit=True):
        # Article Title
        new_title = st.text_input("Title", key="new_title")

        # Article Subtitle
        new_subtitle = st.text_input("Subtitle", key="new_subtitle")

        # Upload .docx File
        st.markdown("### Upload .docx File for Content")
        uploaded_docx = st.file_uploader("Upload a .docx file", type=["docx"], key="docx_upload")

        # Content Editor Section
        st.markdown("### Content Editor")
        new_content = ""

        if uploaded_docx:
            # Extract content from the uploaded .docx file
            new_content = extract_content_from_docx(uploaded_docx, save_uploaded_image_to_github)
            st.text_area(
                "Extracted Content (Read-only)",
                value=new_content,
                height=300,
                key="extracted_content",
                disabled=True,
            )
        else:
            # Use the Quill editor if no .docx is uploaded
            new_content = st_quill("Write your content here", key="new_content_quill")

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
                    "content": new_content,  # Content includes extracted content or manual text
                    "takeaway": new_takeaway,
                }
                # Append the new article to the news data
                news_data.append(new_article)
                # Save updated news data to GitHub
                save_news_data(news_data)
                st.success("Article added successfully!")
            else:
                st.error("All fields are required except Takeaway.")
