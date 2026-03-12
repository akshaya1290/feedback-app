# Student Feedback System - Backend Setup Guide

## Overview
Complete Django REST API for a comprehensive student feedback management system with support for students, instructors, and admin users.

## Features

### 📋 Core Features
- **User Authentication**: Student, Instructor, and Admin registration & login
- **Feedback Management**: Submit, view, and filter feedback
- **Analytics**: Course ratings, instructor performance, feedback distribution
- **Comparison**: Compare feedback across courses
- **Role-Based Access**: Different permissions for student, instructor, and admin

### 📊 Analytics & Reporting
- Overall feedback statistics
- Course performance metrics
- Instructor ratings and notifications
- Negative feedback tracking (≤2 stars)
- Top-performing and struggling courses

## Installation

### 1. Prerequisites
- Python 3.8+
- Django 3.2+
- pip

### 2. Setup Database

```bash
# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser for admin access
python manage.py createsuperuser
```

### 3. Create Initial Data

```python
# Python manage.py shell
from feedback.models import Institution, Course

# Create institution
inst = Institution.objects.create(
    name="ABC University",
    location="New York, USA",
    description="Premier educational institution"
)

# Create courses
courses_data = [
    ("Data Science 101", "Dr. Smith"),
    ("Web Development", "Prof. Johnson"),
    ("Machine Learning", "Dr. Williams"),
    ("Python Basics", "Prof. Brown"),
    ("Cloud Computing", "Dr. Davis"),
]

for course_name, instructor in courses_data:
    Course.objects.create(
        name=course_name,
        instructor=instructor,
        institution=inst
    )
```

## API Endpoints

### Authentication
```
POST   /api/auth/register/student/      - Register student
POST   /api/auth/register/instructor/   - Register instructor
POST   /api/auth/register/admin/        - Register admin
POST   /api/auth/login/                 - Login user
POST   /api/auth/logout/                - Logout user
```

### Institutions
```
GET    /api/institutions/               - List all institutions
GET    /api/institutions/<id>/          - Get institution details
```

### Courses
```
GET    /api/courses/                    - List all courses
GET    /api/courses/<id>/               - Get course details
```

### Feedback
```
POST   /api/feedback/submit/            - Submit feedback
GET    /api/feedback/                   - List feedback (with filters)
GET    /api/feedback/course/<id>/       - Get feedback for course
```

### Analytics
```
GET    /api/analytics/feedback/         - Overall feedback stats
GET    /api/analytics/instructor/<id>/  - Instructor analytics
GET    /api/analytics/compare/          - Compare courses
```

## Request/Response Examples

### Register Student
```json
POST /api/auth/register/student/
{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "securepass123",
  "student_id": "STU001",
  "full_name": "John Doe",
  "institution_id": 1
}

Response:
{
  "success": true,
  "message": "Student registered successfully",
  "user_id": 1
}
```

### Login
```json
POST /api/auth/login/
{
  "username": "john_doe",
  "password": "securepass123",
  "role": "student"
}

Response:
{
  "success": true,
  "message": "Login successful",
  "user": {
    "user_id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "role": "student",
    "profile_id": 1
  }
}
```

### Submit Feedback
```json
POST /api/feedback/submit/
{
  "course_id": 1,
  "rating": 5,
  "comment": "Excellent course! Very informative.",
  "anonymous": false
}

Response:
{
  "success": true,
  "message": "Feedback submitted successfully",
  "feedback_id": 1,
  "created_at": "2024-03-11T10:30:00Z"
}
```

### Get Feedback (with filters)
```
GET /api/feedback/?course_id=1&rating=5&search=excellent

Parameters:
- course_id: Filter by course
- rating: Filter by rating (1-5, or "negative" for ≤2)
- search: Search in comments and course names

Response:
{
  "success": true,
  "data": [
    {
      "id": 1,
      "course_id": 1,
      "course_name": "Data Science 101",
      "instructor": "Dr. Smith",
      "rating": 5,
      "comment": "Excellent course!",
      "anonymous": false,
      "student": "john_doe",
      "created_at": "2024-03-11T10:30:00Z",
      "is_negative": false
    }
  ],
  "count": 1
}
```

### Get Analytics
```
GET /api/analytics/feedback/

Response:
{
  "success": true,
  "data": {
    "total_feedbacks": 45,
    "average_rating": 4.2,
    "negative_count": 8,
    "negative_percentage": 17.8,
    "rating_distribution": {
      "1": 2,
      "2": 6,
      "3": 8,
      "4": 15,
      "5": 14
    },
    "top_courses": [
      {
        "id": 1,
        "name": "Data Science 101",
        "instructor": "Dr. Smith",
        "average_rating": 4.6,
        "feedback_count": 10
      }
    ],
    "low_courses": [
      {
        "id": 4,
        "name": "Python Basics",
        "instructor": "Prof. Brown",
        "average_rating": 2.1,
        "feedback_count": 8
      }
    ]
  }
}
```

## Database Models

### Institution
- name (unique)
- location
- description
- created_at, updated_at

### Course
- name
- instructor
- institution (FK)
- description
- created_at, updated_at

### Feedback
- student (FK, optional)
- course (FK)
- rating (1-5)
- comment
- anonymous (boolean)
- created_at, updated_at

### StudentProfile
- user (OneToOne FK)
- student_id (unique)
- institution (FK)
- enrollment_date

### InstructorProfile
- user (OneToOne FK)
- employee_id (unique)
- department
- institution (FK)

### AdminProfile
- user (OneToOne FK)
- admin_id (unique)
- institution (FK)

## Security Features

- CSRF protection (enable in production)
- Anonymous feedback support
- User authentication required for some endpoints
- Password hashing (Django default)
- Role-based access control
- SQL injection prevention (Django ORM)

## Running the Server

```bash
# Development
python manage.py runserver

# Production (with gunicorn)
pip install gunicorn
gunicorn feedback_project.wsgi:application --bind 0.0.0.0:8000
```

## Settings Configuration

Update `feedback_project/settings.py`:

```python
# Add to INSTALLED_APPS
INSTALLED_APPS = [
    ...
    'feedback',
    'corsheaders',  # For CORS if needed
]

# CORS settings (if using with frontend on different domain)
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:8000",
]

# CSRF (disable only for development with frontend on different port)
CSRF_TRUSTED_ORIGINS = [
    "http://localhost:3000",
]
```

## Testing

```bash
# Run tests
python manage.py test

# With coverage
pip install coverage
coverage run --source='feedback' manage.py test
coverage report
```

## Troubleshooting

### Migration Issues
```bash
python manage.py makemigrations feedback
python manage.py migrate
```

### Reset Database
```bash
python manage.py flush          # Clears all data
python manage.py migrate        # Recreates tables
```

### Debug Mode
Set `DEBUG = True` in `settings.py` for development only

## API Response Format

All successful responses follow this format:
```json
{
  "success": true,
  "data": {...} or [...],
  "message": "Optional message"
}
```

All error responses:
```json
{
  "error": "Error message",
  "status": 400 or 401 or 404 or 500
}
```

## License
MIT License

## Support
For issues or questions, contact the development team.