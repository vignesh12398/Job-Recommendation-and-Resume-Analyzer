import pandas as pd
from groq import Groq
import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import Ridge
def predict_score(resume_text):
    text = resume_text.lower()

    df = pd.read_csv("Final_Fixed_Dataset_V2.csv")
    df['text'] = df['User_Skills'] + " " + df['Job_Requirements'] + " " + df['Projects'] + " " + df['Certifications']
    df['Score'] = df['text'].apply(resume_score)
    df['Score'] = (df['Score'] / df['Score'].max()) * 100
    df['text'] = df['text'].fillna("")
    df['text'] = df['text'].astype(str)
    v = TfidfVectorizer(stop_words='english', max_features=3000, min_df=2, ngram_range=(1, 2))
    X = df['text']
    y = df['Score']
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    X_train = v.fit_transform(X_train)
    X_test = v.transform(X_test)
    s = Ridge()
    s.fit(X_train, y_train)
    user_vector = v.transform([resume_text])

    score = s.predict(user_vector)[0]
    return score

def resume_score(resume_text):
    text = resume_text.lower()

    scores = {
        "skills": 0,
        "projects": 0,
        "experience": 0,
        "education": 0,
        "tools": 0,
        "certifications": 0,
        "structure": 5
    }

    skills = [
        "python", "java", "c++", "machine learning", "deep learning",
        "tensorflow", "pytorch", "sql", "pandas", "numpy", "css", "javascript",
        "mongodb", "devops", "node.js", "next.js", "react",
        "flask", "django", "scikit-learn"
    ]

    skills_count = sum(1 for skill in skills if skill in text)
    scores['skills'] = min(skills_count * 5, 50)  # increased weight

    # Projects (your dataset has actual project names)
    if any(word in text for word in ["model", "system", "app", "pipeline", "dashboard"]):
        scores['projects'] = 15

    # Experience (not in dataset → keep small)
    if "experience" in text or "internship" in text:
        scores['experience'] = 10

    # Education (optional)
    if any(word in text for word in ["btech", "degree"]):
        scores["education"] = 5

    tools = [
        "git", "streamlit", "docker", "linux", "aws", "jupyter",
        "kubernetes", "vs code", "mysql", "mongodb", "postman"
    ]

    tools_count = sum(1 for tool in tools if tool in text)
    scores['tools'] = min(tools_count * 3, 15)

    if any(word in text for word in ["certification", "coursera", "aws", "certificate"]):
        scores["certifications"] = 15

    total_score = sum(scores.values())

    return total_score

def resume_suggestions(resume_text):
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{
            "role":"user",
            "content":f"""You are an ATS resume expert. Analyze this resume and give exactly 5 specific improvement suggestions.
Format each suggestion on a new line starting with a number.
Resume: {resume_text}"""
        }]
    )
    result=response.choices[0].message.content
    tips=[line.strip() for line in result.split("\n") if line.strip()]

    return tips
