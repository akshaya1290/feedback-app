// Sample Data
let mockData = {
    courses: [
        { id: 1, name: "Data Science 101", instructor: "Dr. Smith", avgRating: 4.5, feedbackCount: 25 },
        { id: 2, name: "Web Development", instructor: "Prof. Johnson", avgRating: 3.8, feedbackCount: 18 },
        { id: 3, name: "Machine Learning", instructor: "Dr. Williams", avgRating: 4.2, feedbackCount: 22 },
        { id: 4, name: "Python Basics", instructor: "Prof. Brown", avgRating: 2.1, feedbackCount: 15 },
        { id: 5, name: "Cloud Computing", instructor: "Dr. Davis", avgRating: 3.5, feedbackCount: 12 }
    ],
    feedback: [],
    institution: {
        name: "ABC University",
        location: "New York, USA",
        totalCourses: 12,
        totalStudents: 456
    }
};

// Load courses from API
async function loadCoursesFromAPI() {
    try {
        console.log('Loading courses from API...');
        const response = await fetch('http://localhost:8000/api/courses/');
        const data = await response.json();
        
        console.log('API Response:', data);
        
        if (data.success && Array.isArray(data.data)) {
            // Replace mockData courses with API courses
            mockData.courses = data.data.map(course => ({
                id: course.id,
                name: course.name,
                instructor: course.instructor,
                avgRating: 0,
                feedbackCount: 0
            }));
            console.log('Courses loaded from API:', mockData.courses);
        } else if (Array.isArray(data)) {
            mockData.courses = data.map(course => ({
                id: course.id,
                name: course.name,
                instructor: course.instructor,
                avgRating: 0,
                feedbackCount: 0
            }));
            console.log('Courses loaded (array format):', mockData.courses);
        }
    } catch(error) {
        console.error('Error loading courses from API:', error);
        console.log('Using fallback mockData courses');
    }
}

// Page Navigation
document.querySelectorAll('.sidebar .nav-link').forEach(link => {
    link.addEventListener('click', (e) => {
        e.preventDefault();
        const pageId = link.getAttribute('data-page');
        navigateToPage(pageId);
    });
});

function navigateToPage(pageId) {
    // Check access control for admin and institution pages
    const userRole = localStorage.getItem('userRole');
    
    if ((pageId === 'admin-dashboard' || pageId === 'feedback-comparison' || pageId === 'institution') && userRole !== 'admin') {
        alert('Access Denied! Admin access required.');
        return;
    }

    if (pageId === 'instructor-dashboard' && userRole !== 'instructor' && userRole !== 'admin') {
        alert('Access Denied! Instructor access required.');
        return;
    }

    // Hide all pages
    document.querySelectorAll('.page-content').forEach(page => {
        page.classList.remove('active');
    });

    // Show selected page
    const selectedPage = document.getElementById(pageId);
    if (selectedPage) {
        selectedPage.classList.add('active');
    }

    // Update page title
    const titles = {
        'student-dashboard': 'Student Dashboard',
        'feedback-form': 'Submit Feedback',
        'instructor-dashboard': 'My Notifications',
        'admin-dashboard': 'Admin Dashboard',
        'feedback-comparison': 'Compare Feedback',
        'institution': 'Institution Summary'
    };

    document.getElementById('page-title').textContent = titles[pageId] || 'Dashboard';

    // Initialize page-specific content
    switch(pageId) {
        case 'student-dashboard':
            initStudentDashboard();
            break;
        case 'feedback-form':
            initFeedbackForm();
            break;
        case 'instructor-dashboard':
            initInstructorDashboard();
            break;
        case 'admin-dashboard':
            initAdminDashboard();
            break;
        case 'feedback-comparison':
            initFeedbackComparison();
            break;
        case 'institution':
            initInstitutionSummary();
            break;
    }
}

// Student Dashboard
function initStudentDashboard() {
    const studentFeedback = mockData.feedback.slice(0, 5);
    
    document.getElementById('avg-rating').textContent = (4.5).toFixed(1);
    document.getElementById('total-feedback').textContent = studentFeedback.length;
    document.getElementById('courses-rated').textContent = new Set(studentFeedback.map(f => f.courseId)).size;

    const feedbackList = document.getElementById('student-feedback-list');
    feedbackList.innerHTML = '';

    studentFeedback.forEach(fb => {
        const course = mockData.courses.find(c => c.id === fb.courseId);
        const stars = '★'.repeat(fb.rating) + '☆'.repeat(5 - fb.rating);
        
        feedbackList.innerHTML += `
            <div class="feedback-item${fb.rating <= 2 ? ' negative-feedback' : ''}">
                <div class="d-flex justify-content-between align-items-start mb-2">
                    <div>
                        <h6 class="mb-0">${course.name}</h6>
                        <small class="text-muted">Instructor: ${course.instructor}</small>
                    </div>
                    <span class="rating-badge">${stars}</span>
                </div>
                <p class="mb-2">"${fb.comment}"</p>
                <small class="text-muted">${fb.date}</small>
            </div>
        `;
    });
}

// Feedback Form
async function initFeedbackForm() {
    const courseSelect = document.getElementById('course-select');
    courseSelect.innerHTML = '<option value="">-- Loading Courses --</option>';
    
    try {
        const response = await fetch('http://localhost:8000/api/courses/');
        const data = await response.json();
        
        let courses = [];
        if (data.success && Array.isArray(data.data)) {
            courses = data.data;
        } else if (Array.isArray(data)) {
            courses = data;
        }
        
        courseSelect.innerHTML = '<option value="">-- Choose a Course --</option>';
        courses.forEach(course => {
            courseSelect.innerHTML += `<option value="${course.id}">${course.name} - ${course.instructor}</option>`;
        });
    } catch(error) {
        console.error('Error loading courses:', error);
        courseSelect.innerHTML = '<option value="">Error loading courses</option>';
        
        // Fallback to mockData
        courseSelect.innerHTML = '<option value="">-- Choose a Course --</option>';
        mockData.courses.forEach(course => {
            courseSelect.innerHTML += `<option value="${course.id}">${course.name} - ${course.instructor}</option>`;
        });
    }

    // Rating selection
    document.querySelectorAll('input[name="rating"]').forEach(radio => {
        radio.addEventListener('change', updateRatingText);
    });

    // Initialize rating text on page load
    updateRatingText();

    // Form submission
    document.getElementById('feedback-form-element').addEventListener('submit', function(e) {
        e.preventDefault();
        
        const courseId = document.getElementById('course-select').value.trim();
        const ratingElement = document.querySelector('input[name="rating"]:checked');
        const rating = ratingElement ? ratingElement.value : null;
        const comment = document.getElementById('comment').value.trim();
        const anonymous = document.getElementById('anonymous').checked;

        // Validation - all fields must be filled
        if (!courseId) {
            alert('⚠️ Please select a course');
            return;
        }

        if (!rating) {
            alert('⚠️ Please select a rating');
            return;
        }

        if (!comment) {
            alert('⚠️ Please write a comment');
            return;
        }

        // Add new feedback
        const newFeedback = {
            id: mockData.feedback.length + 1,
            courseId: parseInt(courseId),
            rating: parseInt(rating),
            comment: comment,
            anonymous: anonymous,
            student: anonymous ? null : "Current Student",
            date: new Date().toISOString().split('T')[0]
        };

        mockData.feedback.push(newFeedback);
        
        // Save to localStorage
        localStorage.setItem('feedbackData', JSON.stringify(mockData.feedback));

        // Reset form
        document.getElementById('feedback-form-element').reset();
        document.getElementById('rate4').checked = true;
        updateRatingText();

        // Show success message
        showAlert('✅ Feedback submitted successfully!', 'success');
    });
}

function updateRatingText() {
    const rating = document.querySelector('input[name="rating"]:checked').value;
    const ratings = { 1: 'Poor', 2: 'Fair', 3: 'Average', 4: 'Good', 5: 'Excellent' };
    document.getElementById('rating-text').textContent = `${ratings[rating]} (${rating})`;
}

// Admin Dashboard
let ratingChart = null;
let courseChart = null;

function initAdminDashboard() {
    // Calculate statistics
    const negativeCount = mockData.feedback.filter(f => f.rating <= 2).length;
    const avgRating = (mockData.feedback.reduce((sum, f) => sum + f.rating, 0) / mockData.feedback.length).toFixed(2);
    
    document.getElementById('admin-total-feedback').textContent = mockData.feedback.length;
    document.getElementById('admin-negative-feedback').textContent = negativeCount;
    document.getElementById('admin-avg-rating').textContent = avgRating;
    
    // Count instructors with many negative ratings
    const instructorsAtRisk = mockData.courses.filter(course => {
        const courseFeedback = mockData.feedback.filter(f => f.courseId === course.id);
        const negativeCount = courseFeedback.filter(f => f.rating <= 2).length;
        return negativeCount >= 2;
    }).length;
    document.getElementById('instructors-at-risk').textContent = instructorsAtRisk;

    // Populate course filter
    const courseFilter = document.getElementById('filter-course');
    courseFilter.innerHTML = '<option value="">All Courses</option>';
    mockData.courses.forEach(course => {
        courseFilter.innerHTML += `<option value="${course.id}">${course.name}</option>`;
    });

    // Show instructor warnings
    showInstructorWarnings();

    // Render feedback list
    renderFeedbackList(mockData.feedback);

    // Draw charts
    drawCharts();

    // Add event listeners for search and filter
    document.getElementById('search-feedback').addEventListener('input', filterFeedback);
    document.getElementById('filter-rating').addEventListener('change', filterFeedback);
    document.getElementById('filter-course').addEventListener('change', filterFeedback);
    document.getElementById('reset-filters').addEventListener('click', resetFilters);
}

function showInstructorWarnings() {
    const container = document.getElementById('instructor-warnings');
    container.innerHTML = '';

    mockData.courses.forEach(course => {
        const courseFeedback = mockData.feedback.filter(f => f.courseId === course.id);
        const negativeCount = courseFeedback.filter(f => f.rating <= 2).length;
        const avgRating = courseFeedback.length > 0
            ? (courseFeedback.reduce((sum, f) => sum + f.rating, 0) / courseFeedback.length).toFixed(2)
            : 0;

        if (negativeCount >= 2) {
            container.innerHTML += `
                <div class="alert alert-danger alert-dismissible fade show" role="alert">
                    <i class="fas fa-exclamation-circle"></i> <strong>Warning!</strong>
                    <br>Instructor <strong>"${course.instructor}"</strong> for <strong>"${course.name}"</strong> has received ${negativeCount} negative ratings (≤2 stars). 
                    Current average: <strong>${avgRating}/5</strong>
                    <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                </div>
            `;
        }
    });
}

function renderFeedbackList(feedbacks) {
    const feedbackList = document.getElementById('feedback-list');
    feedbackList.innerHTML = '';

    if (feedbacks.length === 0) {
        feedbackList.innerHTML = '<p class="text-muted">No feedback found</p>';
        return;
    }

    feedbacks.forEach(fb => {
        const course = mockData.courses.find(c => c.id === fb.courseId);
        const stars = '★'.repeat(fb.rating) + '☆'.repeat(5 - fb.rating);
        const isNegative = fb.rating <= 2;

        feedbackList.innerHTML += `
            <div class="feedback-card${isNegative ? ' negative-feedback' : ''}">
                <div class="feedback-header">
                    <div>
                        <h6 class="mb-0">${course.name}</h6>
                        <small class="text-muted">Instructor: ${course.instructor}</small>
                    </div>
                    <div class="d-flex gap-2">
                        <span class="rating-badge">${stars}</span>
                        ${isNegative ? '<span class="badge bg-danger">⚠ Negative</span>' : ''}
                    </div>
                </div>
                <p class="feedback-comment">${fb.comment}</p>
                <div class="feedback-footer">
                    <small class="text-muted">
                        ${fb.anonymous ? '<i class="fas fa-mask"></i> Anonymous' : 'By: ' + fb.student}
                    </small>
                    <small class="text-muted">${fb.date}</small>
                </div>
            </div>
        `;
    });
}

function filterFeedback() {
    const searchTerm = document.getElementById('search-feedback').value.toLowerCase();
    const ratingFilter = document.getElementById('filter-rating').value;
    const courseFilter = document.getElementById('filter-course').value;

    let filtered = mockData.feedback.filter(fb => {
        const course = mockData.courses.find(c => c.id === fb.courseId);
        
        // Search filter
        if (searchTerm && !course.name.toLowerCase().includes(searchTerm) && 
            !fb.comment.toLowerCase().includes(searchTerm)) {
            return false;
        }

        // Rating filter
        if (ratingFilter) {
            if (ratingFilter === 'negative' && fb.rating > 2) {
                return false;
            } else if (ratingFilter !== 'negative' && fb.rating !== parseInt(ratingFilter)) {
                return false;
            }
        }

        // Course filter
        if (courseFilter && fb.courseId !== parseInt(courseFilter)) {
            return false;
        }

        return true;
    });

    renderFeedbackList(filtered);
}

function resetFilters() {
    document.getElementById('search-feedback').value = '';
    document.getElementById('filter-rating').value = '';
    document.getElementById('filter-course').value = '';
    renderFeedbackList(mockData.feedback);
}

// Instructor Dashboard
function initInstructorDashboard() {
    const userRole = localStorage.getItem('userRole');
    
    // Get all courses taught by this instructor (in a real app, filter by actual instructor)
    const instructorCourses = mockData.courses;
    let totalNotifications = 0;
    let totalRating = 0;
    let feedbackCount = 0;

    // Calculate notifications and ratings
    instructorCourses.forEach(course => {
        const courseFeedback = mockData.feedback.filter(f => f.courseId === course.id);
        const negativeCount = courseFeedback.filter(f => f.rating <= 2).length;
        
        if (negativeCount >= 2) {
            totalNotifications += negativeCount;
        }

        courseFeedback.forEach(fb => {
            totalRating += fb.rating;
            feedbackCount++;
        });
    });

    const avgRating = feedbackCount > 0 ? (totalRating / feedbackCount).toFixed(2) : 0;
    
    document.getElementById('notification-count').textContent = totalNotifications;
    document.getElementById('instructor-avg-rating').textContent = avgRating;

    // Show notifications
    const notificationContainer = document.getElementById('instructor-notifications');
    notificationContainer.innerHTML = '';
    
    let hasNotifications = false;
    instructorCourses.forEach(course => {
        const courseFeedback = mockData.feedback.filter(f => f.courseId === course.id);
        const negativeCount = courseFeedback.filter(f => f.rating <= 2).length;
        const avgCourseRating = courseFeedback.length > 0
            ? (courseFeedback.reduce((sum, f) => sum + f.rating, 0) / courseFeedback.length).toFixed(2)
            : 0;

        if (negativeCount >= 2) {
            hasNotifications = true;
            notificationContainer.innerHTML += `
                <div class="alert alert-danger" role="alert">
                    <i class="fas fa-exclamation-circle"></i> <strong>Attention Required!</strong>
                    <br><strong>${course.name}</strong> has received <strong>${negativeCount} negative ratings</strong> (≤2 stars)
                    <br>Current Average: <strong>${avgCourseRating}/5</strong>
                    <br><small class="text-muted">Review this feedback and make improvements</small>
                </div>
            `;
        }
    });

    // Show recent feedback for this instructor
    const recentFeedback = mockData.feedback.slice(-5).reverse();
    if (recentFeedback.length > 0) {
        notificationContainer.innerHTML += '<h6 class="mt-4 mb-3">Recent Feedback</h6>';
        recentFeedback.forEach(fb => {
            const course = mockData.courses.find(c => c.id === fb.courseId);
            const stars = '★'.repeat(fb.rating) + '☆'.repeat(5 - fb.rating);
            const isNegative = fb.rating <= 2;
            
            notificationContainer.innerHTML += `
                <div class="feedback-card${isNegative ? ' negative-feedback' : ''}">
                    <div class="feedback-header">
                        <div>
                            <h6 class="mb-0">${course.name}</h6>
                            <small class="text-muted">${new Date(fb.date).toLocaleDateString()}</small>
                        </div>
                        <span class="rating-badge">${stars}</span>
                    </div>
                    <p class="feedback-comment">"${fb.comment}"</p>
                    <small class="text-muted">${fb.anonymous ? '<i class="fas fa-mask"></i> Anonymous' : 'By: ' + fb.student}</small>
                </div>
            `;
        });
    }

    if (!hasNotifications && recentFeedback.length === 0) {
        notificationContainer.innerHTML = '<p class="text-muted" style="text-align:center; padding: 30px;">No notifications at this time. Keep up the good work!</p>';
    }
}

// Feedback Comparison
function initFeedbackComparison() {
    // Populate course selects
    const fromSelect = document.getElementById('compare-from-course');
    const toSelect = document.getElementById('compare-to-course');
    
    fromSelect.innerHTML = '<option value="">Select Course</option>';
    toSelect.innerHTML = '<option value="">Select Course</option>';
    
    mockData.courses.forEach(course => {
        fromSelect.innerHTML += `<option value="${course.id}">${course.name}</option>`;
        toSelect.innerHTML += `<option value="${course.id}">${course.name}</option>`;
    });

    // Handle comparison
    document.getElementById('run-comparison').addEventListener('click', compareFeedback);
}

function compareFeedback() {
    const courseId1 = parseInt(document.getElementById('compare-from-course').value);
    const courseId2 = parseInt(document.getElementById('compare-to-course').value);

    if (!courseId1 || !courseId2 || courseId1 === courseId2) {
        alert('Please select two different courses');
        return;
    }

    const course1 = mockData.courses.find(c => c.id === courseId1);
    const course2 = mockData.courses.find(c => c.id === courseId2);
    
    const feedback1 = mockData.feedback.filter(f => f.courseId === courseId1);
    const feedback2 = mockData.feedback.filter(f => f.courseId === courseId2);

    // Calculate stats
    const stats1 = {
        rating: feedback1.length > 0 ? (feedback1.reduce((sum, f) => sum + f.rating, 0) / feedback1.length).toFixed(2) : 0,
        count: feedback1.length,
        negative: feedback1.filter(f => f.rating <= 2).length
    };

    const stats2 = {
        rating: feedback2.length > 0 ? (feedback2.reduce((sum, f) => sum + f.rating, 0) / feedback2.length).toFixed(2) : 0,
        count: feedback2.length,
        negative: feedback2.filter(f => f.rating <= 2).length
    };

    // Display course 1 info
    document.getElementById('course1-name').textContent = course1.name;
    document.getElementById('course1-rating').textContent = stats1.rating;
    document.getElementById('course1-count').textContent = stats1.count;
    document.getElementById('course1-negative').textContent = stats1.negative;

    let course1Html = '';
    feedback1.forEach(fb => {
        const stars = '★'.repeat(fb.rating) + '☆'.repeat(5 - fb.rating);
        course1Html += `
            <div class="feedback-item${fb.rating <= 2 ? ' negative-feedback' : ''}" style="margin-bottom: 10px;">
                <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                    <span>${stars}</span>
                </div>
                <small>"${fb.comment}"</small>
            </div>
        `;
    });
    document.getElementById('course1-feedback').innerHTML = course1Html || '<p class="text-muted">No feedback yet</p>';

    // Display course 2 info
    document.getElementById('course2-name').textContent = course2.name;
    document.getElementById('course2-rating').textContent = stats2.rating;
    document.getElementById('course2-count').textContent = stats2.count;
    document.getElementById('course2-negative').textContent = stats2.negative;

    let course2Html = '';
    feedback2.forEach(fb => {
        const stars = '★'.repeat(fb.rating) + '☆'.repeat(5 - fb.rating);
        course2Html += `
            <div class="feedback-item${fb.rating <= 2 ? ' negative-feedback' : ''}" style="margin-bottom: 10px;">
                <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                    <span>${stars}</span>
                </div>
                <small>"${fb.comment}"</small>
            </div>
        `;
    });
    document.getElementById('course2-feedback').innerHTML = course2Html || '<p class="text-muted">No feedback yet</p>';

    // Comparison analysis
    let analysis = `
        <div class="row">
            <div class="col-md-6">
                <h6>Rating Difference</h6>
                <p>${Math.abs(stats1.rating - stats2.rating).toFixed(2)} points</p>
                <p class="text-muted"><strong>${course1.name}</strong> is ${stats1.rating > stats2.rating ? 'better' : 'worse'} rated</p>
            </div>
            <div class="col-md-6">
                <h6>Feedback Volume</h6>
                <p>Total: ${stats1.count + stats2.count}</p>
                <p class="text-muted">${course1.name}: ${stats1.count} | ${course2.name}: ${stats2.count}</p>
            </div>
        </div>
        <hr>
        <div class="row">
            <div class="col-md-6">
                <h6>Negative Feedback</h6>
                <p>${course1.name}: <span class="text-danger">${stats1.negative}</span></p>
                <p>${course2.name}: <span class="text-danger">${stats2.negative}</span></p>
            </div>
            <div class="col-md-6">
                <h6>Overall Status</h6>
                <p class="text-muted">${stats1.rating >= 4 ? '✓ ' + course1.name + ' performing well' : '⚠ ' + course1.name + ' needs improvement'}</p>
                <p class="text-muted">${stats2.rating >= 4 ? '✓ ' + course2.name + ' performing well' : '⚠ ' + course2.name + ' needs improvement'}</p>
            </div>
        </div>
    `;

    document.getElementById('comparison-analysis').innerHTML = analysis;
    document.getElementById('comparison-results').style.display = 'block';
}

function drawCharts() {
    // Rating Distribution Chart
    const ratingCounts = { 1: 0, 2: 0, 3: 0, 4: 0, 5: 0 };
    mockData.feedback.forEach(fb => {
        ratingCounts[fb.rating]++;
    });

    const ratingCtx = document.getElementById('ratingChart').getContext('2d');
    if (ratingChart) ratingChart.destroy();
    
    ratingChart = new Chart(ratingCtx, {
        type: 'bar',
        data: {
            labels: ['1 Star', '2 Stars', '3 Stars', '4 Stars', '5 Stars'],
            datasets: [{
                label: 'Feedback Count',
                data: [ratingCounts[1], ratingCounts[2], ratingCounts[3], ratingCounts[4], ratingCounts[5]],
                backgroundColor: ['#dc3545', '#fd7e14', '#ffc107', '#28a745', '#20c997']
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            scales: {
                y: { beginAtZero: true }
            },
            plugins: {
                legend: { display: false }
            }
        }
    });

    // Course Performance Chart
    const courseLabels = mockData.courses.map(c => c.name.substring(0, 12));
    const courseRatings = mockData.courses.map(course => {
        const feedbacks = mockData.feedback.filter(f => f.courseId === course.id);
        return feedbacks.length > 0 
            ? (feedbacks.reduce((sum, f) => sum + f.rating, 0) / feedbacks.length).toFixed(2)
            : 0;
    });

    const courseCtx = document.getElementById('courseChart').getContext('2d');
    if (courseChart) courseChart.destroy();
    
    courseChart = new Chart(courseCtx, {
        type: 'radar',
        data: {
            labels: courseLabels,
            datasets: [{
                label: 'Average Rating',
                data: courseRatings,
                borderColor: '#007bff',
                backgroundColor: 'rgba(0, 123, 255, 0.1)',
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            scales: {
                r: {
                    min: 0,
                    max: 5
                }
            }
        }
    });
}

// Institution Summary
function initInstitutionSummary() {
    const inst = mockData.institution;
    document.getElementById('inst-name').textContent = inst.name;
    document.getElementById('inst-location').textContent = inst.location;
    document.getElementById('inst-courses').textContent = inst.totalCourses;
    document.getElementById('inst-students').textContent = inst.totalStudents;

    const avgRating = (mockData.feedback.reduce((sum, f) => sum + f.rating, 0) / mockData.feedback.length).toFixed(2);
    const negativeCount = mockData.feedback.filter(f => f.rating <= 2).length;
    const negativeRate = ((negativeCount / mockData.feedback.length) * 100).toFixed(1);

    document.getElementById('inst-avg-rating').textContent = avgRating;
    document.getElementById('inst-total-feedback').textContent = mockData.feedback.length;
    document.getElementById('inst-negative-count').textContent = negativeCount;
    document.getElementById('inst-negative-rate').textContent = negativeRate + '%';

    // Top courses
    const coursePerformance = mockData.courses.map(course => {
        const feedbacks = mockData.feedback.filter(f => f.courseId === course.id);
        const avgRating = feedbacks.length > 0
            ? (feedbacks.reduce((sum, f) => sum + f.rating, 0) / feedbacks.length).toFixed(2)
            : 0;
        return { ...course, avgRating: parseFloat(avgRating), feedbackCount: feedbacks.length };
    });

    const topCourses = coursePerformance
        .sort((a, b) => b.avgRating - a.avgRating)
        .slice(0, 3);

    const topCoursesContainer = document.getElementById('top-courses');
    topCoursesContainer.innerHTML = '';
    topCourses.forEach(course => {
        const stars = '★'.repeat(Math.round(course.avgRating)) + '☆'.repeat(5 - Math.round(course.avgRating));
        topCoursesContainer.innerHTML += `
            <div class="course-item">
                <div class="course-info">
                    <h6 class="mb-0">${course.name}</h6>
                    <small class="text-muted">Instructor: ${course.instructor}</small>
                </div>
                <div class="course-stats">
                    <span class="rating-badge">${stars}</span>
                    <span>${course.avgRating}/5 (${course.feedbackCount} reviews)</span>
                </div>
            </div>
        `;
    });

    // Low rated courses
    const lowRatedCourses = coursePerformance
        .sort((a, b) => a.avgRating - b.avgRating)
        .slice(0, 3);

    const lowCoursesContainer = document.getElementById('low-rated-courses');
    lowCoursesContainer.innerHTML = '';
    lowRatedCourses.forEach(course => {
        const stars = '★'.repeat(Math.round(course.avgRating)) + '☆'.repeat(5 - Math.round(course.avgRating));
        lowCoursesContainer.innerHTML += `
            <div class="course-item low-rated">
                <div class="course-info">
                    <h6 class="mb-0">${course.name}</h6>
                    <small class="text-muted">Instructor: ${course.instructor}</small>
                </div>
                <div class="course-stats">
                    <span class="rating-badge">${stars}</span>
                    <span class="text-danger">${course.avgRating}/5 (${course.feedbackCount} reviews)</span>
                </div>
            </div>
        `;
    });
}

// Utility function to show alerts
function showAlert(message, type) {
    const alertBox = document.createElement('div');
    alertBox.className = `alert alert-${type} alert-dismissible fade show`;
    alertBox.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    document.querySelector('.content-area').insertBefore(alertBox, document.querySelector('.page-content.active'));
    setTimeout(() => alertBox.remove(), 5000);
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', async () => {
    // Load courses from API first
    await loadCoursesFromAPI();
    
    // Check authentication
    const userRole = localStorage.getItem('userRole');
    const username = localStorage.getItem('username');
    
    if (!userRole) {
        window.location.href = 'index.html';
        return;
    }

    // Display user info
    const userDisplay = username || 'User';
    const userElements = document.querySelectorAll('#username');
    userElements.forEach(el => el.textContent = userDisplay);
    
    const roleBadgeMap = {
        'student': 'Student',
        'admin': 'Admin',
        'instructor': 'Instructor'
    };
    const roleBadges = document.querySelectorAll('#user-role-badge');
    roleBadges.forEach(badge => {
        badge.textContent = roleBadgeMap[userRole] || 'User';
    });
    
    // Color code the badge
    const colorMap = {
        'student': '#667eea',
        'admin': '#dc3545',
        'instructor': '#fd7e14'
    };
    roleBadges.forEach(badge => {
        badge.style.background = colorMap[userRole] || '#667eea';
    });

    // Load feedback from localStorage if exists
    const savedFeedback = localStorage.getItem('feedbackData');
    if (savedFeedback) {
        try {
            mockData.feedback = JSON.parse(savedFeedback);
        } catch(e) {
            console.error('Error loading feedback data:', e);
            mockData.feedback = [];
        }
    }

    // Show/hide nav items based on role
    if (userRole === 'admin') {
        document.querySelectorAll('.admin-only').forEach(item => item.style.display = '');
        document.querySelectorAll('.instructor-only').forEach(item => item.style.display = 'none');
    } else if (userRole === 'instructor') {
        document.querySelectorAll('.instructor-only').forEach(item => item.style.display = '');
        document.querySelectorAll('.admin-only').forEach(item => item.style.display = 'none');
    } else {
        document.querySelectorAll('.admin-only').forEach(item => item.style.display = 'none');
        document.querySelectorAll('.instructor-only').forEach(item => item.style.display = 'none');
    }
    
    navigateToPage('student-dashboard');
});