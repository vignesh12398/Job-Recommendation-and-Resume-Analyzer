import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression

@st.cache_resource
def train_model():

    df = pd.read_csv('Final_Specialized_Dataset_Fixed.csv')
    df['combined_text'] = (
        df['User_Skills'].fillna('') + ' ' +
        df['Job_Requirements'].fillna('') + ' ' +
        df['Job_Role'].fillna('')
    )
    
    
    # 2. Clean text
    import re
    def clean_text(text):
        text = text.lower()
        text = re.sub(r'\W+', ' ', text)
        return text
    
    df['combined_text'] = df['combined_text'].apply(clean_text)
    
    counts = df['Job_Role'].value_counts()
    df = df[df['Job_Role'].isin(counts[counts >= 10].index)]
    
    # 🔥 LIMIT ROLES (MOST IMPORTANT)
    top_roles = df['Job_Role'].value_counts().head(50).index
    df = df[df['Job_Role'].isin(top_roles)]
    print(df['Job_Role'].value_counts())
    # role_df = df.groupby('Job_Role')['combined_text'].apply(lambda x: ' '.join(x)).reset_index()
    tfidf_row = TfidfVectorizer(
        stop_words='english',
        ngram_range=(1,2),
        max_features=15000,
        min_df=3
    )
    
    X_train_text, X_test_text, y_train, y_test = train_test_split(
        df['combined_text'],
        df['Job_Role'],
        test_size=0.2,
        random_state=42,
        stratify=df['Job_Role']
    )
    
    X_train = tfidf_row.fit_transform(X_train_text)
    X_test = tfidf_row.transform(X_test_text)
    from sklearn.linear_model import LogisticRegression
    
    model = LogisticRegression(max_iter=1000, class_weight="balanced")
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    return model,tfidf_row


model, tfidf = train_model()

def predict(user_input):

    user_vector = tfidf.transform([user_input])

    role_name = model.predict(user_vector)[0]

    prob = model.predict_proba(user_vector).max()

    return prob, role_name
