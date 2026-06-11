# Streamlit Community Cloud Deployment Guide

This project is ready for Streamlit Community Cloud because it has a single entry file, `app.py`, and a dependency list in `requirements.txt`.

## GitHub Repository Setup

1. Create a new GitHub repository for the project.
2. Push the full project folder to that repository.
3. Make sure these files are present at the repository root:
   - `app.py`
   - `requirements.txt`
   - `README.md`
4. Keep the repository public if you want easy deployment on Streamlit Community Cloud.
5. Confirm that the main app entry point is `app.py`.

## requirements.txt

The deployment file already contains the needed packages:

```text
streamlit>=1.35
PyPDF2>=3.0.1
scikit-learn>=1.4
```

Why this matters:

1. Streamlit Cloud installs dependencies from this file.
2. `PyPDF2` is needed for resume PDF extraction.
3. `scikit-learn` is needed for TF-IDF and cosine similarity.

## Deployment Steps

1. Open [Streamlit Community Cloud](https://share.streamlit.io/).
2. Sign in with your GitHub account.
3. Click "New app".
4. Select your GitHub repository.
5. Choose the branch, usually `main`.
6. Set the main file path to `app.py`.
7. Click "Deploy".
8. Wait for the build to finish.
9. Open the app URL once deployment is complete.

## Common Deployment Errors

### 1. `ModuleNotFoundError`
Cause: A required package is missing from `requirements.txt`.

Fix: Add the missing package to `requirements.txt` and redeploy.

### 2. `FileNotFoundError` or import path issues
Cause: The app is trying to import a file from the wrong path.

Fix: Keep `app.py` at the repository root and use package imports like `from resume_analyzer...`.

### 3. PDF upload works locally but fails online
Cause: The uploaded file object is not being handled correctly.

Fix: Make sure the code uses the uploaded Streamlit file object directly and resets the pointer with `seek(0)` before reading.

### 4. Build fails during installation
Cause: A dependency version is incompatible or a package is missing.

Fix: Use simple version pins and keep the dependency list small.

### 5. App deploys but shows an error on the page
Cause: A runtime exception occurred while reading the PDF or processing text.

Fix: Check Streamlit logs and keep the existing error handling in place.

## Troubleshooting Guide

1. If the app does not start, confirm that `app.py` is the entry file.
2. If dependencies fail, check `requirements.txt` for spelling mistakes.
3. If imports fail, verify that the package folder contains `__init__.py`.
4. If the PDF extraction fails, test with a simple text-based PDF first.
5. If the score looks wrong, confirm that the job description has enough skill keywords.
6. If the app is slow, reduce unnecessary processing and keep the logic simple.

## Deployment Checklist

- [ ] `app.py` exists at the repository root.
- [ ] `requirements.txt` includes Streamlit, PyPDF2, and scikit-learn.
- [ ] All project files are pushed to GitHub.
- [ ] The repository is public or properly accessible.
- [ ] The Streamlit Cloud main file is set to `app.py`.
- [ ] The app runs locally with `streamlit run app.py`.
- [ ] PDF upload works with a simple test file.
- [ ] The app shows score, matched skills, missing skills, and suggestions.
- [ ] Error handling is present for invalid or empty PDFs.
- [ ] The README explains the project clearly.

## Best Practice for a Freshers' Project

Keep the deployment simple. Do not add extra services, databases, or API keys unless they are actually needed. For this project, Streamlit Community Cloud plus GitHub is enough.