import streamlit as st
from urllib.parse import urlencode

# Set up page configuration
st.set_page_config(page_title="هەواڵی نوێ", page_icon="📰", layout="wide")

# Single news article
news_id = "ai_and_streaming"
news_title = "AI و بڵاوکردنەوە: نوێترین هاوکاتەکان"
news_content = """
AI و خزمەتگوزاریەکانی بڵاوکردنەوە گۆڕانکاری زۆرییان کردووە. سام ئالتمن، بەڕێوەبەرە گشتییەکەی OpenAI، ئیتر باوەڕی نییە ئەوەی AGI (زانستی گشتیی ئەندامە گشتییەکان) ئەو کەڵکەی پێشتر هەژمار کراوە دابنێ. هەرواە بەردەوامە بە کاربەرکردنی بەرزکردنەوەیەکە بۆ AI بە نرخێکی مانگانی ٢٠٠ دۆلار.

گووگڵ و ئەمەزوون بەردەوامن بە پاراستنی زانستە بەرزەکان بەرەوپێش بەرین، بەڵام AI یەکان هەیە تا ئێستا کێشەیانی لەناو دڵنیابوون و ڕاستبوونەوە.

لە بڵاوکردنەوەدا، تەختەی بڵاوکردنەوە ئەو زانستیانەی داوایان ئەکا قەبارەی تەلەفیزیۆنێکی کەیبیەوە. دیزنەی ئەسپێین لەگەڵ Disney Plus بەردەوامە بە هاوکاتکردن، و ماکس زانیارە هەیە چەناڵە HBO بڵاوکردنەوەکانی بەردەوامە بەرەوپێش بەرین.

لە ئەمەدا، بیتکوین بە نرخێکی ١٠٠٠٠٠ دۆلار گەیشت، Spotify بە هاوکاری AI بڵاوکردنەوەی پۆدکاستە نوێیەکی دا، و The Verge هاوکاریەکەی بۆ خزمەتگوزاری بەشداری نوێ بڵاوکردنەوە کرد.

زانیاریە زانست و بڵاوکردنەوە زۆر گۆڕاوە—لە پاشدا زۆر بەردەوام دەبێت!
"""
news_image_url = "https://i.imgur.com/38GVvtY.jpg"  # News banner image
telegram_logo_url = "https://i.imgur.com/Hxr3jCj.png"  # Telegram logo

# Helper function to generate a shareable link
def generate_shareable link(news_id):
    base_url = "https://q5c32sstqku8zyyrmxtcil.streamlit.app"  # Replace with your Streamlit URL
    params = {"news_id": news_id}
    return f"{base_url}?{urlencode(params)}"

# Add custom CSS for enhanced styling with custom font
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

        .news-content {
            font-size: 20px;
            line-height: 1.8;
            color: #555555;
            direction: rtl;
        }

        .telegram-logo {
            width: 16px;  /* Reduced size */
            height: 16px; /* Reduced size */
            vertical-align: middle;
            margin-right: 8px;
        }
    </style>
""", unsafe_allow_html=True)

# Check if the app is accessed with a query parameter
query_params = st.experimental_get_query_params()
if query_params.get("news_id", [None])[0] == news_id:
    st.image(news_image_url, use_column_width=True, caption="AI و بڵاوکردنەوە: نوێترین گۆڕانکاریەکان")
    st.markdown(f"""
        <div class="news-container">
            <div class="news-title">{news_title}</div>
            <div class="news-content">{news_content}</div>
        </div>
    """, unsafe_allow_html=True)
else:
    st.image(news_image_url, use_column_width=True, caption="AI و بڵاوکردنەوە: نوێترین گۆڕانکاریەکان")
    st.markdown(f"""
        <div class="news-container">
            <div class="news-title">{news_title}</div>
            <div class="news-content">{news_content[:250]}...</div>
        </div>
    """, unsafe_allow_html=True)

    shareable_link = generate_shareable_link(news_id)
    if st.button("🔗 هاوکاری بکە و هەواڵەکەی بڵاو بکە", key="share_button", help="کرتە بکە بۆ هاوکاری کردن"):
        st.success("بەستەرەکە دروست کرا!")
        st.write("کرتە بکە لە بەستەرەکە بۆ هاوکاری:")
        st.markdown(f'<a class="share-button" href="{shareable_link}" target="_blank">بڵاوکردنەوە</a>', unsafe_allow_html=True)

st.markdown(f"""
    <div class="footnote-container">
        فەرەی <strong>ھەوکەر علی عبدولحق</strong> لە تێلەگرام:
        <a href="https://t.me/habdulaq" target="_blank"><img src="{telegram_logo_url}" class="telegram-logo"></a>
        <br>
        <a href="https://www.habdulhaq.com" target="_blank">www.habdulhaq.com</a><br>
        <a href="mailto:connect@habdulhaq.com">connect@habdulhaq.com</a>
    </div>
""", unsafe_allow_html=True)

st.markdown("""
    <div class="footer">
        پەروەردەکراو بە <strong>Streamlit</strong> | <a href="https://streamlit.io" target="_blank">فێرببە</a>
    </div>
""", unsafe_allow_html=True)
