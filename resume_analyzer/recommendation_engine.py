"""Rule-based recommendation helpers for ATS results.

This module does not use machine learning. It turns the ATS score and missing
skills into simple messages that are easy to explain in an interview.
"""


def get_match_level(score):
    """Return the match level based on the score thresholds."""
    if score < 50:
        return "weak match"
    if score <= 75:
        return "moderate match"
    return "strong match"


def build_recommendation(score, missing_skills):
    """Create a simple recommendation message from the score and gaps.

    Rules:
    - score < 50  -> weak match
    - 50 to 75    -> moderate match
    - score > 75  -> strong match
    """
    match_level = get_match_level(score)

    if missing_skills:
        skill_message = "Add the missing skills to improve keyword coverage: " + ", ".join(missing_skills)
    else:
        skill_message = "No major missing skills were detected."

    if score < 50:
        relevance_message = (
            "Improve resume relevance by aligning your projects, internship work, and technical summary "
            "more closely with the job description."
        )
    elif score <= 75:
        relevance_message = (
            "Improve resume relevance by repeating the most important job keywords in your skills, "
            "projects, and experience sections where they are actually true."
        )
    else:
        relevance_message = (
            "The resume is already strong. Keep the content focused on the most relevant skills and achievements."
        )

    summary = f"This is a {match_level}."

    return {
        "match_level": match_level,
        "summary": summary,
        "skill_message": skill_message,
        "relevance_message": relevance_message,
    }
