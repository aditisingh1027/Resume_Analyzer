"""Simple keyword matching for ATS-style resume analysis.

This module avoids machine learning and uses direct phrase matching against a
small, readable skill dictionary.
"""

import re

from resume_analyzer.preprocessing import preprocess_text


SKILL_DICTIONARY = {
    "Programming Languages": [
        "python",
        "java",
        "sql",
        "javascript",
        "c",
        "cplusplus",
        "cpp",
    ],
    "Web Development": [
        "html",
        "css",
        "react",
        "node js",
        "express js",
        "django",
        "flask",
        "streamlit",
        "api",
        "rest api",
    ],
    "Data and Analytics": [
        "pandas",
        "numpy",
        "excel",
        "power bi",
        "tableau",
    ],
    "Tools and Platforms": [
        "git",
        "github",
        "linux",
        "dbms",
    ],
    "Computer Science Basics": [
        "oop",
        "data structures",
        "algorithms",
    ],
    "Soft Skills": [
        "communication",
        "teamwork",
        "problem solving",
    ],
}


def flatten_skill_dictionary(skill_dictionary=None):
    """Convert the predefined skill dictionary into one searchable list."""
    dictionary = skill_dictionary or SKILL_DICTIONARY
    skills = []

    for category_skills in dictionary.values():
        for skill in category_skills:
            if skill not in skills:
                skills.append(skill)

    return skills


def normalize_for_keywords(text):
    """Prepare text for keyword matching.

    The preprocessing step converts the text to lowercase and removes special
    characters. We also normalize a few common skill names into the same form
    used by the catalog.
    """
    cleaned_text = text.lower()
    cleaned_text = cleaned_text.replace("c++", "cplusplus")
    cleaned_text = cleaned_text.replace("c plus plus", "cplusplus")
    cleaned_text = preprocess_text(cleaned_text)
    cleaned_text = cleaned_text.replace("nodejs", "node js")
    cleaned_text = cleaned_text.replace("expressjs", "express js")
    cleaned_text = cleaned_text.replace("restapi", "rest api")
    cleaned_text = cleaned_text.replace("problem-solving", "problem solving")
    return cleaned_text


def phrase_exists(text, phrase):
    """Check whether a skill phrase appears in the text."""
    pattern = r"\b" + re.escape(phrase) + r"\b"
    return re.search(pattern, text) is not None


def extract_skills(text, skill_catalog=None):
    """Extract skills from a piece of text using direct keyword matching."""
    searchable_text = normalize_for_keywords(text)
    catalog = skill_catalog or flatten_skill_dictionary()
    found_skills = []

    for skill in catalog:
        if phrase_exists(searchable_text, skill):
            found_skills.append(skill)

    return found_skills


def analyze_skill_gap(resume_text, job_description, skill_dictionary=None):
    """Compare the job description and resume using a predefined skill dictionary.

    Returns:
        required_skills: skills found in the job description
        found_skills: skills present in the resume
        missing_skills: skills present in the job description but missing in the resume
    """
    catalog = flatten_skill_dictionary(skill_dictionary)
    required_skills = extract_skills(job_description, catalog)
    found_skills = extract_skills(resume_text, catalog)

    required_skill_set = set(required_skills)
    found_skill_set = set(found_skills)

    matched_skills = sorted(required_skill_set & found_skill_set)
    missing_skills = sorted(required_skill_set - found_skill_set)

    return required_skills, found_skills, matched_skills, missing_skills


def compare_resume_with_job_description(resume_text, job_description):
    """Compatibility wrapper used by the existing ATS score flow."""
    return analyze_skill_gap(resume_text, job_description)
