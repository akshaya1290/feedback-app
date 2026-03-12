#!/usr/bin/env python
"""
Quick Start Script for Student Feedback System
Automates initial database setup and test data creation
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'feedback_project.settings')
django.setup()

from django.contrib.auth.models import User
from feedback.models import Institution, Course, StudentProfile, InstructorProfile, AdminProfile

def create_institution(name, location, description):
    """Create an institution"""
    try:
        inst, created = Institution.objects.get_or_create(
            name=name,
            defaults={'location': location, 'description': description}
        )
        if created:
            print(f"✓ Created Institution: {name}")
        else:
            print(f"✓ Institution already exists: {name}")
        return inst
    except Exception as e:
        print(f"✗ Error creating institution: {e}")
        return None

def create_courses(institution, courses_list):
    """Create courses for an institution"""
    created_count = 0
    for course_name, instructor, description in courses_list:
        try:
            course, created = Course.objects.get_or_create(
                name=course_name,
                instructor=instructor,
                institution=institution,
                defaults={'description': description}
            )
            if created:
                created_count += 1
                print(f"  ✓ Created Course: {course_name}")
            else:
                print(f"  ✓ Course already exists: {course_name}")
        except Exception as e:
            print(f"  ✗ Error creating {course_name}: {e}")
    
    print(f"\n✓ Created {created_count} new courses\n")

def create_user(username, email, password, first_name, last_name):
    """Create a Django user"""
    try:
        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                'email': email,
                'first_name': first_name,
                'last_name': last_name
            }
        )
        if created:
            user.set_password(password)
            user.save()
            print(f"✓ Created User: {username}")
        else:
            print(f"✓ User already exists: {username}")
        return user
    except Exception as e:
        print(f"✗ Error creating user {username}: {e}")
        return None

def create_student(username, email, password, first_name, last_name, student_id, institution):
    """Create a student user with profile"""
    user = create_user(username, email, password, first_name, last_name)
    if user:
        try:
            profile, created = StudentProfile.objects.get_or_create(
                user=user,
                defaults={'student_id': student_id, 'institution': institution}
            )
            if created:
                print(f"  ✓ Created Student Profile: {student_id}")
            else:
                print(f"  ✓ Student Profile already exists: {student_id}")
        except Exception as e:
            print(f"  ✗ Error creating student profile: {e}")

def create_instructor(username, email, password, first_name, last_name, employee_id, department, institution):
    """Create an instructor user with profile"""
    user = create_user(username, email, password, first_name, last_name)
    if user:
        try:
            profile, created = InstructorProfile.objects.get_or_create(
                user=user,
                defaults={
                    'employee_id': employee_id,
                    'department': department,
                    'institution': institution
                }
            )
            if created:
                print(f"  ✓ Created Instructor Profile: {employee_id}")
            else:
                print(f"  ✓ Instructor Profile already exists: {employee_id}")
        except Exception as e:
            print(f"  ✗ Error creating instructor profile: {e}")

def create_admin(username, email, password, first_name, last_name, admin_id, institution):
    """Create an admin user with profile"""
    user = create_user(username, email, password, first_name, last_name)
    if user:
        user.is_staff = True
        user.is_superuser = True
        user.save()
        try:
            profile, created = AdminProfile.objects.get_or_create(
                user=user,
                defaults={'admin_id': admin_id, 'institution': institution}
            )
            if created:
                print(f"  ✓ Created Admin Profile: {admin_id}")
            else:
                print(f"  ✓ Admin Profile already exists: {admin_id}")
        except Exception as e:
            print(f"  ✗ Error creating admin profile: {e}")

def main():
    """Main setup function"""
    print("\n" + "="*60)
    print("  Student Feedback System - Quick Setup")
    print("="*60 + "\n")
    
    # Create Institution
    print("Creating Institution...")
    institution = create_institution(
        "ABC University",
        "New York, USA",
        "A premier educational institution offering quality education"
    )
    
    if not institution:
        print("✗ Failed to create institution. Exiting.")
        sys.exit(1)
    
    # Create Courses
    print("\nCreating Courses...")
    courses_data = [
        ("Data Science 101", "Dr. Smith", "Introduction to data science and analytics"),
        ("Web Development", "Prof. Johnson", "Learn modern web development with HTML, CSS, and JavaScript"),
        ("Machine Learning", "Dr. Williams", "Deep dive into machine learning algorithms and applications"),
        ("Python Basics", "Prof. Brown", "Master Python programming fundamentals"),
        ("Cloud Computing", "Dr. Davis", "Cloud architecture and deployment strategies"),
        ("Database Design", "Prof. Miller", "Relational and NoSQL database design"),
        ("Mobile App Development", "Dr. Wilson", "Build cross-platform mobile applications"),
        ("Cybersecurity", "Prof. Moore", "Security principles and ethical hacking"),
    ]
    create_courses(institution, courses_data)
    
    # Create Students
    print("Creating Sample Students...")
    students_data = [
        ("student1", "student1@example.com", "pass123", "John", "Doe", "STU001"),
        ("student2", "student2@example.com", "pass123", "Jane", "Smith", "STU002"),
        ("student3", "student3@example.com", "pass123", "Bob", "Johnson", "STU003"),
    ]
    for username, email, password, first_name, last_name, student_id in students_data:
        create_student(username, email, password, first_name, last_name, student_id, institution)
    
    # Create Instructors
    print("\nCreating Sample Instructors...")
    instructors_data = [
        ("instructor1", "instructor1@example.com", "pass123", "Dr.", "Smith", "EMP001", "Computer Science"),
        ("instructor2", "instructor2@example.com", "pass123", "Prof.", "Johnson", "EMP002", "Engineering"),
        ("instructor3", "instructor3@example.com", "pass123", "Dr.", "Williams", "EMP003", "Mathematics"),
    ]
    for username, email, password, first_name, last_name, emp_id, dept in instructors_data:
        create_instructor(username, email, password, first_name, last_name, emp_id, dept, institution)
    
    # Create Admin
    print("\nCreating Admin User...")
    create_admin("admin", "admin@example.com", "admin123", "Admin", "User", "ADM001", institution)
    
    print("\n" + "="*60)
    print("  ✓ Setup Complete!")
    print("="*60)
    print("\n📝 Login Credentials (Demo):")
    print("  Student:    username='student1' password='pass123'")
    print("  Instructor: username='instructor1' password='pass123'")
    print("  Admin:      username='admin' password='admin123'")
    print("\n🚀 Start the server with: python manage.py runserver")
    print("📊 Access admin panel at: http://localhost:8000/admin")
    print("\n" + "="*60 + "\n")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n✗ Setup cancelled by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n✗ Setup failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)