# AI-based-student-introduction-analyzer
AI-powered speech analysis tool for student introductions

# 🎯 AI-Based Student Introduction Analyzer

A Flask web application that analyzes student self-introductions using multiple AI-powered metrics including sentiment analysis, grammar checking, speech patterns, and content evaluation.

## 🌐 Live Demo

**Live Website:** [https://ai-based-student-introduction-analyzer.onrender.com](https://ai-based-student-introduction-analyzer.onrender.com)

## 📊 Features

### Analysis Criteria
- **Salutation Score** - Evaluates greeting effectiveness
- **Keyword Presence** - Checks for essential introduction elements
- **Flow & Structure** - Analyzes logical progression
- **Speech Rate** - Measures words per minute (WPM)
- **Grammar & Spelling** - Identifies errors and improvements
- **Vocabulary Richness** - Assesses word diversity (TTR)
- **Filler Words** - Detects unnecessary speech fillers
- **Sentiment Analysis** - Evaluates emotional tone

### Detailed Analytics
- Sentence-by-sentence sentiment breakdown
- Spelling error identification
- Filler word detection
- Vocabulary complexity analysis
- Structural flow assessment
- Comprehensive scoring with weights

## 🛠️ Technology Stack

- **Backend:** Python, Flask
- **Frontend:** HTML, CSS, JavaScript
- **AI/ML Libraries:**
  - VADER Sentiment Analysis
  - PySpellChecker
- **Deployment:** Render

## 📁 Project Structure
student-introduction-analyzer/
│
-├── app.py # Main Flask application
-├── requirements.txt # Python dependencies
├── Sample text for case study.txt # Sample text for testing
├── index.html # Frontend interface
└── README.md # Project documentation


## 🚀 Local Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Theheerpatel/AI-based-student-introduction-analyzer.git
   cd AI-based-student-introduction-analyzer

Create virtual environment

bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
Install dependencies

bash
pip install -r requirements.txt
Run the application

bash
python app.py
Access the application
Open http://localhost:5000 in your browser
📋 Usage

Paste Introduction Text: Enter or paste a student's self-introduction
Set Duration: Input the speech duration in seconds
Analyze: Click "Analyze Introduction" to get comprehensive results
Review: Examine detailed scores and improvement suggestions
🎯 Scoring System

Criteria	Weight	Description
Keyword Presence	30%	Essential introduction elements
Sentiment	15%	Positive emotional tone
Filler Words	15%	Minimal unnecessary words
Speech Rate	10%	Optimal speaking pace
Grammar	10%	Spelling and grammar accuracy
Vocabulary	10%	Word diversity and richness
Salutation	5%	Effective greeting
Flow	5%	Logical structure
