"""
Configuration settings for AI ATS Resume Platform
"""

import os
from datetime import datetime

# ==================== APPLICATION SETTINGS ====================
APP_NAME = "AI ATS Resume Screening Platform"
APP_VERSION = "1.0.0"
APP_AUTHOR = "Recruitment AI Team"
APP_DESCRIPTION = "Production-level recruitment platform powered by ML and NLP"

# ==================== FILE SETTINGS ====================
ALLOWED_UPLOAD_FORMATS = ['pdf', 'docx', 'doc']
MAX_FILE_SIZE_MB = 25
UPLOAD_FOLDER = "./outputs"
TEMP_FOLDER = "./temp"

# ==================== ATS SCORING SETTINGS ====================
ATS_WEIGHTS = {
    "formatting": 0.25,
    "completeness": 0.25,
    "keyword": 0.25,
    "job_match": 0.25
}

ATS_GRADE_THRESHOLDS = {
    "A": 90,
    "B": 80,
    "C": 70,
    "D": 60,
    "F": 0
}

# ==================== SKILL SETTINGS ====================
IMPORTANT_SKILLS_COUNT = 10
RECOMMENDED_SKILLS_COUNT = 5

SKILL_CATEGORIES_PRIORITY = {
    "programming_languages": 1,
    "web_frameworks": 1,
    "databases": 1,
    "cloud_platforms": 1,
    "devops_tools": 2,
    "ai_ml": 2,
}

# ==================== RANKING SETTINGS ====================
RANKING_WEIGHTS = {
    "ats_score": 0.35,
    "skill_match": 0.30,
    "experience": 0.20,
    "education": 0.10,
    "certifications": 0.05
}

SELECTION_PROBABILITY_THRESHOLDS = {
    "high": 80,
    "moderate": 60,
    "low": 0
}

# ==================== UI/UX SETTINGS ====================
THEME = "dark"
PRIMARY_COLOR = "#00d4ff"
SECONDARY_COLOR = "#7b2ff7"
BACKGROUND_COLOR = "#0f0c29"

# Chart colors
CHART_COLORS = {
    "primary": "#00d4ff",
    "secondary": "#7b2ff7",
    "success": "#22c55e",
    "warning": "#eab308",
    "danger": "#ef4444",
    "info": "#3b82f6"
}

# ==================== PARSING SETTINGS ====================
NLP_MODEL = "en_core_web_sm"
EXTRACT_SECTIONS = [
    "contact",
    "summary",
    "skills",
    "experience",
    "education",
    "certifications",
    "projects"
]

# ==================== LOGGING SETTINGS ====================
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
SAVE_LOGS = True
LOG_FILE = "./logs/app.log"

# ==================== EMAIL SETTINGS (Optional) ====================
EMAIL_ENABLED = False
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_FROM = "resume@platform.com"

# ==================== DATABASE SETTINGS ====================
DB_TYPE = "sqlite"
DB_PATH = "./data/resume_platform.db"
DB_BACKUP_ENABLED = True

# ==================== CACHE SETTINGS ====================
CACHE_ENABLED = True
CACHE_TTL = 3600  # 1 hour
CACHE_MAX_SIZE = 100

# ==================== API SETTINGS ====================
API_DEBUG = False
API_RATE_LIMIT = 100  # requests per minute
API_TIMEOUT = 30

# ==================== ANALYTICS SETTINGS ====================
ANALYTICS_ENABLED = True
ANALYTICS_RETENTION_DAYS = 90

# ==================== SECURITY SETTINGS ====================
SECURE_UPLOADS = True
SCAN_FOR_VIRUSES = False
DELETE_UPLOADED_FILES_AFTER_PROCESSING = False
ENCRYPTION_ENABLED = False

# ==================== FEATURE FLAGS ====================
FEATURES = {
    "resume_parsing": True,
    "ats_scoring": True,
    "skill_analysis": True,
    "resume_ranking": True,
    "analytics_dashboard": True,
    "recommendations": True,
    "batch_processing": True,
    "export_reports": True,
    "email_notifications": False,
    "api_endpoints": False,
    "advanced_analytics": True
}

# ==================== MODEL SETTINGS ====================
ML_MODELS = {
    "ner_model": "en_core_web_sm",
    "tfidf_max_features": 100,
    "min_skill_frequency": 1
}

# ==================== DEFAULTS ====================
DEFAULT_LANGUAGE = "en"
DEFAULT_TIMEZONE = "UTC"
DATE_FORMAT = "%Y-%m-%d"
TIME_FORMAT = "%H:%M:%S"

# ==================== HELPER FUNCTIONS ====================
def get_config_summary():
    """Get configuration summary"""
    return {
        "app_name": APP_NAME,
        "version": APP_VERSION,
        "theme": THEME,
        "features_enabled": sum(1 for v in FEATURES.values() if v),
        "total_features": len(FEATURES)
    }

def is_feature_enabled(feature_name):
    """Check if a feature is enabled"""
    return FEATURES.get(feature_name, False)

# ==================== ENVIRONMENT VARIABLES ====================
# Override settings with environment variables if present
def load_env_config():
    """Load configuration from environment variables"""
    global LOG_LEVEL, DB_PATH, API_DEBUG
    
    LOG_LEVEL = os.getenv("LOG_LEVEL", LOG_LEVEL)
    DB_PATH = os.getenv("DB_PATH", DB_PATH)
    API_DEBUG = os.getenv("API_DEBUG", API_DEBUG).lower() == "true"

# Load on import
load_env_config()
