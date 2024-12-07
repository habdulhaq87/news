import streamlit as st


@st.cache_data
def apply_styles():
    """
    Apply custom CSS styles for the application.
    """
    st.markdown("""
        <style>
            @font-face {
                font-family: 'SpedaBold';
                src: url('font/Speda-Bold.eot');
                src: url('font/Speda-Bold.eot?#iefix') format('embedded-opentype'),
                     url('font/Speda-Bold.woff') format('woff'),
                     url('font/Speda-Bold.ttf') format('truetype'),
                     url('font/Speda-Bold.svg#SpedaBold') format('svg');
                font-weight: normal;
                font-style: normal;
            }

            body {
                background-color: #f4f4f4;
                font-family: 'SpedaBold', Arial, sans-serif;
                direction: rtl;
            }

            .footer-container {
                background-color: #f8f9fa;
                padding: 20px;
                text-align: center;
                border-top: 2px solid #dee2e6;
                margin-top: 30px;
                display: flex;
                justify-content: center;
                gap: 50px;
            }

            .footer-item {
                text-align: center;
                font-family: Arial, sans-serif;
            }

            .footer-item img {
                width: 60px;
                height: 60px;
                margin-bottom: 10px;
            }

            .footer-item a {
                text-decoration: none;
                color: #007bff;
                font-size: 16px;
                font-weight: bold;
            }

            .footer-item a:hover {
                text-decoration: underline;
            }

            .footer-item p {
                margin: 5px 0 0;
                font-size: 14px;
                color: #333;
            }
        </style>
    """, unsafe_allow_html=True)


def footer():
    """
    Add a styled footer to the application.
    """
    st.markdown("""
        <div class="footer-container">
            <div class="footer-item">
                <a href="https://t.me/habdulaq" target="_blank">
                    <img src="https://i.imgur.com/Hxr3jCj.png" alt="Telegram Logo">
                    <p>کەناڵی هاوکار علی عبدالحق لە تێلەگرام</p>
                </a>
            </div>
            <div class="footer-item">
                <a href="https://www.habdulhaq.com" target="_blank">
                    <img src="https://raw.githubusercontent.com/habdulhaq87/news/main/photo/DT.jpg" alt="DT Logo">
                    <p>پایثۆن فێربە بەخۆڕایی لەگەڵ هاوکار</p>
                </a>
            </div>
        </div>
    """, unsafe_allow_html=True)


def clear_cache():
    """
    Provide a button to clear Streamlit's cache.
    """
    if st.sidebar.button("Clear Cache"):
        st.cache_data.clear()
        st.cache_resource.clear()
        st.experimental_rerun()
