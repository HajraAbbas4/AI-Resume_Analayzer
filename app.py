"""
app.py — AI Resume Analyzer
============================
Main Flask application entry-point.

Run locally:
    pip install -r requirements.txt
    python app.py
"""

import os
import uuid

from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.utils import secure_filename
import PyPDF2

from utils.skill_extractor import extract_skills, extract_contact_info, count_resume_sections
from utils.matcher import calculate_match, generate_suggestions, get_all_roles, ats_score

# ─── App Configuration ───────────────────────────────────────────────────────

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "ai-resume-analyzer-secret-2024")

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "uploads")
ALLOWED_EXTENSIONS = {"pdf"}
MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5 MB limit

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = MAX_CONTENT_LENGTH

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# ─── Helpers ─────────────────────────────────────────────────────────────────

def allowed_file(filename: str) -> bool:
    """Return True if the file extension is in the allowed set."""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def extract_text_from_pdf(filepath: str) -> str:
    """Extract all text from a PDF file using PyPDF2."""
    text = ""
    try:
        with open(filepath, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        print(f"[PDF Error] {e}")
    return text


# ─── Routes ──────────────────────────────────────────────────────────────────

@app.route("/", methods=["GET"])
def index():
    """Home page — upload form."""
    roles = get_all_roles()
    return render_template("index.html", roles=roles)


@app.route("/analyze", methods=["POST"])
def analyze():
    """Handle resume upload + analysis pipeline."""

    # ── 1. Validate file ──────────────────────────────────────────
    if "resume" not in request.files:
        flash("No file selected. Please upload your resume.", "danger")
        return redirect(url_for("index"))

    file = request.files["resume"]
    job_role = request.form.get("job_role", "").strip()

    if file.filename == "":
        flash("Please select a PDF file to upload.", "warning")
        return redirect(url_for("index"))

    if not allowed_file(file.filename):
        flash("Only PDF files are accepted. Please upload a valid resume.", "danger")
        return redirect(url_for("index"))

    if not job_role:
        flash("Please select a target job role.", "warning")
        return redirect(url_for("index"))

    # ── 2. Save file ──────────────────────────────────────────────
    original_name = secure_filename(file.filename)
    unique_name   = f"{uuid.uuid4().hex}_{original_name}"
    filepath      = os.path.join(app.config["UPLOAD_FOLDER"], unique_name)
    file.save(filepath)

    # ── 3. Extract text ───────────────────────────────────────────
    raw_text = extract_text_from_pdf(filepath)

    if len(raw_text.strip()) < 50:
        flash("Could not extract text from the PDF. Please ensure it is not a scanned/image PDF.", "warning")
        os.remove(filepath)
        return redirect(url_for("index"))

    # ── 4. NLP analysis ───────────────────────────────────────────
    skills_data   = extract_skills(raw_text)
    contact_info  = extract_contact_info(raw_text)
    sections      = count_resume_sections(raw_text)
    match_result  = calculate_match(skills_data["all"], job_role)
    suggestions   = generate_suggestions(match_result, sections, contact_info)
    ats           = ats_score(raw_text, sections, contact_info)

    # ── 5. Resume strength (composite) ───────────────────────────
    strength = round((match_result["score"] * 0.5) + (ats * 0.3) + (min(len(skills_data["all"]), 15) / 15 * 20))

    # ── 6. Clean up uploaded file ─────────────────────────────────
    try:
        os.remove(filepath)
    except OSError:
        pass

    # ── 7. Render result ──────────────────────────────────────────
    return render_template(
        "result.html",
        filename=original_name,
        job_role=job_role,
        skills=skills_data,
        contact=contact_info,
        sections=sections,
        match=match_result,
        suggestions=suggestions,
        ats_score=ats,
        strength=strength,
        word_count=len(raw_text.split()),
    )


@app.errorhandler(413)
def file_too_large(e):
    flash("File too large. Maximum allowed size is 5 MB.", "danger")
    return redirect(url_for("index"))


@app.errorhandler(404)
def not_found(e):
    return render_template("index.html", roles=get_all_roles()), 404


# ─── Entry Point ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_ENV", "development") == "development"
    app.run(debug=debug, host="0.0.0.0", port=port)
