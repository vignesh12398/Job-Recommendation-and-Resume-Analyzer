import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
import re

def clean_text(text):
    text = text.lower()
    text = re.sub(r'\W+', ' ', text)
    return text
@st.cache_resource
def load_model():
    df = pd.read_csv("Final_Specialized_Dataset_Fixed.csv")

    df['combined_text'] = (
        df['User_Skills'].fillna('') + ' ' +
        df['Job_Requirements'].fillna('')
    )

    df['combined_text'] = df['combined_text'].apply(clean_text)



    X_train, X_test, y_train, y_test = train_test_split(
        df['combined_text'],
        df['Job_Role'],
        test_size=0.2,
        random_state=42,
        stratify=df['Job_Role']
    )

    tfidf_row = TfidfVectorizer(
        stop_words='english',
        ngram_range=(1, 2),
        max_features=10000,
        min_df=1,
        sublinear_tf=True
    )
    X_train = tfidf_row.fit_transform(X_train)
    X_test = tfidf_row.transform(X_test)

    model = LogisticRegression(
        max_iter=1000,
        class_weight='balanced',
        C=1.0,
        solver='lbfgs',   # ← faster than saga for your data size
        n_jobs=-1
    )
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    return model, tfidf_row,acc

model, tfidf_row,acc= load_model()
# y_pred = model.predict(X_test)
# acc = accuracy_score(y_test, y_pred)

print(f"Model accuracy: {acc*100:.2f}%")

def predict(user_input):
    user_input = clean_text(user_input)
    user_vector = tfidf_row.transform([user_input])

    role_name = model.predict(user_vector)[0]

    prob = model.predict_proba(user_vector).max()


    return prob, role_name


