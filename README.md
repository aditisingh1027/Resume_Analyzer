# Resume Analyzer

Resume Analyzer is a Streamlit project built for placement preparation. The app takes a resume PDF and a job description, then compares them using simple text processing. It shows an ATS score, ATS health score, skill gap analysis, and recommendations.

The application uses traditional text-processing techniques and does not rely on external APIs, making it lightweight, explainable, and easy to deploy.

## Project Overview

This project helps a user check how closely a resume matches a job description before applying for a role. It does not try to replace a real ATS system. It only gives a basic idea of the match score, missing skills, and whether the resume contains common sections like skills, projects, education, and experience.

The app focuses on placement preparation and basic resume review.

## Features

- Upload a resume in PDF format
- Extract text from the uploaded PDF
- Calculate ATS score using TF-IDF and cosine similarity
- Run ATS health checks for common resume fields
- Perform skill gap analysis using a predefined skills dictionary
- Show matched and missing skills
- Generate simple recommendations based on the analysis
- Display results in a clean Streamlit interface

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

## Installation

1. Clone or open the project folder in VS Code.
2. Create and activate a Python virtual environment.
3. Install the dependencies from `requirements.txt`.

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Usage

1. Start the Streamlit app.

```bash
streamlit run app.py
```

2. Upload a PDF resume.
3. Paste the job description.
4. Click the Analyze button.
5. Review the ATS score, ATS health score, skill gap analysis, and recommendations.

## Limitations

- The project works best with text-based PDF resumes. Scanned PDFs may not extract properly.
- The ATS score is only an approximation based on text similarity.
- Skill matching depends on a predefined dictionary, so some synonyms or related terms may be missed.
- ATS health checks are rule based and only check for basic resume sections and contact details.
- The project does not evaluate formatting quality, page design, or visual layout.

## Future Improvements

- Add OCR support for scanned resumes
- Expand the skills dictionary
- Export analysis reports
- Improve skill categorization
- Add automated tests for PDF extraction, scoring, and skill matching
