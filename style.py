import streamlit as st

# Global style configuration dictionary
STYLE_CONFIG = {
    "background_color": "#f4f4f4",
    "font_family": "'SpedaBold', Arial, sans-serif",
    "primary_color": "#007bff",
    "news_title_size": "36px",
    "news_content_size": "20px",
    "footer_bg_color": "#f8f9fa",
    "footer_border_color": "#dee2e6",
}

def generate_styles():
    """
    Generate CSS styles dynamically based on STYLE_CONFIG.
    """
    return f"""
        <style>
            @font-face {{
                font-family: 'SpedaBold';
                src: url('font/Speda-Bold.eot');
                src: url('font/Speda-Bold.eot?#iefix') format('embedded-opentype'),
                     url('font/Speda-Bold.woff') format('woff'),
                     url('font/Speda-Bold.ttf') format('truetype'),
                     url('font/Speda-Bold.svg#SpedaBold') format('svg');
                font-weight: normal;
                font-style: normal;
            }}

            body {{
                background-color: {STYLE_CONFIG['background_color']};
                font-family: {STYLE_CONFIG['font_family']};
                direction: rtl;
            }}

            .news-title {{
                font-size: {STYLE_CONFIG['news_title_size']};
                color: {STYLE_CONFIG['primary_color']};
                margin-bottom: 10px;
            }}

            .news-content {{
                font-size: {STYLE_CONFIG['news_content_size']};
                line-height: 1.8;
                color: #555555;
                margin-bottom: 20px;
            }}

            .footer-container {{
                background-color: {STYLE_CONFIG['footer_bg_color']};
                padding: 20px 0;
                text-align: center;
                border-top: 2px solid {STYLE_CONFIG['footer_border_color']};
                margin-top: 30px;
            }}
        </style>
    """

def apply_styles():
    """
    Apply custom CSS styles dynamically.
    """
    st.markdown(generate_styles(), unsafe_allow_html=True)

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
