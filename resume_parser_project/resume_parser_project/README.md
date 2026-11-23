# Automated Resume Parser

This is a Flask-based project that parses resumes (PDFs) and extracts key information (Name, Email, Phone, Skills, Education) using spaCy and pdfplumber. The extracted data is stored in a PostgreSQL database.

## Setup Instructions

1. Install PostgreSQL and create a database named `resume_db`.
2. Install the required Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Download the required spaCy model:
   ```bash
   python -m spacy download en_core_web_sm
   ```
4. Update the database connection string in `app.py` if necessary.
5. Run the application:
   ```bash
   python app.py
   ```

## Endpoints
- `POST /upload`: Upload a PDF resume (`file` form-data parameter).
- `GET /candidates`: Retrieve all parsed candidates.
- `GET /candidates?skill=python`: Retrieve candidates filtered by a specific skill.
