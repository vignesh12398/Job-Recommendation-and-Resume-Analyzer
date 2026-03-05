# 💼  Job Recommendation & Resume Analyzer

An ** Job Recommendation and Resume Analysis system** built using **Python, Machine Learning, and Streamlit**.  
The system analyzes resumes or user-entered skills to:

- Predict the **most suitable career role**
- Recommend **top matching jobs**
- Evaluate **resume quality**
- Provide **ATS improvement suggestions**

---
-open here-https://job-recommendation-and-resume-analyzer-ndvbujlwjxqp8nz5jkujtp.streamlit.app/

# 🚀 Features

## 1️⃣ Career Role Prediction
Predicts the most suitable **job role** based on skills or resume text using:

- TF-IDF Vectorization
- Logistic Regression

Displays **model confidence score**.

---

## 2️⃣ Job Recommendation System
Recommends **Top 5 relevant job roles** using:

- TF-IDF
- Cosine Similarity

Matches resume content with job dataset.

---

## 3️⃣ Resume Analyzer
Evaluates resume quality and generates a **score out of 100** based on:

- Skills
- Projects
- Experience
- Education
- Tools
- Certifications
- Resume structure

---

## 4️⃣ ATS Improvement Suggestions
Provides suggestions like:

- Add more technical skills
- Include projects
- Add GitHub profile
- Mention tools like Docker, Git, Cloud
- Improve ATS keywords

---

# 🧠 Machine Learning Techniques

| Technique | Purpose |
|--------|--------|
| TF-IDF Vectorization | Convert text to numerical features |
| Logistic Regression | Career role prediction |
| Cosine Similarity | Job recommendation |
| NLP | Resume analysis |

---

# 📁 Project Structure

```
Job-Recommendation-System
│
├── app.py
├── prediction.py
├── helper.py
├── resume_score.py
├── main.py
├── requirements.txt
├── README.md
└── dataset
      └── Expanded_Roles_Job_Dataset.csv
```

---

# 📊 Dataset

The dataset contains:

- **User_Skills**
- **Job_Requirements**
- **Job_Role**

These columns are combined to create training text for the ML models.

---

# ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/vignesh12398/job-recommendation-system.git
cd job-recommendation-system
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# ▶️ Run the Application

Run the Streamlit app:

```bash
streamlit run app.py
```

Open in browser:

```
http://localhost:8501
```

---

# 📂 Application Pages

## 📄 Resume Analyzer
- Resume score
- Breakdown of evaluation
- ATS suggestions

## 🧠 Career Prediction
- Predicts most suitable job role
- Shows model confidence

## 💼 Job Recommendation
- Shows top 5 job roles based on similarity

---

# 🛠 Tech Stack

- Python
- Scikit-learn
- Streamlit
- Pandas
- NumPy
- PyPDF2
- TF-IDF
- Cosine Similarity

---

# 🔮 Future Improvements

- Use **BERT / Transformers for better predictions**
- Add **real job data from LinkedIn / Indeed**
- Improve **resume ATS scoring**
- Deploy using **Docker + AWS**
- Add **resume skill extraction with NLP**

---

# 👨‍💻 Author

**Vignesh Balaji**  
BTech AIML Student

Interested in:
- Artificial Intelligence
- Machine Learning
- Building AI assistants like **Jarvis**

---

⭐ If you like this project, consider giving it a **star on GitHub!**
