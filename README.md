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
