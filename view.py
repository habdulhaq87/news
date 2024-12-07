import streamlit as st
from streamlit_quill import st_quill
from bot import post_to_telegram  # Import Telegram posting functionality

def view_articles(news_data, save_news_data, save_uploaded_image_to_github):
    """
    Display and manage articles: edit, delete, and post to Telegram.
    
    Args:
        news_data (list): List of articles loaded from the JSON file.
        save_news_data (function): Function to save updated news data back to the JSON file.
        save_uploaded_image_to_github (function): Function to save uploaded images to GitHub.
    """
    st.title("View and Manage Articles")

    for i, article in enumerate(news_data):
        st.subheader(f"Article {i+1}: {article['title']}")
        with st.expander("View / Edit Article"):
            # Edit article fields
            edit_title = st.text_input("Title", value=article["title"], key=f"edit_title_{i}")
            edit_subtitle = st.text_input("Subtitle", value=article["subtitle"], key=f"edit_subtitle_{i}")
            
            # Correct implementation of st_quill
            edit_content = st_quill(
                key=f"edit_content_{i}",
                value=article["content"]  # Provide initial content
            )
            
            edit_takeaway = st.text_area("Takeaway (Markdown supported)", value=article["takeaway"], key=f"edit_takeaway_{i}")
            
            # Display current image
            st.image(article["image_url"], caption="Current Image", use_container_width=True)
            
            # Replace image
            uploaded_image = st.file_uploader(f"Replace Image for Article {i+1} (jpg, png)", type=["jpg", "png"], key=f"edit_image_{i}")

            if uploaded_image:
                # Save new image and update the article
                image_url = save_uploaded_image_to_github(uploaded_image)
                if image_url:
                    article["image_url"] = image_url

            # Save changes
            if st.button("Save Changes", key=f"save_{i}"):
                news_data[i] = {
                    "id": edit_title.replace(" ", "_").lower(),
                    "title": edit_title,
                    "subtitle": edit_subtitle,
                    "content": edit_content or article["content"],
                    "takeaway": edit_takeaway,
                    "image_url": article["image_url"],
                }
                save_news_data(news_data)
                st.success(f"Article '{edit_title}' updated successfully!")

            # Delete article
            if st.button("Delete Article", key=f"delete_{i}"):
                del news_data[i]
                save_news_data(news_data)
                st.success("Article deleted successfully!")
                st.experimental_set_query_params(rerun="true")  # Force a page reload using query parameters
                st.stop()  # Ensure the script stops after updating the query parameters

            # Post article to Telegram
            if st.button("Post to Telegram", key=f"post_telegram_{i}"):
                short_url = f"https://habdulhaqnews.streamlit.app/?news_id={article['id']}"
                post_to_telegram(
                    title=article["title"],
                    subtitle=article["subtitle"],
                    content=article["content"],
                    takeaway=article["takeaway"],
                    image_url=article["image_url"],
                    link=short_url,
                )
