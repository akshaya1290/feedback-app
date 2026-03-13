#!/usr/bin/env python
"""
Quick Start Script for Student Feedback System
Automates initial database setup and test data creation
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from feedback.models import User, Course, Enrollment, Feedback

def create_user(username, email, name, password, role):
    """Create a user"""
    try:
        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                'email': email,
                'name': name,
                'role': role
            }
        )
        if created:
            user.set_password(password)
            user.save()
            print(f"✓ Created {role}: {name}")
        else:
            print(f"✓ {role} already exists: {name}")
        return user
    except Exception as e:
        print(f"✗ Error creating user: {e}")
        return None

def create_course(course_name, instructor, description=''):
    """Create a course"""
    try:
        course, created = Course.objects.get_or_create(
            course_name=course_name,
            instructor=instructor,
            defaults={'description': description}
        )
        if created:
            print(f"✓ Created Course: {course_name}")
        else:
            print(f"✓ Course already exists: {course_name}")
        return course
    except Exception as e:
        print(f"✗ Error creating course: {e}")
        return None

def main():
    print("🚀 Setting up Student Feedback System Demo Data...")
    print("=" * 50)

    # Create admin
    admin = create_user('admin', 'admin@example.com', 'Admin User', 'admin123', 'admin')

    # Create instructors
    instructor1 = create_user('john_doe', 'john@example.com', 'John Doe', 'pass123', 'instructor')
    instructor2 = create_user('jane_smith', 'jane@example.com', 'Jane Smith', 'pass123', 'instructor')

    # Create students
    student1 = create_user('alice', 'alice@example.com', 'Alice Johnson', 'pass123', 'student')
    student2 = create_user('bob', 'bob@example.com', 'Bob Wilson', 'pass123', 'student')
    student3 = create_user('charlie', 'charlie@example.com', 'Charlie Brown', 'pass123', 'student')

    # Create courses
    course1 = create_course('Web Development', instructor1, 'Learn HTML, CSS, JavaScript')
    course2 = create_course('Data Science', instructor2, 'Introduction to data analysis')
    course3 = create_course('Artificial Intelligence', instructor1, 'AI fundamentals')
    course4 = create_course('Cloud Computing', instructor2, 'AWS and cloud technologies')

    # Create enrollments
    if student1 and course1:
        Enrollment.objects.get_or_create(student=student1, course=course1)
        print("✓ Enrolled Alice in Web Development")

    if student1 and course2:
        Enrollment.objects.get_or_create(student=student1, course=course2)
        print("✓ Enrolled Alice in Data Science")

    if student2 and course1:
        Enrollment.objects.get_or_create(student=student2, course=course1)
        print("✓ Enrolled Bob in Web Development")

    # Create feedback
    if student1 and course1:
        Feedback.objects.get_or_create(
            student=student1,
            course=course1,
            defaults={
                'feedback_text': 'Great course! Learned a lot about web development.',
                'sentiment': 'positive'
            }
        )
        print("✓ Created feedback from Alice for Web Development")

    print("=" * 50)
    print("✅ Demo data setup complete!")
    print("\nLogin Credentials:")
    print("Admin: username=admin, password=admin123")
    print("Instructor: username=john_doe, password=pass123")
    print("Student: username=alice, password=pass123")

if __name__ == '__main__':
    main()