import os
import io
import base64
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import streamlit as st
from groq import Groq

# =========================================================
# PAGE SETTINGS
# =========================================================
st.set_page_config(
    page_title="AI Poster & Social Media Caption Maker",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# =========================================================
# CUSTOM DESIGN
# Dark Purple + Light Purple split background
# Black text everywhere
# =========================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&family=Poppins:wght@600;700;800&display=swap');

* {
    font-family: 'DM Sans', sans-serif;
}

.stApp {
    background:
        linear-gradient(118deg,
            #35106f 0%,
            #6f2acb 42%,
            #b66bea 50%,
            #eee4ff 50.5%,
            #faf5ff 100%);
    color: #000000 !important;
}

.block-container {
    max-width: 1450px;
    padding-top: 1.4rem;
    padding-bottom: 3rem;
}

header[data-testid="stHeader"] {
    background: transparent !important;
}

/* ---------- HERO ---------- */
.hero {
    min-height: 235px;
    padding: 38px 44px;
    border-radius: 32px;
    background:
        linear-gradient(115deg,
            rgba(255,255,255,.18) 0%,
            rgba(255,255,255,.12) 48%,
            rgba(255,255,255,.62) 49%,
            rgba(255,255,255,.78) 100%);
    border: 1px solid rgba(255,255,255,.7);
    box-shadow: 0 20px 55px rgba(39, 11, 76, .28);
    overflow: hidden;
    position: relative;
}

.hero h1 {
    font-family: 'Poppins', sans-serif;
    color: #000000 !important;
    font-size: clamp(2rem, 4.8vw, 4rem);
    line-height: 1.04;
    font-weight: 800;
    letter-spacing: -1.5px;
    margin: 0;
    max-width: 850px;
}

.hero h1 span {
    color: #000000 !important;
}

.hero p {
    color: #000000 !important;
    font-size: 1.05rem;
    font-weight: 600;
    max-width: 820px;
    margin-top: 15px;
}

.badges {
    display: flex;
    gap: 9px;
    flex-wrap: wrap;
    margin-top: 20px;
}

.badge {
    color: #000000 !important;
    background: rgba(255,255,255,.55);
    border: 1px solid rgba(80,35,130,.25);
    padding: 8px 13px;
    border-radius: 999px;
    font-weight: 700;
    font-size: .85rem;
}

/* ---------- SECTION ---------- */
.section-title {
    color: #000000 !important;
    font-family: 'Poppins', sans-serif;
    font-size: 1.8rem;
    font-weight: 800;
    margin-top: 20px;
    margin-bottom: 4px;
}

.section-subtitle {
    color: #000000 !important;
    font-size: 1rem;
    font-weight: 600;
    margin-bottom: 17px;
}

/* ---------- CARDS ---------- */
.info-card {
    background: rgba(255,255,255,.88);
    border: 1px solid rgba(255,255,255,.95);
    border-radius: 25px;
    padding: 25px;
    box-shadow: 0 15px 42px rgba(45, 14, 83, .20);
    min-height: 100%;
}

.info-card h3,
.info-card h4,
.info-card p,
.info-card div,
.info-card span {
    color: #000000 !important;
}

.info-card h3 {
    font-family: 'Poppins', sans-serif;
    font-size: 1.35rem;
    font-weight: 800;
    margin-bottom: 8px;
}

.info-card p {
    line-height: 1.55;
    font-weight: 500;
}

/* ---------- FEATURE CARDS ---------- */
.feature-card {
    background: rgba(255,255,255,.9);
    border: 1px solid rgba(255,255,255,.95);
    border-radius: 22px;
    padding: 20px;
    box-shadow: 0 12px 32px rgba(45,14,83,.16);
    min-height: 145px;
}

.feature-card * {
    color: #000000 !important;
}

.feature-icon {
    font-size: 1.9rem;
}

.feature-card h4 {
    font-family: 'Poppins', sans-serif;
    font-size: 1.05rem;
    margin: 7px 0 5px;
    font-weight: 800;
}

/* ---------- STREAMLIT INPUTS ---------- */
label,
.stMarkdown,
.stMarkdown p,
.stMarkdown span,
.stTextInput label,
.stTextArea label,
.stSelectbox label,
.stFileUploader label {
    color: #000000 !important;
}

div[data-baseweb="input"] > div,
div[data-baseweb="textarea"] > div,
div[data-baseweb="select"] > div {
    background: #ffffff !important;
    border: 1.5px solid #b98ae9 !important;
    border-radius: 14px !important;
}

input,
textarea {
    color: #000000 !important;
    background: #ffffff !important;
    font-weight: 500 !important;
}

textarea::placeholder,
input::placeholder {
    color: #777777 !important;
    opacity: 1 !important;
}

/* Select text */
div[data-baseweb="select"] * {
    color: #000000 !important;
}

/* ---------- FILE UPLOADER ---------- */
div[data-testid="stFileUploader"] {
    background: rgba(255,255,255,.95);
    border: 2px dashed #9b59e6;
    border-radius: 19px;
    padding: 10px;
}

div[data-testid="stFileUploader"] * {
    color: #000000 !important;
}

/* ---------- BUTTON ---------- */
div.stButton > button {
    width: 100%;
    min-height: 55px;
    border: 0 !important;
    border-radius: 17px !important;
    background: linear-gradient(90deg, #7c2fd1, #a63de2) !important;
    color: #000000 !important;
    font-weight: 900 !important;
    font-size: 1.05rem !important;
    box-shadow: 0 12px 28px rgba(90,30,150,.30);
}

div.stButton > button:hover {
    transform: translateY(-2px);
    background: linear-gradient(90deg, #8c3be0, #b54ae9) !important;
}

/* Download button */
div.stDownloadButton > button {
    width: 100%;
    border-radius: 14px !important;
    background: #ffffff !important;
    color: #000000 !important;
    border: 2px solid #8b4bd3 !important;
    font-weight: 800 !important;
}

/* ---------- TABS ---------- */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    background: rgba(255,255,255,.45);
    padding: 7px;
    border-radius: 18px;
}

.stTabs [data-baseweb="tab"] {
    color: #000000 !important;
    font-weight: 800 !important;
    border-radius: 12px;
}

.stTabs [aria-selected="true"] {
    color: #000000 !important;
    background: rgba(255,255,255,.85);
}

/* ---------- ALERTS ---------- */
div[data-testid="stAlert"] * {
    color: #000000 !important;
}

/* ---------- RESULT ---------- */
.result-box {
    background: rgba(255,255,255,.93);
    border: 1px solid #d8b9f3;
    border-radius: 23px;
    padding: 24px;
    margin-top: 20px;
    box-shadow: 0 12px 35px rgba(45,14,83,.15);
}

.result-box * {
    color: #000000 !important;
}

.result-box h3 {
    font-family: 'Poppins', sans-serif;
    color: #000000 !important;
}

/* ---------- FOOTER ---------- */
.footer {
    margin-top: 35px;
    padding: 18px 22px;
    border-radius: 20px;
    background: rgba(255,255,255,.75);
    border: 1px solid rgba(255,255,255,.9);
    text-align: center;
    color: #000000 !important;
    font-weight: 800;
    box-shadow: 0 10px 30px rgba(45,14,83,.12);
}

/* Mobile */
@media (max-width: 900px) {
    .hero {
        padding: 28px 24px;
    }

    .hero h1 {
        font-size: 2.25rem;
    }
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# API
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
    return Groq(api_key=key) if key else None

def image_to_data_url(image_bytes):
    encoded = base64.b64encode(image_bytes).decode("utf-8")
    return f"data:image/jpeg;base64,{encoded}"

# =========================================================
# POSTER MAKER
# =========================================================
def font(size, bold=False):
    path = (
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
        if bold else
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    )
    return ImageFont.truetype(path, size)

def wrap_text(draw, text, fnt, max_width):
    words = text.split()
    lines = []
    current = ""

    for word in words:
        test = word if not current else current + " " + word
        width = draw.textbbox((0, 0), test, font=fnt)[2]
        if width <= max_width:
            current = test
        else:
            if current:
                lines.append(current)
            current = word

    if current:
        lines.append(current)

    return lines

def make_poster(img, headline, platform, style):
    img = img.convert("RGB")
    canvas = Image.new("RGB", (1080, 1350), "white")

    img_ratio = img.width / img.height
    target_ratio = 1080 / 820

    if img_ratio > target_ratio:
        h = 820
        w = int(h * img_ratio)
    else:
        w = 1080
        h = int(w / img_ratio)

    img = img.resize((w, h), Image.Resampling.LANCZOS)
    left = max(0, (w - 1080) // 2)
    top = max(0, (h - 820) // 2)
    img = img.crop((left, top, left + 1080, top + 820))

    img = ImageEnhance.Color(img).enhance(1.08)
    canvas.paste(img, (0, 0))

    overlay = Image.new("RGBA", (1080, 820), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)

    for y in range(350, 820):
        alpha = int(170 * ((y - 350) / 470))
        od.line((0, y, 1080, y), fill=(20, 5, 35, alpha))

    canvas.paste(overlay, (0, 0), overlay)

    d = ImageDraw.Draw(canvas)

    d.rounded_rectangle(
        (45, 850, 1035, 1305),
        radius=32,
        fill=(255, 255, 255),
        outline=(210, 180, 240),
        width=4,
    )

    accent = {
        "Modern": "#7c3aed",
        "Minimal": "#111827",
        "Luxury": "#9a6b15",
        "Cute": "#db2777",
        "Business": "#1d4ed8",
        "Festival": "#ea580c",
    }.get(style, "#7c3aed")

    d.rounded_rectangle((78, 890, 250, 940), radius=20, fill=accent)
    d.text((106, 903), platform.upper(), font=font(23, True), fill="white")

    title_font = font(54, True)
    lines = wrap_text(
        d,
        headline.strip() or "Create Something Amazing",
        title_font,
        900
    )

    y = 975
    for line in lines[:3]:
        d.text((80, y), line, font=title_font, fill="#000000")
        y += 68

    d.text(
        (80, 1215),
        "Created with AI Poster & Social Media Caption Maker",
        font=font(21),
        fill="#555555",
    )

    return canvas

# =========================================================
# AI GENERATION
# =========================================================
def generate_content(client, topic, platform, style, image_bytes=None):
    system = """You are a professional social media content strategist.
Create concise, attractive and natural social media copy.
Return exactly:
HEADLINE:
CAPTION:
HASHTAGS:
CTA:
Do not add extra sections."""

    prompt = f"""
Business/product/event/topic: {topic}
Platform: {platform}
Style: {style}

Create:
- A short poster headline, maximum 8 words.
- A professional caption of 60-100 words.
- 6 relevant hashtags.
- One short call-to-action.

Make it engaging, natural and suitable for the selected platform.
"""

    # Text generation
    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": prompt},
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
    <p>Create beautiful posters, captions, hashtags and calls-to-action with the power of AI.</p>

    <div class="badges">
        <span class="badge">✨ AI Powered</span>
        <span class="badge">📱 Instagram</span>
        <span class="badge">📘 Facebook</span>
        <span class="badge">🎵 TikTok</span>
        <span class="badge">🚀 Easy to Use</span>
    </div>
</div>
""", unsafe_allow_html=True)

# =========================================================
# TABS
# =========================================================
home, features, how, tips = st.tabs(
    ["🏠 Home", "✨ Features", "📖 How It Works", "💡 Tips"]
)

# =========================================================
# HOME
# =========================================================
with home:

    st.markdown(
        '<div class="section-title">Create Your Social Media Content</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-subtitle">Upload an image, describe your idea, choose a platform and let AI create the copy.</div>',
        unsafe_allow_html=True
    )

    left, right = st.columns(2, gap="large")

    # LEFT
    with left:
        st.markdown("""
        <div class="info-card">
            <h3>🖼️ Upload Your Image</h3>
            <p>Add your poster, product image, event design or social media graphic.</p>
        </div>
        """, unsafe_allow_html=True)

        uploaded = st.file_uploader(
            "Upload your image",
            type=["png", "jpg", "jpeg", "webp"],
            label_visibility="collapsed"
        )

        uploaded_image = None

        if uploaded:
            uploaded_image = Image.open(uploaded).convert("RGB")
            st.image(
                uploaded_image,
                caption="Your Uploaded Image",
                use_container_width=True
            )

        st.markdown("""
        <div class="info-card" style="margin-top:12px; min-height:auto;">
            <p>💡 You can continue without an image and create AI copy from your topic.</p>
        </div>
        """, unsafe_allow_html=True)

    # RIGHT
    with right:
        st.markdown("""
        <div class="info-card">
            <h3>📝 Enter Your Content</h3>
            <p>Tell the AI what your business, product, event or post is about.</p>
        </div>
        """, unsafe_allow_html=True)

        topic = st.text_area(
            "Business / Product / Event / Topic",
            placeholder="Example: New luxury coffee shop opening in Islamabad with premium coffee and a modern atmosphere.",
            height=145,
            label_visibility="collapsed"
        )

        st.markdown("### 📱 Choose Your Platform")

        platform = st.selectbox(
            "Platform",
            ["Instagram", "Facebook", "TikTok"],
            label_visibility="collapsed"
        )

        st.markdown("### 🎨 Choose Your Style")

        style = st.selectbox(
            "Style",
            ["Modern", "Minimal", "Luxury", "Cute", "Business", "Festival"],
            label_visibility="collapsed"
        )

    st.write("")

    generate = st.button(
        "✨ Generate Poster & Caption",
        use_container_width=True
    )

    if generate:
        if not topic.strip():
            st.warning("Please enter your content topic first.")
        else:
            client = get_client()

            if client is None:
                st.error("GROQ_API_KEY is missing. Add it in Streamlit Secrets.")
            else:
                with st.spinner("✨ AI is creating your content..."):
                    try:
                        result = generate_content(
                            client,
                            topic,
                            platform,
                            style
                        )

                        st.session_state["result"] = result

                        if uploaded_image:
                            poster = make_poster(
                                uploaded_image,
                                topic[:70],
                                platform,
                                style
                            )

                            buffer = io.BytesIO()
                            poster.save(buffer, format="PNG")

                            st.session_state["poster"] = buffer.getvalue()

                    except Exception as e:
                        st.error(f"Generation failed: {e}")

    # RESULTS
    if "result" in st.session_state:
        st.markdown("""
        <div class="result-box">
            <h3>✨ Your AI Content</h3>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(st.session_state["result"])

        st.download_button(
            "⬇️ Download AI Caption",
            data=st.session_state["result"],
            file_name="ai_social_media_caption.txt",
            mime="text/plain",
            use_container_width=True
        )

    if "poster" in st.session_state:
        st.markdown("""
        <div class="result-box">
            <h3>🖼️ Your Poster Preview</h3>
        </div>
        """, unsafe_allow_html=True)

        st.image(
            st.session_state["poster"],
            use_container_width=True
        )

        st.download_button(
            "⬇️ Download Poster",
            data=st.session_state["poster"],
            file_name="ai_social_media_poster.png",
            mime="image/png",
            use_container_width=True
        )

# =========================================================
# FEATURES
# =========================================================
with features:

    st.markdown(
        '<div class="section-title">🚀 Powerful Features</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-subtitle">Everything you need to prepare professional social media content.</div>',
        unsafe_allow_html=True
    )

    feature_data = [
        ("🖼️", "Image Upload", "Upload product photos, event designs and social media graphics."),
        ("🤖", "AI Copywriting", "Generate headlines, captions, hashtags and CTAs."),
        ("📱", "3 Platforms", "Create content for Instagram, Facebook and TikTok."),
        ("🎨", "Creative Styles", "Choose Modern, Minimal, Luxury, Cute, Business or Festival."),
        ("⬇️", "Download", "Download your generated caption and poster."),
        ("⚡", "Simple Workflow", "Enter your idea and generate content quickly."),
    ]

    cols = st.columns(3)

    for i, item in enumerate(feature_data):
        icon, title, description = item

        with cols[i % 3]:
            st.markdown(
                f"""
                <div class="feature-card">
                    <div class="feature-icon">{icon}</div>
                    <h4>{title}</h4>
                    <p>{description}</p>
                </div>
                """,
                unsafe_allow_html=True
            )

# =========================================================
# HOW IT WORKS
# =========================================================
with how:

    st.markdown(
        '<div class="section-title">📖 How It Works</div>',
        unsafe_allow_html=True
    )

    steps = [
        ("01", "Upload", "Upload your poster or product image."),
        ("02", "Describe", "Tell AI about your business, product, event or topic."),
        ("03", "Customize", "Choose a platform and creative style."),
        ("04", "Generate", "AI creates your headline, caption, hashtags and CTA."),
        ("05", "Download", "Download your content and use it on social media."),
    ]

    for number, title, description in steps:
        st.markdown(
            f"""
            <div class="info-card" style="margin-bottom:12px;">
                <h3>{number} — {title}</h3>
                <p>{description}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

# =========================================================
# TIPS
# =========================================================
with tips:

    st.markdown(
        '<div class="section-title">💡 Creative Tips</div>',
        unsafe_allow_html=True
    )

    st.markdown("""
    <div class="info-card">
        <h3>✨ Get Better Results</h3>
        <p>
        • Mention your product or service clearly.<br>
        • Add your city or location when important.<br>
        • Tell AI about your target audience.<br>
        • Select a style that matches your brand.<br>
        • Give AI specific information instead of only one or two words.
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
