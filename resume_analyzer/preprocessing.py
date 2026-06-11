import re


def preprocess_text(text):
    """Clean text before ATS comparison.

    Steps:
    - convert to lowercase
    - remove punctuation and special characters
    - collapse extra spaces
    """
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()
