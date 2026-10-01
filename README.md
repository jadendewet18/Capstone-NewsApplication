# News Application - Capstone Project

A full-stack, role-based news platform built with Django, Django REST Framework (DRF), MySQL, and Bootstrap 5. The platform supports three user roles — **readers**, **journalists**, and **editors** — allowing journalists to submit draft articles, editors to review and approve content, and readers to browse verified news items on a public feed. The application also includes REST API endpoints with token authentication, automated signals for background actions, a role-based dashboard, and an automated unit test suite.

## Features

- Role-based access control for readers, journalists, and editors
- Journalist article submission workflow (pending editor approval)
- Editor dashboard for reviewing, approving, or rejecting article drafts
- Public newsfeed displaying only approved articles
- Django REST Framework API endpoints with token authentication
- Automated signals for event logging and background actions
- Automated unit test suite verifying permissions, workflows, and API views

## Prerequisites

- Python 3.10+ installed and available on your PATH
- pip (comes bundled with Python)
- Git (optional, for cloning the repository)
- MySQL / MariaDB (via XAMPP or local server)

## Getting Started

Follow the steps below to get a local copy of the project up and running with MySQL.

### 1. Clone the Repository and Navigate to Project Folder

Open your terminal and clone the repository, then navigate into the project directory:

git clone <https://github.com/hyperiondev-bootcamps/JD26020020047>
cd CAPSTONE_PROJECT-NewsApplication

### 2. Create and Activate a Virtual Environment

A virtual environment keeps this project's dependencies isolated from your system Python installation.

Windows (PowerShell):

python -m venv venv
venv\Scripts\Activate.ps1

> If you get a script execution error, you may need to allow scripts for the current session first:
> Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

macOS/Linux:

python3 -m venv venv
source venv/bin/activate

Once activated, you should see (venv) at the start of your terminal prompt.

### 3. Install Dependencies

With your virtual environment activated, install the required packages (including the database connector) from requirements.txt:

pip install -r requirements.txt

### 4. Create the Database

1. Start your local database server (e.g., MySQL via XAMPP).
2. Create an empty database named news_db:
   CREATE DATABASE news_db;

### 5. Update Database Credentials in settings.py

Open news_project/settings.py and configure your DATABASES setting to use the MySQL backend pointing to your local news_db, root user, and password.

### 6. Apply Database Migrations

Set up the database schema by running Django's migrations:

python manage.py makemigrations
python manage.py migrate

### 7. Create a Superuser

Create an admin account so you can access the Django admin panel:

python manage.py createsuperuser

You'll be prompted to enter a username, email address, and password.

### 8. Run the Local Development Server

Start the development server:

python manage.py runserver

The application will be available at http://127.0.0.1:8000/, and the admin panel at http://127.0.0.1:8000/admin/.