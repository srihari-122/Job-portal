"""
Job Portal Application - Clean Version Without Extraction
Simple job portal with basic functionality
"""

from fastapi import FastAPI, HTTPException, Depends, UploadFile, File, Form
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, EmailStr
import jwt
import hashlib
import os
import json
import re
import aiofiles
import logging
from contextlib import asynccontextmanager
import dateutil.parser
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List
import PyPDF2
import glob
import time

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Simple Career Analysis System
class SimpleCareerAnalyzer:
    """Simple career analyzer without AI/ML"""
    
    def __init__(self):
        self.skill_market_demand = self.load_skill_market_demand()
        self.salary_ranges = self.load_salary_ranges()
        self.career_paths = self.load_career_paths()
    
    def load_skill_market_demand(self):
        """Load skill market demand data"""
        return {
            'high_demand': ['Python', 'JavaScript', 'React', 'AWS', 'Docker', 'Kubernetes'],
            'medium_demand': ['Java', 'Angular', 'Node.js', 'MySQL', 'Git'],
            'emerging': ['Machine Learning', 'Data Science', 'AI', 'Cloud Computing', 'DevOps'],
            'trending': ['TypeScript', 'Vue.js', 'GraphQL', 'Microservices', 'Serverless']
        }
    
    def load_salary_ranges(self):
        """Load salary range data"""
        return {
            'entry_level': {'min': 300000, 'max': 500000},
            'mid_level': {'min': 500000, 'max': 1000000},
            'senior_level': {'min': 1000000, 'max': 2000000},
            'lead_level': {'min': 1500000, 'max': 3000000}
        }
    
    def load_career_paths(self):
        """Load career path data"""
        return {
            'software_developer': {
                'junior': 'Junior Developer → Mid Developer → Senior Developer → Lead Developer',
                'specialization': 'Frontend → Backend → Full Stack → Architecture',
                'management': 'Developer → Tech Lead → Engineering Manager → Director'
            },
            'data_scientist': {
                'junior': 'Data Analyst → Data Scientist → Senior Data Scientist → Principal Data Scientist',
                'specialization': 'Analytics → Machine Learning → AI Research → Product',
                'management': 'Data Scientist → Team Lead → Data Science Manager → VP Data'
            }
        }
    
    def analyze_skills(self, skills):
        """Analyze skills"""
        try:
            if not skills:
                return {'error': 'No skills provided'}
            
            skill_analysis = {
                'total_skills': len(skills),
                'high_demand_skills': [s for s in skills if s in self.skill_market_demand['high_demand']],
                'medium_demand_skills': [s for s in skills if s in self.skill_market_demand['medium_demand']],
                'emerging_skills': [s for s in skills if s in self.skill_market_demand['emerging']],
                'trending_skills': [s for s in skills if s in self.skill_market_demand['trending']],
                'missing_high_demand': [s for s in self.skill_market_demand['high_demand'] if s not in skills],
                'recommendations': []
            }
            
            # Generate recommendations
            if len(skill_analysis['high_demand_skills']) < 3:
                skill_analysis['recommendations'].append("Learn more high-demand skills")
            
            if len(skill_analysis['emerging_skills']) == 0:
                skill_analysis['recommendations'].append("Consider learning emerging technologies")
            
            return skill_analysis
            
        except Exception as e:
            return {'error': f'Skill analysis failed: {str(e)}'}
    
    def project_salary(self, experience_years, skills):
        """Project salary based on experience and skills"""
        try:
            base_salary = 300000
            
            # Adjust based on experience
            if experience_years >= 5:
                level = 'senior_level'
            elif experience_years >= 3:
                level = 'mid_level'
            else:
                level = 'entry_level'
            
            salary_range = self.salary_ranges[level]
            
            # Adjust based on skills
            skill_bonus = len(skills) * 10000
            high_demand_bonus = len([s for s in skills if s in self.skill_market_demand['high_demand']]) * 20000
            
            projected_salary = salary_range['min'] + skill_bonus + high_demand_bonus
            
            return {
                'projected_salary': min(projected_salary, salary_range['max']),
                'salary_range': salary_range,
                'level': level,
                'skill_bonus': skill_bonus,
                'high_demand_bonus': high_demand_bonus
            }
            
        except Exception as e:
            return {'error': f'Salary projection failed: {str(e)}'}
    
    def suggest_career_path(self, role, experience_years):
        """Suggest career path"""
        try:
            role_lower = role.lower()
            
            if 'developer' in role_lower or 'engineer' in role_lower:
                career_path = self.career_paths['software_developer']
            elif 'data' in role_lower or 'analyst' in role_lower:
                career_path = self.career_paths['data_scientist']
            else:
                career_path = self.career_paths['software_developer']  # Default
            
            # Determine current level
            if experience_years >= 5:
                current_level = 'senior'
            elif experience_years >= 2:
                current_level = 'mid'
            else:
                current_level = 'junior'
            
            return {
                'career_path': career_path,
                'current_level': current_level,
                'next_steps': self._get_next_steps(current_level, experience_years)
            }
            
        except Exception as e:
            return {'error': f'Career path suggestion failed: {str(e)}'}
    
    def _get_next_steps(self, current_level, experience_years):
        """Get next steps based on current level"""
        if current_level == 'junior':
            return [
                "Build 2-3 significant projects",
                "Learn version control (Git)",
                "Practice coding problems daily",
                "Get familiar with testing frameworks"
            ]
        elif current_level == 'mid':
            return [
                "Learn system design",
                "Take on leadership responsibilities",
                "Mentor junior developers",
                "Get certified in relevant technologies"
            ]
        else:
            return [
                "Lead technical initiatives",
                "Architect complex systems",
                "Mentor multiple team members",
                "Consider management track"
            ]

# Initialize career analyzer
career_analyzer = SimpleCareerAnalyzer()

# Add analyze_career_path method to SimpleCareerAnalyzer class
def analyze_career_path(self, resume_data):
    """Analyze career path based on resume data"""
    try:
        logger.info("🤖 Starting career path analysis...")
        
        # Extract key information
        name = resume_data.get('name', 'Unknown')
        role = resume_data.get('role', 'Unknown')
        skills = resume_data.get('skills', [])
        experience = resume_data.get('experience', {})
        location = resume_data.get('location', 'Unknown')
        
        # Get experience years
        experience_years = experience.get('total_years', 0) if isinstance(experience, dict) else 0
        
        # Perform analysis
        skill_analysis = self.analyze_skills(skills)
        career_path = self.suggest_career_path(role, experience_years)
        salary_projection = self.project_salary(role, experience_years, location)
        
        # Create comprehensive analysis result
        analysis_result = {
            'candidate_profile': {
                'name': name,
                'role': role,
                'experience_years': experience_years,
                'location': location,
                'skills_count': len(skills)
            },
            'skill_analysis': skill_analysis,
            'career_path': career_path,
            'salary_projection': salary_projection,
            'recommendations': {
                'immediate_actions': [
                    f"Focus on {role} skill development",
                    "Build portfolio projects",
                    "Network in your industry"
                ],
                'long_term_goals': [
                    f"Advance to {career_path.get('next_level', 'Senior Role')}",
                    "Develop leadership skills",
                    "Consider specialization areas"
                ]
            },
            'market_insights': {
                'demand_level': 'High' if any(skill in self.skill_market_demand['high_demand'] for skill in skills) else 'Medium',
                'growth_potential': 'Excellent' if experience_years < 5 else 'Good',
                'trending_skills': self.skill_market_demand['trending'][:3]
            }
        }
        
        logger.info("✅ Career path analysis completed successfully")
        return analysis_result
        
    except Exception as e:
        logger.error(f"❌ Career path analysis error: {e}")
        return {'error': f'Analysis error: {str(e)}'}

# Add the method to the class
SimpleCareerAnalyzer.analyze_career_path = analyze_career_path

# Dynamic resume extraction function
def extract_resume_content_from_text(text, filename=None):
    """Extract resume content using dynamic extraction"""
    try:
        logger.info("📄 Starting dynamic resume extraction...")
        
        # Import and use the dynamic extractor
        from direct_extractor import direct_extractor
        extracted_data = direct_extractor.extract_resume_content(text, filename)
        
        logger.info("✅ Dynamic resume extraction completed successfully")
        return extracted_data
        
    except Exception as e:
        logger.error(f"❌ Error: {e}")
        return {
            'name': 'Error',
            'role': 'Error',
            'email': 'Error',
            'phone': 'Error',
            'skills': [],
            'experience': {'total_years': 0, 'total_months': 0, 'display': 'Error'},
            'raw_text': text[:500] if text else ''
        }

def analyze_career_based_on_resume(resume_data):
    """Simple career analysis without AI/ML"""
    try:
        name = resume_data.get('name', 'Unknown')
        role = resume_data.get('role', 'Unknown')
        skills = resume_data.get('skills', [])
        experience = resume_data.get('experience', {})
        
        experience_years = experience.get('total_years', 0)
        
        # Simple skill analysis
        skill_analysis = {
            "total_skills": len(skills),
            "technical_skills": [s for s in skills if any(tech in s.lower() for tech in ['java', 'python', 'javascript', 'html', 'css', 'sql', 'spring', 'react', 'angular', 'node'])],
            "soft_skills": [s for s in skills if any(soft in s.lower() for soft in ['communication', 'leadership', 'teamwork', 'problem solving', 'analytical'])],
            "skill_categories": {
                "Programming": [s for s in skills if any(prog in s.lower() for prog in ['java', 'python', 'javascript', 'c++', 'c#'])],
                "Web Development": [s for s in skills if any(web in s.lower() for web in ['html', 'css', 'react', 'angular', 'vue', 'bootstrap'])],
                "Database": [s for s in skills if any(db in s.lower() for db in ['sql', 'mysql', 'oracle', 'mongodb', 'postgresql'])],
                "Frameworks": [s for s in skills if any(fw in s.lower() for fw in ['spring', 'django', 'flask', 'express', 'laravel'])]
            }
        }
        
        # Simple salary projection
        base_salary = 300000
        if experience_years > 0:
            salary_projection = {
                "current_range": f"₹{base_salary + (experience_years * 50000):,} - ₹{base_salary + (experience_years * 100000):,}",
                "predicted_salary": f"₹{base_salary + (experience_years * 75000):,}",
                "growth_potential": "Good" if experience_years < 5 else "Excellent"
            }
        else:
            salary_projection = {
                "current_range": "₹300,000 - ₹500,000",
                "predicted_salary": "₹400,000",
                "growth_potential": "Excellent"
            }
        
        # Simple career paths
        career_paths = {
            "immediate": ["Junior Developer", "Associate Developer"],
            "next_2_years": ["Senior Developer", "Team Lead"],
            "long_term": ["Technical Lead", "Architect", "Manager"]
        }
        
        # Simple skill gaps
        skill_gaps = {
            "missing_technical": ["Git", "Docker", "AWS", "Testing"],
            "missing_soft": ["Project Management", "Mentoring"],
            "recommendations": ["Learn version control", "Practice system design", "Improve communication skills"]
        }
        
        # Simple market competitiveness
        market_competitiveness = {
            "score": min(85, 60 + (len(skills) * 2) + (experience_years * 5)),
            "strengths": ["Good technical foundation", "Relevant experience"],
            "improvements": ["Add more modern technologies", "Build portfolio projects"]
        }
        
        # Simple growth recommendations
        growth_recommendations = {
            "short_term": ["Complete online courses", "Build personal projects", "Contribute to open source"],
            "medium_term": ["Get certified", "Attend tech conferences", "Network with professionals"],
            "long_term": ["Consider leadership roles", "Mentor junior developers", "Start a tech blog"]
        }
        
        return {
            "skill_analysis": skill_analysis,
            "salary_projection": salary_projection,
            "career_paths": career_paths,
            "skill_gaps": skill_gaps,
            "market_competitiveness": market_competitiveness,
            "growth_recommendations": growth_recommendations,
            "resume_summary": {
                "name": name,
                "role": role,
                "experience_years": experience_years,
                "skills_count": len(skills)
            }
        }
    except Exception as e:
        return {"error": f"Analysis error: {str(e)}"}

def analyze_fresher_career_based_on_resume(resume_data):
    """Simple fresher career analysis based on resume data"""
    try:
        name = resume_data.get('name', 'Unknown')
        role = resume_data.get('role', 'Unknown')
        skills = resume_data.get('skills', [])
        experience = resume_data.get('experience', {})
        
        experience_years = experience.get('total_years', 0)
        
        # Determine if actually a fresher
        is_fresher = experience_years <= 2 or len(skills) <= 5
        
        # Simple career readiness score
        career_readiness_score = {
            "overall_score": min(95, 50 + (len(skills) * 3) + (experience_years * 10)),
            "technical_readiness": min(95, 40 + (len(skills) * 4)),
            "market_readiness": min(95, 60 + (experience_years * 15)),
            "recommendations": ["Build more projects", "Learn industry tools", "Practice coding"]
        }
        
        # Simple skill gap analysis
        skill_gap_analysis = {
            "critical_gaps": ["Git", "Testing", "Debugging"],
            "nice_to_have": ["Docker", "AWS", "CI/CD"],
            "learning_priority": ["Version Control", "Testing Frameworks", "Code Quality"]
        }
        
        # Simple career growth analysis
        career_growth_analysis = {
            "growth_potential": "High" if is_fresher else "Good",
            "timeline": {
                "0-6_months": "Learn fundamentals",
                "6-12_months": "Build projects",
                "1-2_years": "Get first job",
                "2-3_years": "Become proficient"
            }
        }
        
        # Simple salary projections
        salary_projections = {
            "entry_level": "₹300,000 - ₹500,000",
            "after_1_year": "₹500,000 - ₹700,000",
            "after_2_years": "₹700,000 - ₹1,000,000",
            "growth_rate": "15-20% annually"
        }
        
        # Simple next level positions
        next_level_positions = {
            "immediate": ["Junior Developer", "Associate Developer"],
            "6_months": ["Developer", "Software Engineer"],
            "1_year": ["Senior Developer", "Team Member"],
            "2_years": ["Lead Developer", "Technical Lead"]
        }
        
        # Simple learning roadmap
        learning_roadmap = {
            "month_1": ["Learn Git", "Practice coding", "Build simple projects"],
            "month_2": ["Learn testing", "Study algorithms", "Contribute to open source"],
            "month_3": ["Build portfolio", "Network", "Apply for jobs"],
            "month_4": ["Interview prep", "Mock interviews", "Job applications"]
        }
        
        # Simple recommendations
        recommendations = {
            "immediate": ["Complete online courses", "Build 3-5 projects", "Create GitHub profile"],
            "short_term": ["Get certified", "Attend meetups", "Practice coding daily"],
            "long_term": ["Get first job", "Learn on the job", "Build professional network"]
        }
        
        return {
            "is_fresher": is_fresher,
            "career_readiness_score": career_readiness_score,
            "skill_gap_analysis": skill_gap_analysis,
            "career_growth_analysis": career_growth_analysis,
            "salary_projections": salary_projections,
            "next_level_positions": next_level_positions,
            "learning_roadmap": learning_roadmap,
            "recommendations": recommendations,
            "resume_summary": {
                "name": name,
                "role": role,
                "experience_years": experience_years,
                "skills_count": len(skills)
            }
        }
    except Exception as e:
        return {"error": f"Fresher analysis error: {str(e)}"}

# In-memory storage for demo (no database required)
users_db = {}
jobs_db = {}
applications_db = {}
resumes_db = {}

# Authorized email domains - only these domains can register
AUTHORIZED_DOMAINS = ['gmail.com', 'outlook.com', 'yahoo.com', 'hotmail.com']
AUTHORIZED_EMAILS = ['manjari1998@gmail.com']  # Specific authorized emails

# JWT configuration
SECRET_KEY = "your-secret-key-here"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Security
security = HTTPBearer()

# Initialize database on startup
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    init_database()
    yield
    # Shutdown (if needed)
    pass

app = FastAPI(title="Job Portal API", version="1.0.0", lifespan=lifespan)

# CORS middleware
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Templates
templates = Jinja2Templates(directory="templates")

# Pydantic models
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class JobCreate(BaseModel):
    title: str
    company: str
    location: str
    description: str
    requirements: str
    salary_range: str

# Database functions
def get_db_connection():
    return None  # Using in-memory storage

def validate_email(email: str) -> bool:
    """Validate if email is authorized"""
    # Check if email is in authorized list
    if email in AUTHORIZED_EMAILS:
        return True
    
    # Check if domain is authorized
    domain = email.split('@')[-1].lower()
    if domain in AUTHORIZED_DOMAINS:
        return True
    
    return False

def init_database():
    """Initialize in-memory database with sample data"""
    global users_db, jobs_db, applications_db, resumes_db
    
    # Only authorized user
    users_db["manjari1998@gmail.com"] = {
        'name': 'Manjari Madyalkar',
        'email': 'manjari1998@gmail.com',
        'password': hash_password('password123'),
        'resume_file_path': None,
        'resume_filename': None,
        'resume_upload_date': None
    }
    
    # No fake jobs - jobs will be added by authorized users only

# Authentication functions
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password: str, hashed: str) -> bool:
    return hash_password(password) == hashed

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        token = credentials.credentials
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        logger.info(f"Token verified for user: {email}")
        return email
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token signature")
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid token")

# Routes
@app.get("/", response_class=HTMLResponse)
async def read_root():
    return templates.TemplateResponse("index_final_v3.html", {"request": {}})

@app.post("/api/register")
async def register(user: UserCreate):
    if user.email in users_db:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Validate email authorization
    if not validate_email(user.email):
        raise HTTPException(status_code=403, detail="Email domain not authorized for registration")
    
    users_db[user.email] = {
        'name': user.name,
        'email': user.email,
        'password': hash_password(user.password),
        'resume_file_path': None,
        'resume_filename': None,
        'resume_upload_date': None
    }
    
    return {"message": "User registered successfully"}

@app.post("/api/login")
async def login(user: UserLogin):
    if user.email not in users_db:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    stored_user = users_db[user.email]
    if not verify_password(user.password, stored_user['password']):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token = create_access_token(data={"sub": user.email})
    return {
        "access_token": access_token, 
        "token_type": "bearer",
        "user": {
            "name": stored_user['name'],
            "email": stored_user['email'],
            "role": stored_user.get('role', 'candidate'),
            "phone": stored_user.get('phone', '')
        }
    }

@app.get("/api/jobs")
async def get_jobs():
    return {"jobs": list(jobs_db.values())}

@app.post("/api/jobs")
async def create_job(job: JobCreate, email: str = Depends(verify_token)):
    job_id = len(jobs_db) + 1
    jobs_db[job_id] = {
        'id': job_id,
        'title': job.title,
        'company': job.company,
        'location': job.location,
        'description': job.description,
        'requirements': job.requirements,
        'salary_range': job.salary_range,
        'posted_date': datetime.now().strftime('%Y-%m-%d')
    }
    return {"message": "Job created successfully", "job_id": job_id}

@app.post("/api/apply/{job_id}")
async def apply_job(job_id: int, email: str = Depends(verify_token)):
    if job_id not in jobs_db:
        raise HTTPException(status_code=404, detail="Job not found")
    
    application_id = len(applications_db) + 1
    applications_db[application_id] = {
        'id': application_id,
        'job_id': job_id,
        'user_email': email,
        'status': 'applied',
        'applied_date': datetime.now().strftime('%Y-%m-%d')
    }
    
    return {"message": "Application submitted successfully"}

@app.get("/api/applications")
async def get_applications(email: str = Depends(verify_token)):
    """Get all applications for the current user"""
    user_applications = []
    for app_id, app in applications_db.items():
        if app['user_email'] == email:
            # Get job details
            job = jobs_db.get(app['job_id'], {})
            user_applications.append({
                'id': app['id'],
                'job_id': app['job_id'],
                'job_title': job.get('title', 'Unknown Job'),
                'company': job.get('company', 'Unknown Company'),
                'location': job.get('location', 'Unknown Location'),
                'status': app['status'],
                'applied_date': app['applied_date']
            })
    
    return {"applications": user_applications}

@app.post("/api/ai-resume-analysis")
async def ai_resume_analysis(
    email: str = Depends(verify_token)
):
    """AI-powered resume analysis"""
    try:
        logger.info(f"🤖 Starting AI resume analysis for user: {email}")
        
        # Get user profile
        user_profile = users_db.get(email, {})
        if not user_profile:
            raise HTTPException(status_code=404, detail="User profile not found")
        
        # Get resume data from resumes_db
        if email not in resumes_db:
            raise HTTPException(status_code=404, detail="No resume uploaded. Please upload a resume first.")
        
        resume_data = resumes_db[email]
        
        # Perform AI analysis using career analyzer
        analysis_result = career_analyzer.analyze_career_path(resume_data)
        
        logger.info("✅ AI resume analysis completed successfully")
        return analysis_result
        
    except Exception as e:
        logger.error(f"❌ AI resume analysis error: {e}")
        raise HTTPException(status_code=500, detail=f"Analysis error: {str(e)}")

@app.post("/api/upload-resume")
async def upload_resume(
    file: UploadFile = File(...),
    email: str = Depends(verify_token)
):
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")
    
    # Create uploads directory if not exists
    os.makedirs("uploads", exist_ok=True)
    
    # Remove previous resume file for this user
    previous_files = glob.glob(f"uploads/{email}_*.pdf")
    for old_file in previous_files:
        try:
            os.remove(old_file)
            print(f"Removed previous resume: {old_file}")
        except OSError as e:
            print(f"Error removing old file {old_file}: {e}")
    
    # Generate unique filename with timestamp
    timestamp = int(time.time())
    safe_filename = file.filename.replace(" ", "_").replace("(", "").replace(")", "")
    file_path = f"uploads/{email}_{timestamp}_{safe_filename}"
    
    # Save new file
    async with aiofiles.open(file_path, 'wb') as f:
        content = await file.read()
        await f.write(content)
    
    # Extract text from PDF file first
    try:
        # Read the uploaded file and extract text
        with open(file_path, 'rb') as f:
            pdf_reader = PyPDF2.PdfReader(f)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
        
        logger.info(f"📄 Extracted text from PDF: {len(text)} characters")
        logger.info(f"📄 First 200 chars: {text[:200]}")
        
        # Extract resume content from the extracted text
        extracted_data = extract_resume_content_from_text(text, file.filename)
        
    except Exception as e:
        logger.error(f"❌ Error extracting text from PDF: {e}")
        extracted_data = extract_resume_content_from_text("", file.filename)
    
    # Store in in-memory database
    try:
        # Update user profile with extracted data and file path
        existing_profile = users_db.get(email, {})
        
        # Update with new resume data
        existing_profile.update({
            'resume_file_path': file_path,
            'resume_filename': file.filename,
            'resume_upload_date': timestamp,
            'name': extracted_data.get('name', existing_profile.get('name')),
            'email': extracted_data.get('email', existing_profile.get('email')),
            'phone': extracted_data.get('phone', existing_profile.get('phone')),
            'skills': extracted_data.get('skills', existing_profile.get('skills', [])),
            'experience': extracted_data.get('experience', existing_profile.get('experience')),
            'role': extracted_data.get('role', existing_profile.get('role'))
        })
        
        # Store in in-memory databases
        users_db[email] = existing_profile
        resumes_db[email] = extracted_data
        
        return {
            "message": "Resume uploaded successfully",
            "extracted_data": extracted_data
        }
        
    except Exception as e:
        logger.error(f"Error processing resume: {e}")
        return {"message": f"Resume uploaded but processing failed: {str(e)}"}

@app.get("/api/user-resume")
async def get_user_resume(email: str = Depends(verify_token)):
    """Get user's saved resume data"""
    try:
        # Check if user has a resume in in-memory storage
        if email not in resumes_db:
            return {"message": "No resume uploaded yet", "has_resume": False}
        
        resume_data = resumes_db[email]
        user_profile = users_db.get(email, {})
        
        return {
            "has_resume": True,
            "resume_data": resume_data,
            "user_profile": {
                "name": user_profile.get('name', 'Unknown'),
                "email": user_profile.get('email', 'Unknown'),
                "resume_filename": user_profile.get('resume_filename', 'Unknown'),
                "resume_upload_date": user_profile.get('resume_upload_date', 0)
            }
        }
        
    except Exception as e:
        logger.error(f"Error getting user resume: {e}")
        return {"message": f"Error retrieving resume: {str(e)}"}

@app.delete("/api/remove-resume")
async def remove_resume(email: str = Depends(verify_token)):
    """Remove user's resume"""
    try:
        # Remove from in-memory storage
        if email in resumes_db:
            del resumes_db[email]
        
        # Update user profile
        if email in users_db:
            users_db[email].update({
                'resume_file_path': None,
                'resume_filename': None,
                'resume_upload_date': None
            })
        
        return {"message": "Resume removed successfully"}
        
    except Exception as e:
        logger.error(f"Error removing resume: {e}")
        return {"message": f"Error removing resume: {str(e)}"}

@app.get("/api/career-analysis")
async def get_career_analysis(email: str = Depends(verify_token)):
    """Get career analysis for user"""
    try:
        if email not in resumes_db:
            return {"success": False, "message": "No resume uploaded yet"}
        
        resume_data = resumes_db[email]
        analysis = analyze_career_based_on_resume(resume_data)
        
        return {"success": True, "analysis": analysis}
        
    except Exception as e:
        logger.error(f"Error in career analysis: {e}")
        return {"success": False, "message": f"Analysis error: {str(e)}"}

@app.get("/api/fresher-career-analysis")
async def get_fresher_career_analysis(email: str = Depends(verify_token)):
    """Get fresher career analysis for user"""
    try:
        if email not in resumes_db:
            return {"success": False, "message": "No resume uploaded yet"}
        
        resume_data = resumes_db[email]
        analysis = analyze_fresher_career_based_on_resume(resume_data)
        
        return {"success": True, "analysis": analysis}
        
    except Exception as e:
        logger.error(f"Error in fresher career analysis: {e}")
        return {"success": False, "message": f"Analysis error: {str(e)}"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)

