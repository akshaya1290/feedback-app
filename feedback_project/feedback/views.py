from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Q
from .models import User, Course, Enrollment, Feedback
from .forms import StudentRegistrationForm, LoginForm, CourseForm, FeedbackForm

# ==================== Authentication Views ====================

def login_view(request):
    """Unified login page with Bootstrap styling"""
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if user.role == 'admin':
                    return redirect('admin_dashboard')
                elif user.role == 'instructor':
                    return redirect('instructor_dashboard')
                elif user.role == 'student':
                    return redirect('student_dashboard')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def register_view(request):
    """Student registration page"""
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Registration successful! You can now login.')
            return redirect('login')
    else:
        form = StudentRegistrationForm()
    return render(request, 'register.html', {'form': form})

def logout_view(request):
    """Handle user logout"""
    logout(request)
    return redirect('login')

# ==================== Student Views ====================

@login_required
def student_dashboard(request):
    """Student dashboard - shows enrolled courses and feedback options"""
    if request.user.role != 'student':
        return redirect('login')

    # Get enrolled courses
    enrolled_courses = Enrollment.objects.filter(student=request.user).select_related('course__instructor')
    enrolled_course_ids = enrolled_courses.values_list('course_id', flat=True)

    # Get available courses (not enrolled)
    available_courses = Course.objects.exclude(id__in=enrolled_course_ids).select_related('instructor')

    # Get user's feedback
    user_feedback = Feedback.objects.filter(student=request.user).select_related('course')

    context = {
        'enrolled_courses': enrolled_courses,
        'available_courses': available_courses,
        'user_feedback': user_feedback,
    }
    return render(request, 'student_dashboard.html', context)

@login_required
def course_list(request):
    """List all available courses for enrollment"""
    if request.user.role != 'student':
        return redirect('login')

    enrolled_course_ids = Enrollment.objects.filter(student=request.user).values_list('course_id', flat=True)
    courses = Course.objects.exclude(id__in=enrolled_course_ids).select_related('instructor')

    context = {
        'courses': courses,
    }
    return render(request, 'course_list.html', context)

@login_required
def enroll_course(request, course_id):
    """Enroll in a course"""
    if request.user.role != 'student':
        return redirect('login')

    course = get_object_or_404(Course, id=course_id)

    if Enrollment.objects.filter(student=request.user, course=course).exists():
        messages.warning(request, 'You are already enrolled in this course.')
    else:
        Enrollment.objects.create(student=request.user, course=course)
        messages.success(request, f'Successfully enrolled in {course.course_name}')

    return redirect('student_dashboard')

@login_required
def feedback_form(request, course_id):
    """Submit feedback for an enrolled course"""
    if request.user.role != 'student':
        return redirect('login')

    course = get_object_or_404(Course, id=course_id)

    # Check if enrolled
    if not Enrollment.objects.filter(student=request.user, course=course).exists():
        messages.error(request, 'You must be enrolled in this course to submit feedback.')
        return redirect('student_dashboard')

    # Check if feedback already submitted
    if Feedback.objects.filter(student=request.user, course=course).exists():
        messages.warning(request, 'You have already submitted feedback for this course.')
        return redirect('student_dashboard')

    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.student = request.user
            feedback.course = course
            feedback.save()
            messages.success(request, 'Feedback submitted successfully!')
            return redirect('student_dashboard')
    else:
        form = FeedbackForm()

    context = {
        'form': form,
        'course': course,
    }
    return render(request, 'feedback_form.html', context)

# ==================== Instructor Views ====================

@login_required
def instructor_dashboard(request):
    """Instructor dashboard - shows assigned courses and feedback"""
    if request.user.role != 'instructor':
        return redirect('login')

    # Get courses taught by this instructor
    courses = Course.objects.filter(instructor=request.user).prefetch_related('enrollments', 'feedbacks')

    # Get feedback for instructor's courses
    feedback = Feedback.objects.filter(course__instructor=request.user).select_related('course', 'student')

    context = {
        'courses': courses,
        'feedback': feedback,
    }
    return render(request, 'instructor_dashboard.html', context)

# ==================== Admin Views ====================

@login_required
def admin_dashboard(request):
    """Admin dashboard - course, instructor, student management and analytics"""
    if request.user.role != 'admin':
        return redirect('login')

    # Analytics
    total_students = User.objects.filter(role='student').count()
    total_instructors = User.objects.filter(role='instructor').count()
    total_courses = Course.objects.count()
    total_feedback = Feedback.objects.count()

    # Sentiment distribution
    sentiment_stats = Feedback.objects.values('sentiment').annotate(count=Count('sentiment'))

    # Recent feedback
    recent_feedback = Feedback.objects.select_related('student', 'course').order_by('-created_at')[:10]

    context = {
        'total_students': total_students,
        'total_instructors': total_instructors,
        'total_courses': total_courses,
        'total_feedback': total_feedback,
        'sentiment_stats': sentiment_stats,
        'recent_feedback': recent_feedback,
    }
    return render(request, 'admin_dashboard.html', context)

@login_required
def manage_courses(request):
    """Admin course management"""
    if request.user.role != 'admin':
        return redirect('login')

    courses = Course.objects.all().select_related('instructor')
    instructors = User.objects.filter(role='instructor')

    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Course created successfully!')
            return redirect('manage_courses')
    else:
        form = CourseForm()

    context = {
        'courses': courses,
        'instructors': instructors,
        'form': form,
    }
    return render(request, 'manage_courses.html', context)

@login_required
def manage_users(request):
    """Admin user management"""
    if request.user.role != 'admin':
        return redirect('login')

    users = User.objects.all().order_by('role', 'username')

    context = {
        'users': users,
    }
    return render(request, 'manage_users.html', context)