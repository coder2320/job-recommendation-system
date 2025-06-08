# utils/parser.py

import pdfplumber
import spacy

nlp = spacy.load("en_core_web_sm")

SKILL_KEYWORDS = [
    'python', 'java', 'c++', 'sql', 'excel', 'machine learning', 'deep learning',
    'nlp', 'flask', 'django', 'aws', 'azure', 'react', 'nodejs', 'html', 'css',
    'javascript', 'pandas', 'numpy', 'data analysis'
]

def extract_text_from_pdf(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text

def extract_skills(text):
    text = text.lower()
    found_skills = [skill for skill in SKILL_KEYWORDS if skill.lower() in text]
    return list(set(found_skills))
