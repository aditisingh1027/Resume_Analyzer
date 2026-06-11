"""Rule-based ATS health checker for resumes.

This stays simple on purpose. It only checks for a few resume basics using
regular expressions and keyword matching, which is easy to explain in a viva.
"""

import re


EMAIL_PATTERN = re.compile(r"\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b")

PHONE_PATTERNS = [
    re.compile(r"\b(?:\+91[\s-]?)?[6-9]\d{9}\b"),
    re.compile(r"\b(?:\+?\d{1,3}[\s-]?)?(?:\d{3}[\s-]?){2}\d{4}\b"),
    re.compile(r"\b\d{10}\b"),
]

SECTION_PATTERNS = {
    "Skills Section": [
        "skills",
        "technical skills",
        "key skills",
        "core competencies",
        "technical expertise",
    ],
    "Projects Section": [
        "projects",
        "project",
        "academic projects",
        "personal projects",
    ],
    "Education Section": [
        "education",
        "academic details",
        "academics",
        "educational qualification",
        "qualifications",
    ],
    "Experience Section": [
        "experience",
        "work experience",
        "professional experience",
        "internship",
        "employment history",
    ],
}

WEIGHTS = {
    "Email Address": 15,
    "Phone Number": 15,
    "Skills Section": 20,
    "Projects Section": 15,
    "Education Section": 15,
    "Experience Section": 20,
}


def normalize_lines(text):
    """Turn the resume text into clean lines for section scanning."""
    lines = []

    for raw_line in text.splitlines():
        cleaned_line = raw_line.lower()
        cleaned_line = re.sub(r"[^a-z0-9\s]", " ", cleaned_line)
        cleaned_line = re.sub(r"\s+", " ", cleaned_line).strip()

        if cleaned_line:
            lines.append(cleaned_line)

    return lines


def has_email(text):
    """Check whether the resume has an email address."""
    return EMAIL_PATTERN.search(text) is not None


def has_phone_number(text):
    """Check whether the resume has a phone number."""
    for pattern in PHONE_PATTERNS:
        if pattern.search(text):
            return True
    return False


def has_section(lines, section_names):
    """Check whether any expected heading is present in the cleaned lines."""
    for line in lines:
        for section_name in section_names:
            # This keeps the check easy to read instead of trying to be too clever.
            if line == section_name or line.startswith(section_name + " "):
                return True

    return False


def analyze_ats_health(resume_text):
    """Return a simple ATS health report with a score out of 100."""
    lines = normalize_lines(resume_text)

    email_present = has_email(resume_text)
    phone_present = has_phone_number(resume_text)

    checks = [
        {
            "name": "Email Address",
            "present": email_present,
            "weight": WEIGHTS["Email Address"],
            "note": "Email found" if email_present else "Email not found",
        },
        {
            "name": "Phone Number",
            "present": phone_present,
            "weight": WEIGHTS["Phone Number"],
            "note": "Phone number found" if phone_present else "Phone number not found",
        },
    ]

    for section_name, aliases in SECTION_PATTERNS.items():
        section_present = has_section(lines, aliases)
        checks.append(
            {
                "name": section_name,
                "present": section_present,
                "weight": WEIGHTS[section_name],
                "note": "Section found" if section_present else "Section not found",
            }
        )

    score = sum(item["weight"] for item in checks if item["present"])
    missing_items = [item["name"] for item in checks if not item["present"]]
    present_items = [item["name"] for item in checks if item["present"]]

    if score >= 85:
        summary = "Your resume looks ATS-friendly at a basic level."
    elif score >= 60:
        summary = "Your resume has the main basics, but a few important items are missing."
    else:
        summary = "Your resume needs improvement before it looks ATS-ready."

    return {
        "score": score,
        "summary": summary,
        "checks": checks,
        "present_items": present_items,
        "missing_items": missing_items,
    }