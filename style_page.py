import streamlit as st

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

            .news-container {
                background-color: #ffffff;
                padding: 30px;
                border-radius: 12px;
                box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1);
                max-width: 800px;
                margin: 0 auto;
                direction: rtl;
            }

            .news-title {
                font-size: 36px;
                font-weight: bold;
                color: #333333;
                margin-bottom: 10px;
            }

            .news-subtitle {
                font-size: 20px;
                color: #777777;
                margin-bottom: 20px;
            }

            .news-content {
                font-size: 20px;
                line-height: 1.8;
                color: #555555;
                margin-bottom: 20px;
            }

            .news-takeaway {
                font-size: 18px;
                font-style: italic;
                color: #007BFF;
                margin-top: 20px;
            }

            .telegram-logo {
                width: 24px;
                height: 24px;
                vertical-align: middle;
                margin-right: 8px;
            }

            .footer-container {
                background-color: #f8f9fa;
                padding: 20px 0;
                text-align: center;
                border-top: 2px solid #dee2e6;
                margin-top: 30px;
            }

            .footer-item {
                display: inline-block;
                width: 200px;
                margin: 10px;
                vertical-align: top;
                font-family: Arial, sans-serif;
            }

            .footer-item img {
                width: 50px;
                height: 50px;
                display: block;
                margin: 0 auto;
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
            <!-- Telegram Section -->
            <div class="footer-item">
                <a href="https://t.me/habdulaq" target="_blank">
                    <img src="https://i.imgur.com/Hxr3jCj.png" alt="Telegram Logo">
                    <p>کەناڵی هاوکار علی عبدالحق لە تێلەگرام</p>
                </a>
            </div>
            
            <!-- Website Section -->
            <div class="footer-item">
                <a href="https://www.habdulhaq.com" target="_blank">
                    <img src="https://upload.wikimedia.org/wikipedia/commons/c/c3/Python-logo-notext.svg" alt="Python Logo">
                    <p>پایثۆن فێربە بەخۆڕایی لەگەڵ هاوکار</p>
                </a>
            </div>
        </div>
    """, unsafe_allow_html=True)


def style_page():
    """
    Render the style management page with preview and customizations.
    """
    st.title("Manage Application Styles")
    st.write("Here you can update the styles and preview how the app looks.")
    
    st.markdown("""
        <div style="padding: 20px; border: 2px solid #dee2e6; background-color: #f8f9fa;">
            <h3>Preview Footer</h3>
            <div class="footer-container">
                <div class="footer-item">
                    <a href="https://t.me/habdulaq" target="_blank">
                        <img src="https://i.imgur.com/Hxr3jCj.png" alt="Telegram Logo">
                        <p>کەناڵی هاوکار علی عبدالحق لە تێلەگرام</p>
                    </a>
                </div>
                <div class="footer-item">
                    <a href="https://www.habdulhaq.com" target="_blank">
                        <img src="https://upload.wikimedia.org/wikipedia/commons/c/c3/Python-logo-notext.svg" alt="Python Logo">
                        <p>پایثۆن فێربە بەخۆڕایی لەگەڵ هاوکار</p>
                    </a>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.info("This is a preview of the footer. To modify the styles, update `style_page.py` as needed.")
