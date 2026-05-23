"""
matcher.py
----------
Compares extracted resume skills against predefined job-role requirements
and produces a match score, missing skills list, and improvement suggestions.
"""

# ─── Job Role → Required Skills ─────────────────────────────────────────────

JOB_ROLES = {
    "AI Engineer": [
        "Python", "Machine Learning", "Deep Learning", "Tensorflow",
        "Pytorch", "Numpy", "Pandas", "Scikit-Learn", "Nlp",
        "Data Analysis", "Git", "Github", "Rest Api",
    ],
    "Python Developer": [
        "Python", "Flask", "Django", "Sql", "Git", "Github",
        "Rest Api", "Numpy", "Pandas", "Html", "Css", "Javascript",
    ],
    "Data Analyst": [
        "Python", "Sql", "Data Analysis", "Pandas", "Numpy",
        "Matplotlib", "Excel", "Power Bi", "Tableau", "Data Visualization",
    ],
    "Web Developer": [
        "Html", "Css", "Javascript", "React", "Node.Js",
        "Sql", "Git", "Github", "Rest Api", "Bootstrap",
    ],
    "Software Developer": [
        "Python", "Java", "C++", "Sql", "Git", "Github",
        "Data Structures", "Algorithms", "Rest Api", "Linux",
    ],
    "Cybersecurity Intern": [
        "Networking", "Cybersecurity", "Linux", "Python",
        "Ethical Hacking", "Penetration Testing", "Git",
    ],
    "Machine Learning Intern": [
        "Python", "Machine Learning", "Scikit-Learn", "Numpy",
        "Pandas", "Matplotlib", "Git", "Github", "Data Analysis",
    ],
}


def get_all_roles() -> list:
    """Return list of all available job roles."""
    return list(JOB_ROLES.keys())


def calculate_match(extracted_skills: list, job_role: str) -> dict:
    """
    Compare resume skills with required skills for a role.

    Parameters
    ----------
    extracted_skills : list[str]   Skills pulled from the resume (title-cased)
    job_role         : str         One of the keys in JOB_ROLES

    Returns
    -------
    dict with:
        score          : int   (0-100)
        matched        : list[str]
        missing        : list[str]
        required       : list[str]
        grade          : str   (Excellent / Good / Average / Needs Improvement)
        grade_color    : str   CSS colour token
    """
    required = JOB_ROLES.get(job_role, [])
    if not required:
        return _empty_result()

    # Normalise to lowercase for comparison
    extracted_lower = {s.lower() for s in extracted_skills}
    required_lower  = [r.lower() for r in required]

    matched = [r for r in required_lower if r in extracted_lower]
    missing = [r for r in required_lower if r not in extracted_lower]

    score = round((len(matched) / len(required)) * 100) if required else 0

    grade, grade_color = _grade(score)

    return {
        "score": score,
        "matched": [r.title() for r in matched],
        "missing": [r.title() for r in missing],
        "required": required,
        "grade": grade,
        "grade_color": grade_color,
    }


def _grade(score: int):
    if score >= 80:
        return "Excellent", "success"
    elif score >= 60:
        return "Good", "info"
    elif score >= 40:
        return "Average", "warning"
    else:
        return "Needs Improvement", "danger"


def _empty_result():
    return {
        "score": 0,
        "matched": [],
        "missing": [],
        "required": [],
        "grade": "Unknown",
        "grade_color": "secondary",
    }


def generate_suggestions(match_result: dict, sections: dict, contact: dict) -> list:
    """
    Produce tailored improvement suggestions based on analysis results.
    """
    suggestions = []
    score = match_result["score"]
    missing = match_result["missing"]

    # ── Score-based ────────────────────────────────────────────────
    if score < 50:
        suggestions.append({
            "icon": "fa-rocket",
            "color": "danger",
            "title": "Boost Your Skill Match",
            "text": f"Your resume matches only {score}% of required skills. Focus on learning the missing technologies.",
        })

    # ── Missing skills ─────────────────────────────────────────────
    if missing:
        top3 = ", ".join(missing[:3])
        suggestions.append({
            "icon": "fa-graduation-cap",
            "color": "warning",
            "title": "Learn Missing Skills",
            "text": f"Prioritise these skills: {top3}. Add projects or certifications that demonstrate them.",
        })

    # ── Sections ───────────────────────────────────────────────────
    if not sections.get("projects"):
        suggestions.append({
            "icon": "fa-code",
            "color": "primary",
            "title": "Add Technical Projects",
            "text": "Include 2–3 personal or academic projects with GitHub links, tech stack, and your impact.",
        })

    if not sections.get("certifications"):
        suggestions.append({
            "icon": "fa-certificate",
            "color": "info",
            "title": "Mention Certifications",
            "text": "Add relevant online certifications (Coursera, Udemy, Google) to strengthen credibility.",
        })

    if not sections.get("github"):
        suggestions.append({
            "icon": "fa-github",
            "color": "dark",
            "title": "Include Your GitHub Profile",
            "text": "Add a GitHub URL so recruiters can review your code quality and activity.",
        })

    if not sections.get("achievements"):
        suggestions.append({
            "icon": "fa-trophy",
            "color": "warning",
            "title": "Add Measurable Achievements",
            "text": 'Quantify your impact. E.g., "Improved model accuracy by 15%" or "Built a chatbot used by 200+ users".',
        })

    if not sections.get("experience"):
        suggestions.append({
            "icon": "fa-briefcase",
            "color": "secondary",
            "title": "Add Internship or Work Experience",
            "text": "Even short internships or part-time work significantly improve your profile.",
        })

    if not contact.get("email"):
        suggestions.append({
            "icon": "fa-envelope",
            "color": "danger",
            "title": "Add Contact Information",
            "text": "Make sure your email address is clearly listed on the resume.",
        })

    # ── Generic formatting ─────────────────────────────────────────
    suggestions.append({
        "icon": "fa-file-alt",
        "color": "primary",
        "title": "Improve Resume Formatting",
        "text": "Keep your resume to 1 page, use clean fonts, consistent spacing, and ATS-friendly structure.",
    })

    return suggestions


def ats_score(raw_text: str, sections: dict, contact: dict) -> int:
    """
    Simple ATS (Applicant Tracking System) compatibility score.
    Checks for common ATS-friendly elements.
    """
    score = 40  # base

    if contact.get("email"):   score += 10
    if contact.get("phone"):   score += 5
    if contact.get("linkedin"): score += 5
    if sections.get("education"):      score += 8
    if sections.get("experience"):     score += 10
    if sections.get("projects"):       score += 8
    if sections.get("certifications"): score += 7
    if sections.get("github"):         score += 7

    return min(score, 100)
