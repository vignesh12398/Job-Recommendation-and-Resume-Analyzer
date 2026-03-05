import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression

@st.cache_resource
def train_model():

    df = pd.read_csv("Expanded_Roles_Job_Dataset.csv")

    df['combined_text'] = (
        df['User_Skills'].fillna('') + " " +
        df['Job_Requirements'].fillna('')
    )

    tfidf = TfidfVectorizer(
        stop_words='english',
        ngram_range=(1,2),
        max_features=5000
    )

    X = tfidf.fit_transform(df['combined_text'])
    y = df['Job_Role']

    X_train,X_test,y_train,y_test = train_test_split(
        X,y,test_size=0.2,random_state=42
    )

    model = LogisticRegression(max_iter=1000,class_weight="balanced")
    model.fit(X_train,y_train)

    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test,y_pred)

    return model, tfidf

model, tfidf = train_model()

def predict(user_input):

    user_vector = tfidf.transform([user_input])

    role_name = model.predict(user_vector)[0]

    prob = model.predict_proba(user_vector).max()

    return prob, role_name
