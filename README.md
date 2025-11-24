# 🎯 AI-Based Student Introduction Analyzer

A Flask web application that analyzes student self-introductions using multiple AI-powered metrics such as sentiment, grammar, speech rate, structure, and vocabulary richness.

---

## 🌐 Live Demo

🔗 **Website:** https://ai-based-student-introduction-analyzer.onrender.com

---

## 📊 Features

### 🔍 Analysis Criteria
- **Salutation Score** – Evaluates greeting effectiveness  
- **Keyword Presence** – Checks essential introduction elements  
- **Flow & Structure** – Analyzes logical progression  
- **Speech Rate** – Measures words per minute (WPM)  
- **Grammar & Spelling** – Identifies errors and improvements  
- **Vocabulary Richness** – Assesses word diversity (TTR)  
- **Filler Words Detection** – Tracks unnecessary fillers  
- **Sentiment Analysis** – Evaluates emotional tone  

### 📌 Detailed Analytics Includes:
- Sentence-wise sentiment evaluation  
- Spelling error detection  
- Vocabulary complexity scoring  
- Filler word breakdown  
- Flow & structure assessment  
- Weighted scoring system with feedback  

---

## 🛠️ Technology Stack

| Component      | Technology |
|----------------|------------|
| **Backend**    | Python, Flask |
| **Frontend**   | HTML, CSS, JavaScript |
| **AI/ML**      | VADER Sentiment, PySpellChecker |
| **Deployment** | Render |

---

## 📁 Project Structure

student-introduction-analyzer/
│
├── app.py # Main Flask application
├── requirements.txt # Python dependencies
├── Sample text for case study.txt # Sample testing file
├── index.html # Frontend UI
└── README.md # Project documentation

---

## 🚀 Local Installation

### 1️⃣ Clone the repository
```bash
git clone https://github.com/Theheerpatel/AI-based-student-introduction-analyzer.git
cd AI-based-student-introduction-analyzer

### 2️⃣ Create & activate a virtual environment
```bash
python -m venv venv
source venv/bin/activate        # For Windows: venv\Scripts\activate

### 3️⃣ Install dependencies
```bash
pip install -r requirements.txt

### 4️⃣ Run the application
```bash
python app.py

### 5️⃣ Open in the browser
```bash
http://localhost:5000
