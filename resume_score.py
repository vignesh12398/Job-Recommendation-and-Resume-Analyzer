import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import Ridge
def predict_score(resume_text):
    text = resume_text.lower()

    df = pd.read_csv("Final_Fixed_Dataset.csv")
    df['text'] = df['User_Skills'] + " " + df['Job_Requirements'] + " " + df['Projects'] + " " + df['Certifications']
    df['Score'] = df['text'].apply(resume_score)
    df['Score'] = (df['Score'] / df['Score'].max()) * 100
    df['text'] = df['text'].fillna("")
    df['text'] = df['text'].astype(str)
    v = TfidfVectorizer(stop_words='english', max_features=3000, min_df=2, ngram_range=(1, 2))
    X = df['text']
    y = df['Score']
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
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
    scores={
        "skills": 0,
        "projects": 0,
        "experience": 0,
        "education": 0,
        "tools": 0,
        "certifications": 0,
        "structure": 5
    }
    skills=["python","java","c++","machine learning","deep learning",
              "tensorflow","pytorch","sql","pandas","numpy","css","javascript","mongodb","devops","node.js","next.js","react"
            "flaskApi","django","sickit-learn"]
    skills_count=sum(1 for skill in skills if skill in text)
    scores['skills']=min(skills_count*3,30)
    if "project" in text or "projects" in text:
        project_count=text.count("project")
        scores['projects']=min(project_count*5,20)
    if "experience" in text or "internship" in text:
        scores['experience']+=10
    education_keywords = ["btech", "bachelor", "degree", "university", "college"]
    if any(word in text for word in education_keywords):
        scores["education"] = 10
    tools=["git","streamit","docker","linux","aws","jupyter","kubernetes","VS Code","mysql","mongodb","Postman"]
    tools_count=sum(1 for tool in tools if tool in text)
    scores['tools']=min(tools_count*2,10)
    if "certification" in text or "coursera" in text or "certificate" in text:
        scores["certifications"] = 5

    total_score = sum(scores.values())

    return total_score


def detect_domain(text):
    text = text.lower()

    mech = ["cad", "solidworks", "thermodynamics", "ansys"]
    civil = ["autocad", "structural", "construction"]
    elec = ["circuits", "matlab", "embedded"]
    cse = ["python", "ml", "react", "django"]

    if any(k in text for k in mech):
        return "mechanical"
    elif any(k in text for k in civil):
        return "civil"
    elif any(k in text for k in elec):
        return "electrical"
    elif any(k in text for k in cse):
        return "cse"
    return "general"



def resume_suggestions(resume_text):

    text = resume_text.lower()
    tips = []
    domain = detect_domain(text)
    # Skills
    skills = [

# ---------- CSE / AI ----------
"machine learning","deep learning","neural networks","computer vision",
"nlp","natural language processing","reinforcement learning",
"transformers","pytorch","tensorflow","keras","scikit-learn",
"xgboost","lightgbm","opencv","huggingface","llm","gpt",
"pandas","numpy","matplotlib","seaborn","data analysis",
"data visualization","statistics","tableau","power bi",
"excel","data mining","feature engineering","data wrangling",

# ---------- Web / Software ----------
"html","css","javascript","react","angular","vue",
"node.js","express","django","flask","spring boot",
"rest api","graphql","bootstrap","tailwind",

# ---------- DevOps / Tools ----------
"docker","kubernetes","aws","azure","gcp",
"linux","git","github","gitlab","ci/cd",
"jenkins","terraform","ansible",

# ---------- Mechanical ----------
"cad","solidworks","catia","ansys","thermodynamics",
"heat transfer","fluid mechanics","manufacturing",
"machine design","automotive","hvac",

# ---------- Civil ----------
"autocad","staad pro","structural analysis","surveying",
"construction","geotechnical","transportation engineering",
"concrete technology","site engineering",

# ---------- Electrical / ECE ----------
"circuits","matlab","simulink","embedded systems",
"microcontrollers","pcb design","power systems",
"control systems","vlsi","verilog","digital electronics"
]

    found_skills = [skill for skill in skills if skill in text]

    if len(found_skills) < 5:
        if domain == "mechanical":
            tips.append("Add skills like CAD, SolidWorks, Thermodynamics, ANSYS")
        elif domain == "civil":
            tips.append("Add skills like AutoCAD, Structural Analysis, Surveying")
        elif domain == "electrical":
            tips.append("Add skills like Circuits, MATLAB, Embedded Systems")
        else:
            tips.append("Add more technical skills relevant to your field")


    # Projects
    if "project" not in text:
        tips.append("Include 2-3 strong projects to showcase practical experience")

    # Experience
    if "internship" not in text and "experience" not in text:
        tips.append("Add internship or work experience if available")

    # GitHub
    if "github" not in text:
        tips.append("Add your GitHub profile to show your projects")

    # Tools
    tools = [

# ---------- CSE / Dev ----------
"git", "github", "gitlab",
"docker", "kubernetes",
"aws", "azure", "gcp",
"linux", "ubuntu",
"jupyter", "google colab",
"vscode", "visual studio code",
"pycharm", "intellij",
"eclipse", "postman",
"figma", "tableau", "power bi",
"excel", "notion",

# ---------- Mechanical ----------
"solidworks", "catia", "ansys",
"autodesk inventor", "fusion 360",
"nx cad", "creo",

# ---------- Civil ----------
"autocad", "staad pro", "etabs",
"revit", "primavera", "arcgis",

# ---------- Electrical / ECE ----------
"matlab", "simulink",
"proteus", "multisim",
"pspice", "altium",
"ltspice"
]

    found_tools = [tool for tool in tools if tool in text]

    if len(found_tools) < 2:
        if domain == "mechanical":
            tips.append("Mention tools like SolidWorks, ANSYS, or CAD software")
        elif domain == "civil":
            tips.append("Mention tools like AutoCAD, STAAD Pro, or Revit")
        elif domain == "electrical":
            tips.append("Mention tools like MATLAB, Simulink, or PCB tools")
        else:
            tips.append("Mention tools like Git, Docker, Linux, or Cloud platforms")



    # Keywords
    keywords = [

        # Programming
        "python", "java", "c", "c++", "c#", "javascript", "typescript", "go", "rust", "ruby", "php", "swift", "kotlin",
        "scala", "matlab", "r",

        # Data Science & ML
        "machine learning", "deep learning", "data science", "data analysis", "data mining", "data visualization",
        "statistics", "predictive modeling", "feature engineering", "model evaluation", "model training",
        "hyperparameter tuning", "nlp", "natural language processing", "computer vision",
        "reinforcement learning", "neural networks", "cnn", "rnn", "transformers",

        # ML Frameworks
        "tensorflow", "pytorch", "keras", "scikit-learn", "xgboost", "lightgbm", "huggingface",

        # Data Tools
        "pandas", "numpy", "matplotlib", "seaborn", "plotly", "excel", "tableau", "power bi",

        # Web Development
        "html", "css", "javascript", "react", "angular", "vue", "node.js", "express", "django", "flask",
        "rest api", "graphql", "bootstrap", "tailwind",

        # Databases
        "sql", "mysql", "postgresql", "mongodb", "redis", "sqlite", "oracle", "firebase", "neo4j", "cassandra",

        # DevOps & Cloud
        "docker", "kubernetes", "aws", "azure", "gcp", "linux", "ubuntu",
        "git", "github", "gitlab", "jenkins", "terraform", "ansible",
        "ci/cd", "continuous integration", "continuous deployment",

        # Big Data
        "hadoop", "spark", "pyspark", "kafka", "hive", "flink", "mapreduce",

        # Software Engineering
        "data structures", "algorithms", "object oriented programming",
        "system design", "microservices", "api development",
        "software development lifecycle", "unit testing", "debugging",

        # Tools
        "visual studio code", "vscode", "pycharm", "jupyter", "google colab",
        "intellij", "eclipse", "postman", "figma", "notion",

        # AI modern keywords
        "artificial intelligence", "generative ai", "llm", "gpt", "prompt engineering",

        # Professional keywords
        "problem solving", "teamwork", "communication", "leadership", "project management",
        # ---------- Mechanical ----------
        "cad", "solidworks", "catia", "ansys", "creo",
        "thermodynamics", "heat transfer", "fluid mechanics",
        "machine design", "manufacturing", "automotive",
        "hvac", "cnc", "production engineering",
        
        # ---------- Civil ----------
        "autocad", "staad pro", "etabs", "revit",
        "structural analysis", "surveying", "construction",
        "geotechnical engineering", "transportation engineering",
        "concrete technology", "site engineering",
        
        # ---------- Electrical / ECE ----------
        "circuits", "digital electronics", "analog electronics",
        "embedded systems", "microcontrollers",
        "matlab", "simulink",
        "power systems", "control systems",
        "vlsi", "verilog", "fpga",
        "pcb design", "signal processing"
    ]
    found_keywords = [k for k in keywords if k in text]

    if len(found_keywords) < 2:
        if domain == "mechanical":
            tips.append("Add keywords like CAD, Thermodynamics, Manufacturing")
        elif domain == "civil":
            tips.append("Add keywords like Structural Analysis, Construction")
        elif domain == "electrical":
            tips.append("Add keywords like Circuits, Embedded Systems")
        else:
            tips.append("Add domain-specific keywords for better ATS matching")


    return tips
