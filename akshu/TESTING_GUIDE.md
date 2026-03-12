# 🧪 Testing Guide - Student Feedback System

Comprehensive guide for testing the API endpoints, database models, and frontend integration.

## Table of Contents
1. [Setup Testing Environment](#setup-testing-environment)
2. [Unit Tests](#unit-tests)
3. [API Testing](#api-testing)
4. [Frontend Testing](#frontend-testing)
5. [Integration Testing](#integration-testing)
6. [Performance Testing](#performance-testing)

---

## Setup Testing Environment

### 1. Install Testing Dependencies
```bash
pip install pytest pytest-django pytest-cov django-test-plus
```

### 2. Configure pytest
Create `pytest.ini` in project root:
```ini
[pytest]
DJANGO_SETTINGS_MODULE = feedback_project.settings
python_files = tests.py test_*.py *_tests.py
python_classes = Test*
python_functions = test_*
```

### 3. Create Test Database
```bash
python manage.py migrate --run-syncdb
```

---

## Unit Tests

### Create `feedback/tests.py`

```python
from django.test import TestCase
from django.contrib.auth.models import User
from feedback.models import Institution, Course, Feedback, StudentProfile

class InstitutionTestCase(TestCase):
    def setUp(self):
        self.institution = Institution.objects.create(
            name="Test University",
            location="Test City",
            description="Test Description"
        )
    
    def test_institution_creation(self):
        self.assertEqual(self.institution.name, "Test University")
        self.assertIsNotNone(self.institution.id)
    
    def test_institution_string_representation(self):
        self.assertEqual(str(self.institution), "Test University")

class CourseTestCase(TestCase):
    def setUp(self):
        self.institution = Institution.objects.create(
            name="Test University",
            location="Test City"
        )
        self.course = Course.objects.create(
            name="Test Course",
            instructor="Dr. Test",
            institution=self.institution,
            description="Test Course"
        )
    
    def test_course_creation(self):
        self.assertEqual(self.course.name, "Test Course")
        self.assertEqual(self.course.instructor, "Dr. Test")
    
    def test_course_average_rating_no_feedback(self):
        avg = self.course.get_average_rating()
        self.assertEqual(avg, 0)

class FeedbackTestCase(TestCase):
    def setUp(self):
        self.institution = Institution.objects.create(
            name="Test University",
            location="Test City"
        )
        self.course = Course.objects.create(
            name="Test Course",
            instructor="Dr. Test",
            institution=self.institution
        )
        self.user = User.objects.create_user(
            username='student1',
            password='pass123'
        )
        self.student_profile = StudentProfile.objects.create(
            user=self.user,
            student_id='STU001',
            institution=self.institution
        )
    
    def test_feedback_creation(self):
        feedback = Feedback.objects.create(
            student=self.user,
            course=self.course,
            rating=5,
            comment="Great course!",
            anonymous=False
        )
        self.assertEqual(feedback.rating, 5)
        self.assertFalse(feedback.is_negative())
    
    def test_feedback_negative_detection(self):
        feedback = Feedback.objects.create(
            course=self.course,
            rating=2,
            comment="Poor course",
            anonymous=True
        )
        self.assertTrue(feedback.is_negative())
    
    def test_feedback_rating_validation(self):
        # Test invalid rating
        with self.assertRaises(Exception):
            Feedback.objects.create(
                course=self.course,
                rating=0,  # Invalid
                comment="Test"
            )

class StudentProfileTestCase(TestCase):
    def setUp(self):
        self.institution = Institution.objects.create(
            name="Test University",
            location="Test City"
        )
        self.user = User.objects.create_user(
            username='student1',
            password='pass123'
        )
        self.profile = StudentProfile.objects.create(
            user=self.user,
            student_id='STU001',
            institution=self.institution
        )
    
    def test_student_profile_creation(self):
        self.assertEqual(self.profile.student_id, 'STU001')
        self.assertEqual(self.profile.user.username, 'student1')

# Run tests
# python manage.py test feedback.tests
```

---

## API Testing

### Using cURL (Command Line)

#### 1. Register Student
```bash
curl -X POST http://localhost:8000/api/auth/register/student/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "student_test",
    "email": "student@test.com",
    "password": "testpass123",
    "student_id": "STU999",
    "full_name": "Test Student",
    "institution_id": 1
  }'
```

#### 2. Login
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "student_test",
    "password": "testpass123",
    "role": "student"
  }'
```

#### 3. Submit Feedback
```bash
curl -X POST http://localhost:8000/api/feedback/submit/ \
  -H "Content-Type: application/json" \
  -d '{
    "course_id": 1,
    "rating": 5,
    "comment": "Excellent course!",
    "anonymous": false
  }'
```

#### 4. Get Feedback List
```bash
curl http://localhost:8000/api/feedback/
```

#### 5. Filter Feedback
```bash
curl "http://localhost:8000/api/feedback/?course_id=1&rating=5"
```

#### 6. Get Analytics
```bash
curl http://localhost:8000/api/analytics/feedback/
```

### Using Postman

1. **Create Collection**: "Feedback System"

2. **Authentication Requests**
   - POST: `localhost:8000/api/auth/register/student/`
   - POST: `localhost:8000/api/auth/login/`
   - POST: `localhost:8000/api/auth/logout/`

3. **Course Requests**
   - GET: `localhost:8000/api/courses/`
   - GET: `localhost:8000/api/courses/1/`

4. **Feedback Requests**
   - POST: `localhost:8000/api/feedback/submit/`
   - GET: `localhost:8000/api/feedback/`
   - GET: `localhost:8000/api/feedback/course/1/`

5. **Analytics Requests**
   - GET: `localhost:8000/api/analytics/feedback/`
   - GET: `localhost:8000/api/analytics/instructor/EMP001/`
   - GET: `localhost:8000/api/analytics/compare/?course1_id=1&course2_id=2`

### Using Python requests Library

```python
import requests
import json

BASE_URL = "http://localhost:8000/api"

# Register
response = requests.post(
    f"{BASE_URL}/auth/register/student/",
    json={
        "username": "test_student",
        "email": "test@example.com",
        "password": "pass123",
        "student_id": "STU123",
        "full_name": "Test Student",
        "institution_id": 1
    }
)
print("Register:", response.json())

# Login
response = requests.post(
    f"{BASE_URL}/auth/login/",
    json={
        "username": "test_student",
        "password": "pass123",
        "role": "student"
    }
)
print("Login:", response.json())

# Submit Feedback
response = requests.post(
    f"{BASE_URL}/feedback/submit/",
    json={
        "course_id": 1,
        "rating": 5,
        "comment": "Great course!",
        "anonymous": False
    }
)
print("Feedback:", response.json())

# Get Feedback
response = requests.get(f"{BASE_URL}/feedback/")
print("Feedback List:", response.json())

# Get Analytics
response = requests.get(f"{BASE_URL}/analytics/feedback/")
print("Analytics:", response.json())
```

---

## Frontend Testing

### Manual Testing Checklist

#### Authentication
- [ ] Login page loads correctly
- [ ] Can login as student with credentials
- [ ] Can login as instructor with credentials
- [ ] Can login as admin with credentials
- [ ] Invalid credentials show error
- [ ] Registration form accepts valid data
- [ ] Password validation works
- [ ] Redirect after login is correct based on role

#### Student Dashboard
- [ ] Dashboard loads with user greeting
- [ ] Can see submitted feedback history
- [ ] Can see feedback counts and stats
- [ ] Can navigate between pages

#### Feedback Form
- [ ] Form displays all courses
- [ ] Can select 1-5 stars
- [ ] Course dropdown works
- [ ] Comment field accepts text
- [ ] Anonymous checkbox works
- [ ] Submit button saves feedback
- [ ] Form clears after submission
- [ ] All rating levels (1-5) are accepted

#### Admin Dashboard
- [ ] All feedback displays
- [ ] Can filter by course
- [ ] Can filter by rating
- [ ] Can search by comment text
- [ ] Charts render correctly
- [ ] Statistics update dynamically
- [ ] Responsive on mobile

#### Instructor Dashboard
- [ ] Shows instructor's courses
- [ ] Displays course ratings
- [ ] Warnings show for ≤2 stars (2+ negative)
- [ ] Course feedback displays correctly

### Browser Compatibility Testing

Test in:
- [ ] Chrome/Chromium
- [ ] Firefox
- [ ] Safari
- [ ] Edge
- [ ] Mobile browsers

### Responsive Design Testing

- [ ] Desktop (1920x1080)
- [ ] Tablet (768x1024)
- [ ] Mobile (375x667)

---

## Integration Testing

### End-to-End Flow Test

```python
# test_integration.py

from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time

class FeedbackSystemIntegrationTest(LiveServerTestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
    
    def tearDown(self):
        self.driver.quit()
    
    def test_full_feedback_flow(self):
        # Navigate to login
        self.driver.get(self.live_server_url + '/login.html')
        
        # Enter credentials
        username_field = self.driver.find_element(By.ID, 'username')
        password_field = self.driver.find_element(By.ID, 'password')
        
        username_field.send_keys('student1')
        password_field.send_keys('pass123')
        
        # Click login button
        login_button = self.driver.find_element(By.ID, 'login-btn')
        login_button.click()
        
        # Wait for dashboard
        time.sleep(2)
        
        # Navigate to feedback form
        feedback_link = self.driver.find_element(By.ID, 'feedback-form-link')
        feedback_link.click()
        
        time.sleep(1)
        
        # Fill feedback form
        course_select = Select(self.driver.find_element(By.ID, 'feedback-course'))
        course_select.select_by_value('1')
        
        # Select 5-star rating
        rating_5 = self.driver.find_element(By.ID, 'rating-5')
        rating_5.click()
        
        # Add comment
        comment = self.driver.find_element(By.ID, 'feedback-comment')
        comment.send_keys('Excellent course!')
        
        # Submit
        submit_btn = self.driver.find_element(By.ID, 'submit-feedback')
        submit_btn.click()
        
        # Verify success
        time.sleep(1)
        success_msg = self.driver.find_element(By.CLASS_NAME, 'success-message')
        self.assertIn('submitted successfully', success_msg.text)

# Run: python manage.py test
```

---

## Performance Testing

### Load Testing with Locust
```bash
pip install locust
```

Create `locustfile.py`:
```python
from locust import HttpUser, task, between
import json

class FeedbackSystemUser(HttpUser):
    wait_time = between(1, 3)
    
    @task(3)
    def get_feedback(self):
        self.client.get("/api/feedback/")
    
    @task(2)
    def get_analytics(self):
        self.client.get("/api/analytics/feedback/")
    
    @task(1)
    def submit_feedback(self):
        self.client.post(
            "/api/feedback/submit/",
            json={
                "course_id": 1,
                "rating": 5,
                "comment": "Test feedback",
                "anonymous": False
            }
        )
    
    def on_start(self):
        # Login
        self.client.post(
            "/api/auth/login/",
            json={
                "username": "student1",
                "password": "pass123",
                "role": "student"
            }
        )

# Run: locust -f locustfile.py
```

### Database Query Performance
```python
from django.test.utils import CaptureQueriesContext
from django.db import connection

# Profile queries
with CaptureQueriesContext(connection) as context:
    # Your code here
    Course.objects.all().prefetch_related('feedback_set').get(id=1)

print(f"Queries executed: {len(context.captured_queries)}")
```

---

## Test Coverage Report

```bash
pip install coverage
coverage run --source='feedback' manage.py test
coverage report
coverage html  # Generate HTML report
```

---

## API Response Validation

### Test Success Response Format
```json
{
  "success": true,
  "data": {...},
  "message": "Optional message"
}
```

### Test Error Response Format
```json
{
  "error": "Error message",
  "status": 400
}
```

---

## Continuous Integration (GitHub Actions)

Create `.github/workflows/tests.yml`:
```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    - uses: actions/setup-python@v2
      with:
        python-version: 3.9
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
    
    - name: Run tests
      run: |
        python manage.py test
    
    - name: Coverage
      run: |
        coverage run --source='feedback' manage.py test
        coverage report
```

---

## Testing Checklist

- [ ] All unit tests pass
- [ ] API endpoints return correct responses
- [ ] Database transactions work correctly
- [ ] Authentication validates properly
- [ ] Permissions are enforced
- [ ] Frontend loads without errors
- [ ] Forms validate correctly
- [ ] Charts render with correct data
- [ ] Analytics calculations are accurate
- [ ] CORS headers are present
- [ ] No console errors in browser
- [ ] Mobile responsive design works
- [ ] Load testing passes
- [ ] Security headers present
- [ ] SQL injection prevention works

---

## Debugging Tips

### 1. Enable Query Logging
```python
# In settings.py
LOGGING = {
    'version': 1,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}
```

### 2. Use Django Shell
```bash
python manage.py shell
```

```python
from feedback.models import Course
course = Course.objects.get(id=1)
print(course.get_average_rating())
print(course.get_negative_feedback_count())
```

### 3. Check Request/Response
```python
# In views, add debug prints
def submit_feedback(request):
    print("Request body:", request.body)
    print("Request data:", request.POST or request.data)
    # ... rest of code
```

### 4. Database Inspection
```bash
python manage.py dbshell
SELECT * FROM feedback_feedback;
SELECT * FROM feedback_course;
```

---

## Summary

Regular testing ensures:
- ✓ Code quality and reliability
- ✓ API correctness
- ✓ User experience
- ✓ Performance standards
- ✓ Security compliance

Test early, test often!