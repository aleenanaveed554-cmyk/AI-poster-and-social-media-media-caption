import streamlit as st
from groq import Groq

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="AI Poster & Social Media Caption Maker",
    page_icon="✨",
    layout="wide"
)

# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

.stApp {
    background:
        radial-gradient(circle at top left, #3b1763 0%, transparent 35%),
        linear-gradient(135deg, #160b25 0%, #241035 50%, #12081d 100%);
}

/* Main Heading */
.main-title {
    text-align: center;
    font-size: 46px;
    font-weight: 900;
    color: white !important;
    margin-top: 15px;
    margin-bottom: 5px;
}

.subtitle {
    text-align: center;
    font-size: 18px;
    color: #e5d5f5 !important;
    margin-bottom: 35px;
}

/* Cards */
.card {
    background: rgba(255, 255, 255, 0.96);
    padding: 28px;
    border-radius: 24px;
    box-shadow: 0 12px 40px rgba(0,0,0,0.35);
    margin-bottom: 22px;
}

/* Card headings */
.card h2,
.card h3,
.card p,
.card label {
    color: #111111 !important;
}

/* Result */
.result-card {
    background: #ffffff;
    padding: 35px;
    border-radius: 25px;
    box-shadow: 0 12px 45px rgba(0,0,0,0.35);
    color: #111111 !important;
}

/* Make ALL result text black */
.result-card,
.result-card * {
    color: #111111 !important;
}

/* Result headings */
.result-card h1 {
    font-size: 32px !important;
    font-weight: 900 !important;
    margin-top: 10px;
}

.result-card h2 {
    font-size: 26px !important;
    font-weight: 850 !important;
    margin-top: 30px;
    border-bottom: 2px solid #ddd;
    padding-bottom: 8px;
}

.result-card h3 {
    font-size: 21px !important;
    font-weight: 800 !important;
}

.result-card p,
.result-card li {
    font-size: 17px !important;
    line-height: 1.8 !important;
}

/* Inputs */
.stTextArea textarea,
.stTextInput input {
    background-color: #ffffff !important;
    color: #111111 !important;
    border: 2px solid #9b68c7 !important;
    border-radius: 14px !important;
    font-size: 16px !important;
}

/* Select boxes */
.stSelectbox div {
    color: #111111 !important;
}

/* Button */
div.stButton > button {
    width: 100%;
    min-height: 52px;
    border-radius: 15px;
    border: none;
    background: linear-gradient(90deg, #6d28a9, #9b4dcc);
    color: white !important;
    font-size: 18px;
    font-weight: 800;
}

div.stButton > button:hover {
    background: linear-gradient(90deg, #812fc1, #b05ce0);
    color: white !important;
}

/* Download button */
.stDownloadButton button {
    border-radius: 13px !important;
    font-weight: 700 !important;
}

/* Divider */
hr {
    border-color: rgba(255,255,255,0.25) !important;
}

/* Footer */
.footer {
    text-align: center;
    color: #e5d5f5 !important;
    margin-top: 35px;
    font-size: 14px;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# HEADER
# =========================================================

st.markdown(
    '<div class="main-title">✨ AI Poster & Social Media Caption Maker</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Create detailed, professional and engaging social media content with AI</div>',
    unsafe_allow_html=True
)


# =========================================================
# TWO COLUMN LAYOUT
# =========================================================

left, right = st.columns([1, 1], gap="large")


# =========================================================
# LEFT SIDE
# =========================================================

with left:

    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.markdown("### 📝 Create Your Content")

    topic = st.text_area(
        "What is your content about?",
        placeholder=(
            "Example: New luxury beauty salon opening in Islamabad "
            "with makeup, skincare and hair styling services."
        ),
        height=180
    )

    business_name = st.text_input(
        "🏷️ Business / Brand Name",
        placeholder="Example: Glow Beauty Studio"
    )

    platform = st.selectbox(
        "📱 Select Platform",
        [
            "Instagram",
            "Facebook",
            "TikTok",
            "LinkedIn"
        ]
    )

    content_type = st.selectbox(
        "📌 Content Type",
        [
            "Social Media Caption",
            "Poster Content",
            "Product Promotion",
            "Business Promotion",
            "Event Promotion",
            "Sale / Discount",
            "New Product Launch",
            "Educational Post",
            "Special Announcement"
        ]
    )

    tone = st.selectbox(
        "🎨 Select Tone",
        [
            "Professional",
            "Modern",
            "Luxury",
            "Friendly",
            "Creative",
            "Catchy",
            "Elegant"
        ]
    )

    st.markdown("</div>", unsafe_allow_html=True)


# =========================================================
# RIGHT SIDE
# =========================================================

with right:

    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.markdown("### ✨ AI Content Generator")

    st.markdown(
        """
        **Your AI will create:**

        • Attractive headline  
        • Detailed caption  
        • Business/product description  
        • Key features  
        • Main benefits  
        • Target audience  
        • Promotional message  
        • Call to action  
        • Hashtags  
        • Short version  
        """
    )

    generate = st.button("✨ Generate Detailed Content")

    st.markdown("</div>", unsafe_allow_html=True)


# =========================================================
# GENERATE
# =========================================================

if generate:

    if not topic.strip():
        st.warning("⚠️ Please enter your topic first.")
        st.stop()

    try:

        api_key = st.secrets["GROQ_API_KEY"]

        client = Groq(api_key=api_key)

        prompt = f"""
You are a professional social media marketing expert,
copywriter and content strategist.

Create detailed, attractive and professional social media
content using the information below.

TOPIC:
{topic}

BUSINESS / BRAND:
{business_name if business_name else "Not provided"}

PLATFORM:
{platform}

CONTENT TYPE:
{content_type}

TONE:
{tone}


IMPORTANT:

DO NOT give a short answer.

DO NOT give only one paragraph.

The response must be DETAILED.

Use many clear headings.

Use bullet points where appropriate.

Make the content professional, natural, engaging,
modern and easy to understand.


FOLLOW THIS STRUCTURE:


# ✨ HEADLINE

Create a powerful and attractive headline.


# 📝 MAIN CAPTION

Write a detailed social media caption around
150-200 words.


# 📖 ABOUT

Explain the business, product, service, event
or topic in detail.


# 🌟 KEY FEATURES

Give 5-7 important features in bullet points.


# 💎 MAIN BENEFITS

Give 5-7 benefits in bullet points.


# 👥 TARGET AUDIENCE

Explain who this content/product/service is for.


# 🔥 WHY CHOOSE US

Give 4-6 convincing reasons.


# 🎯 PROMOTIONAL MESSAGE

Write an attractive promotional paragraph.


# 📢 CALL TO ACTION

Write a strong CTA encouraging the audience
to take action.


# 💬 ENGAGEMENT QUESTION

Add a question that encourages people to comment.


# #️⃣ HASHTAGS

Give 10-15 relevant hashtags.


# ⚡ SHORT VERSION

Create a short social media version around
40-60 words.


# 📌 POSTER TEXT

Create short, powerful text that can be placed
directly on a poster/design.


# 💡 CONTENT IDEA

Give one additional creative idea for this post.


Make every section useful.

Do not explain the instructions.

Only provide the final content.
"""

        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an expert social media content "
                        "creator and marketing strategist."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_tokens=3000
        )

        result = response.choices[0].message.content

        # =================================================
        # RESULT
        # =================================================

        st.markdown("---")

        st.markdown(
            '<div class="result-card">',
            unsafe_allow_html=True
        )

        st.markdown("## ✨ AI Generated Content")

        st.markdown(result)

        st.markdown("</div>", unsafe_allow_html=True)

        # =================================================
        # DOWNLOAD
        # =================================================

        st.download_button(
            label="⬇️ Download Content",
            data=result,
            file_name="ai_social_media_content.txt",
            mime="text/plain"
        )

    except Exception as e:

        st.error("❌ Something went wrong.")

        st.code(str(e))


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
    <div class="footer">
        ✨ AI Poster & Social Media Caption Maker
        <br>
        Create • Promote • Grow
    </div>
    """,
    unsafe_allow_html=True
)
