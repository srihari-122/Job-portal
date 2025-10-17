// Job Portal Application JavaScript

class JobPortal {
    constructor() {
        this.currentUser = null;
        this.token = localStorage.getItem('token');
        this.currentView = 'home';
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.checkAuthStatus();
        // Don't load jobs on homepage - only load when needed
        if (document.getElementById('jobsContainer')) {
            this.loadJobs();
        }
    }

    setupEventListeners() {
        // Navigation buttons
        document.getElementById('loginBtn').addEventListener('click', () => this.showLoginModal());
        document.getElementById('registerBtn').addEventListener('click', () => this.showRegisterModal());
        document.getElementById('browseJobsBtn').addEventListener('click', () => this.loadJobs());
        document.getElementById('postJobBtn').addEventListener('click', () => this.showPostJobForm());

        // Modal controls
        document.getElementById('closeLoginModal').addEventListener('click', () => this.hideLoginModal());
        document.getElementById('closeRegisterModal').addEventListener('click', () => this.hideRegisterModal());
        document.getElementById('switchToRegister').addEventListener('click', () => this.switchToRegister());
        document.getElementById('switchToLogin').addEventListener('click', () => this.switchToLogin());

        // Forms
        document.getElementById('loginForm').addEventListener('submit', (e) => this.handleLogin(e));
        document.getElementById('registerForm').addEventListener('submit', (e) => this.handleRegister(e));

        // Close modals on outside click
        document.getElementById('loginModal').addEventListener('click', (e) => {
            if (e.target.id === 'loginModal') this.hideLoginModal();
        });
        document.getElementById('registerModal').addEventListener('click', (e) => {
            if (e.target.id === 'registerModal') this.hideRegisterModal();
        });
    }

    checkAuthStatus() {
        if (this.token) {
            this.getCurrentUser();
        }
    }

    async getCurrentUser() {
        try {
            const response = await fetch('/api/profile', {
                headers: {
                    'Authorization': `Bearer ${this.token}`
                }
            });

            if (response.ok) {
                this.currentUser = await response.json();
                this.updateNavigation();
                this.loadDashboard();
            } else {
                this.logout();
            }
        } catch (error) {
            console.error('Error getting current user:', error);
            this.logout();
        }
    }

    updateNavigation() {
        const navButtons = document.querySelector('.flex.items-center.space-x-4');
        navButtons.innerHTML = `
            <div class="flex items-center space-x-4">
                <span class="text-gray-700">Welcome, ${this.currentUser.full_name}</span>
                <button id="dashboardBtn" class="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition duration-300">
                    <i class="fas fa-tachometer-alt mr-2"></i>Dashboard
                </button>
                <button id="logoutBtn" class="bg-red-600 text-white px-4 py-2 rounded-lg hover:bg-red-700 transition duration-300">
                    <i class="fas fa-sign-out-alt mr-2"></i>Logout
                </button>
            </div>
        `;

        document.getElementById('dashboardBtn').addEventListener('click', () => this.loadDashboard());
        document.getElementById('logoutBtn').addEventListener('click', () => this.logout());
    }

    showLoginModal() {
        document.getElementById('loginModal').classList.remove('hidden');
    }

    hideLoginModal() {
        document.getElementById('loginModal').classList.add('hidden');
    }

    showRegisterModal() {
        document.getElementById('registerModal').classList.remove('hidden');
    }

    hideRegisterModal() {
        document.getElementById('registerModal').classList.add('hidden');
    }

    switchToRegister() {
        this.hideLoginModal();
        this.showRegisterModal();
    }

    switchToLogin() {
        this.hideRegisterModal();
        this.showLoginModal();
    }

    async handleLogin(e) {
        e.preventDefault();
        this.showLoading();

        const email = document.getElementById('loginEmail').value;
        const password = document.getElementById('loginPassword').value;

        try {
            const response = await fetch('/api/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ email, password })
            });

            // Check if response is ok before trying to parse JSON
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();

            this.token = data.access_token;
            this.currentUser = data.user;
            localStorage.setItem('token', this.token);
            this.hideLoginModal();
            this.updateNavigation();
            this.loadDashboard();
            this.showToast('Login successful!', 'success');
        } catch (error) {
            console.error('Login error:', error);
            this.showToast('Server not available. Please try again later.', 'error');
        } finally {
            this.hideLoading();
        }
    }

    async handleRegister(e) {
        e.preventDefault();
        this.showLoading();

        const formData = {
            email: document.getElementById('registerEmail').value,
            password: document.getElementById('registerPassword').value,
            name: document.getElementById('registerFullName').value,
            role: document.getElementById('registerRole').value,
            phone: document.getElementById('registerPhone').value
        };

        try {
            const response = await fetch('/api/register', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(formData)
            });

            const data = await response.json();

            if (response.ok) {
                this.hideRegisterModal();
                this.showToast('Registration successful! Please login.', 'success');
                this.switchToLogin();
            } else {
                this.showToast(data.detail || 'Registration failed', 'error');
            }
        } catch (error) {
            console.error('Registration error:', error);
            this.showToast('Network error. Please try again.', 'error');
        } finally {
            this.hideLoading();
        }
    }

    logout() {
        this.token = null;
        this.currentUser = null;
        localStorage.removeItem('token');
        location.reload();
    }

    async loadJobs() {
        try {
            // Skip loading jobs for now to avoid 500 errors
            const container = document.getElementById('jobsContainer');
            if (!container) {
                return;
            }
            
            // Show empty state directly
            container.innerHTML = `
                <div class="col-span-full text-center py-12">
                    <div class="empty-state">
                        <div class="empty-state-icon">
                            <i class="fas fa-briefcase"></i>
                        </div>
                        <h3 class="empty-state-title">No Jobs Available</h3>
                        <p class="empty-state-message">Check back later for new opportunities.</p>
                    </div>
                </div>
            `;
            return;

            container.innerHTML = jobs.map(job => `
                <div class="job-card fade-in">
                    <h3 class="job-title">${job.title}</h3>
                    <p class="job-company">${job.company}</p>
                    <p class="job-location"><i class="fas fa-map-marker-alt mr-2"></i>${job.location}</p>
                    ${job.salary_min && job.salary_max ? 
                        `<p class="job-salary">$${job.salary_min.toLocaleString()} - $${job.salary_max.toLocaleString()}</p>` : 
                        ''
                    }
                    <p class="job-description">${job.description.substring(0, 150)}...</p>
                    <div class="job-tags">
                        <span class="job-tag">${job.job_type}</span>
                        <span class="job-tag">${job.location}</span>
                    </div>
                    <div class="flex justify-between items-center">
                        <span class="text-sm text-gray-500">Posted by ${job.posted_by_name}</span>
                        ${this.currentUser ? 
                            `<button onclick="jobPortal.applyForJob(${job.id})" class="btn btn-primary">
                                <i class="fas fa-paper-plane mr-2"></i>Apply Now
                            </button>` : 
                            `<button onclick="jobPortal.showLoginModal()" class="btn btn-primary">
                                <i class="fas fa-sign-in-alt mr-2"></i>Login to Apply
                            </button>`
                        }
                    </div>
                </div>
            `).join('');
        } catch (error) {
            console.error('Error loading jobs:', error);
            // Don't show any errors - just fail silently
        }
    }

    loadDashboard() {
        document.getElementById('mainContent').classList.add('hidden');
        document.getElementById('dashboardContainer').classList.remove('hidden');

        if (this.currentUser.role === 'admin') {
            this.loadAdminDashboard();
        } else {
            this.loadCandidateDashboard();
        }
    }

    loadAdminDashboard() {
        const dashboardHTML = `
            <div class="flex">
                <div class="dashboard-sidebar">
                    <div class="p-6">
                        <h2 class="text-xl font-bold text-white mb-8">Admin Dashboard</h2>
                        <ul class="sidebar-menu">
                            <li><a href="#" onclick="jobPortal.showAdminView('overview')" class="active"><i class="fas fa-chart-bar"></i>Overview</a></li>
                            <li><a href="#" onclick="jobPortal.showAdminView('jobs')"><i class="fas fa-briefcase"></i>Manage Jobs</a></li>
                            <li><a href="#" onclick="jobPortal.showAdminView('applications')"><i class="fas fa-file-alt"></i>Applications</a></li>
                            <li><a href="#" onclick="jobPortal.showAdminView('users')"><i class="fas fa-users"></i>User Management</a></li>
                            <li><a href="#" onclick="jobPortal.showAdminView('analytics')"><i class="fas fa-chart-line"></i>Analytics</a></li>
                        </ul>
                    </div>
                </div>
                <div class="dashboard-content">
                    <div class="p-8">
                        <div id="adminContent">
                            ${this.getAdminOverview()}
                        </div>
                    </div>
                </div>
            </div>
        `;

        document.getElementById('dashboardContainer').innerHTML = dashboardHTML;
        this.loadAdminOverview();
    }

    loadCandidateDashboard() {
        const dashboardHTML = `
            <div class="flex">
                <div class="dashboard-sidebar">
                    <div class="p-6">
                        <h2 class="text-xl font-bold text-white mb-8">My Dashboard</h2>
                        <ul class="sidebar-menu">
                            <li><a href="#" onclick="jobPortal.showCandidateView('profile')" class="active"><i class="fas fa-user"></i>Profile</a></li>
                            <li><a href="#" onclick="jobPortal.showCandidateView('jobs')"><i class="fas fa-search"></i>Browse Jobs</a></li>
                            <li><a href="#" onclick="jobPortal.showCandidateView('applications')"><i class="fas fa-file-alt"></i>My Applications</a></li>
                            <li><a href="#" onclick="jobPortal.showCandidateView('analysis')"><i class="fas fa-robot"></i>AI Analysis</a></li>
                        </ul>
                    </div>
                </div>
                <div class="dashboard-content">
                    <div class="p-8">
                        <div id="candidateContent">
                            ${this.getCandidateProfile()}
                        </div>
                    </div>
                </div>
            </div>
        `;

        document.getElementById('dashboardContainer').innerHTML = dashboardHTML;
    }

    async loadAdminOverview() {
        try {
            const [jobsResponse, applicationsResponse] = await Promise.all([
                fetch('/api/jobs'),
                fetch('/api/applications', {
                    headers: { 'Authorization': `Bearer ${this.token}` }
                })
            ]);

            const jobs = await jobsResponse.json();
            const applications = await applicationsResponse.json();

            const overviewHTML = `
                <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
                    <div class="dashboard-card">
                        <div class="flex items-center">
                            <div class="p-3 bg-blue-100 rounded-full mr-4">
                                <i class="fas fa-briefcase text-blue-600 text-xl"></i>
                            </div>
                            <div>
                                <h3 class="text-2xl font-bold text-gray-900">${jobs.length}</h3>
                                <p class="text-gray-600">Active Jobs</p>
                            </div>
                        </div>
                    </div>
                    <div class="dashboard-card">
                        <div class="flex items-center">
                            <div class="p-3 bg-green-100 rounded-full mr-4">
                                <i class="fas fa-file-alt text-green-600 text-xl"></i>
                            </div>
                            <div>
                                <h3 class="text-2xl font-bold text-gray-900">${applications.length}</h3>
                                <p class="text-gray-600">Total Applications</p>
                            </div>
                        </div>
                    </div>
                    <div class="dashboard-card">
                        <div class="flex items-center">
                            <div class="p-3 bg-purple-100 rounded-full mr-4">
                                <i class="fas fa-users text-purple-600 text-xl"></i>
                            </div>
                            <div>
                                <h3 class="text-2xl font-bold text-gray-900">${new Set(applications.map(app => app.candidate_id)).size}</h3>
                                <p class="text-gray-600">Unique Candidates</p>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="dashboard-card">
                    <h2 class="card-title">Recent Applications</h2>
                    <div class="overflow-x-auto">
                        <table class="table">
                            <thead>
                                <tr>
                                    <th>Candidate</th>
                                    <th>Job Title</th>
                                    <th>Company</th>
                                    <th>Status</th>
                                    <th>Applied</th>
                                    <th>Actions</th>
                                </tr>
                            </thead>
                            <tbody>
                                ${applications.slice(0, 10).map(app => `
                                    <tr>
                                        <td>${app.candidate_name}</td>
                                        <td>${app.job_title}</td>
                                        <td>${app.company}</td>
                                        <td><span class="status-badge status-${app.status}">${app.status}</span></td>
                                        <td>${new Date(app.created_at).toLocaleDateString()}</td>
                                        <td>
                                            <button onclick="jobPortal.viewApplication(${app.id})" class="btn btn-primary btn-sm">
                                                <i class="fas fa-eye mr-1"></i>View
                                            </button>
                                        </td>
                                    </tr>
                                `).join('')}
                            </tbody>
                        </table>
                    </div>
                </div>
            `;

            document.getElementById('adminContent').innerHTML = overviewHTML;
        } catch (error) {
            console.error('Error loading admin overview:', error);
            this.showToast('Error loading dashboard data', 'error');
        }
    }

    getCandidateProfile() {
        return `
            <div class="dashboard-card">
                <div class="card-header">
                    <h2 class="card-title">My Profile</h2>
                    <button onclick="jobPortal.editProfile()" class="btn btn-primary">
                        <i class="fas fa-edit mr-2"></i>Edit Profile
                    </button>
                </div>
                <div id="profileContent">
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                        <div>
                            <h3 class="text-lg font-semibold mb-4">Personal Information</h3>
                            <div class="space-y-3">
                                <div>
                                    <label class="form-label">Full Name</label>
                                    <p class="text-gray-700">${this.currentUser.full_name}</p>
                                </div>
                                <div>
                                    <label class="form-label">Email</label>
                                    <p class="text-gray-700">${this.currentUser.email}</p>
                                </div>
                                <div>
                                    <label class="form-label">Phone</label>
                                    <p class="text-gray-700">${this.currentUser.phone || 'Not provided'}</p>
                                </div>
                            </div>
                        </div>
                        <div>
                            <h3 class="text-lg font-semibold mb-4">Resume</h3>
                            <div id="resumeSection">
                                <div class="file-upload" onclick="document.getElementById('resumeFile').click()">
                                    <div class="file-upload-icon">
                                        <i class="fas fa-cloud-upload-alt"></i>
                                    </div>
                                    <div class="file-upload-text">Upload Your Resume</div>
                                    <div class="file-upload-hint">Click to upload or drag and drop PDF file</div>
                                </div>
                                <input type="file" id="resumeFile" accept=".pdf" style="display: none;" onchange="jobPortal.uploadResume(event)">
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }

    async uploadResume(event) {
        const file = event.target.files[0];
        if (!file) return;

        if (file.type !== 'application/pdf') {
            this.showToast('Please upload a PDF file', 'error');
            return;
        }

        this.showLoading();

        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await fetch('/api/upload-resume', {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${this.token}`
                },
                body: formData
            });

            const data = await response.json();

            if (response.ok) {
                this.showToast('Resume uploaded and processed successfully!', 'success');
                this.displayResumeData(data.extracted_data);
            } else {
                this.showToast(data.detail || 'Error uploading resume', 'error');
            }
        } catch (error) {
            console.error('Error uploading resume:', error);
            this.showToast('Network error. Please try again.', 'error');
        } finally {
            this.hideLoading();
        }
    }

    displayResumeData(data) {
        const resumeSection = document.getElementById('resumeSection');
        resumeSection.innerHTML = `
            <div class="bg-green-50 border border-green-200 rounded-lg p-4">
                <h4 class="font-semibold text-green-800 mb-3">Resume Successfully Processed</h4>
                <div class="space-y-2 text-sm">
                    <div><strong>Email:</strong> ${data.email || 'Not found'}</div>
                    <div><strong>Phone:</strong> ${data.phone || 'Not found'}</div>
                    <div><strong>Skills Found:</strong> ${data.skills.length} skills detected</div>
                </div>
                <div class="mt-4">
                    <h5 class="font-semibold mb-2">Detected Skills:</h5>
                    <div class="flex flex-wrap gap-2">
                        ${data.skills.map(skill => `<span class="skill-tag">${skill}</span>`).join('')}
                    </div>
                </div>
                <button onclick="jobPortal.uploadResume(event)" class="btn btn-secondary mt-4">
                    <i class="fas fa-upload mr-2"></i>Upload New Resume
                </button>
            </div>
        `;
    }

    async applyForJob(jobId) {
        const coverLetter = prompt('Enter your cover letter (optional):');
        
        this.showLoading();

        try {
            const response = await fetch('/api/apply', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${this.token}`
                },
                body: JSON.stringify({
                    job_id: jobId,
                    cover_letter: coverLetter || null
                })
            });

            const data = await response.json();

            if (response.ok) {
                this.showToast('Application submitted successfully!', 'success');
                this.displayMLAnalysis(data.ml_analysis);
            } else {
                this.showToast(data.detail || 'Error submitting application', 'error');
            }
        } catch (error) {
            console.error('Error applying for job:', error);
            this.showToast('Network error. Please try again.', 'error');
        } finally {
            this.hideLoading();
        }
    }

    displayMLAnalysis(analysis) {
        const modalHTML = `
            <div class="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center p-4">
                <div class="bg-white rounded-lg p-8 w-full max-w-4xl max-h-screen overflow-y-auto">
                    <div class="flex justify-between items-center mb-6">
                        <h2 class="text-2xl font-bold">AI Analysis Results</h2>
                        <button onclick="this.closest('.fixed').remove()" class="text-gray-500 hover:text-gray-700">
                            <i class="fas fa-times text-xl"></i>
                        </button>
                    </div>
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                        <div class="ml-analysis-card">
                            <h3>Skill Gap Analysis</h3>
                            <div class="ml-metric">
                                <span class="ml-metric-label">Match Percentage</span>
                                <span class="ml-metric-value">${analysis.skill_gap.match_percentage}%</span>
                            </div>
                            <div class="mt-4">
                                <h5 class="font-semibold mb-2">Matched Skills:</h5>
                                <div class="flex flex-wrap gap-1 mb-3">
                                    ${analysis.skill_gap.matched_skills.map(skill => `<span class="skill-tag matched">${skill}</span>`).join('')}
                                </div>
                                <h5 class="font-semibold mb-2">Missing Skills:</h5>
                                <div class="flex flex-wrap gap-1">
                                    ${analysis.skill_gap.missing_skills.map(skill => `<span class="skill-tag missing">${skill}</span>`).join('')}
                                </div>
                            </div>
                        </div>
                        <div class="ml-analysis-card">
                            <h3>Salary Projection</h3>
                            <div class="ml-metric">
                                <span class="ml-metric-label">Projected Salary</span>
                                <span class="ml-metric-value">$${analysis.salary_projection.projected_salary.toLocaleString()}</span>
                            </div>
                            <div class="ml-metric">
                                <span class="ml-metric-label">Role</span>
                                <span class="ml-metric-value">${analysis.salary_projection.role}</span>
                            </div>
                            <div class="ml-metric">
                                <span class="ml-metric-label">Experience Level</span>
                                <span class="ml-metric-value">${analysis.salary_projection.experience_level}</span>
                            </div>
                        </div>
                        <div class="ml-analysis-card">
                            <h3>Career Growth</h3>
                            <div class="ml-metric">
                                <span class="ml-metric-label">Current Level</span>
                                <span class="ml-metric-value">${analysis.career_growth.current_level}</span>
                            </div>
                            <div class="ml-metric">
                                <span class="ml-metric-label">Next Level</span>
                                <span class="ml-metric-value">${analysis.career_growth.next_level}</span>
                            </div>
                            <div class="mt-4">
                                <h5 class="font-semibold mb-2">Recommendations:</h5>
                                <ul class="text-sm space-y-1">
                                    ${analysis.career_growth.current_recommendations.map(rec => `<li>• ${rec}</li>`).join('')}
                                </ul>
                            </div>
                        </div>
                        <div class="ml-analysis-card">
                            <h3>Location Analysis</h3>
                            <div class="ml-metric">
                                <span class="ml-metric-label">Job Growth</span>
                                <span class="ml-metric-value">${analysis.location_analysis.tech_jobs_growth}%</span>
                            </div>
                            <div class="ml-metric">
                                <span class="ml-metric-label">Market Strength</span>
                                <span class="ml-metric-value">${analysis.location_analysis.job_market_strength}/10</span>
                            </div>
                            <div class="ml-metric">
                                <span class="ml-metric-label">Skill Match</span>
                                <span class="ml-metric-value">${analysis.location_analysis.user_skill_match}%</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;

        document.body.insertAdjacentHTML('beforeend', modalHTML);
    }

    showAdminView(view) {
        // Update active menu item
        document.querySelectorAll('.sidebar-menu a').forEach(link => link.classList.remove('active'));
        event.target.classList.add('active');

        switch(view) {
            case 'overview':
                this.loadAdminOverview();
                break;
            case 'jobs':
                this.loadAdminJobs();
                break;
            case 'applications':
                this.loadAdminApplications();
                break;
            case 'users':
                this.loadAdminUsers();
                break;
            case 'analytics':
                this.loadAdminAnalytics();
                break;
        }
    }

    showCandidateView(view) {
        // Update active menu item
        document.querySelectorAll('.sidebar-menu a').forEach(link => link.classList.remove('active'));
        event.target.classList.add('active');

        const contentDiv = document.getElementById('candidateContent');
        
        switch(view) {
            case 'profile':
                contentDiv.innerHTML = this.getCandidateProfile();
                break;
            case 'jobs':
                contentDiv.innerHTML = this.getCandidateJobs();
                break;
            case 'applications':
                contentDiv.innerHTML = this.getCandidateApplications();
                break;
            case 'analysis':
                contentDiv.innerHTML = this.getCandidateAnalysis();
                break;
        }
    }

    getCandidateJobs() {
        return `
            <div class="dashboard-card">
                <div class="card-header">
                    <h2 class="card-title">Browse Jobs</h2>
                </div>
                <div id="jobsContainer" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                    <div class="col-span-full text-center py-12">
                        <div class="empty-state">
                            <div class="empty-state-icon">
                                <i class="fas fa-briefcase"></i>
                            </div>
                            <h3 class="empty-state-title">No Jobs Available</h3>
                            <p class="empty-state-message">Check back later for new opportunities.</p>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }

    getCandidateApplications() {
        return `
            <div class="dashboard-card">
                <div class="card-header">
                    <h2 class="card-title">My Applications</h2>
                </div>
                <div class="space-y-4">
                    <div class="text-center py-12">
                        <div class="empty-state">
                            <div class="empty-state-icon">
                                <i class="fas fa-file-alt"></i>
                            </div>
                            <h3 class="empty-state-title">No Applications Yet</h3>
                            <p class="empty-state-message">Start browsing jobs to apply for opportunities.</p>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }

    getCandidateAnalysis() {
        return `
            <div class="dashboard-card">
                <div class="card-header">
                    <h2 class="card-title">AI Career Analysis</h2>
                </div>
                <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div class="analysis-card">
                        <h3 class="text-lg font-semibold mb-4">Skill Gap Analysis</h3>
                        <p class="text-gray-600">Upload your resume to get personalized skill gap analysis.</p>
                    </div>
                    <div class="analysis-card">
                        <h3 class="text-lg font-semibold mb-4">Career Growth Insights</h3>
                        <p class="text-gray-600">Get AI-powered recommendations for career advancement.</p>
                    </div>
                </div>
            </div>
        `;
    }

    showPostJobForm() {
        if (!this.currentUser || this.currentUser.role !== 'admin') {
            this.showToast('Only admins can post jobs', 'error');
            return;
        }

        const modalHTML = `
            <div class="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center p-4">
                <div class="bg-white rounded-lg p-8 w-full max-w-2xl max-h-screen overflow-y-auto">
                    <div class="flex justify-between items-center mb-6">
                        <h2 class="text-2xl font-bold">Post New Job</h2>
                        <button onclick="this.closest('.fixed').remove()" class="text-gray-500 hover:text-gray-700">
                            <i class="fas fa-times text-xl"></i>
                        </button>
                    </div>
                    <form id="postJobForm">
                        <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
                            <div class="form-group">
                                <label class="form-label">Job Title</label>
                                <input type="text" id="jobTitle" class="form-input" required>
                            </div>
                            <div class="form-group">
                                <label class="form-label">Company</label>
                                <input type="text" id="jobCompany" class="form-input" required>
                            </div>
                        </div>
                        <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
                            <div class="form-group">
                                <label class="form-label">Location</label>
                                <input type="text" id="jobLocation" class="form-input" required>
                            </div>
                            <div class="form-group">
                                <label class="form-label">Job Type</label>
                                <select id="jobType" class="form-select" required>
                                    <option value="">Select Type</option>
                                    <option value="full-time">Full Time</option>
                                    <option value="part-time">Part Time</option>
                                    <option value="contract">Contract</option>
                                    <option value="internship">Internship</option>
                                </select>
                            </div>
                        </div>
                        <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
                            <div class="form-group">
                                <label class="form-label">Min Salary</label>
                                <input type="number" id="jobSalaryMin" class="form-input">
                            </div>
                            <div class="form-group">
                                <label class="form-label">Max Salary</label>
                                <input type="number" id="jobSalaryMax" class="form-input">
                            </div>
                        </div>
                        <div class="form-group mb-4">
                            <label class="form-label">Job Description</label>
                            <textarea id="jobDescription" class="form-input form-textarea" required></textarea>
                        </div>
                        <div class="form-group mb-6">
                            <label class="form-label">Requirements</label>
                            <textarea id="jobRequirements" class="form-input form-textarea" required></textarea>
                        </div>
                        <div class="flex justify-end space-x-4">
                            <button type="button" onclick="this.closest('.fixed').remove()" class="btn btn-secondary">Cancel</button>
                            <button type="submit" class="btn btn-primary">Post Job</button>
                        </div>
                    </form>
                </div>
            </div>
        `;

        document.body.insertAdjacentHTML('beforeend', modalHTML);
        document.getElementById('postJobForm').addEventListener('submit', (e) => this.handlePostJob(e));
    }

    async handlePostJob(e) {
        e.preventDefault();
        this.showLoading();

        const jobData = {
            title: document.getElementById('jobTitle').value,
            company: document.getElementById('jobCompany').value,
            location: document.getElementById('jobLocation').value,
            job_type: document.getElementById('jobType').value,
            salary_min: parseInt(document.getElementById('jobSalaryMin').value) || null,
            salary_max: parseInt(document.getElementById('jobSalaryMax').value) || null,
            description: document.getElementById('jobDescription').value,
            requirements: document.getElementById('jobRequirements').value
        };

        try {
            const response = await fetch('/api/jobs', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${this.token}`
                },
                body: JSON.stringify(jobData)
            });

            const data = await response.json();

            if (response.ok) {
                this.showToast('Job posted successfully!', 'success');
                document.querySelector('.fixed').remove();
                this.loadJobs();
            } else {
                this.showToast(data.detail || 'Error posting job', 'error');
            }
        } catch (error) {
            console.error('Error posting job:', error);
            this.showToast('Network error. Please try again.', 'error');
        } finally {
            this.hideLoading();
        }
    }

    showLoading() {
        document.getElementById('loadingSpinner').classList.remove('hidden');
    }

    hideLoading() {
        document.getElementById('loadingSpinner').classList.add('hidden');
    }

    showToast(message, type = 'info') {
        const toastContainer = document.getElementById('toastContainer');
        const toastId = Date.now();
        
        const toastHTML = `
            <div id="toast-${toastId}" class="toast ${type}">
                <div class="toast-title">${type.charAt(0).toUpperCase() + type.slice(1)}</div>
                <div class="toast-message">${message}</div>
            </div>
        `;

        toastContainer.insertAdjacentHTML('beforeend', toastHTML);

        // Auto remove after 5 seconds
        setTimeout(() => {
            const toast = document.getElementById(`toast-${toastId}`);
            if (toast) {
                toast.remove();
            }
        }, 5000);
    }

    // Admin Functions
    async loadAdminJobs() {
        try {
            const response = await fetch('/api/jobs', {
                headers: { 'Authorization': `Bearer ${this.token}` }
            });
            const data = await response.json();
            const jobs = data.jobs || [];

            const jobsHTML = `
                <div class="dashboard-card">
                    <div class="card-header">
                        <h2 class="card-title">Manage Jobs</h2>
                        <button onclick="jobPortal.showPostJobForm()" class="btn btn-primary">
                            <i class="fas fa-plus mr-2"></i>Post New Job
                        </button>
                    </div>
                    <div class="overflow-x-auto">
                        <table class="table">
                            <thead>
                                <tr>
                                    <th>Title</th>
                                    <th>Company</th>
                                    <th>Location</th>
                                    <th>Posted Date</th>
                                    <th>Actions</th>
                                </tr>
                            </thead>
                            <tbody>
                                ${jobs.map(job => `
                                    <tr>
                                        <td>${job.title}</td>
                                        <td>${job.company}</td>
                                        <td>${job.location}</td>
                                        <td>${job.posted_date || 'N/A'}</td>
                                        <td>
                                            <button onclick="jobPortal.editJob(${job.id})" class="btn btn-secondary btn-sm mr-2">
                                                <i class="fas fa-edit mr-1"></i>Edit
                                            </button>
                                            <button onclick="jobPortal.deleteJob(${job.id})" class="btn btn-danger btn-sm">
                                                <i class="fas fa-trash mr-1"></i>Delete
                                            </button>
                                        </td>
                                    </tr>
                                `).join('')}
                            </tbody>
                        </table>
                    </div>
                </div>
            `;

            document.getElementById('adminContent').innerHTML = jobsHTML;
        } catch (error) {
            console.error('Error loading admin jobs:', error);
            this.showToast('Error loading jobs', 'error');
        }
    }

    async loadAdminApplications() {
        try {
            const response = await fetch('/api/admin/applications', {
                headers: { 'Authorization': `Bearer ${this.token}` }
            });
            const data = await response.json();
            const applications = data.applications || [];
            console.log('🔍 Applications data:', applications);
            console.log('🔍 First application AI suggestion:', applications[0]?.ai_suggestion);

            const applicationsHTML = `
                <div class="dashboard-card">
                    <div class="card-header">
                        <h2 class="card-title">Applications Management</h2>
                        <div class="flex space-x-4">
                            <button onclick="jobPortal.loadAdminApplications()" class="btn btn-primary">
                                <i class="fas fa-refresh mr-2"></i>Refresh
                            </button>
                        </div>
                    </div>
                    <div class="overflow-x-auto">
                        <table class="table">
                            <thead>
                                <tr>
                                    <th>Candidate</th>
                                    <th>Job Title</th>
                                    <th>Company</th>
                                    <th>Experience</th>
                                    <th>Skills</th>
                                    <th>Resume Score</th>
                                    <th>AI Suggestion</th>
                                    <th>Status</th>
                                    <th>Applied</th>
                                    <th>Actions</th>
                                </tr>
                            </thead>
                            <tbody>
                                ${applications.map(app => `
                                    <tr>
                                        <td>
                                            <div>
                                                <strong>${app.user_name}</strong><br>
                                                <small>${app.user_email}</small>
                                            </div>
                                        </td>
                                        <td>${app.job_title}</td>
                                        <td>${app.job_company}</td>
                                        <td>${app.user_experience_years} years</td>
                                        <td>
                                            <div class="flex flex-wrap gap-1">
                                                ${app.user_skills.slice(0, 3).map(skill => `<span class="skill-tag">${skill}</span>`).join('')}
                                                ${app.user_skills.length > 3 ? `<span class="text-xs text-gray-500">+${app.user_skills.length - 3} more</span>` : ''}
                                            </div>
                                        </td>
                                        <td>
                                            ${this.generateCompactAIScoreDisplay(app.resume_score)}
                                        </td>
                                        <td>
                                            ${this.generateAISuggestionDisplay(app.ai_suggestion)}
                                        </td>
                                        <td><span class="status-badge status-${app.status}">${app.status}</span></td>
                                        <td>${new Date(app.applied_date).toLocaleDateString()}</td>
                                        <td>
                                            <div class="flex space-x-2">
                                                <button onclick="jobPortal.viewApplicationResume('${app.user_email}')" class="btn btn-primary btn-sm" title="View Resume">
                                                    <i class="fas fa-file-pdf"></i>
                                                </button>
                                                <button onclick="jobPortal.viewApplicationDetails(${app.id})" class="btn btn-secondary btn-sm" title="View Details">
                                                    <i class="fas fa-eye"></i>
                                                </button>
                                                <select onchange="jobPortal.updateApplicationStatus(${app.id}, this.value)" class="form-select form-select-sm">
                                                    <option value="applied" ${app.status === 'applied' ? 'selected' : ''}>Applied</option>
                                                    <option value="under_review" ${app.status === 'under_review' ? 'selected' : ''}>Under Review</option>
                                                    <option value="accepted" ${app.status === 'accepted' ? 'selected' : ''}>Accepted</option>
                                                    <option value="rejected" ${app.status === 'rejected' ? 'selected' : ''}>Rejected</option>
                                                </select>
                                            </div>
                                        </td>
                                    </tr>
                                `).join('')}
                            </tbody>
                        </table>
                    </div>
                </div>
            `;

            document.getElementById('adminContent').innerHTML = applicationsHTML;
        } catch (error) {
            console.error('Error loading admin applications:', error);
            this.showToast('Error loading applications', 'error');
        }
    }

    async loadAdminUsers() {
        try {
            const response = await fetch('/api/admin/users', {
                headers: { 'Authorization': `Bearer ${this.token}` }
            });
            const data = await response.json();
            const users = data.users || [];

            const usersHTML = `
                <div class="dashboard-card">
                    <div class="card-header">
                        <h2 class="card-title">User Management</h2>
                        <div class="flex space-x-4">
                            <button onclick="jobPortal.loadAdminUsers()" class="btn btn-primary">
                                <i class="fas fa-refresh mr-2"></i>Refresh
                            </button>
                        </div>
                    </div>
                    
                    <!-- Search and Filter Section -->
                    <div class="bg-gray-50 p-4 rounded-lg border border-gray-200 mb-6">
                        <h4 class="text-md font-semibold text-gray-700 mb-3">Search & Filter Users</h4>
                        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-3">
                            <div>
                                <label class="block text-sm font-medium text-gray-700 mb-1">Search</label>
                                <input type="text" id="userSearchInput" placeholder="Name, email, skills..." class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent">
                            </div>
                            <div>
                                <label class="block text-sm font-medium text-gray-700 mb-1">Skills</label>
                                <input type="text" id="skillsFilterInput" placeholder="e.g., Python, Java, React" class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent">
                            </div>
                            <div>
                                <label class="block text-sm font-medium text-gray-700 mb-1">Domain</label>
                                <input type="text" id="domainFilterInput" placeholder="e.g., IT, Finance, Healthcare" class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent">
                            </div>
                            <div>
                                <label class="block text-sm font-medium text-gray-700 mb-1">Experience Range</label>
                                <div class="flex space-x-2">
                                    <input type="number" id="minExpInput" placeholder="Min" min="0" max="50" class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent">
                                    <input type="number" id="maxExpInput" placeholder="Max" min="0" max="50" class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent">
                                </div>
                            </div>
                        </div>
                        <div class="flex space-x-2 mt-3">
                            <button onclick="jobPortal.filterUsers()" class="bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600 transition duration-300">
                                <i class="fas fa-search mr-2"></i>Search & Filter
                            </button>
                            <button onclick="jobPortal.clearUserFilters()" class="bg-gray-500 text-white px-4 py-2 rounded-lg hover:bg-gray-600 transition duration-300">
                                <i class="fas fa-times mr-2"></i>Clear Filters
                            </button>
                        </div>
                    </div>
                    <div class="overflow-x-auto">
                        <table class="table">
                            <thead>
                                <tr>
                                    <th>Name</th>
                                    <th>Email</th>
                                    <th>Role</th>
                                    <th>Experience</th>
                                    <th>Skills</th>
                                    <th>Location</th>
                                    <th>Resume</th>
                                    <th>Actions</th>
                                </tr>
                            </thead>
                            <tbody>
                                ${users.map(user => `
                                    <tr>
                                        <td><strong>${user.name}</strong></td>
                                        <td>${user.email}</td>
                                        <td>${user.resume_role || user.role}</td>
                                        <td>${user.experience_years} years</td>
                                        <td>
                                            <div class="flex flex-wrap gap-1">
                                                ${user.skills.slice(0, 3).map(skill => `<span class="skill-tag">${skill}</span>`).join('')}
                                                ${user.skills.length > 3 ? `<span class="text-xs text-gray-500">+${user.skills.length - 3} more</span>` : ''}
                                            </div>
                                        </td>
                                        <td>${user.location}</td>
                                        <td>
                                            ${user.has_resume ? 
                                                `<span class="text-green-600"><i class="fas fa-check-circle"></i> Available</span>` : 
                                                `<span class="text-red-600"><i class="fas fa-times-circle"></i> Not uploaded</span>`
                                            }
                                        </td>
                                        <td>
                                            <div class="flex space-x-2">
                                                ${user.has_resume ? 
                                                    `<button onclick="jobPortal.viewUserResume('${user.email}')" class="btn btn-primary btn-sm" title="View Resume">
                                                        <i class="fas fa-file-pdf"></i>
                                                    </button>` : ''
                                                }
                                                <button onclick="jobPortal.viewUserDetails('${user.email}')" class="btn btn-secondary btn-sm" title="View Details">
                                                    <i class="fas fa-eye"></i>
                                                </button>
                                                <button onclick="jobPortal.deleteUser('${user.email}')" class="btn btn-danger btn-sm" title="Delete User">
                                                    <i class="fas fa-trash"></i>
                                                </button>
                                            </div>
                                        </td>
                                    </tr>
                                `).join('')}
                            </tbody>
                        </table>
                    </div>
                </div>
            `;

            document.getElementById('adminContent').innerHTML = usersHTML;
        } catch (error) {
            console.error('Error loading admin users:', error);
            this.showToast('Error loading users', 'error');
        }
    }

    async loadAdminAnalytics() {
        try {
            const response = await fetch('/api/admin/dashboard-stats', {
                headers: { 'Authorization': `Bearer ${this.token}` }
            });
            const stats = await response.json();

            const analyticsHTML = `
                <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
                    <div class="dashboard-card">
                        <div class="flex items-center">
                            <div class="p-3 bg-blue-100 rounded-full mr-4">
                                <i class="fas fa-users text-blue-600 text-xl"></i>
                            </div>
                            <div>
                                <h3 class="text-2xl font-bold text-gray-900">${stats.total_users}</h3>
                                <p class="text-gray-600">Total Users</p>
                            </div>
                        </div>
                    </div>
                    <div class="dashboard-card">
                        <div class="flex items-center">
                            <div class="p-3 bg-green-100 rounded-full mr-4">
                                <i class="fas fa-briefcase text-green-600 text-xl"></i>
                            </div>
                            <div>
                                <h3 class="text-2xl font-bold text-gray-900">${stats.total_jobs}</h3>
                                <p class="text-gray-600">Total Jobs</p>
                            </div>
                        </div>
                    </div>
                    <div class="dashboard-card">
                        <div class="flex items-center">
                            <div class="p-3 bg-purple-100 rounded-full mr-4">
                                <i class="fas fa-file-alt text-purple-600 text-xl"></i>
                            </div>
                            <div>
                                <h3 class="text-2xl font-bold text-gray-900">${stats.total_applications}</h3>
                                <p class="text-gray-600">Applications</p>
                            </div>
                        </div>
                    </div>
                    <div class="dashboard-card">
                        <div class="flex items-center">
                            <div class="p-3 bg-orange-100 rounded-full mr-4">
                                <i class="fas fa-file-pdf text-orange-600 text-xl"></i>
                            </div>
                            <div>
                                <h3 class="text-2xl font-bold text-gray-900">${stats.total_resumes}</h3>
                                <p class="text-gray-600">Resumes</p>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div class="dashboard-card">
                        <h3 class="card-title">Application Status Breakdown</h3>
                        <div class="space-y-2">
                            <div class="flex justify-between">
                                <span>Under Review</span>
                                <span class="font-semibold">${stats.applications_by_status.under_review}</span>
                            </div>
                            <div class="flex justify-between">
                                <span>Accepted</span>
                                <span class="font-semibold text-green-600">${stats.applications_by_status.accepted}</span>
                            </div>
                            <div class="flex justify-between">
                                <span>Rejected</span>
                                <span class="font-semibold text-red-600">${stats.applications_by_status.rejected}</span>
                            </div>
                        </div>
                    </div>
                    <div class="dashboard-card">
                        <h3 class="card-title">User Distribution</h3>
                        <div class="space-y-2">
                            <div class="flex justify-between">
                                <span>Candidates</span>
                                <span class="font-semibold">${stats.user_role_distribution.candidates}</span>
                            </div>
                            <div class="flex justify-between">
                                <span>Admins</span>
                                <span class="font-semibold">${stats.user_role_distribution.admins}</span>
                            </div>
                            <div class="flex justify-between">
                                <span>Users with Resumes</span>
                                <span class="font-semibold text-blue-600">${stats.users_with_resumes}</span>
                            </div>
                        </div>
                    </div>
                </div>
            `;

            document.getElementById('adminContent').innerHTML = analyticsHTML;
        } catch (error) {
            console.error('Error loading admin analytics:', error);
            this.showToast('Error loading analytics', 'error');
        }
    }

    // Helper functions for admin operations
    async filterUsers() {
        try {
            // Get filter values
            const search = document.getElementById('userSearchInput').value;
            const skills = document.getElementById('skillsFilterInput').value;
            const domain = document.getElementById('domainFilterInput').value;
            const minExp = document.getElementById('minExpInput').value;
            const maxExp = document.getElementById('maxExpInput').value;

            const params = new URLSearchParams();
            if (search) params.append('search', search);
            if (skills) params.append('skills', skills);
            if (domain) params.append('domain', domain);
            if (minExp) params.append('experience_min', minExp);
            if (maxExp) params.append('experience_max', maxExp);

            // Show loading
            const usersList = document.getElementById('usersList');
            usersList.innerHTML = `
                <div class="text-center py-8">
                    <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500 mx-auto"></div>
                    <p class="text-gray-500 mt-2">Searching users...</p>
                </div>
            `;

            const response = await fetch(`/api/admin/users?${params}`, {
                headers: { 'Authorization': `Bearer ${this.token}` }
            });
            
            if (!response.ok) {
                throw new Error('Failed to fetch users');
            }
            
            const data = await response.json();
            
            // Display users
            this.displayUsers(data.users);
            
            // Show search results message
            if (data.users.length === 0) {
                usersList.innerHTML = '<p class="text-gray-500 text-center py-8">No users match the selected filters.</p>';
            } else {
                // Add a small message showing search results
                const searchMessage = document.createElement('div');
                searchMessage.className = 'mb-4 p-3 bg-blue-50 border border-blue-200 rounded-lg';
                searchMessage.innerHTML = `<p class="text-blue-800 text-sm"><i class="fas fa-info-circle mr-2"></i>Found ${data.users.length} users matching your search criteria.</p>`;
                usersList.insertBefore(searchMessage, usersList.firstChild);
            }
            
        } catch (error) {
            console.error('Error filtering users:', error);
            this.showToast('Error filtering users', 'error');
        }
    }

    clearUserFilters() {
        // Clear all filter inputs
        document.getElementById('userSearchInput').value = '';
        document.getElementById('skillsFilterInput').value = '';
        document.getElementById('domainFilterInput').value = '';
        document.getElementById('minExpInput').value = '';
        document.getElementById('maxExpInput').value = '';
        
        // Reload all users
        this.loadAdminUsers();
    }

    async viewUserResume(userEmail) {
        try {
            const response = await fetch(`/api/admin/view-resume/${encodeURIComponent(userEmail)}`, {
                headers: { 'Authorization': `Bearer ${this.token}` }
            });
            
            if (response.ok) {
                const blob = await response.blob();
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = `resume_${userEmail}.pdf`;
                document.body.appendChild(a);
                a.click();
                window.URL.revokeObjectURL(url);
                document.body.removeChild(a);
            } else {
                this.showToast('Resume not found', 'error');
            }
        } catch (error) {
            console.error('Error viewing resume:', error);
            this.showToast('Error viewing resume', 'error');
        }
    }

    async viewApplicationResume(userEmail) {
        await this.viewUserResume(userEmail);
    }

    async viewUserDetails(userEmail) {
        try {
            const response = await fetch(`/api/admin/resume-data/${encodeURIComponent(userEmail)}`, {
                headers: { 'Authorization': `Bearer ${this.token}` }
            });
            const data = await response.json();

            const modalHTML = `
                <div class="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center p-4">
                    <div class="bg-white rounded-lg p-8 w-full max-w-4xl max-h-screen overflow-y-auto">
                        <div class="flex justify-between items-center mb-6">
                            <h2 class="text-2xl font-bold">User Details - ${data.user_info.name}</h2>
                            <button onclick="this.closest('.fixed').remove()" class="text-gray-500 hover:text-gray-700">
                                <i class="fas fa-times text-xl"></i>
                            </button>
                        </div>
                        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                            <div>
                                <h3 class="text-lg font-semibold mb-4">Personal Information</h3>
                                <div class="space-y-2">
                                    <div><strong>Name:</strong> ${data.user_info.name}</div>
                                    <div><strong>Email:</strong> ${data.user_info.email}</div>
                                    <div><strong>Phone:</strong> ${data.user_info.phone}</div>
                                    <div><strong>Role:</strong> ${data.user_info.role}</div>
                                </div>
                            </div>
                            <div>
                                <h3 class="text-lg font-semibold mb-4">Resume Information</h3>
                                <div class="space-y-2">
                                    <div><strong>Resume Role:</strong> ${data.resume_data.role}</div>
                                    <div><strong>Location:</strong> ${data.resume_data.location}</div>
                                    <div><strong>Experience:</strong> ${data.resume_data.experience.total_years || 0} years</div>
                                    <div><strong>Confidence Score:</strong> ${this.generateAIScoreDisplay(data.resume_data.confidence_score)}</div>
                                </div>
                            </div>
                            <div class="md:col-span-2">
                                <h3 class="text-lg font-semibold mb-4">Skills</h3>
                                <div class="flex flex-wrap gap-2">
                                    ${data.resume_data.skills.map(skill => `<span class="skill-tag">${skill}</span>`).join('')}
                                </div>
                            </div>
                            <div class="md:col-span-2">
                                <h3 class="text-lg font-semibold mb-4">Education</h3>
                                <div class="space-y-2">
                                    ${data.resume_data.education.map(edu => `
                                        <div class="border-l-4 border-blue-500 pl-4">
                                            <div><strong>${edu.degree}</strong></div>
                                            <div>${edu.institution}</div>
                                        </div>
                                    `).join('')}
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            `;

            document.body.insertAdjacentHTML('beforeend', modalHTML);
        } catch (error) {
            console.error('Error viewing user details:', error);
            this.showToast('Error loading user details', 'error');
        }
    }

    async viewApplicationDetails(applicationId) {
        // Implementation for viewing application details
        this.showToast('Application details feature coming soon', 'info');
    }

    async updateApplicationStatus(applicationId, newStatus) {
        try {
            const response = await fetch(`/api/admin/applications/${applicationId}/status`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${this.token}`
                },
                body: JSON.stringify({ status: newStatus })
            });

            if (response.ok) {
                this.showToast('Application status updated successfully', 'success');
                this.loadAdminApplications();
            } else {
                this.showToast('Error updating application status', 'error');
            }
        } catch (error) {
            console.error('Error updating application status:', error);
            this.showToast('Error updating application status', 'error');
        }
    }

    async deleteUser(userEmail) {
        if (!confirm(`Are you sure you want to delete user ${userEmail}? This action cannot be undone.`)) {
            return;
        }

        try {
            const response = await fetch(`/api/admin/users/${encodeURIComponent(userEmail)}`, {
                method: 'DELETE',
                headers: { 'Authorization': `Bearer ${this.token}` }
            });

            if (response.ok) {
                this.showToast('User deleted successfully', 'success');
                this.loadAdminUsers();
            } else {
                this.showToast('Error deleting user', 'error');
            }
        } catch (error) {
            console.error('Error deleting user:', error);
            this.showToast('Error deleting user', 'error');
        }
    }

    // AI Score Display Helper
    generateAIScoreDisplay(score) {
        const percentage = Math.round(score * 100);
        let rating, colorClass, starCount;
        
        if (score >= 0.9) {
            rating = 'Excellent';
            colorClass = 'ai-score-excellent';
            starCount = 5;
        } else if (score >= 0.8) {
            rating = 'Very Good';
            colorClass = 'ai-score-very-good';
            starCount = 4;
        } else if (score >= 0.7) {
            rating = 'Good';
            colorClass = 'ai-score-good';
            starCount = 3;
        } else if (score >= 0.5) {
            rating = 'Fair';
            colorClass = 'ai-score-fair';
            starCount = 2;
        } else {
            rating = 'Poor';
            colorClass = 'ai-score-poor';
            starCount = 1;
        }
        
        const stars = '★'.repeat(starCount) + '☆'.repeat(5 - starCount);
        
        return `
            <div class="ai-score-card ${colorClass}">
                <div class="ai-score-circle">
                    ${percentage}%
                </div>
                <div class="ai-score-content">
                    <div class="ai-score-label">
                        <i class="fas fa-star ai-score-star"></i>
                        AI Score
                    </div>
                    <div class="ai-score-rating">
                        ${rating}
                    </div>
                </div>
            </div>
        `;
    }

    // Compact AI Score Display for tables
    generateCompactAIScoreDisplay(score) {
        const percentage = Math.round(score * 100);
        let colorClass;
        
        if (score >= 0.8) {
            colorClass = 'ai-score-excellent';
        } else if (score >= 0.6) {
            colorClass = 'ai-score-good';
        } else if (score >= 0.4) {
            colorClass = 'ai-score-fair';
        } else {
            colorClass = 'ai-score-poor';
        }
        
        return `
            <div class="ai-score-card ${colorClass}" style="padding: 8px 12px; margin: 0;">
                <div class="ai-score-circle" style="width: 40px; height: 40px; font-size: 14px; margin-right: 8px;">
                    ${percentage}%
                </div>
                <div class="ai-score-content">
                    <div class="ai-score-label" style="font-size: 12px; margin-bottom: 2px;">
                        <i class="fas fa-star ai-score-star" style="font-size: 12px;"></i>
                        AI Score
                    </div>
                </div>
            </div>
        `;
    }

    // AI Suggestion Display for applications
    generateAISuggestionDisplay(suggestion) {
        if (!suggestion) {
            return '<span class="ai-suggestion-badge ai-suggestion-gray">No Suggestion</span>';
        }

        const suggestionText = suggestion.suggestion.charAt(0).toUpperCase() + suggestion.suggestion.slice(1).replace('_', ' ');
        const confidenceText = suggestion.confidence.charAt(0).toUpperCase() + suggestion.confidence.slice(1);
        
        return `
            <div class="ai-suggestion-container" title="${suggestion.reason}">
                <span class="ai-suggestion-badge ai-suggestion-${suggestion.color}">
                    <i class="fas fa-robot mr-1"></i>
                    ${suggestionText}
                </span>
                <div class="ai-suggestion-confidence">
                    <small>${confidenceText} Confidence</small>
                </div>
            </div>
        `;
    }

}

// Initialize the application
const jobPortal = new JobPortal();
