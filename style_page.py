import streamlit as st

# Global style parameters
style_params = {
    "background_color": "#f4f4f4",
    "text_color": "#333333",
    "button_color": "#007BFF",
    "button_hover_color": "#0056b3",
    "footer_background": "#f8f9fa",
    "footer_border_color": "#dee2e6",
    "font_family": "Arial, sans-serif",
    "font_size": "16px",
    "logo_size": "50px",
}


def apply_styles(params):
    """
    Apply custom CSS styles dynamically based on the provided parameters.
    """
    st.markdown(f"""
        <style>
            body {{
                background-color: {params["background_color"]};
                color: {params["text_color"]};
                font-family: {params["font_family"]};
                font-size: {params["font_size"]};
            }}
            .stButton>button {{
                background-color: {params["button_color"]};
                color: white;
                border-radius: 8px;
                border: none;
                padding: 8px 16px;
                margin: 4px 0;
                font-size: 16px;
                font-weight: bold;
            }}
            .stButton>button:hover {{
                background-color: {params["button_hover_color"]};
            }}
            .footer-container {{
                background-color: {params["footer_background"]};
                padding: 20px 0;
                text-align: center;
                border-top: 2px solid {params["footer_border_color"]};
                margin-top: 30px;
            }}
            .footer-item {{
                display: inline-block;
                width: 200px;
                margin: 10px;
                vertical-align: top;
                font-family: {params["font_family"]};
            }}
            .footer-item img {{
                width: {params["logo_size"]};
                height: {params["logo_size"]};
                display: block;
                margin: 0 auto;
            }}
            .footer-item a {{
                text-decoration: none;
                color: {params["button_color"]};
                font-size: 16px;
                font-weight: bold;
            }}
            .footer-item a:hover {{
                text-decoration: underline;
            }}
            .footer-item p {{
                margin: 5px 0 0;
                font-size: 14px;
                color: {params["text_color"]};
            }}
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
                    <img src="https://raw.githubusercontent.com/habdulhaq87/news/main/photo/DT.jpg" alt="DT Logo" style="display: block; margin: 0 auto; max-width: 50px; height: auto;">
                    <p style="margin: 0; font-size: 14px; color: #333;">پایثۆن فێربە بەخۆڕایی لەگەڵ هاوکار</p>
                </a>
            </div>
        </div>
    """, unsafe_allow_html=True)


def style_page():
    """
    Render the style management page with live customization of styles.
    """
    st.title("Style Management")
    st.write("Use the sliders and inputs below to customize the look and feel of your application.")

    # Dynamic style customization
    with st.form("style_form"):
        style_params["background_color"] = st.color_picker("Background Color", style_params["background_color"])
        style_params["text_color"] = st.color_picker("Text Color", style_params["text_color"])
        style_params["button_color"] = st.color_picker("Button Color", style_params["button_color"])
        style_params["button_hover_color"] = st.color_picker("Button Hover Color", style_params["button_hover_color"])
        style_params["footer_background"] = st.color_picker("Footer Background Color", style_params["footer_background"])
        style_params["font_family"] = st.selectbox("Font Family", ["Arial, sans-serif", "Courier New, monospace", "Georgia, serif"])
        style_params["logo_size"] = st.slider("Logo Size (px)", 20, 100, int(style_params["logo_size"].replace("px", "")))

        submitted = st.form_submit_button("Apply Changes")

    # Apply styles dynamically
    if submitted:
        apply_styles(style_params)
        st.success("Styles updated successfully! Refresh the page to see changes take effect.")

    # Preview Footer
    st.subheader("Footer Preview")
    footer()

    st.info("This preview reflects the current style parameters. Use the inputs above to customize further.")
