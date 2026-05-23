# AI Resume Analyzer 🔥

AI Resume Analyzer is a modern Flask-based web application that analyzes uploaded resume PDFs using Python and basic NLP techniques. The system extracts technical and soft skills, compares resumes with selected job roles, calculates ATS compatibility score, identifies missing skills, and generates AI-based improvement suggestions through an interactive dashboard interface.

---

## 🚀 Features

* Resume PDF Upload
* PDF Text Extraction using PyPDF2
* Technical & Soft Skill Detection
* ATS Score Calculation
* Job Role Matching
* Missing Skill Identification
* AI-Based Suggestions
* Modern Dark UI Dashboard
* Responsive Design
* Drag & Drop Resume Upload

---

## 🛠 Technologies Used

### Backend

* Python
* Flask

### Frontend

* HTML5
* CSS3
* JavaScript

### Libraries & Tools

* PyPDF2
* Regex
* NLP-based Keyword Matching
* Bootstrap
* Font Awesome

---

## 📌 Supported Job Roles

* Python Developer
* AI Engineer
* Data Analyst
* Web Developer
* Software Developer
* Machine Learning Intern
* Cybersecurity Intern

---

## ⚡ How It Works

1. User uploads resume PDF
2. System extracts text from resume
3. Skills are detected using NLP-based keyword matching
4. Resume skills are compared with selected job role
5. ATS score and match percentage are calculated
6. Missing skills and improvement suggestions are generated
7. Results are displayed on dashboard

---

## 📂 Project Structure

```text
AI-Resume-Analyzer/
│
├── app.py
├── requirements.txt
│
├── uploads/
│
├── static/
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── script.js
│
├── templates/
│   ├── index.html
│   └── result.html
│
└── utils/
    ├── skill_extractor.py
    ├── matcher.py
    └── __init__.py
```

---

## ▶️ Installation

### Clone Repository

```bash
git clone https://github.com/yourusername/AI-Resume-Analyzer.git
```

### Open Project Folder

```bash
cd AI-Resume-Analyzer
```

### Create Virtual Environment

```bash
python -m venv .venv
```

### Activate Virtual Environment

#### Windows

```bash
.venv\Scripts\activate
```

### Install Dependencies

```bash
pip install flask PyPDF2 spacy werkzeug
```

### Download NLP Model

```bash
python -m spacy download en_core_web_sm
```

### Run Application

```bash
python app.py
```

---

## 🌐 Open in Browser

```text
http://127.0.0.1:5000
```

---

## 📊 Main Functionalities

* Resume Parsing
* Skill Extraction
* ATS Compatibility Analysis
* Job Skill Matching
* Resume Strength Analysis
* Suggestion Generation

---

## 🔥 Future Improvements

* OpenAI API Integration
* Advanced NLP Models
* Resume Ranking System
* AI Chatbot Assistant
* Resume Template Generator
* Recruiter Dashboard
* Cloud Deployment

---

## 👩‍💻 Author

**Hajara Abbas**
BCA Artificial Intelligence Student

---

## ⭐ GitHub Repository Description

```text
AI-powered Resume Analyzer using Python Flask and NLP for ATS scoring, skill extraction, and job-role matching.
```

---

## 📌 Tags

```text
python flask nlp ai resume-analyzer machine-learning web-development ats
```
