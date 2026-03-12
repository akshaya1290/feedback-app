# 🚀 QUICK START - 5 Minute Setup

Get the Student Feedback System up and running in 5 minutes!

## ✅ Prerequisites
- Python 3.8+ installed
- Terminal/Command Prompt open in project directory

---

## Step 1: Install Dependencies (1 min)

```bash
pip install -r requirements.txt
```

**Expected output:** Multiple packages installing... ✓ Success

---

## Step 2: Create Database (1 min)

```bash
python manage.py makemigrations
python manage.py migrate
```

**Expected output:** Creating tables... No errors ✓

---

## Step 3: Load Demo Data (1 min)

```bash
python manage.py setup_demo_data
```

**Output:**
```
=====================================================
  Student Feedback System - Quick Setup
=====================================================

Creating Institution...
✓ Created Institution: ABC University

Creating Courses...
  ✓ Created Course: Data Science 101
  ✓ Created Course: Web Development
  ... (more courses)
✓ Created 8 new courses

Creating Sample Students...
✓ Created User: student1
  ✓ Created Student Profile: STU001
... (more users)

Creating Admin User...
✓ Created User: admin
  ✓ Created Admin Profile: ADM001

=====================================================
  ✓ Setup Complete!
=====================================================

📝 Login Credentials (Demo):
  Student:    username='student1' password='pass123'
  Instructor: username='instructor1' password='pass123'
  Admin:      username='admin' password='admin123'

🚀 Start the server with: python manage.py runserver
📊 Access admin panel at: http://localhost:8000/admin
```

---

## Step 4: Start the Server (1 min)

```bash
python manage.py runserver
```

**Expected output:**
```
Watching for file changes with StatReloader
Quit the server with CTRL-BREAK.
Starting development server at http://127.0.0.1:8000/
```

✓ Server is running!

---

## Step 5: Open Frontend (1 min)

### Option A: Open with Browser
1. Navigate to project folder → `frontend/`
2. Double-click `index.html`
3. Or right-click → "Open with" → Browser

### Option B: Use Simple HTTP Server
```bash
# In project root, open new terminal
python -m http.server 8001
```
Then open: `http://localhost:8001/frontend/index.html`

---

## 🎯 You're Done!

### Login with Demo Credentials

**Student:**
- Username: `student1`
- Password: `pass123`

**Instructor:**
- Username: `instructor1`
- Password: `pass123`

**Admin:**
- Username: `admin`
- Password: `admin123`

---

## 📊 What You Can Do Now

### As an Admin
1. Go to Admin Dashboard
2. See all feedback
3. Filter by course or rating
4. View analytics and charts
5. Compare courses

### As an Instructor
1. View course ratings
2. See student feedback
3. Get notification alerts for low-rated courses

### As a Student
1. Go to Student Dashboard
2. Submit feedback for courses
3. View your feedback history
4. See course ratings

---

## 🔗 Important URLs

```
Frontend:           Open frontend/index.html in browser
Backend Server:     http://localhost:8000
Django Admin:       http://localhost:8000/admin (credentials: admin/admin123)
API Endpoints:      http://localhost:8000/api/courses/
                    http://localhost:8000/api/feedback/
                    http://localhost:8000/api/analytics/feedback/
```

---

## 🛠️ Common Issues

### Issue: "Port 8000 already in use"
```bash
# Use a different port
python manage.py runserver 8001
```

### Issue: "Database not found"
```bash
python manage.py migrate
```

### Issue: Can't find frontend
```bash
# Make sure you're in the right directory
# Frontend files are in: feedback_project/frontend/
```

---

## 📚 Full Documentation

- **README.md** - Complete project overview
- **BACKEND_SETUP.md** - Detailed backend setup
- **INTEGRATION_GUIDE.md** - Frontend-Backend integration
- **TESTING_GUIDE.md** - Testing procedures
- **DJANGO_SETTINGS_GUIDE.md** - Django configuration

---

## 🎓 Next Steps

### 1. Test the System
- Try all 3 login roles
- Submit feedback as a student
- View analytics as admin
- Check instructor notifications

### 2. Create More Data
```bash
python manage.py shell
# Then use Django shell to add more courses/feedback

from feedback.models import Course, Institution
inst = Institution.objects.first()
Course.objects.create(name="New Course", instructor="Prof X", institution=inst)
```

### 3. Test API Directly
```bash
# In new terminal, try API endpoints
curl http://localhost:8000/api/courses/
curl http://localhost:8000/api/feedback/
curl http://localhost:8000/api/analytics/feedback/
```

### 4. Integration with Frontend
Once you're comfortable with the system:
- See INTEGRATION_GUIDE.md for connecting frontend to backend API
- Current frontend uses localStorage (demo mode)
- Replace with fetch() calls to backend API

---

## 💡 Tips

✓ **Keep terminal open** while server is running  
✓ **Press CTRL+C** to stop server  
✓ **First time will be slowest** (initializing database)  
✓ **Clear browser cache** if UI looks wrong  
✓ **Check JavaScript console** (F12) for errors  

---

## ✨ Features to Try

1. **Submit Feedback**
   - Go to feedback form
   - Select a course
   - Give a rating (1-5 stars)
   - Add comment (optional)
   - Check "Anonymous" if you want

2. **View Analytics**
   - Go to admin dashboard
   - See rating distribution chart
   - See course performance radar chart
   - Click filters to narrow data

3. **Compare Courses**
   - Select two courses
   - See side-by-side comparison
   - Compare ratings and feedback count

4. **Instructor Notifications**
   - Login as instructor
   - See warning alerts for low-rated courses
   - Review feedback for your courses

---

## 🎉 Congratulations!

You now have a fully functional Student Feedback System with:
- ✅ 3 user roles (Student, Instructor, Admin)
- ✅ Complete feedback management
- ✅ Advanced analytics
- ✅ Modern responsive UI
- ✅ REST API backends
- ✅ Demo data ready to use

**Enjoy exploring the system!** 🚀