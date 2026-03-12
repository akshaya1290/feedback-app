# 📚 Student Feedback System

A comprehensive web-based feedback management system for educational institutions with role-based access control, analytics, and reporting features.

## 🎯 Overview

The Student Feedback System is a full-stack application that enables students to submit feedback about courses and instructors, while providing administrators and instructors with powerful analytics and insights.

### Key Features

✅ **Three User Roles**
- **Students**: Submit feedback, view submission history
- **Instructors**: View course ratings, notifications for struggling courses
- **Admins**: Comprehensive analytics, feedback management, institution-wide insights

✅ **Feedback Management**
- 5-star rating system
- Text comments with search capability
- Anonymous feedback option
- Course-specific and instructor-specific feedback

✅ **Advanced Analytics**
- Overall institution metrics
- Course performance comparison
- Instructor rating tracking
- Feedback distribution visualization
- Negative feedback warnings (≤2 stars)

✅ **Modern UI/UX**
- Responsive design (mobile, tablet, desktop)
- Interactive charts and visualizations
- Role-based dashboard layouts
- Real-time data updates

## 📁 Project Structure

```
feedback_project/
├── frontend/                    # Frontend files
│   ├── index.html              # Login page
│   ├── register.html           # Registration page
│   ├── dashboard.html          # Main application
│   ├── script.js               # Application logic
│   └── style.css               # Styling
│
├── feedback_project/           # Django project
│   ├── settings.py             # Configuration
│   ├── urls.py                 # Main URL routing
│   └── wsgi.py                 # WSGI configuration
│
├── feedback/                   # Django app
│   ├── models.py               # Database models
│   ├── views.py                # API endpoints
│   ├── urls.py                 # App URL routing
│   ├── admin.py                # Admin customization
│   └── migrations/             # Database migrations
│
├── requirements.txt            # Python dependencies
├── manage.py                   # Django management script
├── BACKEND_SETUP.md           # Backend documentation
└── README.md                   # This file
```

## 🛠️ Technology Stack

### Frontend
- **HTML5** - Structure
- **CSS3** - Responsive styling
- **JavaScript (ES6+)** - Application logic
- **Chart.js** - Data visualization
- **Bootstrap 5** - UI components
- **Font Awesome 6** - Icons

### Backend
- **Django 3.2** - Web framework
- **Django REST Framework** - API
- **SQLite/PostgreSQL** - Database
- **Python 3.8+** - Runtime

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository**
```bash
cd feedback_project
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up database**
```bash
python manage.py makemigrations
python manage.py migrate
```

4. **Create superuser (for admin access)**
```bash
python manage.py createsuperuser
```

5. **Start the server**
```bash
python manage.py runserver
```

6. **Access the application**
- Frontend: Open `frontend/index.html` in your browser
- Admin: http://localhost:8000/admin

## 📖 Usage Guide

### Login Credentials (Demo)

#### Student
- **Username**: student_demo
- **Password**: pass123

#### Instructor
- **Username**: instructor_demo
- **Password**: pass123

#### Admin
- **Username**: admin
- **Password**: admin123

### Creating Test Data

```bash
python manage.py shell
```

```python
from feedback.models import Institution, Course, StudentProfile
from django.contrib.auth.models import User

# Create institution
inst = Institution.objects.create(
    name="Example University",
    location="New York, USA",
    description="A premier educational institution"
)

# Create courses
Course.objects.create(
    name="Python Programming",
    instructor="Dr. Smith",
    institution=inst,
    description="Learn Python from basics to advanced"
)

# Create student
user = User.objects.create_user(
    username='student1',
    email='student@example.com',
    password='pass123'
)

StudentProfile.objects.create(
    user=user,
    student_id='STU001',
    institution=inst
)
```

## 🔗 API Documentation

### Base URL
```
http://localhost:8000/api
```

### Authentication Endpoints

**Register Student**
```http
POST /auth/register/student/
Content-Type: application/json

{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "secure123",
  "student_id": "STU001",
  "full_name": "John Doe",
  "institution_id": 1
}
```

**Login**
```http
POST /auth/login/
Content-Type: application/json

{
  "username": "john_doe",
  "password": "secure123",
  "role": "student"
}

Response:
{
  "success": true,
  "user": {
    "user_id": 1,
    "username": "john_doe",
    "role": "student"
  }
}
```

### Feedback Endpoints

**Submit Feedback**
```http
POST /feedback/submit/
Content-Type: application/json

{
  "course_id": 1,
  "rating": 5,
  "comment": "Great course!",
  "anonymous": false
}
```

**List Feedback**
```http
GET /feedback/?course_id=1&rating=5&search=great

Parameters:
- course_id: Filter by course ID
- rating: Filter by rating (1-5 or "negative" for ≤2 stars)
- search: Search in comments
```

**List Courses**
```http
GET /courses/

Response includes all courses with average ratings and feedback counts
```

### Analytics Endpoints

**Overall Analytics**
```http
GET /analytics/feedback/

Returns:
- Total feedback count
- Average rating
- Negative feedback count
- Rating distribution
- Top performing courses
- Struggling courses
```

**Instructor Analytics**
```http
GET /analytics/instructor/{employee_id}/

Returns instructor-specific metrics and course-wise breakdown
```

**Compare Courses**
```http
GET /analytics/compare/?course1_id=1&course2_id=2

Returns side-by-side comparison of two courses
```

## 📊 Database Schema

### Models

**Institution**
- name (unique)
- location
- description
- timestamps

**Course**
- name
- instructor
- institution (FK)
- description
- timestamps

**Feedback**
- student (FK, optional)
- course (FK)
- rating (1-5, validated)
- comment
- anonymous
- timestamps

**StudentProfile**
- user (OneToOne FK)
- student_id (unique)
- institution (FK)
- enrollment_date

**InstructorProfile**
- user (OneToOne FK)
- employee_id (unique)
- department
- institution (FK)

**AdminProfile**
- user (OneToOne FK)
- admin_id (unique)
- institution (FK)

## 🔒 Security Features

- **Password Hashing**: Django's secure password hashing
- **CSRF Protection**: Built-in Django CSRF tokens
- **SQL Injection Prevention**: Django ORM protection
- **Authentication**: User login and role-based access
- **Anonymous Feedback**: Optional anonymous submission
- **Validation**: Server-side and client-side validation

## 📈 Analytics Features

### Admin Analytics
- Total feedback received
- Average institution rating
- Feedback count by rating
- Top 5 best-rated courses
- Top 5 lowest-rated courses
- Negative feedback percentage
- Course performance trends

### Instructor Analytics
- Average instructor rating
- Course-wise feedback breakdown
- Feedback count per course
- List of courses with 2+ negative reviews (warnings)

### Comparison Tools
- Side-by-side course comparison
- Rating distribution comparison
- Feedback count comparison
- Instruction quality metrics

## 🌐 Frontend Integration

The frontend currently uses **localStorage** for demo purposes. To integrate with the backend API:

1. Update API endpoints in `script.js`
2. Replace localStorage with fetch API calls
3. Configure CORS in Django settings
4. Update authentication flow

See [INTEGRATION_GUIDE.md](INTEGRATION_GUIDE.md) for detailed integration steps.

## 🧪 Testing

### Run Tests
```bash
python manage.py test
```

### Test Coverage
```bash
pip install coverage
coverage run --source='feedback' manage.py test
coverage report
```

### Manual Testing Checklist
- [ ] User registration for all three roles
- [ ] Login with different roles
- [ ] Submit feedback with ratings 1-5
- [ ] Anonymous feedback submission
- [ ] View feedback filters in admin
- [ ] Check analytics calculations
- [ ] Test instructor notifications
- [ ] Verify course comparison

## 📝 Configuration

### Django Settings
Edit `feedback_project/settings.py`:

```python
# Debug mode (disable in production)
DEBUG = True

# Allowed hosts
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# Database (default: SQLite)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# CORS (for frontend on different port)
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:8000",
]
```

### Switch to PostgreSQL
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'feedback_db',
        'USER': 'postgres',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

## 🚀 Deployment

### Using Gunicorn
```bash
pip install gunicorn
gunicorn feedback_project.wsgi:application --bind 0.0.0.0:8000
```

### Environment Variables
Create `.env` file:
```
DEBUG=False
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=yourdomain.com
DATABASE_URL=postgresql://user:pass@localhost/dbname
CORS_ALLOWED_ORIGINS=https://yourdomain.com
```

### Production Checklist
- [ ] Set DEBUG = False
- [ ] Configure allowed hosts
- [ ] Use environment variables for secrets
- [ ] Enable HTTPS
- [ ] Configure CORS properly
- [ ] Use PostgreSQL database
- [ ] Set up static files serving
- [ ] Configure email for notifications
- [ ] Set up logging
- [ ] Use gunicorn/nginx

## 🐛 Troubleshooting

### Database Issues
```bash
# Reset database
python manage.py flush
python manage.py migrate

# Check migrations
python manage.py showmigrations
```

### Port Already in Use
```bash
# Use different port
python manage.py runserver 8001
```

### CORS Errors
- Ensure `django-cors-headers` is installed
- Check CORS settings in settings.py
- Verify frontend URL is in CORS_ALLOWED_ORIGINS

### Migration Conflicts
```bash
python manage.py makemigrations --merge
```

## 📚 Additional Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [Chart.js Documentation](https://www.chartjs.org/)
- [Bootstrap 5](https://getbootstrap.com/)

## 📞 Support

For issues, questions, or feature requests, please contact the development team.

## 📄 License

MIT License - Feel free to use this project for educational purposes.

## 👥 Contributors

- Development Team

---

**Version**: 1.0.0  
**Last Updated**: 2024  
**Status**: Production Ready