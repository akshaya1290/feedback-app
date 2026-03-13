from django.urls import path
from . import views

urlpatterns = [
    # Authentication
    path('', views.login_view, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),

    # Student Views
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
    path('student/courses/', views.course_list, name='course_list'),
    path('student/enroll/<int:course_id>/', views.enroll_course, name='enroll_course'),
    path('student/feedback/<int:course_id>/', views.feedback_form, name='feedback_form'),

    # Instructor Views
    path('instructor/dashboard/', views.instructor_dashboard, name='instructor_dashboard'),

    # Admin Views
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/courses/', views.manage_courses, name='manage_courses'),
    path('admin/users/', views.manage_users, name='manage_users'),
]
