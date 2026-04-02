# 💼 Job Recommendation & Resume Analyzer

An ** Job Recommendation and Resume Analysis system** built using Python, Machine Learning, and Streamlit.

The system analyzes resumes or user-entered skills to:

* Predict the most suitable career role
* Recommend top matching jobs
* Evaluate resume quality
* Provide ATS improvement suggestions
* 📊 Analyze real-time job market trends

👉 **Live App:**
https://job-recommendation-and-resume-analyzer-ndvbujlwjxqp8nz5jkujtp.streamlit.app/

---

# 🚀 Features

## 1️⃣ Career Role Prediction

Predicts the most suitable job role based on skills or resume text using:

* TF-IDF Vectorization
* Logistic Regression

Displays model confidence score.

---

## 2️⃣ Job Recommendation System

Recommends **Top 5 relevant job roles** using:

* TF-IDF
* Cosine Similarity

Matches resume content with job dataset.

---

## 3️⃣ Resume Analyzer

Evaluates resume quality using ML model ridge and tf-idf and generates a **score out of 100** based on:

* Skills
* Projects
* Experience
* Education
* Tools
* Certifications
* Resume structure
---

## 4️⃣ ATS Improvement Suggestions

Provides suggestions like:

* Add more technical skills
* Include projects
* Add GitHub profile
* Mention tools like Docker, Git, Cloud
* Improve ATS keywords

---

## 5️⃣ 📊 Job Market Trends (NEW 🔥)

Analyzes real-world demand for job roles using **Google Trends (Pytrends)**:

* Enter any job role (e.g., AI Engineer, Data Scientist)
* Displays **trend graph over last 12 months**
* Shows market direction:

  * 📈 Increasing
  * 📉 Decreasing
  * ➖ Stable

👉 Includes:

* Smart trend direction detection
* Fallback mechanism (prevents API failure crashes)
* Real-time visualization using Streamlit

---

# 🧠 Machine Learning Techniques

| Technique            | Purpose                            |
| -------------------- | ---------------------------------- |
| TF-IDF Vectorization | Convert text to numerical features |
| Logistic Regression  | Career role prediction             |
| Cosine Similarity    | Job recommendation                 |
| NLP                  | Resume analysis                    |
| Pytrends             | Job market trend analysis          |

---

# 📁 Project Structure

```
Job-Recommendation-System
│
├── app.py
├── prediction.py
├── helper.py
├── resume_score.py
├── trend.py
├── main.py
├── requirements.txt
├── README.md
└── dataset
      └── Expanded_Roles_Job_Dataset.csv
```

---

# 📊 Dataset

The dataset contains:

* User_Skills
* Job_Requirements
* Job_Role

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

```bash
streamlit run app.py
```

Open in browser:

```
http://localhost:8501
```

---

# 📂 Application Pages

* 📄 Resume Analyzer
* 🧠 Career Prediction
* 💼 Job Recommendation
* 📊 Job Market Trends

---

# 🛠 Tech Stack

* Python
* Scikit-learn
* Streamlit
* Pandas
* NumPy
* PyPDF2
* TF-IDF
* Cosine Similarity
* Pytrends (Google Trends API)

---



# 👨‍💻 Author

**Vignesh Balaji**
BTech AIML Student

Interested in:

* Artificial Intelligence
* Machine Learning
