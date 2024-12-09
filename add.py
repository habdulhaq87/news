import streamlit as st
from streamlit_quill import st_quill  # Rich text editor
import time  # For generating unique timestamps for filenames


def main(news_data, save_news_data, save_uploaded_image_to_github):
    """
    Main function to add a new article.
    Allows users to upload images, embed them in the content, and save the article.

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
        st.markdown("### Upload and Embed Images")
        uploaded_images = st.file_uploader(
            "Upload Images to Embed (jpg, png)", 
            type=["jpg", "png"], 
            accept_multiple_files=True,
            key="new_images_embed"
        )

        embedded_images = []
        if uploaded_images:
            for uploaded_image in uploaded_images:
                # Save uploaded image and get the URL
                image_url = save_uploaded_image_to_github(uploaded_file=uploaded_image)
                if image_url:
                    embedded_images.append(image_url)
                    st.success(f"Image uploaded: {image_url}")
                else:
                    st.error(f"Failed to upload image: {uploaded_image.name}. Please try again.")

        # Display a list of embedded images for confirmation
        if embedded_images:
            st.markdown("### Embedded Images Preview")
            for url in embedded_images:
                st.image(url, use_column_width=True)
                # Optionally display the Markdown snippet for manual embedding
                st.markdown(f"`![Image Description]({url})`")

        # Article Takeaway
        new_takeaway = st.text_area("Takeaway (Markdown supported)", key="new_takeaway")

        # Submit Button
        submitted = st.form_submit_button("Add Article")

        # Form Submission Logic
        if submitted:
            if new_title and new_subtitle and new_content:
                # Automatically append embedded images to the content
                for url in embedded_images:
                    new_content += f'\n\n![Image Description]({url})'

                # Create the new article dictionary
                new_article = {
                    "id": new_title.replace(" ", "_").lower(),
                    "title": new_title,
                    "subtitle": new_subtitle,
                    "content": new_content,  # Content now includes embedded image URLs
                    "takeaway": new_takeaway,
                    "images": embedded_images,  # Save all image URLs separately
                }
                # Append the new article to the news data
                news_data.append(new_article)
                # Save updated news data to GitHub
                save_news_data(news_data)
                st.success("Article added successfully!")
            else:
                st.error("All fields are required except Takeaway.")
