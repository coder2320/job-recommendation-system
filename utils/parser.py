# utils/parser.py

import pdfplumber
import spacy

nlp = spacy.load("en_core_web_sm")

SKILL_KEYWORDS = [
    'python', 'java', 'sql', 'machine learning', 'deep learning',
    'django', 'flask', 'react', 'aws', 'nlp', 'excel', 'pandas', 'data analysis'
]

def extract_text_from_pdf(file):
    try:
        text = ""
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        return text
    except Exception:
        return None

def extract_skills(text):
    if not text:
        return []
    text = text.lower()
    return list({skill for skill in SKILL_KEYWORDS if skill in text})
