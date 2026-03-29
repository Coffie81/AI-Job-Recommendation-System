# 🤖 AI-Powered Job Recommendation System

An intelligent, end-to-end machine learning web application that recommends jobs to users based on their skills and experience. Built with Flask, SQLite, and NLP-based TF-IDF cosine similarity.

---

## 📌 Project Overview

In today's competitive job market, finding the right opportunity based on your skillset can be overwhelming. This system solves that by automatically matching users to relevant jobs using machine learning — simulating how platforms like LinkedIn and Internshala work under the hood.

---

## ✨ Features

- 🔍 **Skill-Based Job Recommendations** — Enter your skills and get ranked job matches instantly
- 📄 **Resume Upload & Skill Extraction** — Upload a PDF or DOCX resume and skills are auto-extracted
- 📊 **Skill Gap Analysis** — See which skills you already have and which ones you need to learn for each job
- 💾 **Database Integration** — All users, jobs, and recommendations are stored in SQLite
- 🚫 **Duplicate User Detection** — Prevents duplicate registrations with the same email
- 🎨 **Clean UI** — Simple, responsive frontend with match percentage and progress bars

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Language | Python |
| Backend | Flask |
| Database | SQLite |
| ML Model | TF-IDF + Cosine Similarity (Scikit-learn) |
| Resume Parsing | PyMuPDF, Python-Docx |
| Frontend | HTML, CSS, JavaScript |

---

## 📁 Project Structure

```
job-recommender/
│
├── app.py               # Flask backend — all routes and logic
├── model.py             # ML model — TF-IDF vectorization & cosine similarity
├── database.py          # Database setup, queries, and helpers
├── resume_parser.py     # Resume upload & skill extraction logic
├── data.csv             # Jobs dataset (520 real job listings)
├── database.db          # SQLite database (auto-generated)
│
├── templates/
│   ├── index.html       # Home page — input form
│   └── results.html     # Results page — recommendations & skill gap
│
├── static/
│   └── style.css        # Styling for all pages
│
├── uploads/             # Temporary folder for resume uploads
└── README.md            # Project documentation
```

---

## ⚙️ Setup & Installation

### 1. Clone or download the project

```bash
git clone https://github.com/yourusername/job-recommender.git
cd job-recommender
```

### 2. Install required libraries

```bash
pip install flask scikit-learn pandas numpy pymupdf python-docx
```

### 3. Initialize the database

```bash
python database.py
```

You should see:
```
✅ Tables created successfully.
✅ 520 jobs loaded into database.
```

### 4. Run the application

```bash
python app.py
```

### 5. Open in browser

```
http://127.0.0.1:5000
```

---

## 🧠 How the ML Model Works

```
User enters skills
        ↓
TF-IDF Vectorizer converts skills + job descriptions into numerical vectors
        ↓
Cosine Similarity measures closeness between user vector and each job vector
        ↓
Jobs ranked from highest to lowest similarity score
        ↓
Top 5 jobs returned with match percentage + skill gap analysis
```

The model runs on demand — no pre-training or saved model file needed. It trains instantly every time a user submits their skills.

---

## 🗄️ Database Schema

### Users Table
| Column | Type | Description |
|---|---|---|
| id | INTEGER | Primary key |
| name | TEXT | Full name |
| email | TEXT | Unique email |
| skills | TEXT | User's skills |
| experience | INTEGER | Years of experience |

### Jobs Table
| Column | Type | Description |
|---|---|---|
| id | INTEGER | Primary key |
| job_title | TEXT | Title of the job |
| description | TEXT | Full job description |

### Recommendations Table
| Column | Type | Description |
|---|---|---|
| id | INTEGER | Primary key |
| user_id | INTEGER | Foreign key → Users |
| job_id | INTEGER | Foreign key → Jobs |
| score | REAL | Match score (0–100) |

---

## 📊 Example Output

**Input:** Python, Machine Learning, SQL

**Output:**
```
1. Data Scientist         — 45.3% Match
2. ML Engineer            — 38.7% Match
3. Business Analyst       — 31.2% Match
4. Data Analyst           — 28.9% Match
5. Software Engineer      — 24.1% Match
```

Each result also shows:
- ✅ Skills you already have
- 📚 Skills to learn
- 📊 Skill coverage percentage

---

## 🚀 Advanced Features Implemented

- [x] Resume upload and automatic skill extraction (PDF & DOCX)
- [x] Skill gap analysis per recommended job
- [x] Duplicate user detection with friendly error handling
- [x] Match percentage with visual progress bars
- [x] Recommendation history stored in database

---

## 📦 Dependencies

```
flask
scikit-learn
pandas
numpy
pymupdf
python-docx
```

Install all at once:
```bash
pip install flask scikit-learn pandas numpy pymupdf python-docx
```

---

## 👤 Author

Built as part of a Machine Learning Internship Programme.  
Demonstrates end-to-end ML system development — from data preprocessing and model building to database integration and backend deployment.

---

## 📄 License

This project was built for educational and internship purposes.
