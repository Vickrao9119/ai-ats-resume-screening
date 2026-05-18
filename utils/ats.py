"""
ATS (Applicant Tracking System) Scoring Module
Calculates resume quality and job match scores using ML/NLP
"""

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from typing import Dict, List, Tuple
import re
from collections import Counter


class ATSScorer:
    """Calculate ATS scores and resume quality metrics"""

    def __init__(self):
        """Initialize ATS scorer"""
        self.tfidf = TfidfVectorizer(max_features=100, stop_words='english')
        
        # Keywords impact weights
        self.keyword_weights = {
            "required": 10,
            "years_experience": 8,
            "achievements": 7,
            "certifications": 6,
            "education": 5,
            "keywords_match": 8
        }

    def calculate_ats_score(self, resume_text: str, job_description: str = None) -> Dict:
        """Calculate comprehensive ATS score"""
        
        # Base scores
        formatting_score = self._calculate_formatting_score(resume_text)
        completeness_score = self._calculate_completeness_score(resume_text)
        keyword_score = self._calculate_keyword_score(resume_text)
        
        # Job match score (if JD provided)
        job_match_score = 0
        if job_description:
            job_match_score = self._calculate_job_match_score(resume_text, job_description)
        
        # Calculate weighted ATS score
        if job_description:
            ats_score = (formatting_score * 0.25 + 
                        completeness_score * 0.25 + 
                        keyword_score * 0.25 + 
                        job_match_score * 0.25)
        else:
            ats_score = (formatting_score * 0.33 + 
                        completeness_score * 0.33 + 
                        keyword_score * 0.34)
        
        return {
            "ats_score": round(ats_score, 2),
            "formatting_score": round(formatting_score, 2),
            "completeness_score": round(completeness_score, 2),
            "keyword_score": round(keyword_score, 2),
            "job_match_score": round(job_match_score, 2),
            "grade": self._get_grade(ats_score)
        }

    def _calculate_formatting_score(self, text: str) -> float:
        """Calculate resume formatting score"""
        score = 50  # Base score
        
        # Check for structure indicators
        structure_keywords = ["education", "experience", "skills", "projects", "certifications"]
        found_sections = sum(1 for keyword in structure_keywords if keyword.lower() in text.lower())
        score += found_sections * 5
        
        # Check for contact information
        if re.search(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', text):
            score += 5
        if re.search(r'\+?1?\s*\(?([0-9]{3})\)?[\s.-]?([0-9]{3})[\s.-]?([0-9]{4})', text):
            score += 5
        
        # Check for line breaks and spacing
        lines = text.split('\n')
        if len(lines) > 10:
            score += 5
        
        return min(score, 100)

    def _calculate_completeness_score(self, text: str) -> float:
        """Calculate resume completeness score"""
        score = 0
        required_sections = {
            "name|contact": 15,
            "experience|work|employment": 25,
            "education|degree|university": 20,
            "skills|technical|proficiency": 20,
            "projects|portfolio|achievements": 15,
            "certifications|certificates": 5
        }
        
        text_lower = text.lower()
        for pattern, points in required_sections.items():
            if re.search(pattern, text_lower):
                score += points
        
        # Bonus for additional details
        if re.search(r'\d+\s*(?:years|yrs|months)', text_lower):
            score += 5
        
        return min(score, 100)

    def _calculate_keyword_score(self, text: str) -> float:
        """Calculate keyword richness score"""
        score = 0
        
        # Technical keyword categories
        keywords_by_category = {
            "programming": ["python", "java", "javascript", "react", "angular", "node", "express", 
                           "django", "flask", "cpp", "csharp", "ruby", "php"],
            "data_analysis": ["sql", "pandas", "numpy", "tableau", "power bi", "analytics", "excel"],
            "cloud": ["aws", "azure", "gcp", "cloud", "docker", "kubernetes"],
            "tools": ["git", "github", "jira", "confluence", "jenkins", "ci/cd"],
            "soft_skills": ["leadership", "communication", "teamwork", "problem solving", "strategic"],
            "methodologies": ["agile", "scrum", "waterfall", "lean", "six sigma"]
        }
        
        text_lower = text.lower()
        total_keywords = 0
        found_keywords = set()
        
        for category, keywords in keywords_by_category.items():
            for keyword in keywords:
                if re.search(r'\b' + re.escape(keyword) + r'\b', text_lower):
                    found_keywords.add(keyword)
                    total_keywords += 1
        
        # Score based on keyword diversity
        score = min((len(found_keywords) / 20) * 100, 100)
        
        return round(score, 2)

    def _calculate_job_match_score(self, resume_text: str, job_description: str) -> float:
        """Calculate how well resume matches job description"""
        try:
            # Prepare texts
            texts = [resume_text.lower(), job_description.lower()]
            
            # TF-IDF vectorization
            tfidf_matrix = self.tfidf.fit_transform(texts)
            
            # Calculate cosine similarity
            similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
            
            # Extract job requirements
            job_keywords = self._extract_job_keywords(job_description)
            resume_keywords = self._extract_resume_keywords(resume_text)
            
            # Calculate keyword overlap
            if job_keywords:
                keyword_match = len(set(resume_keywords) & set(job_keywords)) / len(job_keywords)
            else:
                keyword_match = 0
            
            # Combined score
            score = (similarity * 100 * 0.5) + (keyword_match * 100 * 0.5)
            
            return min(score, 100)
        except:
            return 0

    def _extract_job_keywords(self, text: str) -> List[str]:
        """Extract important keywords from job description"""
        importance_words = ["must", "required", "should", "experience", "years", "skills"]
        words = text.lower().split()
        
        # Extract words after importance indicators
        keywords = []
        for i, word in enumerate(words):
            for imp_word in importance_words:
                if imp_word in word and i + 1 < len(words):
                    keywords.append(words[i + 1].strip('.,;:'))
                    break
        
        return list(set(keywords))

    def _extract_resume_keywords(self, text: str) -> List[str]:
        """Extract keywords from resume"""
        # Common technical keywords
        all_keywords = [
            "python", "java", "javascript", "react", "angular", "node", "express", "django", "flask",
            "sql", "mongodb", "postgresql", "mysql", "aws", "azure", "gcp", "docker", "kubernetes",
            "git", "jira", "ci/cd", "agile", "scrum", "leadership", "communication", "teamwork"
        ]
        
        text_lower = text.lower()
        found = [kw for kw in all_keywords if re.search(r'\b' + re.escape(kw) + r'\b', text_lower)]
        return found

    def _get_grade(self, score: float) -> str:
        """Get letter grade for ATS score"""
        if score >= 90:
            return "A (Excellent)"
        elif score >= 80:
            return "B (Good)"
        elif score >= 70:
            return "C (Fair)"
        elif score >= 60:
            return "D (Below Average)"
        else:
            return "F (Poor)"

    def calculate_selection_probability(self, ats_score: float, skills_match: float) -> Dict:
        """Calculate HR selection probability based on ATS and skills"""
        
        # Weighted probability
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
            "description": description
        }

    def get_missing_skills(self, resume_skills: List[str], 
                          required_skills: List[str] = None) -> Dict:
        """Identify missing and present skills"""
        
        if not required_skills:
            # Default important skills
            required_skills = [
                "Python", "Java", "SQL", "React", "AWS", "Communication",
                "Problem Solving", "Teamwork", "Leadership", "Data Analysis"
            ]
        
        resume_skills_lower = [s.lower() for s in resume_skills]
        required_lower = [s.lower() for s in required_skills]
        
        matching = [s for s in required_skills if s.lower() in resume_skills_lower]
        missing = [s for s in required_skills if s.lower() not in resume_skills_lower]
        
        return {
            "matching_skills": matching,
            "missing_skills": missing,
            "skill_coverage": round((len(matching) / len(required_skills)) * 100, 2) if required_skills else 0
        }


def score_resume(resume_text: str, job_description: str = None) -> Dict:
    """Convenience function to score resume"""
    scorer = ATSScorer()
    return scorer.calculate_ats_score(resume_text, job_description)
