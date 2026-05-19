"""ATS (Applicant Tracking System) scoring module for the unified AI Recruiter Hub."""

import re
from typing import Dict, List

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class ATSScorer:
    """Calculate ATS score and resume analytics for modern hiring workflows."""

    def __init__(self) -> None:
        self.tfidf = TfidfVectorizer(max_features=200, stop_words="english")
        self.skill_inventory = [
            "python", "java", "javascript", "react", "angular", "node", "express",
            "django", "flask", "sql", "pandas", "numpy", "tableau", "aws", "azure",
            "docker", "kubernetes", "git", "github", "jira", "agile", "scrum",
            "leadership", "communication", "teamwork", "problem solving", "data analysis"
        ]

    def calculate_ats_score(self, resume_text: str, job_description: str | None = None) -> Dict[str, object]:
        resume_text = (resume_text or "").strip()
        job_description = (job_description or "").strip()

        formatting_score = self._calculate_formatting_score(resume_text)
        completeness_score = self._calculate_completeness_score(resume_text)
        keyword_score = self._calculate_keyword_score(resume_text)
        skill_analysis = self.extract_skills(resume_text)
        match_summary = self.summarize_match(resume_text, job_description)

        job_match_score = self._calculate_job_match_score(resume_text, job_description) if job_description else 0.0

        if job_description:
            ats_score = (
                formatting_score * 0.22
                + completeness_score * 0.22
                + keyword_score * 0.22
                + skill_analysis["skill_coverage"] * 0.17
                + job_match_score * 0.17
            )
        else:
            ats_score = (
                formatting_score * 0.3
                + completeness_score * 0.3
                + keyword_score * 0.25
                + skill_analysis["skill_coverage"] * 0.15
            )

        return {
            "ats_score": round(min(ats_score, 100), 2),
            "formatting_score": round(formatting_score, 2),
            "completeness_score": round(completeness_score, 2),
            "keyword_score": round(keyword_score, 2),
            "job_match_score": round(job_match_score, 2),
            "matched_skills": skill_analysis["matched_skills"],
            "missing_skills": skill_analysis["missing_skills"],
            "skill_coverage": round(skill_analysis["skill_coverage"], 2),
            "matched_keywords": match_summary["matched_keywords"],
            "missing_keywords": match_summary["missing_keywords"],
            "grade": self._get_grade(ats_score),
        }

    def extract_skills(self, text: str) -> Dict[str, object]:
        text_lower = text.lower()
        matched = [skill for skill in self.skill_inventory if re.search(r"\b" + re.escape(skill) + r"\b", text_lower)]
        missing = [skill for skill in self.skill_inventory if skill not in matched]
        coverage = (len(matched) / len(self.skill_inventory)) * 100 if self.skill_inventory else 0.0
        return {
            "matched_skills": sorted(matched),
            "missing_skills": sorted(missing),
            "skill_coverage": coverage,
        }

    def summarize_match(self, resume_text: str, job_description: str) -> Dict[str, List[str]]:
        resume_tokens = set(re.findall(r"\b[\w-]+\b", resume_text.lower()))
        job_tokens = set(re.findall(r"\b[\w-]+\b", job_description.lower()))
        matched = sorted(token for token in job_tokens if token in resume_tokens)
        missing = sorted(token for token in job_tokens if token not in resume_tokens)
        return {
            "matched_keywords": matched,
            "missing_keywords": missing,
        }

    def _calculate_formatting_score(self, text: str) -> float:
        if not text:
            return 0.0
        score = 50.0
        if re.search(r"\beducation\b", text.lower()):
            score += 8
        if re.search(r"\bexperience\b", text.lower()):
            score += 8
        if re.search(r"\bskills\b", text.lower()):
            score += 8
        if re.search(r"\bprojects?\b", text.lower()):
            score += 5
        if re.search(r"\bcertifications?\b", text.lower()):
            score += 5
        if re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text):
            score += 5
        if re.search(r"\+?\d[\d\s().-]{7,}", text):
            score += 5
        return min(score, 100.0)

    def _calculate_completeness_score(self, text: str) -> float:
        if not text:
            return 0.0
        score = 0.0
        checks = [
            (r"\bname\b", 10),
            (r"\bcontact\b", 10),
            (r"\bexperience\b|\bwork\b|\bemployment\b", 25),
            (r"\beducation\b|\bdegree\b|\buniversity\b", 20),
            (r"\bskills\b|\btechnical\b|\bproficiency\b", 20),
            (r"\bprojects?\b|\bportfolio\b|\bachievements?\b", 10),
            (r"\bcertifications?\b|\bcertificates?\b", 5),
        ]
        text_lower = text.lower()
        for pattern, weight in checks:
            if re.search(pattern, text_lower):
                score += weight
        if re.search(r"\d+\s*(?:years|yrs|months)", text_lower):
            score += 5
        return min(score, 100.0)

    def _calculate_keyword_score(self, text: str) -> float:
        if not text:
            return 0.0
        keywords = [
            "python", "java", "javascript", "react", "angular", "node", "express",
            "django", "flask", "sql", "pandas", "numpy", "tableau", "aws", "azure",
            "docker", "kubernetes", "git", "github", "jira", "agile", "scrum"
        ]
        text_lower = text.lower()
        found = [kw for kw in keywords if re.search(r"\b" + re.escape(kw) + r"\b", text_lower)]
        return min((len(set(found)) / len(keywords)) * 100, 100.0)

    def _calculate_job_match_score(self, resume_text: str, job_description: str) -> float:
        if not resume_text or not job_description:
            return 0.0
        try:
            matrix = self.tfidf.fit_transform([resume_text, job_description])
            similarity = cosine_similarity(matrix[0:1], matrix[1:2])[0][0]
        except Exception:
            similarity = 0.0
        summary = self.summarize_match(resume_text, job_description)
        keyword_match = len(summary["matched_keywords"]) / max(len(summary["matched_keywords"]) + len(summary["missing_keywords"]), 1)
        return min((similarity * 100 * 0.6) + (keyword_match * 100 * 0.4), 100.0)

    def _get_grade(self, score: float) -> str:
        if score >= 90:
            return "A (Excellent)"
        if score >= 80:
            return "B (Good)"
        if score >= 70:
            return "C (Fair)"
        if score >= 60:
            return "D (Below Average)"
        return "F (Poor)"

    def calculate_selection_probability(self, ats_score: float, skills_match: float) -> Dict[str, object]:
        probability = (ats_score * 0.6) + (skills_match * 0.4)
        if probability >= 80:
            rating = "🟢 High"
            description = "Excellent match - Highly likely to be selected"
        elif probability >= 60:
            rating = "🟡 Moderate"
            description = "Good match - May be selected with review"
        else:
            rating = "🔴 Low"
            description = "Weak match - Unlikely to be selected"
        return {
            "probability": round(probability, 2),
            "rating": rating,
            "description": description,
        }


def score_resume(resume_text: str, job_description: str | None = None) -> Dict[str, object]:
    scorer = ATSScorer()
    return scorer.calculate_ats_score(resume_text, job_description)
