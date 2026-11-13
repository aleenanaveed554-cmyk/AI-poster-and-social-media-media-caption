import os
import io
import base64
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter
import streamlit as st
from groq import Groq

# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="AI Poster & Social Media Caption Maker",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# =========================================================
# CUSTOM CSS
# =========================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&family=Poppins:wght@500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at 10% 10%, rgba(168, 85, 247, 0.18), transparent 28%),
        radial-gradient(circle at 90% 15%, rgba(236, 72, 153, 0.16), transparent 30%),
        linear-gradient(135deg, #faf7ff 0%, #f5f0ff 48%, #fff8fc 100%);
}

.block-container {
    max-width: 1450px;
    padding-top: 1.2rem;
    padding-bottom: 3rem;
}

.hero {
    border-radius: 30px;
    padding: 38px 42px;
    background:
        radial-gradient(circle at 10% 20%, rgba(255,255,255,.18), transparent 22%),
        radial-gradient(circle at 88% 30%, rgba(255,255,255,.16), transparent 25%),
        linear-gradient(115deg, #32105f 0%, #6d22c9 48%, #c026d3 100%);
    color: white;
    box-shadow: 0 22px 60px rgba(90, 35, 150, .25);
    position: relative;
    overflow: hidden;
    margin-bottom: 22px;
}

.hero h1 {
    font-family: 'Poppins', sans-serif;
    font-size: clamp(2.1rem, 5vw, 4.4rem);
    line-height: 1.05;
    margin: 0;
    font-weight: 800;
    letter-spacing: -2px;
}

.hero h1 span {
    color: #f5a8ff;
}

.hero p {
    font-size: 1.08rem;
    margin: 14px 0 0;
    color: #f7eefe;
}

.hero-badges {
    margin-top: 20px;
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
}

.badge {
    display: inline-block;
    padding: 8px 13px;
    border-radius: 999px;
    background: rgba(255,255,255,.14);
    border: 1px solid rgba(255,255,255,.24);
    color: white;
    font-size: .88rem;
    font-weight: 600;
}

.section-title {
    font-family: 'Poppins', sans-serif;
    font-size: 1.45rem;
    font-weight: 800;
    color: #28133f;
    margin: 12px 0 5px;
}

.section-subtitle {
    color: #755f86;
    margin-bottom: 15px;
}

.info-card {
    background: rgba(255,255,255,.82);
    border: 1px solid rgba(135, 79, 198, .16);
    border-radius: 24px;
    padding: 22px;
    box-shadow: 0 12px 38px rgba(75, 37, 115, .08);
    height: 100%;
}

.info-card h3 {
    color: #32105f;
    margin: 0 0 8px;
    font-family: 'Poppins', sans-serif;
}

.info-card p {
    color: #66536f;
    margin: 0;
    line-height: 1.6;
}

.feature-card {
    background: white;
    border-radius: 20px;
    padding: 18px;
    border: 1px solid #eee4f8;
    box-shadow: 0 8px 25px rgba(75, 37, 115, .07);
    min-height: 145px;
}

.feature-icon {
    font-size: 1.8rem;
}

.feature-card h4 {
    margin: 7px 0 5px;
    color: #2b123f;
}

.feature-card p {
    color: #75647d;
    font-size: .92rem;
    margin: 0;
}

.result-box {
    background: linear-gradient(135deg, #fff 0%, #faf3ff 100%);
    border: 1px solid #ead7fb;
    border-radius: 22px;
    padding: 22px;
    margin-top: 18px;
}

.result-box h3 {
    color: #5b21b6;
    margin-top: 0;
}

.small-note {
    color: #806e88;
    font-size: .86rem;
}

.footer {
    margin-top: 35px;
    padding: 18px 22px;
    border-radius: 20px;
    background: linear-gradient(90deg, #32105f, #7e22ce, #be185d);
    color: white;
    text-align: center;
    font-weight: 600;
}

/* Streamlit inputs */
div[data-baseweb="input"] > div,
div[data-baseweb="textarea"] > div,
div[data-baseweb="select"] > div {
    border-radius: 14px !important;
    border: 1px solid #dcc8ee !important;
    background: white !important;
}

textarea, input {
    color: #24152e !important;
}

label, .stMarkdown p {
    color: #3b2844;
}

div.stButton > button {
    width: 100%;
    border: 0;
    border-radius: 15px;
    min-height: 52px;
    font-size: 1rem;
    font-weight: 800;
    color: white;
    background: linear-gradient(90deg, #7c3aed, #c026d3);
    box-shadow: 0 10px 25px rgba(124, 58, 237, .24);
    transition: .2s ease;
}

div.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 14px 30px rgba(124, 58, 237, .32);
}

div[data-testid="stFileUploader"] {
    background: white;
    border: 2px dashed #c084fc;
    border-radius: 18px;
    padding: 10px;
}

div[data-testid="stFileUploader"] section {
    background: transparent;
}

.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
}

.stTabs [data-baseweb="tab"] {
    border-radius: 12px;
    padding: 9px 16px;
}

@media (max-width: 900px) {
    .hero {
        padding: 28px 24px;
    }
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# HELPERS
# =========================================================
def get_api_key():
    try:
        key = st.secrets.get("GROQ_API_KEY", "")
        if key:
            return key
    except Exception:
        pass
    return os.getenv("GROQ_API_KEY", "")

def get_client():
    key = get_api_key()
    if not key:
        return None
    return Groq(api_key=key)

def image_to_data_url(image_bytes: bytes) -> str:
    encoded = base64.b64encode(image_bytes).decode("utf-8")
    return f"data:image/jpeg;base64,{encoded}"

def safe_font(size=40, bold=False):
    paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold
        else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf" if bold
        else "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf",
    ]
    for path in paths:
        if os.path.exists(path):
            return ImageFont.truetype(path, size=size)
    return ImageFont.load_default()

def wrap_text(draw, text, font, max_width):
    words = text.split()
    lines = []
    current = ""
    for word in words:
        test = word if not current else current + " " + word
        if draw.textbbox((0, 0), test, font=font)[2] <= max_width:
            current = test
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines

def make_poster(image: Image.Image, headline: str, platform: str, style: str) -> Image.Image:
    img = image.convert("RGB").copy()
    img.thumbnail((1080, 1080))

    canvas = Image.new("RGB", (1080, 1350), (245, 238, 255))

    # Cover image area
    img_ratio = img.width / img.height
    target_ratio = 1080 / 820
    if img_ratio > target_ratio:
        new_h = 820
        new_w = int(new_h * img_ratio)
    else:
        new_w = 1080
        new_h = int(new_w / img_ratio)

    img = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
    left = (new_w - 1080) // 2
    top = max(0, (new_h - 820) // 2)
    img = img.crop((left, top, left + 1080, top + 820))

    # Slight enhancement
    img = ImageEnhance.Color(img).enhance(1.08)
    img = ImageEnhance.Contrast(img).enhance(1.04)
    canvas.paste(img, (0, 0))

    # Gradient-like bottom overlay
    overlay = Image.new("RGBA", (1080, 820), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    for y in range(350, 820):
        alpha = int(170 * ((y - 350) / 470))
        od.line((0, y, 1080, y), fill=(20, 8, 35, alpha))
    canvas.paste(overlay, (0, 0), overlay)

    draw = ImageDraw.Draw(canvas)

    # Bottom panel
    draw.rounded_rectangle(
        (48, 855, 1032, 1298),
        radius=34,
        fill=(255, 255, 255),
        outline=(226, 201, 244),
        width=4,
    )

    accent = {
        "Modern": (124, 58, 237),
        "Minimal": (45, 55, 72),
        "Luxury": (153, 101, 21),
        "Cute": (219, 39, 119),
        "Business": (30, 64, 175),
        "Festival": (234, 88, 12),
    }.get(style, (124, 58, 237))

    draw.rounded_rectangle((80, 895, 250, 944), radius=20, fill=accent)
    draw.text((108, 908), platform.upper(), font=safe_font(24, True), fill="white")

    title_font = safe_font(56, True)
    lines = wrap_text(draw, headline.strip() or "Create Something Amazing", title_font, 900)
    y = 980
    for line in lines[:3]:
        draw.text((82, y), line, font=title_font, fill=(38, 19, 63))
        y += 70

    draw.text(
        (82, 1210),
        "Created with AI Poster & Social Media Caption Maker",
        font=safe_font(22, False),
        fill=(115, 92, 128),
    )

    return canvas

def generate_ai_content(client, topic, platform, style, image_bytes=None):
    system = """You are a professional social media content strategist and poster copywriter.
Create concise, attractive and natural social media copy.
Return exactly these sections:
HEADLINE:
CAPTION:
HASHTAGS:
CTA:
Do not add extra sections."""

    user_text = f"""
Business/product/event/topic: {topic}
Platform: {platform}
Creative style: {style}

Create:
1. A short poster headline, maximum 8 words.
2. A platform-appropriate caption, 60-100 words.
3. 6 relevant hashtags.
4. One short call-to-action.

Keep the writing professional, engaging and easy to understand.
"""

    if image_bytes:
        try:
            response = client.chat.completions.create(
                model="qwen/qwen3.8-27b",
                messages=[
                    {"role": "system", "content": system},
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": user_text + "\nAlso inspect the uploaded image and make the copy match its visible content."},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": image_to_data_url(image_bytes)
                                },
                            },
                        ],
                    },
                ],
                temperature=0.7,
                max_tokens=700,
            )
            return response.choices[0].message.content
        except Exception:
            pass

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user_text},
        ],
        temperature=0.7,
        max_tokens=700,
    )
    return response.choices[0].message.content

# =========================================================
# HERO
# =========================================================
st.markdown("""
<div class="hero">
    <h1>🎨 AI Poster & Social Media<br><span>Caption Maker</span></h1>
    <p>Create beautiful poster copy and engaging social media captions with AI — made for creators, businesses and events.</p>
    <div class="hero-badges">
        <span class="badge">✨ AI Powered</span>
        <span class="badge">📱 Instagram</span>
        <span class="badge">📘 Facebook</span>
        <span class="badge">🎵 TikTok</span>
        <span class="badge">🚀 Fast & Easy</span>
    </div>
</div>
""", unsafe_allow_html=True)

# =========================================================
# NAVIGATION
# =========================================================
tab_home, tab_features, tab_how, tab_tips = st.tabs(
    ["🏠 Home", "✨ Features", "📖 How It Works", "💡 Tips"]
)

with tab_home:
    st.markdown('<div class="section-title">Create Your Social Media Content</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-subtitle">Upload an image, describe your idea, choose a platform and let AI create the copy.</div>',
        unsafe_allow_html=True
    )

    left, right = st.columns([1, 1], gap="large")

    with left:
        st.markdown('<div class="info-card">', unsafe_allow_html=True)
        st.markdown("### 🖼️ Upload Your Image")
        st.write("Add your poster, product image, event design or social media graphic.")
        uploaded = st.file_uploader(
            "Upload image",
            type=["png", "jpg", "jpeg", "webp"],
            label_visibility="collapsed",
        )
        if uploaded:
            uploaded_image = Image.open(uploaded).convert("RGB")
            st.image(uploaded_image, caption="Uploaded Image", use_container_width=True)
        else:
            uploaded_image = None
            st.info("You can continue without an image and create AI copy from your topic.")
        st.markdown('</div>', unsafe_allow_html=True)

    with right:
        st.markdown('<div class="info-card">', unsafe_allow_html=True)
        st.markdown("### 📝 Enter Your Content")
        st.write("Tell the AI what your business, product, event or post is about.")

        topic = st.text_area(
            "Business / Product / Event / Topic",
            placeholder="Example: New luxury coffee shop opening in Islamabad with premium coffee and a modern atmosphere.",
            height=145,
            label_visibility="collapsed",
        )

        platform = st.selectbox(
            "📱 Choose Your Platform",
            ["Instagram", "Facebook", "TikTok"],
        )

        style = st.selectbox(
            "🎨 Choose Your Style",
            ["Modern", "Minimal", "Luxury", "Cute", "Business", "Festival"],
        )
        st.markdown('</div>', unsafe_allow_html=True)

    st.write("")
    generate = st.button("✨ Generate Poster & Caption", type="primary", use_container_width=True)

    if generate:
        if not topic.strip():
            st.warning("Please enter your business, product, event or content topic first.")
        else:
            client = get_client()
            if client is None:
                st.error("GROQ_API_KEY is missing. Add it in Streamlit Secrets as GROQ_API_KEY.")
                st.info("Example: Settings → Secrets → GROQ_API_KEY = your_key")
            else:
                with st.spinner("✨ AI is creating your content..."):
                    try:
                        result = generate_ai_content(
                            client,
                            topic,
                            platform,
                            style,
                            uploaded.getvalue() if uploaded else None,
                        )

                        st.session_state["ai_result"] = result

                        if uploaded_image:
                            poster = make_poster(
                                uploaded_image,
                                topic[:70],
                                platform,
                                style,
                            )
                            buf = io.BytesIO()
                            poster.save(buf, format="PNG")
                            st.session_state["poster_bytes"] = buf.getvalue()
                        else:
                            st.session_state["poster_bytes"] = None

                    except Exception as e:
                        st.error(f"AI generation failed: {e}")

    if "ai_result" in st.session_state:
        st.markdown('<div class="result-box">', unsafe_allow_html=True)
        st.markdown("### ✨ Your AI Content")
        st.markdown(st.session_state["ai_result"])
        st.markdown('</div>', unsafe_allow_html=True)

        if st.session_state.get("poster_bytes"):
            st.markdown('<div class="result-box">', unsafe_allow_html=True)
            st.markdown("### 🖼️ Your Poster Preview")
            st.image(st.session_state["poster_bytes"], use_container_width=True)
            st.download_button(
                "⬇️ Download Poster",
                data=st.session_state["poster_bytes"],
                file_name="ai_social_media_poster.png",
                mime="image/png",
                use_container_width=True,
            )
            st.markdown('</div>', unsafe_allow_html=True)

        st.download_button(
            "⬇️ Download AI Caption",
            data=st.session_state["ai_result"],
            file_name="ai_social_media_caption.txt",
            mime="text/plain",
            use_container_width=True,
        )

with tab_features:
    st.markdown('<div class="section-title">🚀 Powerful Features</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">Everything you need to prepare professional social media content.</div>', unsafe_allow_html=True)

    cols = st.columns(3)
    features = [
        ("🖼️", "Image Upload", "Upload product photos, event designs and social media graphics."),
        ("🤖", "AI Copywriting", "Generate headlines, captions, CTAs and hashtags."),
        ("📱", "3 Platforms", "Create content for Instagram, Facebook and TikTok."),
        ("🎨", "Creative Styles", "Choose Modern, Minimal, Luxury, Cute, Business or Festival."),
        ("⬇️", "Download", "Download your generated caption and poster."),
        ("⚡", "Simple Workflow", "No complicated settings — just enter your idea and generate."),
    ]
    for i, (icon, title, desc) in enumerate(features):
        with cols[i % 3]:
            st.markdown(
                f'<div class="feature-card"><div class="feature-icon">{icon}</div><h4>{title}</h4><p>{desc}</p></div>',
                unsafe_allow_html=True
            )

with tab_how:
    st.markdown('<div class="section-title">📖 How It Works</div>', unsafe_allow_html=True)
    steps = [
        ("01", "Upload", "Upload your poster or product image."),
        ("02", "Describe", "Tell AI about your business, event, product or topic."),
        ("03", "Customize", "Choose Instagram, Facebook or TikTok and select a style."),
        ("04", "Generate", "AI creates your headline, caption, hashtags and CTA."),
        ("05", "Download", "Download the content and use it on your social media."),
    ]
    for number, title, desc in steps:
        st.markdown(
            f'<div class="info-card" style="margin-bottom:12px;"><h3>{number} — {title}</h3><p>{desc}</p></div>',
            unsafe_allow_html=True
        )

with tab_tips:
    st.markdown('<div class="section-title">💡 Creative Tips</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="info-card">
    <h3>✨ Get Better Results</h3>
    <p>
    • Mention your product or service clearly.<br>
    • Add the city or location when it matters.<br>
    • Tell the AI about your target audience.<br>
    • Choose a style that matches your brand.<br>
    • Keep your topic specific instead of using only one or two words.
    </p>
    </div>
    """, unsafe_allow_html=True)

# =========================================================
# FOOTER
# =========================================================
st.markdown("""
<div class="footer">
    💜 Made for Creators • AI Poster & Social Media Caption Maker • Create • Share • Grow 🚀
</div>
""", unsafe_allow_html=True)
