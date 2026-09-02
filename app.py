import re
import numpy as np
import streamlit as st
import pandas as pd
from prediction import predict
import helper
from trend import get_trend
from trend import trend_direction
from resume_score import resume_score
from resume_score import resume_suggestions
from resume_score import predict_score

st.set_page_config(
    page_title="Career System | Smart Resume + Job AI",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&family=Inter:wght@400;500;600&display=swap');

html, body, [class*="css"]  {
    font-family: 'Inter', 'Poppins', sans-serif;
}

/* Background */
.stApp {
    background: radial-gradient(circle at 15% 0%, #17233b 0%, #0f172a 45%, #0b1120 100%);
}

/* Hide default streamlit chrome for a cleaner look */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {background: transparent !important;}

/* Titles */
h1 {
    font-family: 'Poppins', sans-serif;
    color: #38bdf8;
    text-align: center;
    font-weight: 800;
    letter-spacing: 0.5px;
    text-shadow: 0px 0px 25px rgba(56,189,248,0.35);
    padding-bottom: 4px;
}

h2 {
    font-family: 'Poppins', sans-serif;
    color: #22d3ee;
    font-weight: 700;
}

h3 {
    font-family: 'Poppins', sans-serif;
    color: #e2e8f0;
    font-weight: 600;
}

p, li, label, span {
    font-family: 'Inter', sans-serif;
}

/* Card style */
.card {
    background: linear-gradient(160deg, rgba(30,41,59,0.9), rgba(15,23,42,0.9));
    padding: 24px 26px;
    border-radius: 18px;
    border: 1px solid rgba(56,189,248,0.15);
    box-shadow: 0px 8px 30px rgba(0,0,0,0.45);
    margin-bottom: 22px;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.card:hover {
    transform: translateY(-2px);
    box-shadow: 0px 10px 40px rgba(56,189,248,0.15);
}

/* Result banner */
.result-banner {
    padding: 26px;
    border-radius: 16px;
    background: linear-gradient(145deg, #10192e, #16233f);
    border: 1px solid rgba(0,187,249,0.35);
    text-align: center;
    box-shadow: 0px 0px 35px rgba(0,187,249,0.12);
    margin-bottom: 16px;
}

.confidence-banner {
    padding: 18px;
    border-radius: 14px;
    background: linear-gradient(145deg, #131a26, #1b2432);
    border: 1px solid rgba(148,163,184,0.15);
    text-align: center;
}

/* Button */
.stButton>button {
    background: linear-gradient(90deg, #06b6d4, #3b82f6);
    color: white;
    border: none;
    border-radius: 12px;
    height: 52px;
    width: 100%;
    font-size: 16px;
    font-weight: 700;
    letter-spacing: 0.3px;
    box-shadow: 0px 6px 18px rgba(59,130,246,0.35);
    transition: all 0.25s ease;
}

.stButton>button:hover {
    background: linear-gradient(90deg, #0891b2, #2563eb);
    box-shadow: 0px 8px 24px rgba(59,130,246,0.5);
    transform: translateY(-1px);
}

.stButton>button:active {
    transform: translateY(0px);
}

/* Text area / input */
textarea, .stTextInput>div>div>input {
    border-radius: 12px !important;
    background-color: #111827 !important;
    color: #e2e8f0 !important;
    border: 1px solid rgba(148,163,184,0.2) !important;
}

/* Progress bar */
.stProgress > div > div {
    background: linear-gradient(90deg, #06b6d4, #38bdf8);
    border-radius: 8px;
}

/* Metric */
[data-testid="stMetricValue"] {
    color: #00f5d4;
    font-family: 'Poppins', sans-serif;
    font-weight: 800;
}

/* Info / warning / error boxes */
.stAlert {
    border-radius: 12px !important;
}

/* Dataframe */
[data-testid="stDataFrame"] {
    border-radius: 14px;
    overflow: hidden;
    border: 1px solid rgba(148,163,184,0.15);
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0b1224, #111a30);
    border-right: 1px solid rgba(56,189,248,0.12);
}

[data-testid="stSidebar"] > div:first-child {
    padding-top: 6px;
}

/* Divider look for sidebar sections */
.sidebar-divider {
    border: none;
    border-top: 1px solid rgba(148,163,184,0.15);
    margin: 14px 0 18px 0;
}

/* Sidebar file uploader dropzone */
[data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"] {
    background: linear-gradient(160deg, rgba(17,24,39,0.9), rgba(11,17,32,0.9));
    border: 1.5px dashed rgba(56,189,248,0.35);
    border-radius: 14px;
    padding: 6px;
    transition: border-color 0.2s ease, box-shadow 0.2s ease;
}

[data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"]:hover {
    border-color: #38bdf8;
    box-shadow: 0px 0px 18px rgba(56,189,248,0.15);
}

[data-testid="stSidebar"] [data-testid="stFileUploaderDropzoneInstructions"] svg {
    fill: #38bdf8 !important;
}

[data-testid="stSidebar"] [data-testid="stFileUploaderDropzoneInstructions"] span,
[data-testid="stSidebar"] [data-testid="stFileUploaderDropzoneInstructions"] small {
    color: #94a3b8 !important;
}

[data-testid="stSidebar"] [data-testid="stBaseButton-secondary"],
[data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"] button {
    background: linear-gradient(90deg, #0f2540, #14304f) !important;
    color: #7dd3fc !important;
    border: 1px solid rgba(56,189,248,0.4) !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
}

/* Uploaded file chip */
[data-testid="stSidebar"] [data-testid="stFileUploaderFile"] {
    background: linear-gradient(160deg, rgba(15,37,64,0.7), rgba(15,23,42,0.7));
    border: 1px solid rgba(56,189,248,0.2);
    border-radius: 10px;
    padding: 6px 10px;
    margin-top: 8px;
}

/* Sidebar navigation radio -> styled pill list */
[data-testid="stSidebar"] .stRadio > div[role="radiogroup"] {
    gap: 6px;
    display: flex;
    flex-direction: column;
}

[data-testid="stSidebar"] .stRadio label {
    background: rgba(148,163,184,0.04);
    border: 1px solid rgba(148,163,184,0.12);
    border-radius: 10px;
    padding: 10px 14px !important;
    margin: 0px !important;
    transition: all 0.2s ease;
    cursor: pointer;
}

[data-testid="stSidebar"] .stRadio label:hover {
    background: rgba(56,189,248,0.08);
    border-color: rgba(56,189,248,0.35);
    transform: translateX(2px);
}

[data-testid="stSidebar"] .stRadio label div p {
    color: #cbd5e1 !important;
    font-weight: 500 !important;
    font-size: 14.5px !important;
}

[data-testid="stSidebar"] .stRadio label[data-checked="true"],
[data-testid="stSidebar"] .stRadio label:has(input:checked) {
    background: linear-gradient(90deg, rgba(6,182,212,0.18), rgba(59,130,246,0.18));
    border: 1px solid rgba(56,189,248,0.55);
    box-shadow: 0px 0px 16px rgba(56,189,248,0.12);
}

[data-testid="stSidebar"] .stRadio label:has(input:checked) div p {
    color: #38bdf8 !important;
    font-weight: 700 !important;
}

/* ATS suggestion tip cards */
.tip-card {
    display: flex;
    gap: 14px;
    align-items: flex-start;
    background: linear-gradient(135deg, rgba(30,41,59,0.85), rgba(15,23,42,0.9));
    border: 1px solid rgba(56,189,248,0.15);
    border-left: 4px solid #22d3ee;
    border-radius: 12px;
    padding: 16px 18px;
    margin-bottom: 14px;
    transition: transform 0.18s ease, box-shadow 0.18s ease, border-color 0.18s ease;
}

.tip-card:hover {
    transform: translateX(3px);
    border-left-color: #38bdf8;
    box-shadow: 0px 6px 22px rgba(56,189,248,0.12);
}

.tip-number {
    flex-shrink: 0;
    width: 30px;
    height: 30px;
    border-radius: 50%;
    background: linear-gradient(135deg, #06b6d4, #3b82f6);
    color: white;
    font-weight: 800;
    font-family: 'Poppins', sans-serif;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 14px;
    box-shadow: 0px 0px 12px rgba(56,189,248,0.35);
}

.tip-text {
    color: #cbd5e1;
    font-size: 15px;
    line-height: 1.55;
}

.tip-text b, .tip-text strong {
    color: #5eead4;
}

</style>
""", unsafe_allow_html=True)

st.sidebar.markdown("""
<div style='text-align:center; padding: 10px 0 4px 0;'>
<h1 style='font-size:26px; margin-bottom:0px; text-shadow:0px 0px 18px rgba(56,189,248,0.4);'>🚀</h1>
<h2 style='text-align:center;color:#38bdf8; margin-bottom:2px; font-size:22px;'>Career System</h2>
<p style='text-align:center;color:#94a3b8; font-size:13px; margin-top:0px;'>Smart Resume + Job AI</p>
</div>
<hr class="sidebar-divider">
""", unsafe_allow_html=True)

st.sidebar.markdown("<p style='color:#94a3b8; font-size:13px; font-weight:600; margin-bottom:6px;'>📎 UPLOAD RESUME</p>", unsafe_allow_html=True)
uploaded_file = st.sidebar.file_uploader("Choose a file", type=["pdf"], label_visibility="collapsed")

st.sidebar.markdown("<hr class='sidebar-divider'>", unsafe_allow_html=True)
st.sidebar.markdown("<p style='color:#94a3b8; font-size:13px; font-weight:600; margin-bottom:6px;'>🧭 NAVIGATION</p>", unsafe_allow_html=True)

page = st.sidebar.radio(
    "Go to",
        [
                "📄 Resume Analyzer",
                "🧠 Career Prediction",
                "💼 Job Recommendation",
                "📊 Job Market Trends"
        ],
        label_visibility="collapsed"
)

st.sidebar.markdown("<hr class='sidebar-divider'>", unsafe_allow_html=True)
st.sidebar.markdown("""
<p style='text-align:center; color:#475569; font-size:11px;'>
Powered by AI • v1.0
</p>
""", unsafe_allow_html=True)

if page == "🧠 Career Prediction":

    st.title("Prediction of getting Recommended")
    st.markdown("""
    <div class="card">
    <h3>🧠 AI Career Prediction</h3>
    <p style="color:#94a3b8;">
    Enter your skills or upload resume to predict your ideal career role.
    </p>
    </div>
    """, unsafe_allow_html=True)

    # st.markdown('<div class="card">', unsafe_allow_html=True)

    st.subheader("💡 Enter Skills (Optional)")
    user_input = st.text_area("Enter your skills")

    st.markdown('</div>', unsafe_allow_html=True)

    if st.button("Check Recommendation"):

        if user_input.strip() != "":
            prob, role_name = predict(user_input)

        elif uploaded_file is not None:
            resume_text = helper.extract_text_from_pdf(uploaded_file)
            prob, role_name = predict(resume_text)

        else:
            st.warning("Please upload a resume or enter skills")
            st.stop()

        st.markdown(f"""
        <div class="result-banner">

        🚀 <b style="color:#e2e8f0; font-size:18px;">Predicted Career Role</b><br><br>
        <span style="color:#00f5d4;font-size:30px; font-weight:800; font-family:'Poppins',sans-serif;">{role_name}</span>

        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="confidence-banner">

        📊 Model Confidence: <b style="color:#00bbf9; font-size:19px;">{prob * 100:.2f}%</b>

        </div>
        """, unsafe_allow_html=True)
elif page=="📊 Job Market Trends":
        st.title("📊 Job Market Trends")
        st.markdown("""
        <div class="card">
        <h3>📈 Real-Time Market Insights</h3>
        <p style="color:#94a3b8;">
        Enter a job role to see how demand is trending.
        </p>
        </div>
        """, unsafe_allow_html=True)
        role = st.text_input("Enter Job Role (e.g., AI Engineer, Data Scientist)")
        if role:
            with st.spinner("Fetching real-time trends...."):
                trend_data=get_trend(role)
            if trend_data is None:
                st.error("no trend data found,try diiferent role.")
            else:
                direction=trend_direction(trend_data,role)
                st.subheader(f"Trend for{role}")
                st.markdown(f"""
                <div class="confidence-banner" style="text-align:left; margin-bottom:16px;">
                <b style="color:#94a3b8;">Market Direction:</b> <span style="color:#00f5d4; font-weight:700;">{direction}</span>
                </div>
                """, unsafe_allow_html=True)

                st.line_chart(trend_data)

elif page=='📄 Resume Analyzer':
        st.markdown("""
        <div style="text-align:center; margin-bottom:20px;">
        <h2 style="color:#38bdf8; margin-bottom:5px;">
        🚀  Career Assistant
        </h2>
        <p style="color:#94a3b8; font-size:15px;">
        Smart Resume Scoring • Career Prediction • Job Recommendations
        </p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("""
        <div class="card">
        <h3>👋 Welcome to Resume Analyzer</h3>
        <p style="color:#94a3b8;">
        Upload your resume from the sidebar to get:
        <br>✔️ ATS Score
        <br>✔️ Resume Feedback
        <br>✔️ Improvement Suggestions
        </p>
        </div>
        """, unsafe_allow_html=True)
        if uploaded_file is None:
            st.info("📄 Upload your resume from the left sidebar to get started!")

            st.markdown("""
            <div class="card">
            <h3>✨ What this tool does:</h3>
            <ul style="color:#cbd5e1; line-height:1.8;">
            <li>Analyze resume using AI</li>
            <li>Give ATS score</li>
            <li>Suggest improvements</li>
            <li>Improve job chances</li>
            </ul>
            </div>
            """, unsafe_allow_html=True)


        if uploaded_file is not None:
                resume_text = helper.extract_text_from_pdf(uploaded_file)
                tips=resume_suggestions(resume_text)

                # breakdown = resume_score(resume_text)
                score=predict_score(resume_text)

                st.markdown('<div class="card">', unsafe_allow_html=True)

                st.subheader("📊 Resume Score")
                st.progress(score / 100)
                st.metric("Score", f"{int(score)}/100")

                # st.markdown('</div>', unsafe_allow_html=True)
                # st.write("Breakdown:", breakdown)

                st.subheader("📌 ATS Improvement Suggestions")
                for i, tip in enumerate(tips, start=1):
                    # display-only: strip a leading "1. " style prefix so it doesn't
                    # duplicate the numbered circle badge (does not touch resume_suggestions())
                    tip_display = re.sub(r"^\s*\d+\.\s*", "", tip)
                    st.markdown(f"""
                    <div class="tip-card">
                    <div class="tip-number">{i}</div>
                    <div class="tip-text">💡 {tip_display}</div>
                    </div>
                    """, unsafe_allow_html=True)



else:
        st.title("Top 5 job recommendations")
        st.markdown("""
        <div class="card">
        <h3>💼 Job Recommendation Engine</h3>
        <p style="color:#94a3b8;">
        Get top job roles based on your skills or resume.
        </p>
        </div>
        """, unsafe_allow_html=True)
        st.subheader("Enter Skills (Optional)")
        user_input = st.text_area("Enter your skills")

        if st.button("Check Recommendation"):

                if user_input.strip() != "":
                        results = helper.recommend_job(user_input)
                        st.dataframe(results)

                elif uploaded_file is not None:
                        resume_text = helper.extract_text_from_pdf(uploaded_file)
                        results = helper.recommend_job(resume_text)

                        st.subheader("💼 Recommended Jobs")
                        st.dataframe(results)
