"""
Analytics Module
Generate analytical data and insights for dashboard visualizations
"""

from typing import Dict, List
import pandas as pd
from collections import defaultdict


class AnalyticsEngine:
    """Generate analytics and insights from resume data"""

    @staticmethod
    def generate_skill_heatmap_data(resumes_data: List[Dict]) -> pd.DataFrame:
        """Generate data for skill heatmap visualization"""
        
        all_skills = set()
        skill_matrix = []
        
        # Collect all unique skills
        for resume in resumes_data:
            skills = resume.get('skills', [])
            all_skills.update(skills)
        
        # Create matrix
        for resume in resumes_data:
            skills = resume.get('skills', [])
            row = {}
            row['Candidate'] = resume.get('name', 'Unknown')
            
            for skill in sorted(list(all_skills)[:15]):  # Top 15 skills
                row[skill] = 1 if skill in skills else 0
            
            skill_matrix.append(row)
        
        return pd.DataFrame(skill_matrix)

    @staticmethod
    def generate_ats_distribution(resumes_data: List[Dict]) -> Dict:
        """Generate ATS score distribution data"""
        
        ats_scores = [resume.get('ats_score', 0) for resume in resumes_data]
        
        return {
            'mean': sum(ats_scores) / len(ats_scores) if ats_scores else 0,
            'median': sorted(ats_scores)[len(ats_scores)//2] if ats_scores else 0,
            'min': min(ats_scores) if ats_scores else 0,
            'max': max(ats_scores) if ats_scores else 0,
            'scores': ats_scores
        }

    @staticmethod
    def generate_skill_distribution(resumes_data: List[Dict]) -> Dict:
        """Generate skill distribution across candidates"""
        
        skill_frequency = defaultdict(int)
        
        for resume in resumes_data:
            skills = resume.get('skills', [])
            for skill in skills:
                skill_frequency[skill] += 1
        
        # Sort by frequency
        sorted_skills = sorted(skill_frequency.items(), key=lambda x: x[1], reverse=True)
        
        return {
            'skills': [item[0] for item in sorted_skills[:10]],
            'frequency': [item[1] for item in sorted_skills[:10]]
        }

    @staticmethod
    def generate_experience_distribution(resumes_data: List[Dict]) -> Dict:
        """Generate experience distribution"""
        
        exp_counts = [len(resume.get('experience', [])) for resume in resumes_data]
        
        if not exp_counts:
            return {'categories': [], 'counts': []}
        
        # Categorize by experience level
        categories = ['Entry Level\n(0-2 roles)', 'Mid Level\n(3-5 roles)', 'Senior\n(6+ roles)']
        counts = [
            sum(1 for e in exp_counts if e <= 2),
            sum(1 for e in exp_counts if 3 <= e <= 5),
            sum(1 for e in exp_counts if e >= 6)
        ]
        
        return {'categories': categories, 'counts': counts}

    @staticmethod
    def generate_education_distribution(resumes_data: List[Dict]) -> Dict:
        """Generate education distribution"""
        
        education_types = defaultdict(int)
        
        for resume in resumes_data:
            education = resume.get('education', [])
            if not education:
                education_types['Not Specified'] += 1
            else:
                for edu in education:
                    degree = edu.get('degree', '').lower()
                    if 'phd' in degree or 'ph.d' in degree:
                        education_types['PhD'] += 1
                    elif 'master' in degree:
                        education_types['Master'] += 1
                    elif 'bachelor' in degree:
                        education_types['Bachelor'] += 1
                    else:
                        education_types['Other'] += 1
        
        return {
            'education_types': list(education_types.keys()),
            'counts': list(education_types.values())
        }

    @staticmethod
    def generate_selection_analytics(resumes_data: List[Dict]) -> Dict:
        """Generate selection probability analytics"""
        
        high_prob = sum(1 for r in resumes_data if r.get('ats_score', 0) >= 80)
        moderate_prob = sum(1 for r in resumes_data if 60 <= r.get('ats_score', 0) < 80)
        low_prob = sum(1 for r in resumes_data if r.get('ats_score', 0) < 60)
        
        total = len(resumes_data)
        
        return {
            'high': {'count': high_prob, 'percentage': (high_prob / total * 100) if total > 0 else 0},
            'moderate': {'count': moderate_prob, 'percentage': (moderate_prob / total * 100) if total > 0 else 0},
            'low': {'count': low_prob, 'percentage': (low_prob / total * 100) if total > 0 else 0},
            'total': total
        }

    @staticmethod
    def generate_candidate_quality_metrics(resume_data: Dict) -> Dict:
        """Generate quality metrics for a single resume"""
        
        metrics = {
            'completeness': AnalyticsEngine._calculate_completeness(resume_data),
            'formatting': resume_data.get('formatting_score', 0),
            'keyword_richness': resume_data.get('keyword_score', 0),
            'contact_info': AnalyticsEngine._check_contact_info(resume_data),
            'sections_present': AnalyticsEngine._count_sections(resume_data)
        }
        
        # Calculate overall quality
        quality_score = sum(metrics.values()) / len(metrics) if metrics else 0
        metrics['overall_quality'] = round(quality_score, 2)
        
        return metrics

    @staticmethod
    def _calculate_completeness(resume_data: Dict) -> float:
        """Calculate resume completeness score"""
        score = 0
        max_score = 100
        
        components = [
            ('name', 15),
            ('email', 10),
            ('phone', 10),
            ('skills', 20),
            ('experience', 20),
            ('education', 15),
        ]
        
        for component, points in components:
            if resume_data.get(component):
                score += points
        
        return score

    @staticmethod
    def _check_contact_info(resume_data: Dict) -> float:
        """Check contact information completeness"""
        score = 0
        if resume_data.get('email'):
            score += 50
        if resume_data.get('phone'):
            score += 50
        return score

    @staticmethod
    def _count_sections(resume_data: Dict) -> int:
        """Count number of resume sections present"""
        count = 0
        sections = ['name', 'email', 'phone', 'skills', 'experience', 'education']
        for section in sections:
            if resume_data.get(section):
                count += 1
        return count

    @staticmethod
    def generate_insights_summary(resumes_data: List[Dict]) -> List[Dict]:
        """Generate key insights from resume batch"""
        
        insights = []
        
        if not resumes_data:
            return [{'type': 'info', 'message': 'No resumes to analyze'}]
        
        # Top skills insight
        skill_freq = defaultdict(int)
        for resume in resumes_data:
            for skill in resume.get('skills', []):
                skill_freq[skill] += 1
        
        if skill_freq:
            top_skill = max(skill_freq, key=skill_freq.get)
            insights.append({
                'type': 'success',
                'title': 'Top Skill',
                'message': f"'{top_skill}' is the most common skill ({skill_freq[top_skill]} candidates)"
            })
        
        # Average ATS score
        avg_ats = sum(r.get('ats_score', 0) for r in resumes_data) / len(resumes_data)
        insights.append({
            'type': 'info',
            'title': 'Average ATS Score',
            'message': f"Average ATS score is {avg_ats:.1f}/100"
        })
        
        # Candidate pool strength
        high_quality = sum(1 for r in resumes_data if r.get('ats_score', 0) >= 80)
        insights.append({
            'type': 'info',
            'title': 'Pool Strength',
            'message': f"{high_quality} out of {len(resumes_data)} candidates are high quality"
        })
        
        return insights

    @staticmethod
    def generate_comparison_report(resume1: Dict, resume2: Dict) -> Dict:
        """Generate detailed comparison report"""
        
        return {
            'candidate1': resume1.get('name', 'Resume 1'),
            'candidate2': resume2.get('name', 'Resume 2'),
            'ats_score_diff': abs(resume1.get('ats_score', 0) - resume2.get('ats_score', 0)),
            'skills_comparison': {
                'candidate1_count': len(resume1.get('skills', [])),
                'candidate2_count': len(resume2.get('skills', []))
            },
            'experience_comparison': {
                'candidate1_count': len(resume1.get('experience', [])),
                'candidate2_count': len(resume2.get('experience', []))
            },
            'common_skills': list(set(resume1.get('skills', [])) & set(resume2.get('skills', []))),
            'unique_to_1': list(set(resume1.get('skills', [])) - set(resume2.get('skills', []))),
            'unique_to_2': list(set(resume2.get('skills', [])) - set(resume1.get('skills', [])))
        }


def get_analytics_dashboard_data(resumes_data: List[Dict]) -> Dict:
    """Convenience function to get all dashboard analytics"""
    engine = AnalyticsEngine()
    
    return {
        'skill_heatmap': engine.generate_skill_heatmap_data(resumes_data),
        'ats_distribution': engine.generate_ats_distribution(resumes_data),
        'skill_distribution': engine.generate_skill_distribution(resumes_data),
        'experience_dist': engine.generate_experience_distribution(resumes_data),
        'education_dist': engine.generate_education_distribution(resumes_data),
        'selection_analytics': engine.generate_selection_analytics(resumes_data),
        'insights': engine.generate_insights_summary(resumes_data)
    }
