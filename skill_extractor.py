"""
skill_extractor.py
------------------
Extracts technical and soft skills from resume text using keyword matching.
"""

import re

# ─── Master Skill Database ──────────────────────────────────────────────────

TECHNICAL_SKILLS = [
    "python", "java", "c++", "c#", "c", "sql", "html", "css",
    "javascript", "typescript", "flask", "django", "react", "angular",
    "vue", "node.js", "nodejs", "express", "machine learning", "deep learning",
    "artificial intelligence", "nlp", "natural language processing",
    "data analysis", "data science", "data visualization", "tensorflow",
    "pytorch", "keras", "scikit-learn", "pandas", "numpy", "matplotlib",
    "git", "github", "docker", "kubernetes", "aws", "azure", "gcp",
    "linux", "networking", "cybersecurity", "ethical hacking",
    "penetration testing", "rest api", "apis", "mongodb", "postgresql",
    "mysql", "sqlite", "firebase", "excel", "power bi", "tableau",
    "r", "php", "ruby", "swift", "kotlin", "hadoop", "spark",
    "opencv", "blockchain", "iot", "cloud computing",
]

SOFT_SKILLS = [
    "communication", "teamwork", "problem solving", "leadership",
    "time management", "critical thinking", "adaptability",
    "creativity", "collaboration", "project management",
    "attention to detail", "analytical thinking", "self motivated",
]

ALL_SKILLS = TECHNICAL_SKILLS + SOFT_SKILLS


def clean_text(text: str) -> str:
    """Lowercase, remove special chars, normalise whitespace."""
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s\.\+\#]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def extract_skills(raw_text: str) -> dict:
    """
    Scan cleaned resume text for known skills.

    Returns
    -------
    dict with keys:
        technical  : list[str]
        soft       : list[str]
        all        : list[str]
    """
    text = clean_text(raw_text)

    found_technical = []
    found_soft = []

    for skill in TECHNICAL_SKILLS:
        # Use word-boundary match so "c" doesn't match inside "css"
        pattern = r"\b" + re.escape(skill) + r"\b"
        if re.search(pattern, text):
            found_technical.append(skill.title())

    for skill in SOFT_SKILLS:
        pattern = r"\b" + re.escape(skill) + r"\b"
        if re.search(pattern, text):
            found_soft.append(skill.title())

    return {
        "technical": found_technical,
        "soft": found_soft,
        "all": found_technical + found_soft,
    }


def extract_contact_info(raw_text: str) -> dict:
    """Extract email, phone, LinkedIn from resume text."""
    info = {"email": None, "phone": None, "linkedin": None}

    email_match = re.search(r"[\w\.-]+@[\w\.-]+\.\w+", raw_text)
    if email_match:
        info["email"] = email_match.group()

    phone_match = re.search(r"(\+?\d[\d\s\-]{8,14}\d)", raw_text)
    if phone_match:
        info["phone"] = phone_match.group().strip()

    linkedin_match = re.search(
        r"(linkedin\.com/in/[\w\-]+|linkedin\.com/[\w/]+)", raw_text, re.IGNORECASE
    )
    if linkedin_match:
        info["linkedin"] = linkedin_match.group()

    return info


def count_resume_sections(raw_text: str) -> dict:
    """Check which standard sections exist in the resume."""
    text = raw_text.lower()
    sections = {
        "education": bool(re.search(r"\beducation\b|\bdegree\b|\buniversity\b|\bcollege\b", text)),
        "experience": bool(re.search(r"\bexperience\b|\binternship\b|\bwork\b|\bjob\b", text)),
        "projects": bool(re.search(r"\bproject\b|\bprojects\b|\bbuilt\b|\bdeveloped\b", text)),
        "certifications": bool(re.search(r"\bcertif\b|\bcourse\b|\bcoursera\b|\budemy\b", text)),
        "achievements": bool(re.search(r"\bachievement\b|\baward\b|\bhonor\b|\brank\b", text)),
        "github": bool(re.search(r"\bgithub\b|\bgitlab\b", text)),
    }
    return sections
