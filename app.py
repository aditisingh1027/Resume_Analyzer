import streamlit as st

from resume_analyzer.ats_health_checker import analyze_ats_health
from resume_analyzer.pdf_utils import extract_text_from_pdf
from resume_analyzer.keyword_matching import analyze_skill_gap
from resume_analyzer.recommendation_engine import build_recommendation
from resume_analyzer.scoring import calculate_ats_score


st.set_page_config(page_title="Resume Analyzer", page_icon="📄", layout="wide")

st.markdown(
    """
    <style>
        .block-container {
            padding-top: 1.25rem;
            padding-bottom: 2rem;
            max-width: 1200px;
        }

        h1, h2, h3, h4, h5, h6 {
            letter-spacing: -0.02em;
        }

        h1 {
            font-size: 2.3rem;
            font-weight: 800;
            margin-bottom: 0.15rem;
        }

        h2 {
            font-size: 1.35rem;
            font-weight: 700;
            margin-top: 0.35rem;
            margin-bottom: 0.35rem;
        }

        h3 {
            font-size: 1.05rem;
            font-weight: 700;
        }

        div[data-testid="stFormSubmitButton"] button,
        .stButton > button {
            background: linear-gradient(90deg, #2563eb 0%, #4f46e5 100%);
            color: #ffffff;
            border: none;
            border-radius: 14px;
            padding: 0.7rem 1.35rem;
            font-weight: 700;
            box-shadow: 0 8px 18px rgba(37, 99, 235, 0.18);
            transition: transform 0.18s ease, box-shadow 0.18s ease, filter 0.18s ease;
        }

        div[data-testid="stFormSubmitButton"] button:hover,
        .stButton > button:hover {
            transform: translateY(-1px);
            box-shadow: 0 12px 24px rgba(37, 99, 235, 0.24);
            filter: brightness(1.04);
        }

        div[data-testid="stVerticalBlockBorderWrapper"] {
            transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
        }

        div[data-testid="stVerticalBlockBorderWrapper"]:hover {
            transform: translateY(-2px);
            box-shadow: 0 14px 30px rgba(15, 23, 42, 0.08);
            border-color: rgba(37, 99, 235, 0.18);
        }

        .score-pill {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            min-width: 92px;
            padding: 0.38rem 0.75rem;
            border-radius: 999px;
            font-weight: 800;
            letter-spacing: 0.01em;
            color: #ffffff;
        }

        .score-pill.red {
            background: #dc2626;
        }

        .score-pill.orange {
            background: #f97316;
        }

        .score-pill.green {
            background: #16a34a;
        }

        .skill-chip {
            display: inline-block;
            padding: 0.33rem 0.65rem;
            margin: 0.22rem 0.28rem 0.22rem 0;
            border-radius: 999px;
            font-size: 0.88rem;
            font-weight: 600;
            line-height: 1.2;
            border: 1px solid transparent;
        }

        .skill-chip.found {
            background: #dcfce7;
            color: #166534;
            border-color: #86efac;
        }

        .skill-chip.missing {
            background: #fee2e2;
            color: #991b1b;
            border-color: #fca5a5;
        }

        .section-note {
            color: #64748b;
            font-size: 0.93rem;
            margin-top: -0.2rem;
            margin-bottom: 0.35rem;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("Resume Analyzer")
st.caption("A clean ATS-style resume checker built with Python and Streamlit.")


def get_score_tone(score):
    """Return a visual tone for the ATS score."""
    if score < 40:
        return "red"
    if score < 70:
        return "orange"
    return "green"


def render_skill_list(title, skills, empty_message):
    """Show a small, readable result block for a list of skills."""
    with st.container(border=True):
        st.subheader(title)
        if skills:
            chip_class = "found" if title != "Missing Skills" else "missing"
            chips = " ".join(
                f'<span class="skill-chip {chip_class}">{skill}</span>' for skill in skills
            )
            st.markdown(chips, unsafe_allow_html=True)
        else:
            st.write(empty_message)


def render_progress_block(label, score):
    """Show a metric and progress bar for a score out of 100."""
    tone = get_score_tone(score)
    st.metric(label, f"{score:.2f}%")
    st.markdown(
        f'<div class="score-pill {tone}">{tone.title()} Zone</div>',
        unsafe_allow_html=True,
    )
    st.progress(min(max(score / 100, 0), 1))


def render_score_card(title, score, summary_text):
    """Render a compact score card with color coding and a progress bar."""
    tone = get_score_tone(score)
    with st.container(border=True):
        st.subheader(title)
        st.markdown(
            f'<div class="score-pill {tone}">{score:.2f}%</div>',
            unsafe_allow_html=True,
        )
        st.progress(min(max(score / 100, 0), 1))
        st.write(summary_text)

with st.form("resume_analysis_form"):
    resume_file = st.file_uploader("Upload Resume", type=["pdf"])
    job_description = st.text_area(
        "Paste Job Description",
        height=240,
        placeholder="Paste the job role, required skills, and responsibilities here...",
    )
    analyze = st.form_submit_button("Analyze")

if analyze:
    if resume_file is None:
        st.error("Please upload a PDF resume.")
    elif not job_description.strip():
        st.error("Please paste a job description.")
    else:
        try:
            resume_text = extract_text_from_pdf(resume_file)
            score = calculate_ats_score(resume_text, job_description)
            required_skills, found_skills, matched_skills, missing_skills = analyze_skill_gap(
                resume_text,
                job_description,
            )
            recommendation = build_recommendation(score, missing_skills)
            health_report = analyze_ats_health(resume_text)

            st.subheader("Analysis Summary")

            metrics_col_1, metrics_col_2, metrics_col_3 = st.columns(3)

            with metrics_col_1:
                st.metric("ATS Score", f"{score:.2f}%")

            with metrics_col_2:
                st.metric("Skills Found", str(len(found_skills)))

            with metrics_col_3:
                st.metric("Missing Skills", str(len(missing_skills)))

            score_col, health_col = st.columns(2)

            with score_col:
                render_score_card("ATS Score", score, recommendation["summary"])

            with health_col:
                render_score_card("ATS Health Score", health_report["score"], health_report["summary"])

            st.divider()
            st.subheader("Skill Gap Analysis")
            st.markdown(
                '<div class="section-note">Found skills are shown in green. Missing skills are shown in red.</div>',
                unsafe_allow_html=True,
            )

            required_col, found_col, missing_col = st.columns(3)

            with required_col:
                render_skill_list(
                    "Required Skills",
                    required_skills,
                    "No predefined skills were detected in the job description.",
                )

            with found_col:
                render_skill_list(
                    "Skills Found",
                    found_skills,
                    "No predefined skills were detected in the resume.",
                )

            with missing_col:
                render_skill_list(
                    "Missing Skills",
                    missing_skills,
                    "No missing skills from the predefined dictionary.",
                )

            st.divider()
            st.subheader("Recommendations")

            rec_col_1, rec_col_2 = st.columns(2)

            with rec_col_1:
                with st.container(border=True):
                    st.subheader("Skill Advice")
                    st.write(recommendation["skill_message"])

            with rec_col_2:
                with st.container(border=True):
                    st.subheader("Relevance Advice")
                    st.write(recommendation["relevance_message"])

            with st.expander("ATS Health Checklist"):
                for item in health_report["checks"]:
                    status_icon = "✅" if item["present"] else "❌"
                    st.write(f"{status_icon} {item['name']}: {item['note']}")

            if matched_skills:
                st.caption("Matched Skills: " + ", ".join(matched_skills))

            with st.expander("Extracted Resume Text"):
                st.write(resume_text)
        except ValueError as error:
            st.error(str(error))
        except Exception:
            st.error("Something went wrong while reading the PDF. Please try another file.")
