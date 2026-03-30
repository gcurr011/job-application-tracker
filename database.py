# database.py - Database connection and helper functions
# Job Application Tracker

import mysql.connector
from mysql.connector import Error
import json

# Configure your database connection here
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'database': 'job_tracker'
}


def get_connection():
    return mysql.connector.connect(**DB_CONFIG)


# DASHBOARD

def get_dashboard_stats():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    stats = {}

    cursor.execute("SELECT COUNT(*) AS count FROM companies")
    stats['companies'] = cursor.fetchone()['count']

    cursor.execute("SELECT COUNT(*) AS count FROM jobs")
    stats['jobs'] = cursor.fetchone()['count']

    cursor.execute("SELECT COUNT(*) AS count FROM applications")
    stats['applications'] = cursor.fetchone()['count']

    cursor.execute("SELECT COUNT(*) AS count FROM contacts")
    stats['contacts'] = cursor.fetchone()['count']

    cursor.execute("SELECT status, COUNT(*) AS count FROM applications GROUP BY status")
    stats['by_status'] = cursor.fetchall()

    cursor.execute("""
        SELECT a.application_id, a.application_date, a.status,
               j.job_title, c.company_name
        FROM applications a
        JOIN jobs j ON a.job_id = j.job_id
        JOIN companies c ON j.company_id = c.company_id
        ORDER BY a.application_date DESC
        LIMIT 5
    """)
    stats['recent'] = cursor.fetchall()

    conn.close()
    return stats


# COMPANIES

def get_all_companies():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM companies ORDER BY company_name")
    rows = cursor.fetchall()
    conn.close()
    return rows


def get_company(company_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM companies WHERE company_id = %s", (company_id,))
    row = cursor.fetchone()
    conn.close()
    return row


def add_company(data):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO companies (company_name, industry, website, city, state, notes)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (data['company_name'], data.get('industry'), data.get('website'),
          data.get('city'), data.get('state'), data.get('notes')))
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return new_id


def update_company(company_id, data):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE companies
        SET company_name=%s, industry=%s, website=%s, city=%s, state=%s, notes=%s
        WHERE company_id=%s
    """, (data['company_name'], data.get('industry'), data.get('website'),
          data.get('city'), data.get('state'), data.get('notes'), company_id))
    conn.commit()
    conn.close()


def delete_company(company_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM companies WHERE company_id = %s", (company_id,))
    conn.commit()
    conn.close()


# JOBS

def get_all_jobs():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT j.*, c.company_name
        FROM jobs j
        LEFT JOIN companies c ON j.company_id = c.company_id
        ORDER BY j.date_posted DESC
    """)
    rows = cursor.fetchall()
    for row in rows:
        if row['requirements']:
            if isinstance(row['requirements'], str):
                row['requirements'] = json.loads(row['requirements'])
        else:
            row['requirements'] = []
    conn.close()
    return rows


def get_job(job_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT j.*, c.company_name
        FROM jobs j
        LEFT JOIN companies c ON j.company_id = c.company_id
        WHERE j.job_id = %s
    """, (job_id,))
    row = cursor.fetchone()
    if row and row['requirements']:
        if isinstance(row['requirements'], str):
            row['requirements'] = json.loads(row['requirements'])
    elif row:
        row['requirements'] = []
    conn.close()
    return row


def add_job(data):
    conn = get_connection()
    cursor = conn.cursor()
    skills_raw = data.get('requirements', '')
    skills_list = [s.strip() for s in skills_raw.split(',') if s.strip()]
    requirements_json = json.dumps(skills_list)
    cursor.execute("""
        INSERT INTO jobs (company_id, job_title, job_type, salary_min, salary_max,
                          job_url, date_posted, requirements)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, (data.get('company_id') or None,
          data['job_title'],
          data.get('job_type') or None,
          data.get('salary_min') or None,
          data.get('salary_max') or None,
          data.get('job_url') or None,
          data.get('date_posted') or None,
          requirements_json))
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return new_id


def update_job(job_id, data):
    conn = get_connection()
    cursor = conn.cursor()
    skills_raw = data.get('requirements', '')
    skills_list = [s.strip() for s in skills_raw.split(',') if s.strip()]
    requirements_json = json.dumps(skills_list)
    cursor.execute("""
        UPDATE jobs
        SET company_id=%s, job_title=%s, job_type=%s, salary_min=%s, salary_max=%s,
            job_url=%s, date_posted=%s, requirements=%s
        WHERE job_id=%s
    """, (data.get('company_id') or None,
          data['job_title'],
          data.get('job_type') or None,
          data.get('salary_min') or None,
          data.get('salary_max') or None,
          data.get('job_url') or None,
          data.get('date_posted') or None,
          requirements_json,
          job_id))
    conn.commit()
    conn.close()


def delete_job(job_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM jobs WHERE job_id = %s", (job_id,))
    conn.commit()
    conn.close()


# APPLICATIONS

def get_all_applications():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT a.*, j.job_title, c.company_name
        FROM applications a
        LEFT JOIN jobs j ON a.job_id = j.job_id
        LEFT JOIN companies c ON j.company_id = c.company_id
        ORDER BY a.application_date DESC
    """)
    rows = cursor.fetchall()
    conn.close()
    return rows


def get_application(application_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT a.*, j.job_title, c.company_name
        FROM applications a
        LEFT JOIN jobs j ON a.job_id = j.job_id
        LEFT JOIN companies c ON j.company_id = c.company_id
        WHERE a.application_id = %s
    """, (application_id,))
    row = cursor.fetchone()
    conn.close()
    return row


def add_application(data):
    conn = get_connection()
    cursor = conn.cursor()
    cover = 1 if data.get('cover_letter_sent') == 'on' else 0
    cursor.execute("""
        INSERT INTO applications (job_id, application_date, status,
                                  resume_version, cover_letter_sent)
        VALUES (%s, %s, %s, %s, %s)
    """, (data.get('job_id') or None,
          data['application_date'],
          data.get('status', 'Applied'),
          data.get('resume_version') or None,
          cover))
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return new_id


def update_application(application_id, data):
    conn = get_connection()
    cursor = conn.cursor()
    cover = 1 if data.get('cover_letter_sent') == 'on' else 0
    cursor.execute("""
        UPDATE applications
        SET job_id=%s, application_date=%s, status=%s,
            resume_version=%s, cover_letter_sent=%s
        WHERE application_id=%s
    """, (data.get('job_id') or None,
          data['application_date'],
          data.get('status', 'Applied'),
          data.get('resume_version') or None,
          cover,
          application_id))
    conn.commit()
    conn.close()


def delete_application(application_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM applications WHERE application_id = %s", (application_id,))
    conn.commit()
    conn.close()


# CONTACTS

def get_all_contacts():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT ct.*, c.company_name
        FROM contacts ct
        LEFT JOIN companies c ON ct.company_id = c.company_id
        ORDER BY ct.contact_name
    """)
    rows = cursor.fetchall()
    conn.close()
    return rows


def get_contact(contact_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT ct.*, c.company_name
        FROM contacts ct
        LEFT JOIN companies c ON ct.company_id = c.company_id
        WHERE ct.contact_id = %s
    """, (contact_id,))
    row = cursor.fetchone()
    conn.close()
    return row


def add_contact(data):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO contacts (company_id, contact_name, title, email, phone,
                              linkedin_url, notes)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (data.get('company_id') or None,
          data['contact_name'],
          data.get('title') or None,
          data.get('email') or None,
          data.get('phone') or None,
          data.get('linkedin_url') or None,
          data.get('notes') or None))
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return new_id


def update_contact(contact_id, data):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE contacts
        SET company_id=%s, contact_name=%s, title=%s, email=%s, phone=%s,
            linkedin_url=%s, notes=%s
        WHERE contact_id=%s
    """, (data.get('company_id') or None,
          data['contact_name'],
          data.get('title') or None,
          data.get('email') or None,
          data.get('phone') or None,
          data.get('linkedin_url') or None,
          data.get('notes') or None,
          contact_id))
    conn.commit()
    conn.close()


def delete_contact(contact_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM contacts WHERE contact_id = %s", (contact_id,))
    conn.commit()
    conn.close()


# JOB MATCH

def calculate_job_match(user_skills_input):
    user_skills = [s.strip().lower() for s in user_skills_input.split(',') if s.strip()]
    if not user_skills:
        return []

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT j.job_id, j.job_title, j.requirements,
               c.company_name, j.salary_min, j.salary_max
        FROM jobs j
        LEFT JOIN companies c ON j.company_id = c.company_id
        WHERE j.requirements IS NOT NULL AND j.requirements != '[]'
    """)
    jobs = cursor.fetchall()
    conn.close()

    results = []
    for job in jobs:
        reqs = job['requirements']
        if isinstance(reqs, str):
            reqs = json.loads(reqs)
        if not reqs:
            continue
        job_skills = [r.strip().lower() for r in reqs]
        matched = [s for s in job_skills if s in user_skills]
        missing = [s for s in job_skills if s not in user_skills]
        pct = round(len(matched) / len(job_skills) * 100) if job_skills else 0
        results.append({
            'job_id': job['job_id'],
            'job_title': job['job_title'],
            'company_name': job['company_name'],
            'salary_min': job['salary_min'],
            'salary_max': job['salary_max'],
            'total_skills': len(job_skills),
            'matched': matched,
            'missing': missing,
            'percentage': pct,
        })

    results.sort(key=lambda x: x['percentage'], reverse=True)
    return results