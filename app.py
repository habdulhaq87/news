import streamlit as st
from streamlit_quill import st_quill  # Rich text editor
from backend import save_uploaded_image_to_github, save_news_data  # Import backend functions

def main(news_data):
    """
    Main function to add a new article.
    Allows users to upload an image, embed it in the content, and save the article.
    """
    st.title("Add New Article")  # Relies on backend.py's st.set_page_config

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
        if uploaded_image:
            # Save uploaded image and get the URL
            image_url = save_uploaded_image_to_github(uploaded_image)
            if image_url:
                # Automatically embed the image in the content
                new_content += f'\n\n![Image Description]({image_url})'
                st.success("Image uploaded and embedded in the content!")

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
                    "image_url": image_url if uploaded_image else None,  # Preserve separate image URL if needed
                }
                # Append the new article to the news data
                news_data.append(new_article)
                # Save updated news data to the backend
                save_news_data(news_data)
                st.success("Article added successfully!")
            else:
                st.error("All fields are required except Takeaway.")
