from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Count, Q
from django.utils import timezone
import json
from datetime import datetime, timedelta

from .models import (
    Institution, Course, Feedback, StudentProfile, 
    InstructorProfile, AdminProfile
)


# ==================== Authentication Views ====================

@csrf_exempt
@require_http_methods(["POST"])
def register_student(request):
    """Register a new student"""
    try:
        data = json.loads(request.body)
        
        # Validate required fields
        if not all(k in data for k in ['username', 'email', 'password', 'student_id', 'full_name']):
            return JsonResponse({'error': 'Missing required fields'}, status=400)
        
        # Check if user already exists
        if User.objects.filter(username=data['username']).exists():
            return JsonResponse({'error': 'Username already exists'}, status=400)
        
        if User.objects.filter(email=data['email']).exists():
            return JsonResponse({'error': 'Email already exists'}, status=400)
        
        # Create user
        user = User.objects.create_user(
            username=data['username'],
            email=data['email'],
            password=data['password'],
            first_name=data.get('full_name', '').split()[0],
            last_name=' '.join(data.get('full_name', '').split()[1:])
        )
        
        # Create student profile
        institution = None
        if data.get('institution_id'):
            institution = get_object_or_404(Institution, id=data['institution_id'])
        
        StudentProfile.objects.create(
            user=user,
            student_id=data['student_id'],
            institution=institution
        )
        
        return JsonResponse({
            'success': True,
            'message': 'Student registered successfully',
            'user_id': user.id
        }, status=201)
    
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def register_instructor(request):
    """Register a new instructor"""
    try:
        data = json.loads(request.body)
        
        if not all(k in data for k in ['username', 'email', 'password', 'employee_id', 'full_name']):
            return JsonResponse({'error': 'Missing required fields'}, status=400)
        
        if User.objects.filter(username=data['username']).exists():
            return JsonResponse({'error': 'Username already exists'}, status=400)
        
        user = User.objects.create_user(
            username=data['username'],
            email=data['email'],
            password=data['password'],
            first_name=data.get('full_name', '').split()[0],
            last_name=' '.join(data.get('full_name', '').split()[1:])
        )
        
        institution = None
        if data.get('institution_id'):
            institution = get_object_or_404(Institution, id=data['institution_id'])
        
        InstructorProfile.objects.create(
            user=user,
            employee_id=data['employee_id'],
            department=data.get('department', ''),
            institution=institution
        )
        
        return JsonResponse({
            'success': True,
            'message': 'Instructor registered successfully',
            'user_id': user.id
        }, status=201)
    
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def register_admin(request):
    """Register a new admin"""
    try:
        data = json.loads(request.body)
        
        if not all(k in data for k in ['username', 'email', 'password', 'admin_id', 'full_name']):
            return JsonResponse({'error': 'Missing required fields'}, status=400)
        
        if User.objects.filter(username=data['username']).exists():
            return JsonResponse({'error': 'Username already exists'}, status=400)
        
        user = User.objects.create_user(
            username=data['username'],
            email=data['email'],
            password=data['password'],
            is_staff=True,
            first_name=data.get('full_name', '').split()[0],
            last_name=' '.join(data.get('full_name', '').split()[1:])
        )
        
        institution = None
        if data.get('institution_id'):
            institution = get_object_or_404(Institution, id=data['institution_id'])
        
        AdminProfile.objects.create(
            user=user,
            admin_id=data['admin_id'],
            institution=institution
        )
        
        return JsonResponse({
            'success': True,
            'message': 'Admin registered successfully',
            'user_id': user.id
        }, status=201)
    
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def user_login(request):
    """Login user"""
    try:
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        role = data.get('role', 'student')  # student, instructor, admin
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            
            # Determine user role and return appropriate data
            user_data = {
                'user_id': user.id,
                'username': user.username,
                'email': user.email,
                'is_staff': user.is_staff
            }
            
            if role == 'student' and hasattr(user, 'studentprofile'):
                user_data['role'] = 'student'
                user_data['profile_id'] = user.studentprofile.id
            elif role == 'instructor' and hasattr(user, 'instructorprofile'):
                user_data['role'] = 'instructor'
                user_data['profile_id'] = user.instructorprofile.id
            elif role == 'admin' and hasattr(user, 'adminprofile'):
                user_data['role'] = 'admin'
                user_data['profile_id'] = user.adminprofile.id
            
            return JsonResponse({
                'success': True,
                'message': 'Login successful',
                'user': user_data
            })
        else:
            return JsonResponse({'error': 'Invalid credentials'}, status=401)
    
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
def user_logout(request):
    """Logout user"""
    logout(request)
    return JsonResponse({'success': True, 'message': 'Logout successful'})


# ==================== Institution Views ====================

@require_http_methods(["GET"])
def list_institutions(request):
    """Get all institutions"""
    try:
        institutions = Institution.objects.all()
        data = [{
            'id': inst.id,
            'name': inst.name,
            'location': inst.location,
            'description': inst.description,
            'average_rating': inst.get_average_rating(),
            'total_feedback': Feedback.objects.filter(course__institution=inst).count(),
            'negative_feedback': inst.get_negative_feedback_count(),
            'total_courses': inst.courses.count()
        } for inst in institutions]
        
        return JsonResponse({'success': True, 'data': data})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@require_http_methods(["GET"])
def institution_detail(request, institution_id):
    """Get institution details"""
    try:
        institution = get_object_or_404(Institution, id=institution_id)
        
        courses = institution.courses.all()
        total_feedback = Feedback.objects.filter(course__institution=institution)
        
        data = {
            'id': institution.id,
            'name': institution.name,
            'location': institution.location,
            'description': institution.description,
            'average_rating': institution.get_average_rating(),
            'total_courses': courses.count(),
            'total_feedback': total_feedback.count(),
            'negative_feedback': institution.get_negative_feedback_count(),
            'negative_feedback_rate': round((institution.get_negative_feedback_count() / max(total_feedback.count(), 1)) * 100, 1),
            'courses': [{
                'id': course.id,
                'name': course.name,
                'instructor': course.instructor,
                'average_rating': course.get_average_rating(),
                'total_feedback': course.get_feedback_count(),
                'negative_feedback': course.get_negative_feedback_count()
            } for course in courses]
        }
        
        return JsonResponse({'success': True, 'data': data})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


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