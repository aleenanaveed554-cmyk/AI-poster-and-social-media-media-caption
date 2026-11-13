import streamlit as st
from groq import Groq

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="AI Poster & Social Media Caption Maker",
    page_icon="✨",
    layout="wide"
)

# =========================
# CUSTOM CSS
# =========================
st.markdown("""
<style>

.stApp {
    background: linear-gradient(135deg, #eee5ff 0%, #d8c4f5 50%, #f5edff 100%);
}

.main-title {
    text-align: center;
    font-size: 42px;
    font-weight: 800;
    color: #111111;
    margin-top: 10px;
    margin-bottom: 5px;
}

.subtitle {
    text-align: center;
    font-size: 18px;
    color: #333333;
    margin-bottom: 30px;
}

.card {
    background: rgba(255,255,255,0.92);
    padding: 25px;
    border-radius: 22px;
    box-shadow: 0 8px 30px rgba(70,40,100,0.15);
    margin-bottom: 20px;
}

.result-card {
    background: white;
    padding: 30px;
    border-radius: 22px;
    box-shadow: 0 8px 30px rgba(50,30,80,0.18);
    color: #111111;
}

.result-card h1,
.result-card h2,
.result-card h3,
.result-card p,
.result-card li {
    color: #111111 !important;
}

.result-card h2 {
    font-size: 25px;
    margin-top: 22px;
}

.result-card h3 {
    font-size: 20px;
}

.stTextArea textarea {
    background-color: white !important;
    color: #111111 !important;
    border-radius: 14px !important;
    border: 2px solid #a875d6 !important;
}

.stTextInput input {
    background-color: white !important;
    color: #111111 !important;
    border-radius: 14px !important;
    border: 2px solid #a875d6 !important;
}

.stSelectbox div {
    color: #111111 !important;
}

div.stButton > button {
    width: 100%;
    border-radius: 14px;
    border: none;
    padding: 13px;
    font-size: 17px;
    font-weight: 700;
    background: linear-gradient(90deg, #7b2cbf, #a855d8);
    color: white;
}

div.stButton > button:hover {
    background: linear-gradient(90deg, #6a1fb0, #933fc4);
    color: white;
}

.footer {
    text-align: center;
    color: #333333;
    font-size: 14px;
    margin-top: 30px;
}

</style>
""", unsafe_allow_html=True)


# =========================
# HEADER
# =========================
st.markdown(
    '<div class="main-title">✨ AI Poster & Social Media Caption Maker</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Create professional posters, captions and social media content with AI</div>',
    unsafe_allow_html=True
)


# =========================
# MAIN LAYOUT
# =========================
left, right = st.columns([1, 1])


# =========================
# LEFT SIDE - INPUT
# =========================
with left:

    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.markdown("### 📝 Tell AI About Your Content")

    topic = st.text_area(
        "What is your business, product, event or post about?",
        placeholder=(
            "Example: New luxury beauty salon opening in Islamabad "
            "with professional makeup, skincare and hair styling services."
        ),
        height=180
    )

    business_name = st.text_input(
        "Business / Brand Name",
        placeholder="Example: Glow Beauty Studio"
    )

    platform = st.selectbox(
        "Choose Platform",
        [
            "Instagram",
            "Facebook",
            "TikTok",
            "LinkedIn"
        ]
    )

    content_type = st.selectbox(
        "Content Type",
        [
            "Social Media Caption",
            "Poster Content",
            "Product Promotion",
            "Business Promotion",
            "Event Promotion",
            "Sale / Discount",
            "New Product Launch",
            "Educational Post"
        ]
    )

    tone = st.selectbox(
        "Choose Tone",
        [
            "Professional",
            "Modern",
            "Luxury",
            "Friendly",
            "Creative",
            "Catchy"
        ]
    )

    st.markdown('</div>', unsafe_allow_html=True)


# =========================
# RIGHT SIDE - GENERATOR
# =========================
with right:

    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.markdown("### ✨ Generate Your Content")

    st.write(
        "AI will create detailed content with headings, "
        "descriptions, highlights, CTA and hashtags."
    )

    generate = st.button("✨ Generate AI Content")

    st.markdown('</div>', unsafe_allow_html=True)


# =========================
# AI GENERATION
# =========================
if generate:

    if not topic.strip():
        st.warning("⚠️ Please enter your business, product, event or post topic.")
        st.stop()

    try:

        api_key = st.secrets["GROQ_API_KEY"]

        client = Groq(api_key=api_key)

        prompt = f"""
You are a professional social media content writer and marketing expert.

Create high-quality content based on the information below.

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

IMPORTANT INSTRUCTIONS:

Do NOT give only one short paragraph.

Create a detailed, professional and visually organized response.

Use CLEAR HEADINGS for every section.

The output must follow this structure:

## HEADLINE
Write a powerful and attractive headline.

## MAIN CAPTION
Write a detailed social media caption of around 100-150 words.

## ABOUT
Explain the business, product, event or topic in detail.

## KEY HIGHLIGHTS
Give 5-6 useful bullet points.

## BENEFITS
Explain the main benefits or reasons people should choose this product, service or event.

## CALL TO ACTION
Write a strong and attractive CTA.

## HASHTAGS
Give 8-12 relevant hashtags.

## SHORT VERSION
Create a short version suitable for a quick social media post.

Make everything natural, professional, engaging and easy to understand.

Do not mention these instructions.
Do not add unnecessary explanations.
"""


        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert social media marketing content creator."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_tokens=2200
        )

        result = response.choices[0].message.content

        # =========================
        # RESULT
        # =========================
        st.markdown("---")

        st.markdown(
            '<div class="result-card">',
            unsafe_allow_html=True
        )

        st.markdown("## ✨ Your AI Generated Content")

        st.markdown(result)

        st.markdown("</div>", unsafe_allow_html=True)

        # =========================
        # DOWNLOAD
        # =========================
        st.download_button(
            "⬇️ Download Content",
            data=result,
            file_name="ai_social_media_content.txt",
            mime="text/plain"
        )

    except Exception as e:

        st.error(
            "Something went wrong. Please check your Groq API key and try again."
        )

        st.code(str(e))


# =========================
# FOOTER
# =========================
st.markdown(
    """
    <div class="footer">
        ✨ AI Poster & Social Media Caption Maker • Create • Share • Grow
    </div>
    """,
    unsafe_allow_html=True
)
