"""
app.py - Main Flask Application
Job Application Tracker
COP4751 - Advanced Database Management
"""

from flask import Flask, render_template, request, redirect, url_for, flash
import database as db

app = Flask(__name__)
app.secret_key = 'job_tracker_secret_key_2024'  # needed for flash messages


# ─── DASHBOARD ────────────────────────────────────────────────────────────────

@app.route('/')
def dashboard():
    stats = db.get_dashboard_stats()
    return render_template('dashboard.html', stats=stats)


# ─── COMPANIES ────────────────────────────────────────────────────────────────

@app.route('/companies')
def companies():
    all_companies = db.get_all_companies()
    return render_template('companies.html', companies=all_companies)


@app.route('/companies/add', methods=['GET', 'POST'])
def add_company():
    if request.method == 'POST':
        data = request.form
        if not data.get('company_name'):
            flash('Company name is required.', 'error')
            return render_template('company_form.html', company=data, action='Add')
        db.add_company(data)
        flash('Company added successfully!', 'success')
        return redirect(url_for('companies'))
    return render_template('company_form.html', company={}, action='Add')


@app.route('/companies/edit/<int:company_id>', methods=['GET', 'POST'])
def edit_company(company_id):
    if request.method == 'POST':
        data = request.form
        if not data.get('company_name'):
            flash('Company name is required.', 'error')
            return render_template('company_form.html', company=data, action='Edit')
        db.update_company(company_id, data)
        flash('Company updated!', 'success')
        return redirect(url_for('companies'))
    company = db.get_company(company_id)
    return render_template('company_form.html', company=company, action='Edit')


@app.route('/companies/delete/<int:company_id>', methods=['POST'])
def delete_company(company_id):
    db.delete_company(company_id)
    flash('Company deleted.', 'success')
    return redirect(url_for('companies'))


# ─── JOBS ─────────────────────────────────────────────────────────────────────

@app.route('/jobs')
def jobs():
    all_jobs = db.get_all_jobs()
    return render_template('jobs.html', jobs=all_jobs)


@app.route('/jobs/add', methods=['GET', 'POST'])
def add_job():
    companies = db.get_all_companies()
    if request.method == 'POST':
        data = request.form
        if not data.get('job_title'):
            flash('Job title is required.', 'error')
            return render_template('job_form.html', job=data, companies=companies, action='Add')
        db.add_job(data)
        flash('Job added!', 'success')
        return redirect(url_for('jobs'))
    return render_template('job_form.html', job={}, companies=companies, action='Add')


@app.route('/jobs/edit/<int:job_id>', methods=['GET', 'POST'])
def edit_job(job_id):
    companies = db.get_all_companies()
    if request.method == 'POST':
        data = request.form
        if not data.get('job_title'):
            flash('Job title is required.', 'error')
            return render_template('job_form.html', job=data, companies=companies, action='Edit')
        db.update_job(job_id, data)
        flash('Job updated!', 'success')
        return redirect(url_for('jobs'))
    job = db.get_job(job_id)
    # Convert requirements list back to comma string for the form
    if job and isinstance(job.get('requirements'), list):
        job['requirements_str'] = ', '.join(job['requirements'])
    return render_template('job_form.html', job=job, companies=companies, action='Edit')


@app.route('/jobs/delete/<int:job_id>', methods=['POST'])
def delete_job(job_id):
    db.delete_job(job_id)
    flash('Job deleted.', 'success')
    return redirect(url_for('jobs'))


# ─── APPLICATIONS ─────────────────────────────────────────────────────────────

@app.route('/applications')
def applications():
    all_apps = db.get_all_applications()
    return render_template('applications.html', applications=all_apps)


@app.route('/applications/add', methods=['GET', 'POST'])
def add_application():
    jobs = db.get_all_jobs()
    if request.method == 'POST':
        data = request.form
        if not data.get('application_date'):
            flash('Application date is required.', 'error')
            return render_template('application_form.html', application=data, jobs=jobs, action='Add')
        db.add_application(data)
        flash('Application added!', 'success')
        return redirect(url_for('applications'))
    return render_template('application_form.html', application={}, jobs=jobs, action='Add')


@app.route('/applications/edit/<int:application_id>', methods=['GET', 'POST'])
def edit_application(application_id):
    jobs = db.get_all_jobs()
    if request.method == 'POST':
        data = request.form
        if not data.get('application_date'):
            flash('Application date is required.', 'error')
            return render_template('application_form.html', application=data, jobs=jobs, action='Edit')
        db.update_application(application_id, data)
        flash('Application updated!', 'success')
        return redirect(url_for('applications'))
    application = db.get_application(application_id)
    return render_template('application_form.html', application=application, jobs=jobs, action='Edit')


@app.route('/applications/delete/<int:application_id>', methods=['POST'])
def delete_application(application_id):
    db.delete_application(application_id)
    flash('Application deleted.', 'success')
    return redirect(url_for('applications'))


# ─── CONTACTS ─────────────────────────────────────────────────────────────────

@app.route('/contacts')
def contacts():
    all_contacts = db.get_all_contacts()
    return render_template('contacts.html', contacts=all_contacts)


@app.route('/contacts/add', methods=['GET', 'POST'])
def add_contact():
    companies = db.get_all_companies()
    if request.method == 'POST':
        data = request.form
        if not data.get('contact_name'):
            flash('Contact name is required.', 'error')
            return render_template('contact_form.html', contact=data, companies=companies, action='Add')
        db.add_contact(data)
        flash('Contact added!', 'success')
        return redirect(url_for('contacts'))
    return render_template('contact_form.html', contact={}, companies=companies, action='Add')


@app.route('/contacts/edit/<int:contact_id>', methods=['GET', 'POST'])
def edit_contact(contact_id):
    companies = db.get_all_companies()
    if request.method == 'POST':
        data = request.form
        if not data.get('contact_name'):
            flash('Contact name is required.', 'error')
            return render_template('contact_form.html', contact=data, companies=companies, action='Edit')
        db.update_contact(contact_id, data)
        flash('Contact updated!', 'success')
        return redirect(url_for('contacts'))
    contact = db.get_contact(contact_id)
    return render_template('contact_form.html', contact=contact, companies=companies, action='Edit')


@app.route('/contacts/delete/<int:contact_id>', methods=['POST'])
def delete_contact(contact_id):
    db.delete_contact(contact_id)
    flash('Contact deleted.', 'success')
    return redirect(url_for('contacts'))


# ─── JOB MATCH ────────────────────────────────────────────────────────────────

@app.route('/job-match', methods=['GET', 'POST'])
def job_match():
    results = []
    user_skills = ''
    if request.method == 'POST':
        user_skills = request.form.get('skills', '')
        if user_skills.strip():
            results = db.calculate_job_match(user_skills)
        else:
            flash('Please enter at least one skill.', 'error')
    return render_template('job_match.html', results=results, user_skills=user_skills)


# ─── RUN ──────────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    app.run(debug=True)
