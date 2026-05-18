"""
Resume Ranking Module
Compare and rank multiple resumes against each other and job requirements
"""

from typing import List, Dict
import pandas as pd


class ResumeRanker:
    """Rank and compare multiple resumes"""

    @staticmethod
    def rank_resumes(resumes_data: List[Dict], 
                    weights: Dict = None) -> pd.DataFrame:
        """
        Rank multiple resumes based on various metrics
        
        Args:
            resumes_data: List of resume data dictionaries
            weights: Custom scoring weights
        """
        
        if not weights:
            # Default weights
            weights = {
                'ats_score': 0.35,
                'skill_match': 0.30,
                'experience': 0.20,
                'education': 0.10,
                'certifications': 0.05
            }
        
        rankings = []
        
        for idx, resume in enumerate(resumes_data):
            score = ResumeRanker._calculate_composite_score(resume, weights)
            
            rankings.append({
                'rank': 0,  # Will be assigned after sorting
                'filename': resume.get('filename', f'Resume {idx + 1}'),
                'candidate_name': resume.get('name', 'Unknown'),
                'ats_score': resume.get('ats_score', 0),
                'skill_match_score': resume.get('skill_match_score', 0),
                'experience_score': ResumeRanker._calculate_experience_score(resume),
                'education_score': ResumeRanker._calculate_education_score(resume),
                'certification_score': ResumeRanker._calculate_certification_score(resume),
                'composite_score': score,
                'email': resume.get('email', 'N/A'),
                'phone': resume.get('phone', 'N/A'),
                'skill_count': len(resume.get('skills', [])),
                'recommendation': ResumeRanker._get_recommendation(score)
            })
        
        # Convert to DataFrame and sort
        df = pd.DataFrame(rankings)
        df = df.sort_values('composite_score', ascending=False).reset_index(drop=True)
        df['rank'] = range(1, len(df) + 1)
        
        return df[['rank', 'candidate_name', 'ats_score', 'skill_match_score', 
                   'experience_score', 'education_score', 'certification_score', 
                   'composite_score', 'recommendation', 'email', 'phone']]

    @staticmethod
    def _calculate_composite_score(resume: Dict, weights: Dict) -> float:
        """Calculate weighted composite score"""
        
        ats = resume.get('ats_score', 0) * weights.get('ats_score', 0.35)
        skills = resume.get('skill_match_score', 0) * weights.get('skill_match', 0.30)
        experience = ResumeRanker._calculate_experience_score(resume) * weights.get('experience', 0.20)
        education = ResumeRanker._calculate_education_score(resume) * weights.get('education', 0.10)
        certification = ResumeRanker._calculate_certification_score(resume) * weights.get('certifications', 0.05)
        
        composite = ats + skills + experience + education + certification
        return round(min(composite, 100), 2)

    @staticmethod
    def _calculate_experience_score(resume: Dict) -> float:
        """Calculate experience score based on job titles and companies"""
        experience = resume.get('experience', [])

        # If experience is provided as an integer (count), use it directly
        if isinstance(experience, int):
            score = min(experience * 15, 100)
            return float(score)

        # If it's a list, compute based on number of entries
        if isinstance(experience, list):
            score = min(len(experience) * 15, 100)

            # Bonus for senior roles when structured as dicts
            senior_keywords = ['senior', 'lead', 'manager', 'director', 'architect']
            for exp in experience:
                if isinstance(exp, dict):
                    title = exp.get('title', '') or ''
                    title = title.lower()
                    if any(keyword in title for keyword in senior_keywords):
                        score = min(score + 10, 100)
                        break
                else:
                    # If entries are simple strings, check them too
                    try:
                        title = str(exp).lower()
                        if any(keyword in title for keyword in senior_keywords):
                            score = min(score + 10, 100)
                            break
                    except Exception:
                        continue

            return float(score)

        # Fallback
        return 0.0

    @staticmethod
    def _calculate_education_score(resume: Dict) -> float:
        """Calculate education score"""
        education = resume.get('education', [])

        score = 50  # Base score

        # If education provided as count
        if isinstance(education, int):
            score = min(50 + education * 10, 100)
            return float(score)

        # If list of education entries
        if isinstance(education, list):
            for edu in education:
                if isinstance(edu, dict):
                    degree = (edu.get('degree') or '').lower()

                    if 'bachelor' in degree:
                        score = max(score, 75)
                    elif 'master' in degree:
                        score = max(score, 90)
                    elif 'phd' in degree:
                        score = 100
                    elif 'diploma' in degree or 'associate' in degree:
                        score = max(score, 60)
                else:
                    # If entry is a simple string, inspect it
                    try:
                        degree = str(edu).lower()
                        if 'bachelor' in degree:
                            score = max(score, 75)
                        elif 'master' in degree:
                            score = max(score, 90)
                        elif 'phd' in degree:
                            score = 100
                        elif 'diploma' in degree or 'associate' in degree:
                            score = max(score, 60)
                    except Exception:
                        continue

            return float(score)

        return float(score)

    @staticmethod
    def _calculate_certification_score(resume: Dict) -> float:
        """Calculate certification score"""
        # This could be enhanced with actual certification detection
        # For now, using skill count as proxy
        skills = resume.get('skills', [])
        cert_keywords = ['certified', 'certification', 'aws certified', 'gcp certified']
        
        score = min(len(skills) * 2, 50)
        
        # Bonus for certifications mentioned
        text = " ".join(skills).lower()
        if any(cert_keyword in text for cert_keyword in cert_keywords):
            score += 20
        
        return min(score, 100)

    @staticmethod
    def _get_recommendation(score: float) -> str:
        """Get recommendation based on score"""
        if score >= 85:
            return "🟢 Highly Recommended"
        elif score >= 70:
            return "🟡 Recommended"
        elif score >= 50:
            return "🟠 Consider"
        else:
            return "🔴 Review Required"

    @staticmethod
    def compare_resumes(resume1: Dict, resume2: Dict) -> Dict:
        """Compare two resumes in detail"""
        
        comparison = {
            'resume1_name': resume1.get('name', 'Resume 1'),
            'resume2_name': resume2.get('name', 'Resume 2'),
            'metrics': {
                'ats_score': {
                    'resume1': resume1.get('ats_score', 0),
                    'resume2': resume2.get('ats_score', 0),
                    'winner': 'Resume 1' if resume1.get('ats_score', 0) > resume2.get('ats_score', 0) else 'Resume 2'
                },
                'skill_count': {
                    'resume1': len(resume1.get('skills', [])),
                    'resume2': len(resume2.get('skills', [])),
                    'winner': 'Resume 1' if len(resume1.get('skills', [])) > len(resume2.get('skills', [])) else 'Resume 2'
                },
                'experience_count': {
                    'resume1': len(resume1.get('experience', [])),
                    'resume2': len(resume2.get('experience', [])),
                    'winner': 'Resume 1' if len(resume1.get('experience', [])) > len(resume2.get('experience', [])) else 'Resume 2'
                },
                'education_count': {
                    'resume1': len(resume1.get('education', [])),
                    'resume2': len(resume2.get('education', [])),
                    'winner': 'Resume 1' if len(resume1.get('education', [])) > len(resume2.get('education', [])) else 'Resume 2'
                }
            }
        }
        
        return comparison

    @staticmethod
    def suggest_improvements_for_rank(resume: Dict, target_score: float = 85) -> List[Dict]:
        """Suggest improvements to improve ranking"""
        current_score = resume.get('ats_score', 0)
        gap = target_score - current_score
        
        suggestions = []
        
        if gap <= 0:
            return [{"priority": "info", "suggestion": "Resume is already at target score!"}]
        
        # Based on missing components
        if len(resume.get('skills', [])) < 10:
            suggestions.append({
                "priority": "high",
                "suggestion": "Add more technical skills",
                "impact": "+5-10 points"
            })
        
        if not resume.get('certifications') or len(resume.get('certifications', [])) == 0:
            suggestions.append({
                "priority": "medium",
                "suggestion": "Add relevant certifications",
                "impact": "+5 points"
            })
        
        if len(resume.get('experience', [])) < 3:
            suggestions.append({
                "priority": "high",
                "suggestion": "Highlight more work experience",
                "impact": "+10 points"
            })
        
        if not resume.get('education') or len(resume.get('education', [])) == 0:
            suggestions.append({
                "priority": "medium",
                "suggestion": "Include education details",
                "impact": "+5 points"
            })
        
        return suggestions


def rank_resumes(resumes_data: List[Dict]) -> pd.DataFrame:
    """Convenience function"""
    return ResumeRanker.rank_resumes(resumes_data)


def compare_two_resumes(resume1: Dict, resume2: Dict) -> Dict:
    """Convenience function"""
    return ResumeRanker.compare_resumes(resume1, resume2)
