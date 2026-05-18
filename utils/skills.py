"""
Skills Analysis Module
Extract, match, and analyze technical and soft skills
"""

from typing import List, Dict, Set, Tuple
import re
from collections import Counter


class SkillsAnalyzer:
    """Analyze and manage resume skills"""

    # Comprehensive skill database organized by category
    SKILL_DATABASE = {
        "programming_languages": {
            "python": ["python", "py"],
            "java": ["java"],
            "javascript": ["javascript", "js", "nodejs", "node.js"],
            "typescript": ["typescript", "ts"],
            "cpp": ["c++", "cpp"],
            "csharp": ["c#", "c#", "csharp"],
            "php": ["php"],
            "ruby": ["ruby", "rails"],
            "go": ["golang", "go"],
            "rust": ["rust"],
            "kotlin": ["kotlin"],
            "swift": ["swift"],
            "scala": ["scala"],
            "r": ["r programming", "r language"],
        },
        "web_frameworks": {
            "react": ["react", "reactjs"],
            "angular": ["angular", "angularjs"],
            "vue": ["vue", "vuejs"],
            "django": ["django"],
            "flask": ["flask"],
            "express": ["express", "express.js"],
            "spring": ["spring", "spring boot"],
            "asp_net": ["asp.net", "aspnet"],
        },
        "databases": {
            "sql": ["sql", "mysql", "postgresql", "mssql", "oracle"],
            "mongodb": ["mongodb", "mongo"],
            "nosql": ["nosql", "dynamodb", "cassandra"],
            "redis": ["redis"],
            "elasticsearch": ["elasticsearch"],
            "firebase": ["firebase"],
        },
        "cloud_platforms": {
            "aws": ["aws", "amazon web services", "ec2", "s3", "lambda"],
            "azure": ["azure", "microsoft azure"],
            "gcp": ["gcp", "google cloud", "google cloud platform"],
            "heroku": ["heroku"],
            "digitalocean": ["digitalocean"],
        },
        "devops_tools": {
            "docker": ["docker"],
            "kubernetes": ["kubernetes", "k8s"],
            "jenkins": ["jenkins"],
            "gitlab_ci": ["gitlab ci"],
            "github_actions": ["github actions"],
            "terraform": ["terraform"],
            "ansible": ["ansible"],
        },
        "version_control": {
            "git": ["git"],
            "github": ["github"],
            "gitlab": ["gitlab"],
            "bitbucket": ["bitbucket"],
        },
        "ai_ml": {
            "machine_learning": ["machine learning", "ml"],
            "deep_learning": ["deep learning"],
            "nlp": ["nlp", "natural language processing"],
            "computer_vision": ["computer vision", "cv"],
            "tensorflow": ["tensorflow"],
            "pytorch": ["pytorch"],
            "scikit_learn": ["scikit-learn", "sklearn"],
            "keras": ["keras"],
        },
        "data_tools": {
            "pandas": ["pandas"],
            "numpy": ["numpy"],
            "spark": ["spark", "apache spark"],
            "hadoop": ["hadoop"],
            "tableau": ["tableau"],
            "power_bi": ["power bi"],
            "excel": ["excel"],
        },
        "soft_skills": {
            "leadership": ["leadership", "leader"],
            "communication": ["communication", "communicator"],
            "teamwork": ["teamwork", "team player"],
            "problem_solving": ["problem solving", "analytical"],
            "project_management": ["project management", "pm"],
            "agile": ["agile", "scrum", "kanban"],
            "critical_thinking": ["critical thinking"],
            "time_management": ["time management"],
        }
    }

    def extract_skills(self, text: str) -> Dict[str, List[str]]:
        """Extract all skills from text, organized by category"""
        text_lower = text.lower()
        extracted_skills = {}
        
        for category, skills in self.SKILL_DATABASE.items():
            found_skills = []
            for skill_name, variations in skills.items():
                for variation in variations:
                    if re.search(r'\b' + re.escape(variation) + r'\b', text_lower):
                        found_skills.append(skill_name.replace('_', ' ').title())
                        break
            
            if found_skills:
                extracted_skills[category.replace('_', ' ').title()] = list(set(found_skills))
        
        return extracted_skills

    def flatten_skills(self, extracted_skills: Dict[str, List[str]]) -> List[str]:
        """Flatten extracted skills to single list"""
        all_skills = []
        for skills_list in extracted_skills.values():
            all_skills.extend(skills_list)
        return list(set(all_skills))

    def match_skills(self, resume_skills: List[str], 
                    required_skills: List[str]) -> Dict:
        """Match resume skills against required skills"""
        resume_lower = [s.lower() for s in resume_skills]
        required_lower = [s.lower() for s in required_skills]
        
        # Find matches and missing
        matches = [s for s in required_skills if s.lower() in resume_lower]
        missing = [s for s in required_skills if s.lower() not in resume_lower]
        extra = [s for s in resume_skills if s.lower() not in required_lower]
        
        match_percentage = (len(matches) / len(required_skills) * 100) if required_skills else 0
        
        return {
            "matching": matches,
            "missing": missing,
            "extra": extra,
            "match_percentage": round(match_percentage, 2),
            "total_required": len(required_skills),
            "total_matched": len(matches)
        }

    def get_skill_recommendations(self, resume_skills: List[str], 
                                 required_skills: List[str] = None) -> List[str]:
        """Recommend skills to add based on industry trends"""
        
        if not required_skills:
            # Industry standard recommendations for 2024
            required_skills = [
                "python", "react", "aws", "docker", "git", "sql", 
                "communication", "problem solving", "agile"
            ]
        
        resume_lower = [s.lower() for s in resume_skills]
        
        # Recommend missing skills
        recommendations = [s for s in required_skills if s.lower() not in resume_lower]
        
        # Add trending skills if multiple skills already present
        trending_skills = {
            "ai": ["machine learning", "tensorflow", "nlp"],
            "devops": ["kubernetes", "terraform", "ansible"],
            "fullstack": ["typescript", "react", "node", "mongodb"],
            "data": ["spark", "tableau", "python"]
        }
        
        if len(resume_skills) >= 5:
            for trend_category, trend_skills in trending_skills.items():
                for skill in trend_skills:
                    if skill.lower() not in resume_lower and skill not in recommendations:
                        recommendations.append(skill)
        
        return recommendations[:5]  # Return top 5 recommendations

    def calculate_skill_score(self, resume_skills: List[str], 
                             required_skills: List[str] = None) -> Dict:
        """Calculate detailed skill score"""
        
        if not required_skills:
            required_skills = [
                "python", "java", "sql", "react", "aws", "docker",
                "git", "communication", "problem solving", "teamwork"
            ]
        
        # Get match details
        match_result = self.match_skills(resume_skills, required_skills)
        
        # Calculate score components
        core_skill_score = match_result['match_percentage']
        
        # Bonus for additional skills
        extra_skill_bonus = min((len(match_result['extra']) / 5) * 20, 20)
        
        # Category diversity bonus
        category_count = len(self.extract_skills(" ".join(resume_skills)))
        diversity_bonus = min((category_count / 5) * 15, 15)
        
        # Total skill score
        total_score = min(core_skill_score + extra_skill_bonus + diversity_bonus, 100)
        
        return {
            "total_score": round(total_score, 2),
            "core_match": round(core_skill_score, 2),
            "skill_diversity": round(diversity_bonus, 2),
            "extra_skills_bonus": round(extra_skill_bonus, 2),
            "matched_count": match_result['total_matched'],
            "required_count": match_result['total_required'],
            "missing": match_result['missing']
        }

    def get_skill_categories(self, resume_skills: List[str]) -> Dict:
        """Categorize resume skills"""
        categorized = {}
        skills_lower = [s.lower() for s in resume_skills]
        
        for category, skills in self.SKILL_DATABASE.items():
            category_skills = []
            for skill_name, variations in skills.items():
                for variation in variations:
                    if any(skill.lower() == variation for skill in resume_skills):
                        category_skills.append(skill_name.replace('_', ' ').title())
                        break
            
            if category_skills:
                categorized[category.replace('_', ' ').title()] = list(set(category_skills))
        
        return categorized

    def suggest_improvements(self, resume_data: Dict) -> List[Dict]:
        """Suggest skill-based improvements"""
        suggestions = []
        skills = resume_data.get('skills', [])
        
        # Check skill count
        if len(skills) < 5:
            suggestions.append({
                "type": "skill_quantity",
                "severity": "medium",
                "message": f"Add more skills. You have {len(skills)}, aim for 10-15 relevant skills.",
                "action": "Expand your skills section with relevant technical and soft skills"
            })
        
        # Check for technical skills
        technical_count = sum(1 for s in skills if any(
            tech in s.lower() for tech in ["python", "java", "react", "aws", "sql", "docker"]
        ))
        
        if technical_count < 3:
            suggestions.append({
                "type": "technical_skills",
                "severity": "high",
                "message": "Add more technical skills relevant to your target role",
                "action": "Include programming languages, frameworks, and tools"
            })
        
        # Check for soft skills
        soft_skills_keywords = ["leadership", "communication", "teamwork", "problem solving"]
        soft_count = sum(1 for s in skills if any(soft in s.lower() for soft in soft_skills_keywords))
        
        if soft_count < 2:
            suggestions.append({
                "type": "soft_skills",
                "severity": "medium",
                "message": "Add soft skills that employers value",
                "action": "Include communication, leadership, teamwork, or problem-solving"
            })
        
        return suggestions


def extract_skills_from_text(text: str) -> Dict[str, List[str]]:
    """Convenience function"""
    analyzer = SkillsAnalyzer()
    return analyzer.extract_skills(text)
