from django.urls import path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    # Frontend pages
    path('', TemplateView.as_view(template_name='index.html'), name='home'),
    path('index.html', TemplateView.as_view(template_name='index.html'), name='index'),
    path('student_login.html', TemplateView.as_view(template_name='student_login.html'), name='student_login'),
    path('admin_login.html', TemplateView.as_view(template_name='admin_login.html'), name='admin_login'),
    path('instructor_login.html', TemplateView.as_view(template_name='instructor_login.html'), name='instructor_login'),
    path('dashboard.html', TemplateView.as_view(template_name='dashboard.html'), name='dashboard'),
    path('register.html', TemplateView.as_view(template_name='register.html'), name='register'),
    path('admin_dashboard.html', TemplateView.as_view(template_name='admin_dashboard.html'), name='admin_dashboard'),
    path('student_dashboard.html', TemplateView.as_view(template_name='student_dashboard.html'), name='student_dashboard'),
    
    # Authentication
    path('api/auth/register/student/', views.register_student, name='register_student'),
    path('api/auth/register/instructor/', views.register_instructor, name='register_instructor'),
    path('api/auth/register/admin/', views.register_admin, name='register_admin'),
    path('api/auth/login/', views.user_login, name='user_login'),
    path('api/auth/logout/', views.user_logout, name='user_logout'),
    
    # Institution
    path('api/institutions/', views.list_institutions, name='list_institutions'),
    path('api/institutions/<int:institution_id>/', views.institution_detail, name='institution_detail'),
    
    # Courses
    path('api/courses/', views.list_courses, name='list_courses'),
    path('api/courses/<int:course_id>/', views.course_detail, name='course_detail'),
    
    # Feedback
    path('api/feedback/submit/', views.submit_feedback, name='submit_feedback'),
    path('api/feedback/', views.list_feedback, name='list_feedback'),
    path('api/feedback/course/<int:course_id>/', views.course_feedback, name='course_feedback'),
    
    # Analytics
    path('api/analytics/feedback/', views.feedback_analytics, name='feedback_analytics'),
    path('api/analytics/instructor/<str:employee_id>/', views.instructor_analytics, name='instructor_analytics'),
    path('api/analytics/compare/', views.compare_courses, name='compare_courses'),
]
