from django.contrib import admin
from .models import Institution, Course, Feedback, StudentProfile, InstructorProfile, AdminProfile


@admin.register(Institution)
class InstitutionAdmin(admin.ModelAdmin):
    list_display = ['name', 'location', 'created_at']
    search_fields = ['name', 'location']
    list_filter = ['created_at']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['name', 'instructor', 'institution', 'get_average_rating', 'get_feedback_count', 'created_at']
    search_fields = ['name', 'instructor']
    list_filter = ['institution', 'created_at']
    readonly_fields = ['created_at', 'updated_at']
    
    def get_average_rating(self, obj):
        return f"{obj.get_average_rating()}/5"
    get_average_rating.short_description = 'Avg Rating'


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['course', 'rating', 'student_name', 'is_negative', 'created_at']
    search_fields = ['course__name', 'comment', 'student__username']
    list_filter = ['rating', 'course', 'anonymous', 'created_at']
    readonly_fields = ['created_at', 'updated_at']
    
    def student_name(self, obj):
        if obj.anonymous:
            return '🔒 Anonymous'
        return obj.student.username if obj.student else 'Unknown'
    student_name.short_description = 'Student'


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'student_id', 'institution', 'enrollment_date']
    search_fields = ['user__username', 'student_id']
    list_filter = ['institution', 'enrollment_date']
    readonly_fields = ['enrollment_date']


@admin.register(InstructorProfile)
class InstructorProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'employee_id', 'department', 'institution', 'get_average_rating']
    search_fields = ['user__username', 'employee_id', 'department']
    list_filter = ['institution', 'department']
    
    def get_average_rating(self, obj):
        return f"{obj.get_average_rating()}/5"
    get_average_rating.short_description = 'Avg Rating'


@admin.register(AdminProfile)
class AdminProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'admin_id', 'institution']
    search_fields = ['user__username', 'admin_id']
    list_filter = ['institution']