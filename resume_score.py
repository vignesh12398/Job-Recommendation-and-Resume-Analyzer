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

    return total_score, scores





def resume_suggestions(resume_text):

    text = resume_text.lower()
    tips = []

    # Skills
    skills = ["machine learning","deep learning","neural networks","computer vision",
"nlp","natural language processing","reinforcement learning",
"transformers","pytorch","tensorflow","keras","scikit-learn",
"xgboost","lightgbm","opencv","huggingface","llm","gpt","pandas","numpy","matplotlib","seaborn","data analysis",
"data visualization","statistics","tableau","power bi",
"excel","data mining","feature engineering","data wrangling","html","css","javascript","react","angular","vue",
"node.js","express","django","flask","spring boot",
"rest api","graphql","bootstrap","tailwind","docker","kubernetes","aws","azure","gcp",
"linux","git","github","gitlab","ci/cd",
"jenkins","terraform","ansible"]

    found_skills = [skill for skill in skills if skill in text]

    if len(found_skills) < 5:
        tips.append("Add more technical skills relevant to your field (at least 5 skills recommended)")

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
        "git", "github", "gitlab",
        "docker", "kubernetes",
        "aws", "azure", "gcp",
        "linux", "ubuntu",
        "jupyter", "google colab",
        "vscode", "visual studio code",
        "pycharm", "intellij",
        "eclipse", "postman",
        "figma", "tableau", "power bi",
        "excel", "notion"
    ]

    found_tools = [tool for tool in tools if tool in text]

    if len(found_tools) < 2:
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
        "problem solving", "teamwork", "communication", "leadership", "project management"
    ]
    found_keywords = [k for k in keywords if k in text]

    if len(found_keywords) < 2:
        tips.append("Add domain-specific keywords for better ATS matching")


    return tips
