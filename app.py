import streamlit as st
from groq import Groq

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Postify AI",
    page_icon="✨",
    layout="wide"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #160b24 0%, #6d3fa9 50%, #c99bea 100%);
    }

    .main-title {
        text-align: center;
        font-size: 52px;
        font-weight: 800;
        color: #ffffff;
        margin-bottom: 5px;
    }

    .subtitle {
        text-align: center;
        font-size: 18px;
        color: #f5eaff;
        margin-bottom: 30px;
    }

    .section-title {
        font-size: 26px;
        font-weight: 800;
        color: #111111;
        margin-top: 10px;
    }

    .result-box {
        background: rgba(255,255,255,0.96);
        border-radius: 22px;
        padding: 30px;
        box-shadow: 0 10px 35px rgba(0,0,0,0.18);
        color: #111111;
    }

    .result-box h1,
    .result-box h2,
    .result-box h3,
    .result-box p,
    .result-box li {
        color: #111111 !important;
    }

    .stTextArea textarea {
        background-color: #ffffff !important;
        color: #111111 !important;
        border-radius: 15px !important;
        border: 2px solid #b77be8 !important;
        font-size: 16px !important;
    }

    .stSelectbox div {
        color: #111111 !important;
    }

    div.stButton > button {
        width: 100%;
        border-radius: 14px;
        background: linear-gradient(90deg, #7b2cbf, #c77dff);
        color: white;
        font-size: 18px;
        font-weight: 700;
        border: none;
        padding: 13px;
    }

    div.stButton > button:hover {
        background: linear-gradient(90deg, #9d4edd, #e0aaff);
        color: white;
    }
</style>
""", unsafe_allow_html=True)


# ---------------- HEADER ----------------
st.markdown(
    '<div class="main-title">✨ Postify AI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Smart Social Media Content Studio</div>',
    unsafe_allow_html=True
)


# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.markdown("## ⚙️ Content Settings")

    platform = st.selectbox(
        "Choose Platform",
        ["Instagram", "Facebook", "TikTok", "LinkedIn"]
    )

    content_type = st.selectbox(
        "Content Type",
        [
            "Social Media Post",
            "Product Promotion",
            "Business Promotion",
            "Event Promotion",
            "Sale / Discount",
            "New Product Launch",
            "Educational Post"
        ]
    )

    tone = st.selectbox(
        "Tone",
        [
            "Professional",
            "Modern",
            "Luxury",
            "Friendly",
            "Creative",
            "Catchy"
        ]
    )


# ---------------- INPUT ----------------
st.markdown("### 💡 Tell the AI what your content is about")

topic = st.text_area(
    "Enter your business, product, event or post idea:",
    placeholder="Example: New luxury beauty salon opening in Islamabad with makeup, skincare and hair styling services.",
    height=150
)


# ---------------- GENERATE BUTTON ----------------
if st.button("✨ Generate Detailed Content"):

    if not topic.strip():
        st.warning("Please enter a topic first.")
        st.stop()

    try:
        api_key = st.secrets["GROQ_API_KEY"]

        client = Groq(api_key=api_key)

        prompt = f"""
You are a professional social media content strategist.

Create detailed, professional and attractive social media content.

TOPIC:
{topic}

PLATFORM:
{platform}

CONTENT TYPE:
{content_type}

TONE:
{tone}

IMPORTANT:
Do NOT give a short paragraph only.

The response MUST be properly organized with clear headings,
detailed information, bullet points where useful, and a strong
call-to-action.

Use this exact structure:

## HEADLINE
Write an attractive headline.

## MAIN CAPTION
Write a detailed and engaging caption of around 100-150 words.

## ABOUT / DESCRIPTION
Explain the business, product, event or topic in detail.

## KEY HIGHLIGHTS
Give 4-6 useful bullet points.

## WHY CHOOSE US
Give 3-5 convincing points if relevant.

## CALL TO ACTION
Write a strong CTA suitable for the selected platform.

## HASHTAGS
Give 8-12 relevant hashtags.

## SHORT VERSION
Give one short version suitable for a social media post.

Make the content professional, natural and easy to understand.
Do not write explanations about your instructions.
"""

        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert social media content creator."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_tokens=1800
        )

        result = response.choices[0].message.content

        # ---------------- RESULT ----------------
        st.markdown("---")
        st.markdown("## ✨ Your AI Content")

        st.markdown(
            f"""
            <div class="result-box">
                {result.replace("## ", "<h2>").replace("\n", "<br>")}
            </div>
            """,
            unsafe_allow_html=True
        )

        # ---------------- DOWNLOAD ----------------
        st.download_button(
            label="⬇️ Download AI Content",
            data=result,
            file_name="postify_ai_content.txt",
            mime="text/plain"
        )

    except Exception as e:
        st.error(f"Something went wrong: {e}")


# ---------------- FOOTER ----------------
st.markdown("---")

st.markdown(
    """
    <div style="text-align:center; color:white; font-size:14px;">
        ✨ Postify AI • Smart Social Media Content Studio
    </div>
    """,
    unsafe_allow_html=True
)
