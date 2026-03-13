from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Course, Enrollment, Feedback


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'name', 'email', 'role', 'is_active']
    list_filter = ['role', 'is_active', 'is_staff']
    search_fields = ['username', 'name', 'email']
    ordering = ['username']

    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('role', 'name')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Info', {'fields': ('role', 'name', 'email')}),
    )


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['course_name', 'instructor', 'created_at']
    search_fields = ['course_name', 'instructor__name']
    list_filter = ['created_at']
    readonly_fields = ['created_at']


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ['student', 'course', 'enrolled_at']
    search_fields = ['student__username', 'course__course_name']
    list_filter = ['enrolled_at']
    readonly_fields = ['enrolled_at']


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['student', 'course', 'sentiment', 'created_at']
    search_fields = ['student__username', 'course__course_name', 'feedback_text']
    list_filter = ['sentiment', 'created_at']
    readonly_fields = ['created_at']