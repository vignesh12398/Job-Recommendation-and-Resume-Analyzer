import numpy as np
import streamlit as st
import pandas as pd
from prediction import predict
import helper
from resume_score import resume_score
from resume_score import resume_suggestions
st.markdown("""
<style>

.main {
    background-color: #0e1117;
}

h1 {
    color: #00f5d4;
    text-align: center;
}

h2 {
    color: #00bbf9;
}

.stButton>button {
    background-color: #00bbf9;
    color: white;
    border-radius: 8px;
    height: 45px;
    width: 200px;
    font-size: 16px;
}

.stButton>button:hover {
    background-color: #0077b6;
    color: white;
}

</style>
""", unsafe_allow_html=True)

st.sidebar.markdown("""
<h2 style='color:#00bbf9'>💼Job Recommendation System</h2>
""", unsafe_allow_html=True)
uploaded_file = st.sidebar.file_uploader("Choose a file", type=["pdf"])
st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Go to",
        [
                "📄 Resume Analyzer",
                "🧠 Career Prediction",
                "💼 Job Recommendation"
        ]
)

if page == "🧠 Career Prediction":

    st.title("Prediction of getting Recommended")

    st.subheader("Enter Skills (Optional)")
    user_input = st.text_area("Enter your skills")

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
elif page=='📄 Resume Analyzer':
        st.title("📄 Resume Analyzer")



        if uploaded_file is not None:
                resume_text = helper.extract_text_from_pdf(uploaded_file)
                tips=resume_suggestions(resume_text)

                score, breakdown = resume_score(resume_text)

                st.subheader("Resume Score")
                st.progress(score / 100)
                st.write(f"Score: {score}/100")

                st.write("Breakdown:", breakdown)

                st.subheader("📌 ATS Improvement Suggestions")
                for tip in tips:
                        st.write(".",tip)



else:
        st.title("Top 5 job recommendations")
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

