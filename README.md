# VIT Complaint Management System

A Django-based Complaint Management System for Victorian Institute of Technology Melbourne.

The system allows students, faculty, and staff to lodge complaints, automatically assign reviewers based on role hierarchy, upload optional evidence, post comments, update verdicts, and view complaint histories.

---

## Features

- User login and logout
- Role-based complaint management
- Automatic reviewer assignment
- Complaint lodging with optional evidence upload
- Active and previous complaint history
- Complaint editing by complainant
- Reviewer comments and verdict updates
- Complaint history/audit trail
- Accused user privacy protection
- Local SQLite database
- Django admin panel
- SonarQube-ready project structure

---

## Technology Used

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| Django | Web framework |
| SQLite | Local database |
| HTML | Page structure |
| Bootstrap | Basic visual styling |
| SonarQube | Code quality analysis |
| Coverage.py | Test coverage report |

---

## User Roles

The system supports the following roles:

- Student
- Faculty
- Unit Coordinator
- Admin Staff
- Admin Director
- Pro-VC
- VC

---

## Reviewer Assignment Rules

| Accused Role | Assigned Reviewer |
|---|---|
| Student | Faculty |
| Faculty | Unit Coordinator |
| Unit Coordinator | Admin Director |
| Admin Staff | Admin Director |
| Admin Director | Pro-VC |
| Pro-VC | VC |
| VC | Not allowed |

No user can lodge a complaint against the VC.

---

## Project Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY_NAME.git
cd YOUR_REPOSITORY_NAME
```

Replace `YOUR_USERNAME` and `YOUR_REPOSITORY_NAME` with your actual GitHub username and repository name.

---

### 2. Create a Virtual Environment

For macOS/Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

For Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

---

### 3. Install Required Packages

```bash
pip install -r requirements.txt
```

If `requirements.txt` is not available, install Django manually:

```bash
pip install django
```

Then create the requirements file:

```bash
pip freeze > requirements.txt
```

---

### 4. Apply Database Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

This will create the local SQLite database.

---

### 5. Create a Superuser

```bash
python manage.py createsuperuser
```

Example:

```text
Username: admin
Email: admin@vit.edu.au
Password: Admin@12345
```

---

### 6. Run the Development Server

```bash
python manage.py runserver
```

Open the project in your browser:

```text
http://127.0.0.1:8000/
```

Open the Django admin panel:

```text
http://127.0.0.1:8000/admin/
```

---

## Creating Demo Users

After logging into the Django admin panel, create users and profiles manually.

### Recommended Demo Users

| Username | Password | Role |
|---|---|---|
| student1 | Testpass123 | Student |
| faculty1 | Testpass123 | Faculty |
| uc1 | Testpass123 | Unit Coordinator |
| staff1 | Testpass123 | Admin Staff |
| director1 | Testpass123 | Admin Director |
| provc1 | Testpass123 | Pro-VC |
| vc1 | Testpass123 | VC |

For each user:

1. Go to `Users`
2. Create a new user
3. Go to `Profiles`
4. Create a profile for that user
5. Assign the correct role

---

## How to Use the System

### 1. Login

Go to:

```text
http://127.0.0.1:8000/login/
```

Login using one of the demo users.

---

### 2. Lodge a Complaint

1. Click `Lodge Complaint`
2. Enter complaint title
3. Enter complaint description
4. Select the accused person
5. Upload evidence if needed
6. Submit the complaint

The system will automatically assign a reviewer based on the accused user's role.

---

### 3. View Active Complaints

Click:

```text
Active
```

This page shows complaints that are currently active or under review.

---

### 4. View Previous Complaints

Click:

```text
Previous
```

This page shows resolved, rejected, or closed complaints.

---

### 5. View Complaint Details

Open any complaint to view:

- Complaint title
- Description
- Status
- Accused person
- Reviewer
- Evidence
- Comments
- Verdict
- Complaint history

The accused person cannot see the complainant's identity.

---

### 6. Edit a Complaint

Only the complainant can edit a complaint.

A complaint cannot be edited after it is:

- Resolved
- Rejected
- Closed

The complainant and reviewer can see the edit history.

---

### 7. Reviewer Verdict

Only the assigned reviewer can:

- Add reviewer comments
- Update complaint status
- Add verdict

---

## Running Tests

Run Django tests:

```bash
python manage.py test
```

Run tests with coverage:

```bash
coverage run manage.py test
coverage report
coverage xml
```

The `coverage.xml` file can be used for SonarQube analysis.

---

## Running SonarQube Analysis

Make sure SonarQube is running locally.

Example using Docker:

```bash
docker run -d --name sonarqube -p 9000:9000 sonarqube:lts-community
```

Open:

```text
http://localhost:9000
```

Then run:

```bash
sonar-scanner
```

Make sure your project contains a `sonar-project.properties` file before running the scanner.

---

## Example `sonar-project.properties`

Create a file named:

```text
sonar-project.properties
```

Add this:

```properties
sonar.projectKey=vit-complaint-management
sonar.projectName=VIT Complaint Management System
sonar.projectVersion=1.0

sonar.sources=.
sonar.exclusions=**/migrations/**,**/venv/**,**/__pycache__/**,**/static/**,**/media/**,manage.py,config/settings.py,config/asgi.py,config/wsgi.py

sonar.python.version=3.11
sonar.sourceEncoding=UTF-8
sonar.python.coverage.reportPaths=coverage.xml
```

---

## Project Structure

```text
vit_complaint_system/
│
├── complaints/
│   ├── migrations/
│   ├── templates/
│   │   └── complaints/
│   │       ├── base.html
│   │       ├── login.html
│   │       ├── dashboard.html
│   │       ├── lodge_complaint.html
│   │       ├── complaint_list.html
│   │       ├── complaint_detail.html
│   │       └── edit_complaint.html
│   │
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── services.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
│
├── config/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── media/
├── db.sqlite3
├── manage.py
├── requirements.txt
├── sonar-project.properties
└── README.md
```

---

## Recommended `.gitignore`

Create a file named:

```text
.gitignore
```

Add this:

```gitignore
venv/
__pycache__/
*.pyc
db.sqlite3
media/
coverage.xml
.coverage
htmlcov/
.env
.DS_Store
```

---

## Important Notes

- This project uses SQLite as the local database.
- Uploaded evidence files are stored inside the `media/` directory.
- The `db.sqlite3` file should not be pushed to GitHub for production use.
- Demo users should be created manually through the Django admin panel.
- The system is designed as an academic prototype.
- The system can be extended with stronger security, email notifications, advanced reporting, and role-based dashboards.

---

## Common Commands

Activate virtual environment on macOS/Linux:

```bash
source venv/bin/activate
```

Activate virtual environment on Windows:

```bash
venv\Scripts\activate
```

Run migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

Create admin user:

```bash
python manage.py createsuperuser
```

Run server:

```bash
python manage.py runserver
```

Run tests:

```bash
python manage.py test
```

Generate coverage report:

```bash
coverage run manage.py test
coverage xml
```

Run SonarQube scanner:

```bash
sonar-scanner
```

---

## Academic Purpose

This project was developed for academic purposes as a Complaint Management System prototype for Victorian Institute of Technology Melbourne.

It demonstrates:

- Django web development
- Local database management
- Role-based access control
- File upload handling
- Complaint workflow automation
- Audit history tracking
- Basic software quality analysis using SonarQube

---

## Author

Developed by Tanvir Opy for academic project work.
