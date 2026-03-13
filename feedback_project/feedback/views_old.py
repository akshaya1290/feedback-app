from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Count, Q
from django.utils import timezone
from django.contrib import messages
import json
from datetime import datetime, timedelta

from .models import User, Course, Enrollment, Feedback


# ==================== Authentication Views ====================

def admin_login_view(request):
    """Admin login and registration view"""
    if request.method == 'POST':
        if 'name' in request.POST:  # Registration
            name = request.POST.get('name')
            email = request.POST.get('email')
            username = request.POST.get('username')
            password = request.POST.get('password')

            if not all([name, email, username, password]):
                messages.error(request, 'All fields are required.')
            else:
                # validation
                if User.objects.filter(username=username).exists():
                    messages.error(request, f"Username '{username}' already exists.")
                elif User.objects.filter(email=email).exists():
                    messages.error(request, f"Email '{email}' already exists.")
                else:
                    # create the user
                    user = User.objects.create_user(
                        username=username,
                        email=email,
                        password=password,
                        name=name,
                        role='admin'
                    )
                    messages.success(request, 'Admin registered successfully! You can now login.')
        else:  # Login
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)
            if user is not None and user.role == 'admin':
                login(request, user)
                messages.success(request, f'Welcome {user.name}!')
                return redirect('admin_dashboard')
            else:
                messages.error(request, 'Invalid admin credentials')

    return render(request, 'admin_login.html')


def instructor_login_view(request):
    """Instructor login and registration view"""
    if request.method == 'POST':
        if 'name' in request.POST:  # Registration
            name = request.POST.get('name')
            email = request.POST.get('email')
            username = request.POST.get('username')
            password = request.POST.get('password')

            if not all([name, email, username, password]):
                messages.error(request, 'All fields are required.')
            else:
                # validation
                if User.objects.filter(username=username).exists():
                    messages.error(request, f"Username '{username}' already exists.")
                elif User.objects.filter(email=email).exists():
                    messages.error(request, f"Email '{email}' already exists.")
                else:
                    # create the user
                    user = User.objects.create_user(
                        username=username,
                        email=email,
                        password=password,
                        name=name,
                        role='instructor'
                    )
                    messages.success(request, 'Instructor registered successfully! You can now login.')
        else:  # Login
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)
            if user is not None and user.role == 'instructor':
                login(request, user)
                messages.success(request, f'Welcome {user.name}!')
                return redirect('instructor_dashboard')
            else:
                messages.error(request, 'Invalid instructor credentials')

    return render(request, 'instructor_login.html')


def student_login_view(request):
    """Student login and registration view"""
    if request.method == 'POST':
        if 'name' in request.POST:  # Registration
            name = request.POST.get('name')
            email = request.POST.get('email')
            password = request.POST.get('password')

            if not all([name, email, password]):
                messages.error(request, 'All fields are required.')
            else:
                # auto-generate username from email
                username = email.split('@')[0] if '@' in email else email

                # validation
                if User.objects.filter(username=username).exists():
                    messages.error(request, f"Username '{username}' already exists.")
                elif User.objects.filter(email=email).exists():
                    messages.error(request, f"Email '{email}' already exists.")
                else:
                    # create the user
                    user = User.objects.create_user(
                        username=username,
                        email=email,
                        password=password,
                        name=name,
                        role='student'
                    )
                    messages.success(request, 'Student registered successfully! You can now login.')
        else:  # Login
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)
            if user is not None and user.role == 'student':
                login(request, user)
                messages.success(request, f'Welcome {user.name}!')
                return redirect('student_dashboard')
            else:
                messages.error(request, 'Invalid student credentials')

    return render(request, 'student_login.html')


def logout_view(request):
    """Handle user logout"""
    logout(request)
    return redirect('login')


# ==================== Student Views ====================

def register_student(request):
    """Student registration with auto-generated username."""
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not all([name, email, password]):
            messages.error(request, 'All fields are required.')
            return redirect('register')

        # auto-generate username from email
        username = email.split('@')[0] if '@' in email else email

        # validation
        if User.objects.filter(username=username).exists():
            messages.error(request, f"Username '{username}' already exists.")
            return redirect('register')
        if User.objects.filter(email=email).exists():
            messages.error(request, f"Email '{email}' already exists.")
            return redirect('register')

        # create the user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            name=name,
            role='student'
        )
        messages.success(request, 'Student registered successfully! You can now login.')
        return redirect('login')

    return render(request, 'register.html')


@login_required
def student_dashboard(request):
    """Student dashboard - shows only enrolled courses and user's feedback"""
    if request.user.role != 'student':
        return redirect('login')

    # Get enrolled courses and all available courses for convenience
    enrolled_courses = Enrollment.objects.filter(student=request.user).select_related('course')
    enrolled_course_ids = enrolled_courses.values_list('course_id', flat=True)
    courses = Course.objects.all().select_related('instructor')

    # Get user's feedback
    user_feedback = Feedback.objects.filter(student=request.user).select_related('course')

    # Dashboard metrics
    total_enrolled = enrolled_courses.count()
    total_feedback = user_feedback.count()

    context = {
        'courses': courses,
        'enrolled_courses': enrolled_courses,
        'enrolled_course_ids': enrolled_course_ids,
        'user_feedback': user_feedback,
        'total_enrolled': total_enrolled,
        'total_feedback': total_feedback,
    }
    return render(request, 'student_dashboard.html', context)


@login_required
def view_courses(request):
    """View all available courses for enrollment"""
    if request.user.role != 'student':
        return redirect('login')

    # Get all courses
    courses = Course.objects.all().select_related('instructor')

    # Get enrolled course IDs for this student
    enrolled_course_ids = Enrollment.objects.filter(student=request.user).values_list('course_id', flat=True)

    context = {
        'courses': courses,
        'enrolled_course_ids': enrolled_course_ids,
    }
    return render(request, 'courses.html', context)


@login_required
def enroll_course(request, course_id):
    """Enroll student in a course"""
    if request.user.role != 'student':
        return redirect('login')

    course = get_object_or_404(Course, id=course_id)

    # Check if already enrolled
    if Enrollment.objects.filter(student=request.user, course=course).exists():
        messages.warning(request, 'You are already enrolled in this course.')
    else:
        Enrollment.objects.create(student=request.user, course=course)
        messages.success(request, f'Successfully enrolled in {course.course_name}')

    return redirect('view_courses')


@login_required
def submit_feedback(request, course_id):
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
        feedback_text = request.POST.get('feedback_text')
        sentiment = request.POST.get('sentiment', 'neutral')

        Feedback.objects.create(
            student=request.user,
            course=course,
            feedback_text=feedback_text,
            sentiment=sentiment
        )

        messages.success(request, 'Feedback submitted successfully!')
        return redirect('student_dashboard')

    context = {
        'course': course,
    }
    return render(request, 'submit_feedback.html', context)


# ==================== Instructor Views ====================

@login_required
def instructor_dashboard(request):
    """Instructor dashboard - shows assigned courses and feedback"""
    if request.user.role != 'instructor':
        return redirect('login')

    # Get courses taught by this instructor
    courses = Course.objects.filter(instructor=request.user)

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
    """Admin dashboard - shows analytics and management options"""
    if request.user.role != 'admin':
        return redirect('login')

    # Analytics data
    total_students = User.objects.filter(role='student').count()
    total_instructors = User.objects.filter(role='instructor').count()
    total_courses = Course.objects.count()
    total_feedback = Feedback.objects.count()

    # Feedback sentiment distribution
    sentiment_stats = Feedback.objects.values('sentiment').annotate(count=Count('sentiment'))

    context = {
        'total_students': total_students,
        'total_instructors': total_instructors,
        'total_courses': total_courses,
        'total_feedback': total_feedback,
        'sentiment_stats': sentiment_stats,
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
        course_name = request.POST.get('course_name')
        instructor_id = request.POST.get('instructor')
        description = request.POST.get('description')

        if course_name and instructor_id:
            instructor = get_object_or_404(User, id=instructor_id, role='instructor')
            Course.objects.create(
                course_name=course_name,
                instructor=instructor,
                description=description
            )
            messages.success(request, 'Course created successfully!')
            return redirect('manage_courses')

    context = {
        'courses': courses,
        'instructors': instructors,
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


# ==================== API Views ====================

@csrf_exempt
@login_required
def api_enroll_course(request, course_id):
    """API endpoint for course enrollment"""
    if request.user.role != 'student':
        return JsonResponse({'error': 'Unauthorized'}, status=403)

    if request.method == 'POST':
        course = get_object_or_404(Course, id=course_id)

        if Enrollment.objects.filter(student=request.user, course=course).exists():
            return JsonResponse({'error': 'Already enrolled'}, status=400)

        Enrollment.objects.create(student=request.user, course=course)
        return JsonResponse({'success': True, 'message': 'Enrolled successfully'})

    return JsonResponse({'error': 'Method not allowed'}, status=405)


@csrf_exempt
@login_required
def api_submit_feedback(request, course_id):
    """API endpoint for feedback submission"""
    if request.user.role != 'student':
        return JsonResponse({'error': 'Unauthorized'}, status=403)

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            course = get_object_or_404(Course, id=course_id)

            # Check enrollment
            if not Enrollment.objects.filter(student=request.user, course=course).exists():
                return JsonResponse({'error': 'Not enrolled in this course'}, status=403)

            # Check if feedback already exists
            if Feedback.objects.filter(student=request.user, course=course).exists():
                return JsonResponse({'error': 'Feedback already submitted'}, status=400)

            Feedback.objects.create(
                student=request.user,
                course=course,
                feedback_text=data.get('feedback_text', ''),
                sentiment=data.get('sentiment', 'neutral')
            )

            return JsonResponse({'success': True, 'message': 'Feedback submitted'})

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

    return JsonResponse({'error': 'Method not allowed'}, status=405)




# ==================== Course Views ====================

@require_http_methods(["GET"])
def list_courses(request):
    """Get all courses"""
    try:
        courses = Course.objects.all()
        data = [{
            'id': course.id,
            'name': course.name,
            'instructor': course.instructor,
            'institution_id': course.institution.id if course.institution else None,
            'average_rating': course.get_average_rating(),
            'total_feedback': course.get_feedback_count(),
            'negative_feedback': course.get_negative_feedback_count()
        } for course in courses]
        
        return JsonResponse({'success': True, 'data': data})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@require_http_methods(["GET"])
def course_detail(request, course_id):
    """Get course details"""
    try:
        course = get_object_or_404(Course, id=course_id)
        
        data = {
            'id': course.id,
            'name': course.name,
            'instructor': course.instructor,
            'institution_id': course.institution.id if course.institution else None,
            'average_rating': course.get_average_rating(),
            'total_feedback': course.get_feedback_count(),
            'negative_feedback': course.get_negative_feedback_count(),
            'rating_distribution': course.get_rating_distribution()
        }
        
        return JsonResponse({'success': True, 'data': data})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


# ==================== Feedback Views ====================

@csrf_exempt
@require_http_methods(["POST"])
def submit_feedback(request):
    """Submit feedback for a course"""
    try:
        data = json.loads(request.body)
        
        if not all(k in data for k in ['course_id', 'rating', 'comment']):
            return JsonResponse({'error': 'Missing required fields'}, status=400)
        
        course = get_object_or_404(Course, id=data['course_id'])
        
        # Get student (optional if anonymous)
        student = None
        if request.user.is_authenticated:
            student = request.user
        
        feedback = Feedback.objects.create(
            course=course,
            student=student,
            rating=data['rating'],
            comment=data.get('comment', ''),
            anonymous=data.get('anonymous', False)
        )
        
        return JsonResponse({
            'success': True,
            'message': 'Feedback submitted successfully',
            'feedback_id': feedback.id,
            'created_at': feedback.created_at.isoformat()
        }, status=201)
    
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@require_http_methods(["GET"])
def list_feedback(request):
    """Get all feedback with optional filters"""
    try:
        feedbacks = Feedback.objects.select_related('course', 'student')
        
        # Apply filters
        course_id = request.GET.get('course_id')
        rating = request.GET.get('rating')
        search = request.GET.get('search')
        
        if course_id:
            feedbacks = feedbacks.filter(course_id=course_id)
        
        if rating:
            if rating == 'negative':
                feedbacks = feedbacks.filter(rating__lte=2)
            else:
                feedbacks = feedbacks.filter(rating=int(rating))
        
        if search:
            feedbacks = feedbacks.filter(
                Q(comment__icontains=search) | Q(course__name__icontains=search)
            )
        
        data = [{
            'id': fb.id,
            'course_id': fb.course.id,
            'course_name': fb.course.name,
            'instructor': fb.course.instructor,
            'rating': fb.rating,
            'comment': fb.comment,
            'anonymous': fb.anonymous,
            'student': None if fb.anonymous else (fb.student.username if fb.student else 'Unknown'),
            'created_at': fb.created_at.isoformat(),
            'is_negative': fb.is_negative()
        } for fb in feedbacks]
        
        return JsonResponse({'success': True, 'data': data, 'count': len(data)})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@require_http_methods(["GET"])
def course_feedback(request, course_id):
    """Get all feedback for a specific course"""
    try:
        course = get_object_or_404(Course, id=course_id)
        feedbacks = course.feedback_set.all()
        
        data = [{
            'id': fb.id,
            'rating': fb.rating,
            'comment': fb.comment,
            'anonymous': fb.anonymous,
            'student': None if fb.anonymous else (fb.student.username if fb.student else 'Unknown'),
            'created_at': fb.created_at.isoformat(),
            'is_negative': fb.is_negative()
        } for fb in feedbacks]
        
        return JsonResponse({'success': True, 'data': data, 'count': len(data)})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


# ==================== Analytics Views ====================

@require_http_methods(["GET"])
def feedback_analytics(request):
    """Get overall feedback analytics"""
    try:
        total_feedbacks = Feedback.objects.count()
        average_rating = Feedback.objects.aggregate(Avg('rating'))['rating__avg']
        negative_count = Feedback.objects.filter(rating__lte=2).count()
        
        # Rating distribution
        rating_distribution = {}
        for i in range(1, 6):
            rating_distribution[i] = Feedback.objects.filter(rating=i).count()
        
        # Top rated courses
        top_courses = Course.objects.annotate(
            avg_rating=Avg('feedback_set__rating'),
            feedback_count=Count('feedback_set')
        ).filter(feedback_count__gt=0).order_by('-avg_rating')[:5]
        
        # Courses needing attention
        low_courses = Course.objects.annotate(
            avg_rating=Avg('feedback_set__rating'),
            feedback_count=Count('feedback_set')
        ).filter(avg_rating__lt=3, feedback_count__gt=0).order_by('avg_rating')[:5]
        
        data = {
            'total_feedbacks': total_feedbacks,
            'average_rating': round(average_rating or 0, 2),
            'negative_count': negative_count,
            'negative_percentage': round((negative_count / max(total_feedbacks, 1)) * 100, 1),
            'rating_distribution': rating_distribution,
            'top_courses': [{
                'id': course.id,
                'name': course.name,
                'instructor': course.instructor,
                'average_rating': round(course.avg_rating or 0, 2),
                'feedback_count': course.feedback_count or 0
            } for course in top_courses],
            'low_courses': [{
                'id': course.id,
                'name': course.name,
                'instructor': course.instructor,
                'average_rating': round(course.avg_rating or 0, 2),
                'feedback_count': course.feedback_count or 0
            } for course in low_courses]
        }
        
        return JsonResponse({'success': True, 'data': data})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@require_http_methods(["GET"])
def instructor_analytics(request, employee_id):
    """Get instructor analytics"""
    try:
        instructor = get_object_or_404(InstructorProfile, employee_id=employee_id)
        courses = instructor.get_courses()
        
        total_feedbacks = Feedback.objects.filter(course__in=courses).count()
        average_rating = instructor.get_average_rating()
        negative_count = instructor.get_negative_feedback_count()
        
        course_data = [{
            'id': course.id,
            'name': course.name,
            'average_rating': course.get_average_rating(),
            'total_feedback': course.get_feedback_count(),
            'negative_feedback': course.get_negative_feedback_count()
        } for course in courses]
        
        data = {
            'instructor': {
                'name': instructor.user.get_full_name() or instructor.user.username,
                'employee_id': instructor.employee_id,
                'department': instructor.department
            },
            'total_feedbacks': total_feedbacks,
            'average_rating': average_rating,
            'negative_count': negative_count,
            'courses': course_data
        }
        
        return JsonResponse({'success': True, 'data': data})
    except ObjectDoesNotExist:
        return JsonResponse({'error': 'Instructor not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@require_http_methods(["GET"])
def compare_courses(request):
    """Compare feedback between two courses"""
    try:
        course1_id = request.GET.get('course1_id')
        course2_id = request.GET.get('course2_id')
        
        if not (course1_id and course2_id):
            return JsonResponse({'error': 'Missing course IDs'}, status=400)
        
        course1 = get_object_or_404(Course, id=course1_id)
        course2 = get_object_or_404(Course, id=course2_id)
        
        data = {
            'course1': {
                'id': course1.id,
                'name': course1.name,
                'instructor': course1.instructor,
                'average_rating': course1.get_average_rating(),
                'total_feedback': course1.get_feedback_count(),
                'negative_feedback': course1.get_negative_feedback_count(),
                'rating_distribution': course1.get_rating_distribution()
            },
            'course2': {
                'id': course2.id,
                'name': course2.name,
                'instructor': course2.instructor,
                'average_rating': course2.get_average_rating(),
                'total_feedback': course2.get_feedback_count(),
                'negative_feedback': course2.get_negative_feedback_count(),
                'rating_distribution': course2.get_rating_distribution()
            }
        }
        
        return JsonResponse({'success': True, 'data': data})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)