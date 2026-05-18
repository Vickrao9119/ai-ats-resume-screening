"""
Resume Parser Module
Extracts text and information from PDF and DOCX files
"""

import re
import io
from typing import Dict, List, Optional, Tuple
import PyPDF2
import docx
import spacy
from datetime import datetime


class ResumeParser:
    """Extract and parse resume information from PDF/DOCX files"""

    def __init__(self):
        """Initialize parser with spacy NLP model"""
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except:
            print("Installing spacy model...")
            import subprocess
            subprocess.check_call(["python", "-m", "spacy", "download", "en_core_web_sm"])
            self.nlp = spacy.load("en_core_web_sm")

    @staticmethod
    def extract_text_from_pdf(file_buffer: io.BytesIO) -> str:
        """Extract text from PDF file"""
        try:
            reader = PyPDF2.PdfReader(file_buffer)
            text_parts = []
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    text_parts.append(text)
            return "\n".join(text_parts)
        except Exception as e:
            return f"Error reading PDF: {str(e)}"

    @staticmethod
    def extract_text_from_docx(file_buffer: io.BytesIO) -> str:
        """Extract text from DOCX file"""
        try:
            doc = docx.Document(file_buffer)
            text_parts = [para.text for para in doc.paragraphs]
            return "\n".join(text_parts)
        except Exception as e:
            return f"Error reading DOCX: {str(e)}"

    def extract_email(self, text: str) -> Optional[str]:
        """Extract email address from resume text"""
        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        match = re.search(email_pattern, text)
        return match.group(0) if match else None

    def extract_phone(self, text: str) -> Optional[str]:
        """Extract phone number from resume text"""
        phone_patterns = [
            r'\+?1?\s*\(?([0-9]{3})\)?[\s.-]?([0-9]{3})[\s.-]?([0-9]{4})',
            r'\+\d{1,3}[\s.-]?\d{1,14}',
            r'(?:\+|0)[1-9]\d{0,2}\s?\d{1,4}\s?\d{1,4}\s?\d{1,9}'
        ]
        for pattern in phone_patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(0)
        return None

    def extract_name(self, text: str) -> Optional[str]:
        """Extract candidate name using NER"""
        lines = text.split('\n')
        for line in lines[:10]:  # Check first 10 lines
            line = line.strip()
            if len(line) > 0 and len(line.split()) <= 4 and not any(char.isdigit() for char in line):
                # Check if it looks like a name
                doc = self.nlp(line)
                for ent in doc.ents:
                    if ent.label_ == "PERSON":
                        return ent.text
        return lines[0].strip() if lines else None

    def extract_education(self, text: str) -> List[Dict]:
        """Extract education information"""
        education_list = []
        
        # Common degree patterns
        degree_patterns = [
            r"(?:bachelor|bachelor's|b\.s\.|b\.a\.|bsc|ba)\s+(?:of\s+)?(?:science|arts|engineering|commerce)?\s+in\s+([a-z\s&]+)",
            r"(?:master|master's|m\.s\.|m\.a\.|msc|ma)\s+(?:of\s+)?(?:science|arts|engineering|business)?\s+in\s+([a-z\s&]+)",
            r"(?:phd|ph\.d\.)\s+in\s+([a-z\s&]+)",
            r"(?:diploma|associate)\s+in\s+([a-z\s&]+)"
        ]
        
        for pattern in degree_patterns:
            matches = re.finditer(pattern, text.lower())
            for match in matches:
                education_list.append({
                    "degree": match.group(0),
                    "field": match.group(1).strip() if match.lastindex >= 1 else "Unknown"
                })
        
        return education_list

    def extract_experience(self, text: str) -> List[Dict]:
        """Extract work experience"""
        experience_list = []
        
        # Pattern for job titles with dates
        exp_pattern = r'([a-z\s&\.]+(?:engineer|developer|manager|specialist|analyst|consultant|architect|lead|director|officer|admin)[\w\s]*)\s+(?:at|@)\s+([a-z\s&\.,]+)'
        
        matches = re.finditer(exp_pattern, text.lower())
        for match in matches:
            experience_list.append({
                "title": match.group(1).strip(),
                "company": match.group(2).strip()
            })
        
        return experience_list

    def extract_skills(self, text: str) -> List[str]:
        """Extract technical skills"""
        # Common technical skills to look for
        technical_skills = [
            "python", "java", "c++", "javascript", "typescript", "c#", "php", "ruby", "swift", "kotlin",
            "golang", "rust", "scala", "r", "matlab", "sql", "nosql", "mongodb", "postgresql", "mysql",
            "html", "css", "react", "angular", "vue", "node", "express", "django", "flask", "spring",
            "aws", "azure", "gcp", "docker", "kubernetes", "jenkins", "git", "linux", "windows",
            "machine learning", "deep learning", "nlp", "computer vision", "tensorflow", "pytorch",
            "scikit-learn", "pandas", "numpy", "spark", "hadoop", "kafka", "elasticsearch",
            "rest", "graphql", "microservices", "ci/cd", "devops", "agile", "scrum",
            "ai", "ml", "data analysis", "analytics", "tableau", "power bi", "excel",
            "communication", "leadership", "project management", "problem solving"
        ]
        
        found_skills = []
        text_lower = text.lower()
        
        for skill in technical_skills:
            if re.search(r'\b' + re.escape(skill) + r'\b', text_lower):
                found_skills.append(skill.title())
        
        return list(set(found_skills))

    def parse_resume(self, file_buffer: io.BytesIO, filename: str) -> Dict:
        """Main parsing function"""
        
        # Extract text based on file type
        if filename.endswith('.pdf'):
            text = self.extract_text_from_pdf(file_buffer)
        elif filename.endswith('.docx'):
            text = self.extract_text_from_docx(file_buffer)
        else:
            return {"error": "Unsupported file format"}
        
        if text.startswith("Error"):
            return {"error": text}
        
        # Parse information
        parsed_data = {
            "filename": filename,
            "raw_text": text,
            "name": self.extract_name(text),
            "email": self.extract_email(text),
            "phone": self.extract_phone(text),
            "skills": self.extract_skills(text),
            "education": self.extract_education(text),
            "experience": self.extract_experience(text),
            "text_length": len(text),
            "parsed_at": datetime.now().isoformat()
        }
        
        return parsed_data


def parse_resume_file(file_buffer: io.BytesIO, filename: str) -> Dict:
    """Convenience function to parse resume"""
    parser = ResumeParser()
    return parser.parse_resume(file_buffer, filename)
