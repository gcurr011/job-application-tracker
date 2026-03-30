# Job Application Tracker

A full-stack web application to track job applications, built with MySQL, Python/Flask, and HTML/CSS.

**Course:** COP4751 — Advanced Database Management  
**Project:** Full-Stack Database Application with GenAI Integration

---

## Features

- **Dashboard** — Stats overview and recent activity
- **Companies** — Add, view, edit, delete companies
- **Jobs** — Add, view, edit, delete job listings with skill requirements
- **Applications** — Track application status, resume version, and cover letters
- **Contacts** — Store recruiter and hiring manager info
- **Job Match** — Enter your skills and see jobs ranked by match percentage

---

## Tech Stack

| Layer    | Technology                  |
|----------|-----------------------------|
| Database | MySQL 8.x                   |
| Backend  | Python 3 + Flask            |
| Frontend | HTML5 + CSS3 (no framework) |
| Auth     | None (local use)            |

---

## Prerequisites

- Python 3.8 or higher
- MySQL 8.x running locally
- pip

---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/job-tracker.git
cd job-tracker
```

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 3. Set Up the Database

Option A — If starting fresh:
```sql
-- Run schema.sql in MySQL Workbench or CLI
mysql -u root -p < schema.sql
```

Option B — If you already have the `job_tracker` database from the assignments, skip this step.

### 4. Configure Your Database Password

Open `database.py` and update line 16:

```python
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'YOUR_PASSWORD_HERE',   # <-- change this
    'database': 'job_tracker'
}
```

### 5. Run the Application

```bash
python app.py
```

Open your browser to: **http://localhost:5000**

---

## Project Structure

```
job_tracker/
├── app.py              # Flask routes
├── database.py         # Database functions (CONFIGURE PASSWORD HERE)
├── schema.sql          # Database creation script
├── requirements.txt    # Python dependencies
├── AI_USAGE.md         # GenAI documentation
├── README.md           # This file
├── templates/
│   ├── base.html
│   ├── dashboard.html
│   ├── companies.html
│   ├── company_form.html
│   ├── jobs.html
│   ├── job_form.html
│   ├── applications.html
│   ├── application_form.html
│   ├── contacts.html
│   ├── contact_form.html
│   └── job_match.html
└── static/
    └── style.css
```

---

## Using the Job Match Feature

1. Go to **Jobs** and add jobs with skill requirements (comma-separated, e.g. `Python, SQL, Flask`)
2. Go to **Job Match** in the navbar
3. Enter your skills (e.g. `Python, SQL, HTML`)
4. The app ranks all jobs by match percentage, showing which skills you have and which are missing

---

## Troubleshooting

| Error | Fix |
|-------|-----|
| `Access denied for user 'root'` | Wrong password in `database.py` |
| `Unknown database 'job_tracker'` | Run `schema.sql` first |
| `ModuleNotFoundError: flask` | Run `pip install -r requirements.txt` |
| Port 5000 already in use | Change `app.run(port=5001)` in `app.py` |
