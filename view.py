import streamlit as st
from streamlit_quill import st_quill

def view_articles(news_data, save_news_data, save_uploaded_image_to_github, post_to_telegram):
    """
    Display and manage articles: edit, delete, check validity, and post to Telegram.

    Args:
        news_data (list): List of articles loaded from the JSON file.
        save_news_data (function): Function to save updated news data back to the JSON file.
        save_uploaded_image_to_github (function): Function to save uploaded images to GitHub.
        post_to_telegram (function): Function to post articles to Telegram.
    """
    st.title("View and Manage Articles")

    for i, article in enumerate(news_data):
        st.subheader(f"Article {i + 1}: {article.get('title', 'Untitled')}")
        with st.expander("View / Edit Article"):
            # Edit article fields
            edit_title = st.text_input("Title", value=article.get("title", ""), key=f"edit_title_{i}")
            edit_subtitle = st.text_input("Subtitle", value=article.get("subtitle", ""), key=f"edit_subtitle_{i}")
            edit_content = st_quill(key=f"edit_content_{i}", value=article.get("content", ""))
            edit_takeaway = st.text_area("Takeaway (Markdown supported)", value=article.get("takeaway", ""), key=f"edit_takeaway_{i}")
            
            # Display current image if available
            image_url = article.get("image_url", None)
            if image_url:
                st.image(image_url, caption="Current Image", use_column_width=True)
            else:
                st.warning("No image associated with this article.")

            # Replace image
            uploaded_image = st.file_uploader(f"Replace Image for Article {i + 1} (jpg, png)", type=["jpg", "png"], key=f"edit_image_{i}")
            if uploaded_image:
                new_image_url = save_uploaded_image_to_github(uploaded_image)
                if new_image_url:
                    article["image_url"] = new_image_url
                    st.success("Image updated successfully!")

            # Save changes
            if st.button("Save Changes", key=f"save_{i}"):
                news_data[i] = {
                    "id": edit_title.replace(" ", "_").lower(),
                    "title": edit_title,
                    "subtitle": edit_subtitle,
                    "content": edit_content or article.get("content", ""),
                    "takeaway": edit_takeaway,
                    "image_url": article.get("image_url", None),  # Preserve existing image URL
                }
                save_news_data(news_data)
                st.success(f"Article '{edit_title}' updated successfully!")

            # Check article validity
            if st.button("Check Article", key=f"check_{i}"):
                missing_fields = [field for field in ["id", "title", "subtitle", "content", "image_url"] if not article.get(field)]
                if missing_fields:
                    st.error(f"Article is invalid. Missing fields: {', '.join(missing_fields)}")
                else:
                    st.success("Article is valid!")

            # Delete article
            if st.button("Delete Article", key=f"delete_{i}"):
                del news_data[i]
                save_news_data(news_data)
                st.success("Article deleted successfully!")
                st.experimental_rerun()

            # Post article to Telegram
            if st.button("Post to Telegram", key=f"post_telegram_{i}"):
                short_url = f"https://habdulhaqnews.streamlit.app/?news_id={article['id']}"
                success, debug_message = post_to_telegram(
                    title=article.get("title", ""),
                    subtitle=article.get("subtitle", ""),
                    content=article.get("content", ""),
                    takeaway=article.get("takeaway", ""),
                    image_url=article.get("image_url", None),
                    link=short_url,
                )
                if success:
                    st.success(f"Article '{article.get('title', '')}' posted to Telegram successfully!")
                else:
                    st.error("Failed to post the article to Telegram.")
                    st.text_area("Debug Information", debug_message, height=200)
