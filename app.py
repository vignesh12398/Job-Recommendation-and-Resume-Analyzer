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
st.markdown("""
<style>

/* Background */
.stApp {
    background: linear-gradient(135deg, #0f172a, #1e293b);
}

/* Titles */
h1 {
    color: #38bdf8;
    text-align: center;
    font-weight: bold;
}

h2 {
    color: #00bbf9;
}

/* Card style */
.card {
    background-color: #1e293b;
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0px 4px 20px rgba(0,0,0,0.4);
    margin-bottom: 20px;
}

/* Button */
.stButton>button {
    background: linear-gradient(90deg, #06b6d4, #3b82f6);
    color: white;
    border-radius: 10px;
    height: 50px;
    width: 100%;
    font-size: 16px;
    font-weight: bold;
}

.stButton>button:hover {
    background: linear-gradient(90deg, #0891b2, #2563eb);
}

/* Text area */
textarea {
    border-radius: 10px !important;
}

</style>
""", unsafe_allow_html=True)

st.sidebar.markdown("""
<h2 style='text-align:center;color:#38bdf8;'>🚀  Career System</h2>
<p style='text-align:center;color:#94a3b8;'>Smart Resume + Job AI</p>
""", unsafe_allow_html=True)
uploaded_file = st.sidebar.file_uploader("Choose a file", type=["pdf"])
st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Go to",
        [
                "📄 Resume Analyzer",
                "🧠 Career Prediction",
                "💼 Job Recommendation",
                "📊 Job Market Trends"
        ]
)

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
        <div style="
        padding:20px;
        border-radius:10px;
        background-color:#1c1f26;
        border:2px solid #00bbf9;
        text-align:center;
        font-size:22px;
        ">

        🚀 <b>Predicted Career Role</b><br><br>
        <span style="color:#00f5d4;font-size:28px">{role_name}</span>

        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div style="
        padding:15px;
        border-radius:8px;
        background-color:#222831;
        text-align:center;
        font-size:18px;
        ">

        📊 Model Confidence: <b style="color:#00bbf9">{prob * 100:.2f}%</b>

        </div>
        """, unsafe_allow_html=True)
elif page=="📊 Job Market Trends":
        st.title("📊 Job Market Trends")
        role = st.text_input("Enter Job Role (e.g., AI Engineer, Data Scientist)")
        if role:
            with st.spinner("Fetching real-time trends...."):
                trend_data=get_trend(role)
            if trend_data is None:
                st.error("no trend data found,try diiferent role.")
            else:
                direction=trend_direction(trend_data,role)
                st.subheader(f"Trend for{role}")
                st.write(f"**Market Direction:** {direction}")

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
            <ul>
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
                for tip in tips:
                         st.info(f"💡 {tip}")



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

