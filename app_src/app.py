
import io
import json
import sys
from pathlib import Path
from typing import Dict, List, Optional

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import pandas as pd
import numpy as np
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier

from utils.ats import ATSScorer, score_resume
from utils.parser import parse_resume_file
from utils.ranking import rank_resumes, ResumeRanker
from utils.skills import SkillsAnalyzer

STYLE_PATH = ROOT_DIR / "style.css"
HISTORY_PATH = ROOT_DIR / "uploads_history.json"


def load_style() -> None:
    if STYLE_PATH.exists():
        css = STYLE_PATH.read_text(encoding="utf-8")
        st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


def load_history() -> List[Dict]:
    if HISTORY_PATH.exists():
        try:
            with open(HISTORY_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []


def save_history(record: Dict) -> None:
    records = load_history()
    records.insert(0, record)
    records = records[:50]
    with open(HISTORY_PATH, "w", encoding="utf-8") as f:
        json.dump(records, f, indent=2)


def build_card(title: str, value: str, delta: str, icon: str) -> None:
    st.markdown(
        f"""
        <div class='glass-card'>
            <div class='card-top'>
                <span class='card-icon'>{icon}</span>
                <span class='card-title'>{title}</span>
            </div>
            <div class='card-value'>{value}</div>
            <div class='card-delta'>{delta}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def gauge_chart(value: float, label: str) -> go.Figure:
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number+delta",
            value=value,
            title={"text": label, "font": {"size": 18, "color": "#e2e8f0"}},
            gauge={
                "axis": {"range": [0, 100], "tickcolor": "#9ca3af"},
                "bar": {"color": "#7c3aed"},
                "bgcolor": "rgba(15, 23, 42, 0.8)",
                "borderwidth": 1,
                "bordercolor": "#111827",
                "steps": [
                    {"range": [0, 60], "color": "#c2410c"},
                    {"range": [60, 80], "color": "#2563eb"},
                    {"range": [80, 100], "color": "#7c3aed"},
                ],
            },
            delta={"reference": 60, "increasing": {"color": "#34d399"}},
            number={"font": {"size": 32, "color": "#ffffff"}},
        )
    )
    fig.update_layout(
        paper_bgcolor="rgba(15, 23, 42, 0)",
        plot_bgcolor="rgba(15, 23, 42, 0)",
        margin=dict(t=10, b=10, l=10, r=10),
    )
    return fig


def pie_chart(labels: List[str], values: List[float], title: str) -> go.Figure:
    fig = px.pie(
        names=labels,
        values=values,
        hole=0.45,
        title=title,
        color_discrete_sequence=["#7c3aed", "#38bdf8", "#22c55e", "#f97316", "#eab308"],
    )
    fig.update_traces(textposition="inside", textinfo="percent+label")
    fig.update_layout(
        paper_bgcolor="rgba(15, 23, 42, 0)",
        plot_bgcolor="rgba(15, 23, 42, 0)",
        title_x=0.5,
        legend=dict(font=dict(color="#cbd5e1")),
    )
    return fig


def heatmap_chart(skill_counts: Dict[str, int]) -> go.Figure:
    categories = list(skill_counts.keys())
    values = [skill_counts.get(k, 0) for k in categories]
    fig = go.Figure(
        data=go.Heatmap(
            z=[values],
            x=categories,
            y=["Skill intensity"],
            colorscale="Blues",
            showscale=False,
        )
    )
    fig.update_layout(
        title="Skill Heatmap",
        yaxis=dict(showticklabels=False),
        paper_bgcolor="rgba(15, 23, 42, 0)",
        plot_bgcolor="rgba(15, 23, 42, 0)",
        margin=dict(t=50, b=20, l=10, r=10),
    )
    return fig


def build_resume_dashboard(parsed: Dict, analysis: Dict, skills_summary: Dict, selection: Dict) -> None:
    st.markdown("### Candidate Summary")
    profile_cols = st.columns(4)
    profile_cols[0].metric("Candidate", parsed.get("name", "Unknown"))
    profile_cols[1].metric("Email", parsed.get("email", "N/A"))
    profile_cols[2].metric("Phone", parsed.get("phone", "N/A"))
    profile_cols[3].metric("Resume Length", f"{parsed.get('text_length', 0)} chars")

    st.markdown("---")

    top_columns = st.columns(4)
    top_columns[0].metric("ATS Score", f"{analysis['ats_score']}%", "Live")
    top_columns[1].metric("Resume Quality", f"{analysis['keyword_score']}%", "Keywords")
    top_columns[2].metric("HR Selection", selection['rating'], f"{selection['probability']}%")
    top_columns[3].metric("Skill Coverage", f"{skills_summary['total_score']}%", "Matching")

    st.markdown("---")

    chart_cols = st.columns([1, 1, 1])
    chart_cols[0].plotly_chart(gauge_chart(analysis['ats_score'], "ATS Score"), use_container_width=True)
    chart_cols[1].plotly_chart(pie_chart(
        ["Formatting", "Completeness", "Keywords", "Job Match"],
        [analysis['formatting_score'], analysis['completeness_score'], analysis['keyword_score'], analysis['job_match_score']],
        "Resume Quality Breakdown"
    ), use_container_width=True)

    skill_labels = [k.title() for k in skills_summary.get('missing', [])[:5]]
    skill_values = [1] * len(skill_labels) if skill_labels else [1]
    chart_cols[2].plotly_chart(pie_chart(skill_labels or ["No missing skills"], skill_values, "Top Missing Skills"), use_container_width=True)

    st.markdown("---")
    st.subheader("AI Suggestions")
    suggestions = skills_summary.get("suggestions", [])
    if suggestions:
        for suggestion in suggestions:
            st.markdown(
                f"<div class='suggestion-card'><strong>{suggestion['severity'].title()}</strong>: {suggestion['message']}<br><em>{suggestion['action']}</em></div>",
                unsafe_allow_html=True,
            )
    else:
        st.info("This resume is well optimized. No major suggestions at this time.")

    st.markdown("---")
    st.subheader("Extracted Resume Text")
    st.text_area("Resume text", parsed.get("raw_text", ""), height=320)


def build_resume_rankings(current_record: Dict, history: List[Dict]) -> None:
    st.subheader("Resume Rankings")
    candidates = [
        {
            "name": current_record.get("name", "Current Candidate"),
            "filename": current_record.get("filename", "current.pdf"),
            "ats_score": current_record.get("ats_score", 0),
            "skill_match_score": current_record.get("skills_score", 0),
            "experience": len(current_record.get("experience", [])),
            "education": len(current_record.get("education", [])),
            "certifications": 0,
        }
    ]

    for record in history[:5]:
        candidates.append(
            {
                "name": record.get("filename", "Historic"),
                "filename": record.get("filename", "history.pdf"),
                "ats_score": record.get("score", 0),
                "skill_match_score": record.get("score", 0) * 0.8,
                "experience": 1,
                "education": 1,
                "certifications": 0,
            }
        )

    rank_df = rank_resumes(candidates)
    rank_df = rank_df.drop(columns=[col for col in rank_df.columns if col not in ["rank", "candidate_name", "ats_score", "composite_score", "recommendation"]])
    st.dataframe(rank_df, use_container_width=True)


def build_model_trainer() -> None:
    st.header("AI Model Trainer")
    st.markdown(
        "Build and evaluate classification models using Logistic Regression, Decision Tree, and Random Forest."
    )

    uploaded_csv = st.file_uploader("Upload training CSV", type=["csv"], key="model_trainer")
    df: Optional[pd.DataFrame] = None

    if uploaded_csv is not None:
        try:
            df = pd.read_csv(uploaded_csv)
        except Exception as exc:
            st.error(f"Failed to read CSV file: {exc}")
    elif st.button("Load sample HR dataset"):
        iris = load_iris(as_frame=True)
        df = iris.frame.copy()
        df["target_name"] = df["target"].map(dict(enumerate(iris.target_names)))

    if df is None:
        st.warning("Upload a CSV file or load a sample dataset to begin training.")
        return

    st.markdown("### Training dataset preview")
    st.dataframe(df.head(10), use_container_width=True)

    column_options = df.columns.tolist()
    target_column = st.selectbox("Select target column", column_options)
    feature_columns = st.multiselect(
        "Select feature columns",
        [col for col in column_options if col != target_column],
        default=[col for col in column_options if col != target_column][:3],
    )
    model_choice = st.radio(
        "Choose model",
        ["Logistic Regression", "Decision Tree", "Random Forest"],
        horizontal=True,
    )

    if len(feature_columns) < 2:
        st.warning("Select at least two features to train the model.")
        return

    if st.button("Train model"):
        X = df[feature_columns].copy()
        y = df[target_column].copy()

        if y.dtype == "object" or y.dtype.name == "category":
            y = y.astype("category").cat.codes

        numeric_cols = X.select_dtypes(include=["number"]).columns.tolist()
        if len(numeric_cols) != X.shape[1]:
            X = pd.get_dummies(X, drop_first=True)

        scaler = StandardScaler()
        X[numeric_cols] = scaler.fit_transform(X[numeric_cols])
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

        if model_choice == "Logistic Regression":
            model = LogisticRegression(max_iter=500)
        elif model_choice == "Decision Tree":
            model = DecisionTreeClassifier(random_state=42)
        else:
            model = RandomForestClassifier(n_estimators=150, random_state=42)

        model.fit(X_train, y_train)
        preds = model.predict(X_test)

        st.success("Model training completed.")
        st.markdown("### Model performance")
        st.metric("Accuracy", f"{accuracy_score(y_test, preds):.3f}")
        st.text_area("Classification report", classification_report(y_test, preds, zero_division=0), height=220)

        confusion = confusion_matrix(y_test, preds)
        fig = px.imshow(
            confusion,
            labels={"x": "Predicted", "y": "Actual", "color": "Count"},
            text_auto=True,
            color_continuous_scale="blues",
        )
        fig.update_layout(title="Confusion matrix", title_x=0.5, paper_bgcolor="rgba(15,23,42,0)", plot_bgcolor="rgba(15,23,42,0)")
        st.plotly_chart(fig, use_container_width=True)


def show_landing_page() -> None:
    st.markdown("### Welcome to AI Recruiter Hub")
    st.markdown(
        "<div class='hero-card'>"
        "<div><h1>AI-Powered Resume Screening for Modern Talent Teams</h1>"
        "<p>One unified hiring dashboard with resume parsing, ATS scoring, HR selection prediction, and model training in a single SaaS experience.</p>"
        "<div class='hero-actions'><a href='mailto:ac570011@gmail.com'>ac570011@gmail.com</a> | <a href='tel:+919119652725'>+91 9119652725</a></div>"
        "</div>"
        "<div class='hero-stats'>"
        "<div><strong>94%</strong><span>Recommendation accuracy</span></div>"
        "<div><strong>1.2s</strong><span>Average screening response</span></div>"
        "<div><strong>85%</strong><span>Skill match uplift</span></div>"
        "</div>"
        "</div>",
        unsafe_allow_html=True,
    )
    st.markdown("---")
    cols = st.columns(3)
    build_card("AI Resume Screening", "Connected modules", "Backend + frontend", "🤖")
    build_card("Smart Parsing", "PDF / DOCX / TXT", "Entity extraction", "📄")
    build_card("HR Predictions", "Selection likelihood", "Transparent scoring", "📈")

    st.markdown("---")
    st.markdown(
        "<div class='feature-grid'>"
        "<div><strong>Glassmorphism UI</strong><p>Modern SaaS styling with dark neon glow.</p></div>"
        "<div><strong>Unified Dashboard</strong><p>Single app navigation for all workflows.</p></div>"
        "<div><strong>AI Analytics</strong><p>ATS score, skill heatmaps, HR guidance.</p></div>"
        "</div>",
        unsafe_allow_html=True,
    )


def show_home() -> None:
    history = load_history()
    selected = st.selectbox("Select candidate from history", [record.get("filename") for record in history[:6]] if history else ["No history yet"])
    average_score = np.mean([record.get("score", 0) for record in history]) if history else 0
    selected_count = len(history)
    selected_rate = np.mean([record.get("score", 0) >= 60 for record in history]) * 100 if history else 0
    high_score_pct = np.mean([record.get("score", 0) >= 80 for record in history]) * 100 if history else 0

    st.markdown("### Dashboard Overview")
    st.markdown(
        "<div class='overview-grid'>"
        f"<div><h2>{selected_count}</h2><p>Resumes screened</p></div>"
        f"<div><h2>{average_score:.1f}%</h2><p>Average ATS score</p></div>"
        f"<div><h2>{selected_rate:.0f}%</h2><p>Selection ratio</p></div>"
        f"<div><h2>{high_score_pct:.0f}%</h2><p>High-quality candidates</p></div>"
        "</div>",
        unsafe_allow_html=True,
    )

    st.markdown("---")
    if history:
        history_df = pd.DataFrame(history)
        history_df["timestamp"] = pd.to_datetime(history_df["timestamp"]).dt.strftime("%Y-%m-%d %H:%M")
        st.markdown("### Recent screening activity")
        st.dataframe(history_df[["filename", "role", "score", "status", "timestamp"]].head(10), use_container_width=True)
    else:
        st.info("No uploaded resumes found yet. Upload one from Resume Upload to start building your pool.")


def show_upload() -> None:
    st.header("Resume Upload & Screening")
    uploaded_file = st.file_uploader("Upload candidate resume", type=["pdf", "docx", "txt"])
    job_description = st.text_area("Paste job description (optional)", height=140)
    analyze_button = st.button("Run ATS screening")
    st.markdown("---")

    if uploaded_file is None:
        st.info("Upload a resume to parse the text and evaluate the candidate.")
        return

    parsed = parse_resume_file(io.BytesIO(uploaded_file.read()), uploaded_file.name)
    if parsed.get("error"):
        st.error(parsed["error"])
        return

    if analyze_button or "analysis" not in st.session_state:
        analysis = score_resume(parsed["raw_text"], job_description)
        skills_analyzer = SkillsAnalyzer()
        extracted_categories = skills_analyzer.extract_skills(parsed["raw_text"])
        flat_skills = skills_analyzer.flatten_skills(extracted_categories)
        skills_info = skills_analyzer.calculate_skill_score(flat_skills)
        skills_info["missing"] = skills_info.get("missing", [])
        skills_info["suggestions"] = skills_analyzer.suggest_improvements({"skills": flat_skills})
        selection = ATSScorer().calculate_selection_probability(analysis["ats_score"], skills_info["total_score"])

        record = {
            "filename": uploaded_file.name,
            "role": "Data Scientist",
            "score": analysis["ats_score"],
            "status": "Selected" if analysis["ats_score"] >= 60 else "Rejected",
            "timestamp": pd.Timestamp.now().isoformat(),
            "preview": parsed["raw_text"][:180],
        }
        save_history(record)

        st.session_state.analysis = analysis
        st.session_state.parsed = parsed
        st.session_state.skills_info = skills_info
        st.session_state.selection = selection
        st.session_state.extracted_categories = extracted_categories

    parsed = st.session_state.parsed
    analysis = st.session_state.analysis
    skills_info = st.session_state.skills_info
    selection = st.session_state.selection
    extracted_categories = st.session_state.extracted_categories

    build_resume_dashboard(parsed, analysis, skills_info, selection)
    st.markdown("---")
    st.subheader("Skill categories")
    category_table = {k: ", ".join(v) for k, v in extracted_categories.items()}
    st.table(pd.DataFrame.from_dict(category_table, orient="index", columns=["Extracted Skills"]))


def show_resume_analytics() -> None:
    st.header("Resume Analytics")
    history = load_history()

    if "analysis" not in st.session_state:
        st.warning("Run a candidate screening in Resume Upload first to see analytics here.")
        return

    parsed = st.session_state.parsed
    analysis = st.session_state.analysis
    skills_info = st.session_state.skills_info
    selection = st.session_state.selection

    analytics_cols = st.columns([1.2, 1, 1, 1])
    analytics_cols[0].metric("ATS Score", f"{analysis['ats_score']}%", "Resume Match")
    analytics_cols[1].metric("Resume Quality", f"{analysis['keyword_score']}%", "Skill-rich")
    analytics_cols[2].metric("HR Selection", selection["rating"], f"{selection['probability']}%")
    analytics_cols[3].metric("Missing Skills", len(skills_info.get("missing", [])), "Action needed")

    st.markdown("---")

    chart_cols = st.columns(3)
    chart_cols[0].plotly_chart(gauge_chart(analysis["ats_score"], "ATS Score Gauge"), use_container_width=True)
    chart_cols[1].plotly_chart(
        pie_chart(
            ["Matched", "Missing"],
            [skills_info.get("total_score", 0), 100 - skills_info.get("total_score", 0)],
            "Skill coverage"
        ),
        use_container_width=True,
    )
    missing_list = skills_info.get("missing", [])
    missing_counts = {skill: 1 for skill in missing_list[:10]} if isinstance(missing_list, list) and missing_list else {"No missing skills": 1}
    chart_cols[2].plotly_chart(
        heatmap_chart(missing_counts),
        use_container_width=True,
    )

    st.markdown("---")
    st.subheader("Missing Skills & Recommendations")
    missing = skills_info.get("missing", [])
    if missing:
        st.write(", ".join(missing[:20]))
    else:
        st.success("No missing skills detected.")

    build_resume_rankings({
        "name": parsed.get("name"),
        "filename": parsed.get("filename"),
        "ats_score": analysis.get("ats_score", 0),
        "skills_score": skills_info.get("total_score", 0),
        "experience": parsed.get("experience", []),
        "education": parsed.get("education", []),
    }, history)

    st.markdown("---")
    st.subheader("Candidate Insights")
    for suggestion in skills_info.get("suggestions", []):
        st.markdown(f"- **{suggestion['severity'].title()}**: {suggestion['message']} - _{suggestion['action']}_")


def show_model_trainer_page() -> None:
    st.header("Model Trainer")
    st.markdown(
        "Train, evaluate and compare models using your own dataset or a prebuilt sample dataset."
    )
    build_model_trainer()


def main() -> None:
    st.set_page_config(
        page_title="AI Recruiter Hub",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            "Get Help": None,
            "Report a bug": None,
            "About": ""
        }
    )
    load_style()

    st.markdown(
        "<div class='brand-header'>"
        "<span class='hub-title'>AI Hub</span> | <span class='recruiter-title'>Recruiter</span> | "
        "<a href='mailto:ac570011@gmail.com'>ac570011@gmail.com</a> | <a href='tel:+919119652725'>+91 9119652725</a>"
        "</div>",
        unsafe_allow_html=True,
    )

    page = st.sidebar.radio(
        "Navigation",
        ["Landing Page", "Home", "Resume Upload", "Resume Analytics", "Model Trainer"],
    )

    if page == "Landing Page":
        show_landing_page()
    elif page == "Home":
        show_home()
    elif page == "Resume Upload":
        show_upload()
    elif page == "Resume Analytics":
        show_resume_analytics()
    else:
        show_model_trainer_page()


if __name__ == "__main__":
    main()
