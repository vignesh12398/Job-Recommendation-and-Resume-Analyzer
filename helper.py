import pandas as pd
import streamlit as st
from sentence_transformers import SentenceTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from PyPDF2 import PdfReader

# Load dataset
@st.cache_data
def load_dataset():
    df = pd.read_csv('Final_Specialized_Dataset_Fixed.csv')

    # Combine text columns
    df['Job_Profile'] = (
        df['Job_Role'].fillna('') + ' ' +
        df['Job_Requirements'].fillna('')
    )
    return df
@st.cache_data
def load_model():
    return SentenceTransformer(
        "sentence-transformers/all-MiniLM-L6-v2")
# Group by role


@st.cache_resource
def load_job_embeddings():
    df = load_dataset()
    model = load_model()

    embeddings = model.encode(
        df["Job_Profile"].tolist(),
        batch_size=64,
        normalize_embeddings=True,
        show_progress_bar=False
    )

    return embeddings
# Load resources
df = load_dataset()
model = load_model()
job_embeddings = load_job_embeddings()
# Extract text from PDF
def extract_text_from_pdf(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text   # <-- moved outside loop

# Recommendation function
def recommend_job(text, top_n=5):
    if not isinstance(text, str) or not text.strip():
        return pd.DataFrame(columns=["Job_Role"])
    query_embedding = model.encode(
        text,
        normalize_embeddings=True
    )
    scores = job_embeddings @ query_embedding
    results = pd.DataFrame({
        "Job_Role": df["Job_Role"].values,
        "similarity": scores
    })
    groups = results.groupby("Job_Role")["similarity"].apply(
        lambda values:values.nlargest(5).mean()
    )
    top_roles = groups.sort_values(ascending=False).head(top_n)
    return top_roles.rename_axis("Job_Role").reset_index()[
        ["Job_Role"]
    ]
