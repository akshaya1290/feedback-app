# Frontend-Backend Integration Guide

## Overview
This guide explains how to integrate the frontend (HTML/CSS/JavaScript) with the Django REST API backend.

## Current State

### Frontend
- Currently uses **localStorage** for data persistence (demo mode)
- All functionality works with mock data
- Ready for backend API integration

### Backend
- 13 API endpoints ready
- REST format with JSON requests/responses
- Authentication system implemented
- Role-based access control

## Integration Steps

### Step 1: Update Login Page

**Current:** `index.html` - Uses hardcoded credentials
**New Approach:** POST to `/api/auth/login/`

#### Changes to Make:

```javascript
// In index.html, update the login form handler:

// BEFORE (current)
const credentials = {
    admin: { username: 'admin', password: 'admin123' },
    instructor: { password: 'pass123' }
};

// AFTER (new)
function handleLogin(role) {
    const username = document.getElementById(`${role}-username`).value;
    const password = document.getElementById(`${role}-password`).value;
    
    fetch('http://localhost:8000/api/auth/login/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            username: username,
            password: password,
            role: role
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            localStorage.setItem('userRole', data.user.role);
            localStorage.setItem('userId', data.user.user_id);
            localStorage.setItem('username', data.user.username);
            localStorage.setItem('institutionId', data.user.institution_id);
            window.location.href = 'dashboard.html';
        } else {
            alert('Login failed: ' + data.error);
        }
    })
    .catch(error => console.error('Login error:', error));
}
```

### Step 2: Update Registration Pages

**Current:** `register.html` - Uses localStorage
**New Approach:** POST to `/api/auth/register/{student|instructor|admin}/`

#### Changes to Make:

```javascript
// Replace the registration form submission

// BEFORE (current)
function registerUser() {
    const formData = {
        fullName: document.getElementById('full-name').value,
        email: document.getElementById('email').value,
        password: document.getElementById('password').value,
        studentId: document.getElementById('student-id').value
    };
    localStorage.setItem('user', JSON.stringify(formData));
}

// AFTER (new)
async function registerStudent() {
    const formData = {
        full_name: document.getElementById('student-full-name').value,
        email: document.getElementById('student-email').value,
        password: document.getElementById('student-password').value,
        student_id: document.getElementById('student-id').value,
        username: document.getElementById('student-username').value,
        institution_id: 1  // Get from institution selector or API
    };
    
    const response = await fetch('http://localhost:8000/api/auth/register/student/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
    });
    
    const data = await response.json();
    if (data.success) {
        alert('Registration successful! Redirecting to login...');
        window.location.href = 'index.html';
    } else {
        alert('Registration failed: ' + data.error);
    }
}

// Similar for registerInstructor() and registerAdmin()
```

### Step 3: Update Dashboard Data Loading

**Current:** `script.js` - Uses mockData object and localStorage
**New Approach:** Fetch from API endpoints

#### Initialize Dashboard:

```javascript
// BEFORE (current)
let mockData = {
    courses: [],
    feedback: [],
    institution: {}
};

let feedbackData = JSON.parse(localStorage.getItem('feedbackData')) || {
    feedback: []
};

// AFTER (new)
const API_BASE = 'http://localhost:8000/api';
let coursesData = [];
let feedbackData = [];
let userData = {
    userId: localStorage.getItem('userId'),
    username: localStorage.getItem('username'),
    role: localStorage.getItem('userRole'),
    institutionId: localStorage.getItem('institutionId')
};

// Load initial data
async function initializeDashboard() {
    try {
        // Load courses
        const coursesRes = await fetch(`${API_BASE}/courses/`);
        const coursesData_temp = await coursesRes.json();
        if (coursesData_temp.success) {
            coursesData = coursesData_temp.data;
        }
        
        // Load feedback
        const feedbackRes = await fetch(`${API_BASE}/feedback/`);
        const feedbackData_temp = await feedbackRes.json();
        if (feedbackData_temp.success) {
            feedbackData = feedbackData_temp.data;
        }
        
        // Update UI
        updateAllDashboards();
    } catch (error) {
        console.error('Failed to load dashboard data:', error);
    }
}

// Call on page load
window.addEventListener('load', initializeDashboard);
```

### Step 4: Update Feedback Submission

**Current:** Form saves to localStorage
**New Approach:** POST to `/api/feedback/submit/`

#### Changes to Make:

```javascript
// BEFORE (current)
function submitFeedback() {
    const feedback = {
        courseId: parseInt(document.getElementById('feedback-course').value),
        rating: parseInt(document.querySelector('input[name="rating"]:checked').value),
        comment: document.getElementById('feedback-comment').value,
        anonymous: document.getElementById('anonymous').checked,
        timestamp: new Date().toISOString()
    };
    
    let feedbackData = JSON.parse(localStorage.getItem('feedbackData')) || { feedback: [] };
    feedbackData.feedback.push(feedback);
    localStorage.setItem('feedbackData', JSON.stringify(feedbackData));
}

// AFTER (new)
async function submitFeedback() {
    const feedback = {
        course_id: parseInt(document.getElementById('feedback-course').value),
        rating: parseInt(document.querySelector('input[name="rating"]:checked').value),
        comment: document.getElementById('feedback-comment').value,
        anonymous: document.getElementById('anonymous').checked
    };
    
    const response = await fetch(`${API_BASE}/feedback/submit/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(feedback)
    });
    
    const data = await response.json();
    if (data.success) {
        alert('Feedback submitted successfully!');
        document.getElementById('feedback-form').reset();
        // Refresh feedback list
        await initializeDashboard();
    } else {
        alert('Failed to submit feedback: ' + data.error);
    }
}
```

### Step 5: Update Dashboard Filters

**Current:** Filter feedback from localStorage
**New Approach:** Use API query parameters

#### Changes to Make:

```javascript
// BEFORE (current)
function filterFeedback() {
    const courseId = document.getElementById('filter-course')?.value;
    const rating = document.getElementById('filter-rating')?.value;
    const searchTerm = document.getElementById('search-feedback')?.value;
    
    let filtered = feedbackData.feedback;
    
    if (courseId) filtered = filtered.filter(f => f.courseId == courseId);
    // ... more filtering
}

// AFTER (new)
async function filterFeedback() {
    const courseId = document.getElementById('filter-course')?.value;
    const rating = document.getElementById('filter-rating')?.value;
    const searchTerm = document.getElementById('search-feedback')?.value;
    
    let url = `${API_BASE}/feedback/?`;
    if (courseId) url += `course_id=${courseId}&`;
    if (rating) url += `rating=${rating}&`;
    if (searchTerm) url += `search=${searchTerm}`;
    
    const response = await fetch(url);
    const data = await response.json();
    
    if (data.success) {
        feedbackData = data.data;
        renderFeedbackList();
    }
}
```

### Step 6: Update Analytics

**Current:** Calculate from localStorage data
**New Approach:** Fetch pre-calculated from API

#### Changes to Make:

```javascript
// BEFORE (current)
function initAdminDashboard() {
    const stats = {
        totalFeedback: feedbackData.feedback.length,
        avgRating: calculateAverage(),
        negativeFeedback: feedbackData.feedback.filter(f => f.rating <= 2).length
    };
    // ... render stats
}

// AFTER (new)
async function initAdminDashboard() {
    const response = await fetch(`${API_BASE}/analytics/feedback/`);
    const data = await response.json();
    
    if (data.success) {
        const stats = data.data;  // All calculations done on backend
        
        document.getElementById('total-feedback-stat').textContent = stats.total_feedbacks;
        document.getElementById('avg-rating-stat').textContent = stats.average_rating.toFixed(1);
        document.getElementById('negative-stat').textContent = stats.negative_count;
        
        // Draw charts with API data
        drawCharts(stats.rating_distribution, stats.top_courses);
    }
}
```

### Step 7: Update Instructor Dashboard

**Current:** Uses mock notification logic
**New Approach:** Fetch from `/api/analytics/instructor/{employee_id}/`

```javascript
// AFTER (new)
async function initInstructorDashboard() {
    const employeeId = userData.employeeId;  // Get from user profile
    const response = await fetch(`${API_BASE}/analytics/instructor/${employeeId}/`);
    const data = await response.json();
    
    if (data.success) {
        const instructorData = data.data;
        
        // Display instructor's courses and their ratings
        instructorData.courses.forEach(course => {
            if (course.negative_count >= 2) {
                // Show warning notification
                displayNotification(course, 'warning');
            }
        });
    }
}
```

### Step 8: Update Comparison Feature

**Current:** Compares mock data
**New Approach:** Uses `/api/analytics/compare/` endpoint

```javascript
// AFTER (new)
async function initFeedbackComparison() {
    const course1Id = document.getElementById('compare-course1').value;
    const course2Id = document.getElementById('compare-course2').value;
    
    const response = await fetch(
        `${API_BASE}/analytics/compare/?course1_id=${course1Id}&course2_id=${course2Id}`
    );
    const data = await response.json();
    
    if (data.success) {
        const comparison = data.data;
        
        // Display side-by-side comparison
        displayComparison(comparison);
    }
}
```

## CORS Configuration

Since frontend and backend run on different ports, enable CORS:

### In `feedback_project/settings.py`:

```python
INSTALLED_APPS = [
    ...
    'corsheaders',
    ...
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # Add at top
    ...
]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:8000",
    "http://localhost:8000",
]

# Only for development
CSRF_TRUSTED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:8000",
]
```

## API Response Handling Template

```javascript
async function apiCall(endpoint, method = 'GET', data = null) {
    const options = {
        method: method,
        headers: {
            'Content-Type': 'application/json',
        }
    };
    
    if (data) {
        options.body = JSON.stringify(data);
    }
    
    try {
        const response = await fetch(`${API_BASE}${endpoint}`, options);
        const result = await response.json();
        
        if (result.success) {
            return result.data;
        } else {
            console.error('API Error:', result.error);
            alert('Error: ' + result.error);
            return null;
        }
    } catch (error) {
        console.error('Network Error:', error);
        alert('Network error. Please try again.');
        return null;
    }
}

// Usage
const courses = await apiCall('/courses/');
await apiCall('/feedback/submit/', 'POST', feedbackData);
```

## Testing the Integration

### 1. Start Backend
```bash
python manage.py runserver
```

### 2. Open Frontend
```
Open dashboard.html in browser
```

### 3. Test Flow
1. Go to login page (index.html)
2. Enter credentials and login
3. Submit feedback via form
4. Check admin dashboard for submitted feedback
5. Verify analytics update in real-time

## Troubleshooting

### CORS Errors
- Make sure `django-cors-headers` is installed: `pip install django-cors-headers`
- Verify CORS settings in settings.py
- Check frontend and backend URLs match

### Feedback Not Saving
- Check browser Network tab for POST requests
- Verify API endpoint returns `{"success": true}`
- Check Django logs for errors

### Authentication Issues
- Verify user exists in database
- Check password is correct
- Ensure role matches between login and API

### Missing Data
- Run migrations if models changed
- Create test data in admin panel
- Check database connection

## Summary of Changes

| Feature | Before (localStorage) | After (API) |
|---------|-------------------|-----------|
| Login | Hardcoded credentials | POST /api/auth/login/ |
| Register | localStorage.setItem | POST /api/auth/register/ |
| Load Courses | mockData.courses | GET /api/courses/ |
| Load Feedback | localStorage.getItem | GET /api/feedback/ |
| Submit Feedback | localStorage.push | POST /api/feedback/submit/ |
| Analytics | Calculate locally | GET /api/analytics/feedback/ |
| Filter Feedback | Filter array locally | GET /api/feedback/?params |
| Instructor Notifications | Mock logic | GET /api/analytics/instructor/ |
| Course Comparison | Mock comparison | GET /api/analytics/compare/ |

## Next Steps

1. Create configuration file with API base URL
2. Add loading spinners during API calls
3. Implement proper error handling
4. Add authentication tokens/sessions
5. Implement pagination for large datasets
6. Add offline capability (service workers)
7. Deploy backend and update API URL in frontend