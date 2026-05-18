from flask import Flask, request, jsonify
from flask_cors import CORS
import io
import json
from pathlib import Path
from datetime import datetime
from PyPDF2 import PdfReader
from utils.ats import score_resume
from utils.skills import extract_skills_from_text

app = Flask(__name__)
CORS(app)

HISTORY_FILE = Path(__file__).parent / "uploads_history.json"


def load_history():
    """Load upload history from JSON file."""
    if HISTORY_FILE.exists():
        try:
            with open(HISTORY_FILE, "r") as f:
                return json.load(f)
        except Exception:
            return []
    return []


def save_history(records):
    """Save upload history to JSON file."""
    try:
        with open(HISTORY_FILE, "w") as f:
            json.dump(records, f, indent=2)
    except Exception as e:
        print(f"Error saving history: {e}")


def add_to_history(filename, role, score, status, text_preview):
    """Add a new record to history."""
    records = load_history()
    record = {
        "id": len(records) + 1,
        "filename": filename,
        "role": "Data Scientist",  # Default role; can be made dynamic
        "score": int(score),
        "status": status,
        "timestamp": datetime.now().isoformat(),
        "preview": text_preview[:200]
    }
    records.insert(0, record)  # Insert at top (most recent first)
    records = records[:50]  # Keep last 50 records
    save_history(records)


def read_pdf_bytes(file_bytes: bytes) -> str:
    try:
        reader = PdfReader(io.BytesIO(file_bytes))
        parts = []
        for page in reader.pages:
            text = page.extract_text()
            if text:
                parts.append(text)
        return "\n\n".join(parts)
    except Exception:
        return ""


@app.route('/api/analyze', methods=['POST'])
def analyze():
    if 'file' not in request.files:
        return jsonify({'error': 'no file provided'}), 400

    f = request.files['file']
    filename = f.filename or 'upload'
    b = f.read()

    # Extract text for PDF or fallback to raw text
    text = ''
    if filename.lower().endswith('.pdf'):
        text = read_pdf_bytes(b)
    else:
        try:
            text = b.decode('utf-8', errors='ignore')
        except Exception:
            text = ''

    # Perform ATS scoring (best-effort)
    try:
        result = score_resume(text)
    except Exception:
        result = {
            'ats_score': 0,
            'formatting_score': 0,
            'completeness_score': 0,
            'keyword_score': 0,
            'job_match_score': 0,
            'grade': 'F'
        }

    # Extract skills (best-effort)
    try:
        skills = extract_skills_from_text(text)
    except Exception:
        skills = {'matched': [], 'partial': [], 'missing': []}

    ats_score = result.get('ats_score', 0)
    status = "Selected" if ats_score >= 60 else "Rejected"
    
    # Save to history
    add_to_history(filename, "Data Scientist", ats_score, status, text)

    response = {
        'filename': filename,
        'text_preview': (text[:400] + '...') if len(text) > 400 else text,
        'analysis': result,
        'skills': skills
    }

    return jsonify(response)


@app.route('/api/history', methods=['GET'])
def get_history():
    """Retrieve upload history."""
    records = load_history()
    return jsonify(records)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
