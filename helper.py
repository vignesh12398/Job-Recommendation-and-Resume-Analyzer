import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from PyPDF2 import PdfReader

# Load dataset
df = pd.read_csv('Final_Specialized_Dataset_Fixed.csv')

# Combine text columns
df['combined_text'] = (
    df['User_Skills'].fillna('') + ' ' +
    df['Job_Requirements'].fillna('')
)

# Group by role
role_df = df.groupby('Job_Role')['combined_text'].apply(lambda x: ' '.join(x)).reset_index()

# TF-IDF
v = TfidfVectorizer(stop_words='english')
tfidf_matrix = v.fit_transform(role_df['combined_text'])

# Extract text from PDF
def extract_text_from_pdf(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text   # <-- moved outside loop

# Recommendation function
def recommend_job(text, top_n=5):
    user_vector = v.transform([text])
    sim_scores = cosine_similarity(user_vector, tfidf_matrix).flatten()
    sim_series = pd.Series(sim_scores)
    top_indices = sim_series.sort_values(ascending=False).head(top_n).index
    return role_df.iloc[top_indices][['Job_Role']]


