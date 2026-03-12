from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator

class Institution(models.Model):
    name = models.CharField(max_length=200, unique=True)
    location = models.CharField(max_length=300)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name
    
    def get_average_rating(self):
        """Calculate overall average rating for institution"""
        feedbacks = Feedback.objects.filter(course__institution=self)
        if feedbacks.exists():
            return round(sum(f.rating for f in feedbacks) / feedbacks.count(), 2)
        return 0
    
    def get_negative_feedback_count(self):
        """Get count of negative feedback (rating <= 2)"""
        return Feedback.objects.filter(course__institution=self, rating__lte=2).count()


class Course(models.Model):
    name = models.CharField(max_length=200)
    instructor = models.CharField(max_length=200)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE, null=True, blank=True, related_name='courses')
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.instructor}"
    
    def get_average_rating(self):
        """Calculate average rating for this course"""
        feedbacks = self.feedback_set.all()
        if feedbacks.exists():
            return round(sum(f.rating for f in feedbacks) / feedbacks.count(), 2)
        return 0
    
    def get_negative_feedback_count(self):
        """Get count of negative feedback (rating <= 2)"""
        return self.feedback_set.filter(rating__lte=2).count()
    
    def get_feedback_count(self):
        """Get total feedback count"""
        return self.feedback_set.count()
    
    def get_rating_distribution(self):
        """Get distribution of ratings"""
        distribution = {}
        for i in range(1, 6):
            distribution[i] = self.feedback_set.filter(rating=i).count()
        return distribution


class Feedback(models.Model):
    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]
    
    student = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='feedbacks')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='feedback_set')
    rating = models.IntegerField(
        choices=RATING_CHOICES,
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField(blank=True)
    anonymous = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['course', 'rating']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        student_name = 'Anonymous' if self.anonymous else (self.student.username if self.student else 'Unknown')
        return f"Feedback for {self.course} - Rating: {self.rating} - {student_name}"
    
    def is_negative(self):
        """Check if feedback is negative (rating <= 2)"""
        return self.rating <= 2


class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    student_id = models.CharField(max_length=100, unique=True)
    institution = models.ForeignKey(Institution, on_delete=models.SET_NULL, null=True, blank=True)
    enrollment_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.student_id}"


class InstructorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    employee_id = models.CharField(max_length=100, unique=True)
    department = models.CharField(max_length=200, blank=True)
    institution = models.ForeignKey(Institution, on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.employee_id}"
    
    def get_courses(self):
        """Get all courses taught by this instructor"""
        return Course.objects.filter(instructor=self.user.get_full_name() or self.user.username)
    
    def get_average_rating(self):
        """Get average rating across all courses"""
        courses = self.get_courses()
        total_rating = 0
        total_count = 0
        
        for course in courses:
            feedbacks = course.feedback_set.all()
            if feedbacks.exists():
                total_rating += sum(f.rating for f in feedbacks)
                total_count += feedbacks.count()
        
        if total_count > 0:
            return round(total_rating / total_count, 2)
        return 0
    
    def get_negative_feedback_count(self):
        """Get count of negative feedback across all courses"""
        courses = self.get_courses()
        total_negative = 0
        
        for course in courses:
            total_negative += course.feedback_set.filter(rating__lte=2).count()
        
        return total_negative


class AdminProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    admin_id = models.CharField(max_length=100, unique=True)
    institution = models.ForeignKey(Institution, on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.admin_id}"