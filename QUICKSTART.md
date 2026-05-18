# 🚀 Quick Start Guide

## Installation (First Time Only)

```bash
# Navigate to project
cd "C:\New assignment 1"

# Create virtual environment
python -m venv .venv

# Activate virtual environment
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Download spaCy NLP model
python -m spacy download en_core_web_sm

# Verify installation
python -c "import spacy; print('✓ spaCy Ready')"
python -c "import streamlit; print('✓ Streamlit Ready')"
```

## Running the Application

```bash
# Make sure .venv is activated
.venv\Scripts\activate

# Run the app
streamlit run app.py
```

**Application opens at**: http://localhost:8501

---

## First Time Usage

### 1. Upload a Resume
1. Click **"📄 Upload & Parse"** in sidebar
2. Upload a PDF or DOCX resume file
3. Click **"🔄 Parse All"** button
4. View extracted information

### 2. View ATS Analysis
1. Go to **"⚡ ATS Analysis"**
2. Select the candidate you uploaded
3. See ATS score gauge and breakdown
4. View skills by category

### 3. Compare (with multiple resumes)
1. Upload 2+ resumes first
2. Go to **"🎯 Ranking"**
3. View ranking table
4. Select two candidates for detailed comparison

### 4. Explore Analytics
1. Go to **"📊 Analytics"**
2. View skill distribution
3. See experience levels
4. Check selection probability breakdown

### 5. Get Recommendations
1. Go to **"💡 Recommendations"**
2. Select a candidate
3. Read improvement suggestions
4. Understand what to add/change

---

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+S` | Save page |
| `F12` | Open browser dev tools |
| `R` | Reload Streamlit app |

---

## Common Tasks

### Reset the App
```bash
streamlit cache clear
streamlit run app.py
```

### Use Different Port
```bash
streamlit run app.py --server.port 8502
```

### Debug Mode
```bash
streamlit run app.py --logger.level=debug
```

### Full Screen Mode
```
Press 'f' in Streamlit interface
```

---

## Key Features Quick Reference

| Page | What You Can Do |
|------|-----------------|
| 🏠 Dashboard | See overview metrics and top candidates |
| 📄 Upload & Parse | Upload & analyze resumes |
| ⚡ ATS Analysis | View detailed score breakdown |
| 🎯 Ranking | Compare candidates side-by-side |
| 📊 Analytics | Explore hiring pool insights |
| 💡 Recommendations | Get improvement suggestions |

---

## Troubleshooting

### Issue: "ModuleNotFoundError"
```bash
pip install -r requirements.txt
```

### Issue: "spaCy model not found"
```bash
python -m spacy download en_core_web_sm
```

### Issue: Port 8501 already in use
```bash
streamlit run app.py --server.port 8502
```

### Issue: PDF won't upload
- Ensure PDF is not password protected
- Try a different PDF file
- Check file size < 25MB

---

## System Requirements

- **Python**: 3.8 or higher
- **RAM**: 2GB minimum, 4GB recommended
- **Disk Space**: 500MB free
- **OS**: Windows, Mac, or Linux
- **Browser**: Chrome, Firefox, Safari, Edge

---

## File Structure

```
C:\New assignment 1\
├── app.py                    ← Main application
├── requirements.txt          ← Dependencies
├── README.md                 ← Full documentation
├── COMPLETE_GUIDE.md         ← In-depth guide
├── VIVA_QUESTIONS.md         ← Interview prep
├── utils/                    ← Core modules
│   ├── parser.py
│   ├── ats.py
│   ├── skills.py
│   ├── ranking.py
│   └── analytics.py
├── data/                     ← Sample data
│   └── sample_data.py
└── config.py                 ← Settings
```

---

## Next Steps

1. ✅ Install and run the app
2. 📄 Upload some test resumes
3. ⚡ Explore ATS analysis features
4. 📊 Check analytics dashboard
5. 📖 Read COMPLETE_GUIDE.md for deeper understanding
6. 🎓 Review VIVA_QUESTIONS.md for interviews

---

## Need Help?

- **Read**: README.md (general info)
- **Learn**: COMPLETE_GUIDE.md (detailed guide)
- **Interview**: VIVA_QUESTIONS.md (Q&A)
- **Bug**: Check troubleshooting section above

---

**Happy analyzing resumes!** 🚀

Version: 1.0.0
Last Updated: 2024
