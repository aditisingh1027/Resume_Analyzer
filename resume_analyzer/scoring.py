"""ATS scoring utilities based on TF-IDF and cosine similarity.

This module keeps the scoring logic small on purpose so it is easy to explain
in interviews and easy to maintain in a student project.
"""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from resume_analyzer.keyword_matching import compare_resume_with_job_description
from resume_analyzer.preprocessing import preprocess_text


KEYWORD_WEIGHT = 0.60
TFIDF_WEIGHT = 0.40


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


def calculate_tfidf_similarity_percentage(resume_text, job_description):
    """Return the resume relevance percentage based on TF-IDF similarity."""
    documents = prepare_documents(resume_text, job_description)
    tfidf_matrix = build_tfidf_matrix(documents)
    similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
    return round(similarity * 100, 2)


def calculate_keyword_coverage_percentage(resume_text, job_description):
    """Return the keyword coverage percentage based on required skills."""
    required_skills, _, matched_skills, _ = compare_resume_with_job_description(
        resume_text,
        job_description,
    )

    if not required_skills:
        return 0.0

    coverage = len(matched_skills) / len(required_skills)
    return round(coverage * 100, 2)


def get_score_label(score):
    """Map a score to a simple ATS-style label."""
    if score <= 40:
        return "Weak Match"
    if score <= 65:
        return "Moderate Match"
    if score <= 80:
        return "Strong Match"
    return "Excellent Match"


def calculate_ats_score_breakdown(resume_text, job_description):
    """Return keyword coverage, resume relevance, and final ATS score percentages."""
    keyword_coverage = calculate_keyword_coverage_percentage(resume_text, job_description)
    resume_relevance = calculate_tfidf_similarity_percentage(resume_text, job_description)

    final_score = (
        (KEYWORD_WEIGHT * keyword_coverage) + (TFIDF_WEIGHT * resume_relevance)
    )

    return {
        "keyword_coverage": round(keyword_coverage, 2),
        "resume_relevance": round(resume_relevance, 2),
        "final_score": round(final_score, 2),
        "score_label": get_score_label(final_score),
    }


def calculate_ats_score(resume_text, job_description):
    """Calculate a hybrid ATS score between 0 and 100.

    The final score combines:
    - 60% keyword coverage from the predefined skill dictionary
    - 40% TF-IDF cosine similarity

    Keyword coverage keeps the score anchored to required skills, while
    TF-IDF adds a smaller relevance signal. This keeps the score stable and
    explainable for a student resume analyzer.
    """
    breakdown = calculate_ats_score_breakdown(resume_text, job_description)
    return breakdown["final_score"]


def get_ats_score_label(score):
    """Compatibility wrapper for the score label helper."""
    return get_score_label(score)


def calculate_ats_score_details(resume_text, job_description):
    """Compatibility wrapper that returns the full ATS score breakdown."""
    return calculate_ats_score_breakdown(resume_text, job_description)


def extract_skill_matches(resume_text, job_description, limit=8):
    """Compatibility wrapper around the keyword matching module."""
    _, _, matched_skills, missing_skills = compare_resume_with_job_description(
        resume_text,
        job_description,
    )
    return matched_skills[:limit], missing_skills[:limit]
