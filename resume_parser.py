import fitz  # PyMuPDF for PDF parsing
import docx
import os
import re

# Master skills dictionary 
SKILLS_DICTIONARY = [
    # Programming Languages
    "python", "java", "javascript", "typescript", "c++", "c#", "r", "scala",
    "ruby", "php", "swift", "kotlin", "go", "rust", "matlab",

    # Data & ML
    "machine learning", "deep learning", "natural language processing", "nlp",
    "computer vision", "tensorflow", "pytorch", "keras", "scikit-learn",
    "pandas", "numpy", "matplotlib", "seaborn", "xgboost", "lightgbm",

    # Data & Analytics
    "sql", "mysql", "postgresql", "mongodb", "sqlite", "oracle",
    "power bi", "tableau", "excel", "data analysis", "data visualization",
    "statistics", "data mining", "etl", "data warehousing", "hadoop", "spark",

    # Web & Backend
    "flask", "django", "fastapi", "rest api", "html", "css", "react",
    "node.js", "express", "spring boot", "graphql",

    # Cloud & DevOps
    "aws", "azure", "google cloud", "docker", "kubernetes", "ci/cd",
    "linux", "git", "terraform", "jenkins", "airflow",

    # Business & Finance
    "finance", "accounting", "budgeting", "forecasting", "sap",
    "business analysis", "project management", "agile", "scrum",
    "a/b testing", "market research",

    # Soft Skills
    "communication", "leadership", "problem solving", "teamwork",
    "critical thinking", "time management"
]


def extract_text_from_pdf(file_path):
    """Extract all text from a PDF file."""
    text = ""
    try:
        doc = fitz.open(file_path)
        for page in doc:
            text += page.get_text()
        doc.close()
    except Exception as e:
        print(f" Error reading PDF: {e}")
    return text


def extract_text_from_docx(file_path):
    """Extract all text from a Word (.docx) file."""
    text = ""
    try:
        doc = docx.Document(file_path)
        for paragraph in doc.paragraphs:
            text += paragraph.text + " "
    except Exception as e:
        print(f" Error reading DOCX: {e}")
    return text


def extract_text_from_resume(file_path):
    """
    Detect file type and extract text accordingly.
    Supports PDF and DOCX formats.
    """
    _, extension = os.path.splitext(file_path)
    extension = extension.lower()

    if extension == ".pdf":
        return extract_text_from_pdf(file_path)
    elif extension == ".docx":
        return extract_text_from_docx(file_path)
    else:
        return ""


def extract_skills_from_text(text):
    """
    Match extracted resume text against the skills dictionary.
    Returns a comma-separated string of found skills.
    """
    text_lower = text.lower()
    found_skills = []

    for skill in SKILLS_DICTIONARY:
        # Use word boundary matching to avoid partial matches
        pattern = r'\b' + re.escape(skill) + r'\b'
        if re.search(pattern, text_lower):
            found_skills.append(skill.title())  # Capitalize for display

    # Remove duplicates while preserving order
    seen = set()
    unique_skills = []
    for skill in found_skills:
        if skill.lower() not in seen:
            seen.add(skill.lower())
            unique_skills.append(skill)

    return ", ".join(unique_skills)


def parse_resume(file_path):
    """
    Main function: extract text from resume and return found skills.

    Returns:
        dict with 'skills' (str) and 'raw_text_preview' (str)
    """
    raw_text = extract_text_from_resume(file_path)

    if not raw_text.strip():
        return {"skills": "", "raw_text_preview": "", "error": "Could not extract text from resume."}

    skills = extract_skills_from_text(raw_text)

    return {
        "skills": skills,
        "raw_text_preview": raw_text[:500],  # First 500 chars for debugging
        "error": None
    }


# Test directly
if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        result = parse_resume(sys.argv[1])
        print(f"Extracted Skills: {result['skills']}")
    else:
        print("Usage: python resume_parser.py your_resume.pdf")
        