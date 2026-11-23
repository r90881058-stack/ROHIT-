import re
import pdfplumber
import spacy

nlp = spacy.load("en_core_web_sm")

SKILL_KEYWORDS = {
    'python', 'java', 'c++', 'sql', 'javascript', 'react', 'node.js', 
    'flask', 'django', 'spacy', 'machine learning', 'aws', 'docker', 'postgresql'
}

EDU_KEYWORDS = ['bachelor', 'master', 'phd', 'b.s.', 'b.a.', 'm.s.', 'university', 'college', 'institute']

def extract_text_from_pdf(file_path):
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + "\n"
    return text

def parse_resume(text):
    doc = nlp(text)
    
    email_match = re.search(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', text)
    email = email_match.group(0) if email_match else None
    
    phone_match = re.search(r'\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}', text)
    phone = phone_match.group(0) if phone_match else None
    
    name = None
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            name = ent.text.strip()
            break
            
    text_lower = text.lower()
    found_skills = [skill for skill in SKILL_KEYWORDS if skill in text_lower]
    
    education_lines = []
    for sent in doc.sents:
        if any(edu_word in sent.text.lower() for edu_word in EDU_KEYWORDS):
            education_lines.append(sent.text.strip().replace('\n', ' '))
    
    return {
        "name": name,
        "email": email,
        "phone": phone,
        "skills": ", ".join(found_skills) if found_skills else None,
        "education": " | ".join(education_lines[:3]) if education_lines else None
    }
