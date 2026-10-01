# News Application - Capstone Project

A full-stack, role-based news platform built with **Django**, **Django REST Framework (DRF)**, **MySQL**, and **Bootstrap 5**, containerized with **Docker** and documented using **Sphinx**.

The platform supports three user roles — **readers**, **journalists**, and **editors** — allowing journalists to submit draft articles, editors to review and approve content, and readers to browse verified news items on a public feed. The application also includes REST API endpoints with token authentication, automated signals for background actions, a role-based dashboard, and an automated unit test suite.

## Features

- Role-based access control for readers, journalists, and editors
- Journalist article submission workflow (pending editor approval)
- Editor dashboard for reviewing, approving, or rejecting article drafts
- Public newsfeed displaying only approved articles
- Django REST Framework API endpoints with token authentication
- Automated signals for event logging and background actions
- Automated unit test suite verifying permissions, workflows, and API views
- Automated Sphinx documentation generated directly from Python docstrings
- Docker containerization for instant deployment with MySQL

## Prerequisites

- Git
- Docker Desktop installed and running (for Docker setup)
- Python 3.10+ (for local setup without Docker)

## Quick Start (Using Docker)

1. **Clone the repository:**

```bash
   git clone https://github.com/Jadendewet18/Capstone-NewsApplication.git
   cd Capstone-NewsApplication
```

2. **Configure environment variables / passwords:**

   Create a `.env` file in the root directory (or set environment variables) with your database password:

```env
   MYSQL_ROOT_PASSWORD=your_secure_password
```

3. **Start the application with Docker Compose:**

```bash
   docker-compose up --build
```

4. **Access the application:**

   - Web Application: http://localhost:8000
   - MySQL Database: running on port `3306`

## Local Development Setup (Without Docker)

1. **Clone and navigate to the project directory:**

```bash
   git clone https://github.com/Jadendewet18/Capstone-NewsApplication.git
   cd Capstone-NewsApplication
```

2. **Create and activate a virtual environment:**

   - Windows (PowerShell):

```powershell
     python -m venv venv
     venv\Scripts\Activate.ps1
```

   - macOS/Linux:

```bash
     python3 -m venv venv
     source venv/bin/activate
```

3. **Install dependencies:**

```bash
   pip install -r requirements.txt
```

4. **Configure database & apply migrations:**

   Ensure MySQL is running locally and database credentials are set, then run:

```bash
   python manage.py makemigrations
   python manage.py migrate
```

5. **Create a superuser & run the development server:**

```bash
   python manage.py createsuperuser
   python manage.py runserver
```

   Access the app at http://127.0.0.1:8000/.

## Generating & Viewing Sphinx Documentation

Sphinx auto-generates project documentation directly from module, class, and view docstrings.

1. **Build the HTML documentation:**

```bash
   cd docs
   python -m sphinx . _build/html
```

2. **View the documentation:**

   Open `docs/_build/html/index.html` in any web browser.