"""ATS scoring utilities based on TF-IDF and cosine similarity.

This module keeps the scoring logic small on purpose so it is easy to explain
in interviews and easy to maintain in a student project.
"""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from resume_analyzer.keyword_matching import compare_resume_with_job_description
from resume_analyzer.preprocessing import preprocess_text


def normalize_text(text):
    """Clean text before scoring."""
    return preprocess_text(text)


def prepare_documents(resume_text, job_description):
    """Return the two cleaned documents used by TF-IDF."""
    cleaned_resume = normalize_text(resume_text)
    cleaned_job_description = normalize_text(job_description)
    return [cleaned_resume, cleaned_job_description]


def build_tfidf_matrix(documents):
    """Convert text documents into TF-IDF vectors."""
    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = vectorizer.fit_transform(documents)
    return tfidf_matrix


def calculate_ats_score(resume_text, job_description):
    """Calculate a hybrid ATS score between 0 and 100.

    The final score combines:
    - 70% TF-IDF cosine similarity
    - 30% keyword coverage from the predefined skill dictionary

    This keeps the score balanced. TF-IDF rewards overall text relevance,
    while keyword coverage makes sure important skills are not undervalued.
    """
    documents = prepare_documents(resume_text, job_description)
    tfidf_matrix = build_tfidf_matrix(documents)
    similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]

    required_skills, _, matched_skills, _ = compare_resume_with_job_description(
        resume_text,
        job_description,
    )

    if required_skills:
        keyword_coverage = len(matched_skills) / len(required_skills)
    else:
        keyword_coverage = 0

    hybrid_score = (0.7 * similarity + 0.3 * keyword_coverage) * 100
    return round(hybrid_score, 2)


def extract_skill_matches(resume_text, job_description, limit=8):
    """Compatibility wrapper around the keyword matching module."""
    _, _, matched_skills, missing_skills = compare_resume_with_job_description(
        resume_text,
        job_description,
    )
    return matched_skills[:limit], missing_skills[:limit]
