# Resume Analyzer

Resume Analyzer is a Streamlit project made for placement preparation. The app takes a resume PDF and a job description, then compares them using simple text processing. It shows an ATS score, a basic ATS health score, skill gap analysis, and short recommendations.

The project is intentionally kept small so it is easy to explain in a viva or interview.

## Project Overview

This project helps a user check how well a resume matches a job description before applying for a role. It does not try to replace a real ATS system. It only gives a basic idea of how much of the job description is reflected in the resume and whether the resume contains common sections like skills, projects, education, and experience.

The main output includes:

- ATS Score
- ATS Health Score
- Required Skills
- Skills Found
- Missing Skills
- Recommendations

## Motivation

I built this project because resume screening is a common problem during placement season. Many students do not know why their resume is getting filtered out. A basic analyzer like this can help identify missing keywords and missing resume sections before the resume is submitted.

I also wanted to make something realistic for a final-year Computer Science project. So I kept the logic rule based, used a small number of dependencies, and avoided AI models or advanced backend systems.

## Features

- Upload a resume in PDF format
- Paste a job description
- Calculate ATS score using TF-IDF and cosine similarity
- Extract skills from a predefined skills dictionary
- Show skill gap analysis
- Check whether the resume has basic ATS-friendly sections
- Show a simple recommendation message based on the result
- Display the result in a clean Streamlit interface

## Tech Stack

- Python
- Streamlit
- PyPDF2
- scikit-learn
- Regular expressions (`re`)

## Folder Structure

```text
Resume_Analyzer/
├── app.py
├── DEPLOYMENT.md
├── README.md
├── requirements.txt
└── resume_analyzer/
    ├── __init__.py
    ├── ats_health_checker.py
    ├── keyword_matching.py
    ├── pdf_utils.py
    ├── preprocessing.py
    ├── recommendation_engine.py
    └── scoring.py
```

## How It Works

1. The user uploads a PDF resume.
2. The app extracts text from the PDF using `PyPDF2`.
3. The text is cleaned using a simple preprocessing step.
4. The job description and resume are compared using TF-IDF and cosine similarity.
5. A predefined skills dictionary is used to find required skills in the job description and matched skills in the resume.
6. The app calculates the missing skills by comparing both lists.
7. A separate rule-based ATS health checker looks for email, phone number, skills, projects, education, and experience sections.
8. The app shows the final result in Streamlit using score cards, progress bars, and simple text blocks.

### Main Logic Used

- ATS score: TF-IDF + cosine similarity
- Skill gap analysis: predefined skills dictionary + keyword matching
- ATS health check: regular expressions and section-name matching
- Recommendation engine: rule-based messages based on score and missing skills

## How To Run

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Limitations

- The project works best with text-based PDF resumes. Scanned PDFs may not work properly.
- The skills list is based on a predefined dictionary, so it can miss skills that are not included.
- The ATS health checker only checks for basic patterns, not the actual quality of the resume content.
- The similarity score is based on text matching, so it does not fully represent how a real ATS system works.
- The project does not check design formatting, font quality, or page layout.

## Future Improvements

- Add support for scanned PDFs using OCR
- Expand the skills dictionary with more domain-specific skills
- Add category-wise skill gap breakdown
- Add an export option for the analysis report
- Add sample resumes and job descriptions for testing
- Improve the UI with a more structured summary panel
- Add automated tests for PDF extraction, skill matching, and scoring

## Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for Streamlit Community Cloud deployment steps and common issues.
