"""
Job Portal Application - Clean Version Without Extraction
Simple job portal with basic functionality
"""

from fastapi import FastAPI, HTTPException, Depends, UploadFile, File, Form
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from pydantic import BaseModel, EmailStr
import jwt
import hashlib
import os
import json
import re
import aiofiles
import logging
import smtplib
import glob
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from contextlib import asynccontextmanager
import dateutil.parser
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List
import PyPDF2
import glob
import time
import pymongo
from pymongo import MongoClient

# Import Precision extractor and text extractor
from resume_text_extractor import resume_text_extractor
from ai_career_analyzer import ai_career_analyzer
from ai_resume_analyzer import ai_resume_analyzer
from improved_ai_career_analyzer import improved_ai_career_analyzer
from universal_resume_extractor import universal_resume_extractor
from advanced_ai_career_analyzer import advanced_ai_career_analyzer
from simple_ai_analyzer import simple_ai_analyzer
from precise_resume_extractor import precise_resume_extractor
from ultra_precise_extractor import ultra_precise_extractor
from perfect_extractor_v2 import perfect_extractor_v2
from smart_pattern_analyzer import smart_pattern_analyzer
from line_by_line_analyzer import line_by_line_analyzer
from filename_based_extractor import filename_based_extractor
from deep_text_analyzer import deep_text_analyzer
from accurate_name_role_extractor import accurate_name_role_extractor
from comprehensive_accurate_extractor import comprehensive_accurate_extractor
from precise_name_role_extractor import precise_name_role_extractor
from advanced_accurate_extractor import advanced_accurate_extractor
from reliable_extractor import reliable_extractor

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
        """Load skill market demand data dynamically"""
        # This would ideally be loaded from a database or API
        # For now, using a more comprehensive and dynamic approach
        return {
            'high_demand': ['Python', 'JavaScript', 'React', 'AWS', 'Docker', 'Kubernetes', 'TypeScript', 'Node.js', 'Spring Boot', 'Microservices'],
            'medium_demand': ['Java', 'Angular', 'MySQL', 'Git', 'MongoDB', 'PostgreSQL', 'Redis', 'Elasticsearch'],
            'emerging': ['Machine Learning', 'Data Science', 'AI', 'Cloud Computing', 'DevOps', 'Kubernetes', 'Terraform', 'Ansible'],
            'trending': ['Vue.js', 'GraphQL', 'Serverless', 'Edge Computing', 'Blockchain', 'IoT', 'AR/VR']
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
            
            # Generate dynamic recommendations based on skill analysis
            high_demand_count = len(skill_analysis['high_demand_skills'])
            emerging_count = len(skill_analysis['emerging_skills'])
            
            if high_demand_count < 3:
                skill_analysis['recommendations'].append(f"Consider learning more high-demand skills (currently have {high_demand_count})")
            
            if emerging_count == 0:
                skill_analysis['recommendations'].append("Consider learning emerging technologies to stay competitive")
            
            if high_demand_count >= 5:
                skill_analysis['recommendations'].append("Excellent high-demand skill coverage!")
            
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

# AI-powered resume extraction function
def extract_resume_content_from_text(text, filename=None):
    """Extract resume content using accurate name and role extraction"""
    try:
        logger.info("📄 Starting accurate resume extraction...")
        
        # Use reliable extractor for guaranteed accuracy
        try:
            extracted_data = reliable_extractor.extract_resume_data(text, filename)
            logger.info("✅ Using reliable extraction results")
        except Exception as e:
            logger.error(f"❌ Error in reliable extraction: {e}")
            # If reliable extractor fails, return empty result
            logger.error("❌ Reliable extractor failed, returning empty result")
            extracted_data = {
                'name': 'Name not found',
                'email': 'Email not found',
                'phone': 'Phone not found',
                'skills': [],
                'experience': {'total_years': 0, 'total_months': 0, 'display': 'Experience not found'},
                'role': 'Role not found',
                'location': 'Location not found',
                'education': [],
                'raw_text': '',
                'extraction_method': 'reliable_extraction_failed',
                'confidence_score': 0.0,
                'extraction_timestamp': datetime.now().isoformat()
            }
        
        # Add additional fields that might be needed by the system
        if 'skills' not in extracted_data:
            extracted_data['skills'] = []
        if 'experience' not in extracted_data:
            extracted_data['experience'] = {'total_years': 0, 'total_months': 0, 'display': 'Experience not found'}
        if 'location' not in extracted_data:
            extracted_data['location'] = 'Location not found'
        if 'education' not in extracted_data:
            extracted_data['education'] = []
        
        logger.info("✅ Accurate resume extraction completed successfully")
        return extracted_data
        
    except Exception as e:
        logger.error(f"❌ Error in accurate resume extraction: {e}")
        return {
            'name': 'Extraction error',
            'email': 'Extraction error',
            'phone': 'Extraction error',
            'skills': [],
            'experience': {'total_years': 0, 'total_months': 0, 'display': 'Extraction error'},
            'role': 'Extraction error',
            'location': 'Extraction error',
            'education': [],
            'raw_text': text[:500] if text else '',
            'extraction_method': 'accurate_extraction_error',
            'confidence_score': 0.0,
            'extraction_timestamp': datetime.now().isoformat()
        }

# Removed all extraction functions - keeping only simple file handling

# Removed email extraction function

# Removed phone extraction function

# Removed skills extraction function

# Removed experience extraction function

# Removed date calculation function

# Removed role extraction function

# Removed confidence calculation function

def analyze_career_based_on_resume(resume_data):
    """AI-powered career analysis with advanced features"""
    try:
        logger.info("🤖 Starting AI-powered career analysis...")
        
        # Use AI career analyzer for comprehensive analysis
        skill_gap_analysis = ai_career_analyzer.analyze_skills(resume_data.get('skills', []))
        salary_projection = ai_career_analyzer.project_salary(
            resume_data.get('experience', {}).get('total_years', 0),
            resume_data.get('skills', [])
        )
        career_growth_analysis = ai_career_analyzer.suggest_career_path(
            resume_data.get('role', 'Developer'),
            resume_data.get('experience', {}).get('total_years', 0)
        )
        location_growth_analysis = ai_career_analyzer.analyze_location_growth(
            resume_data.get('location', 'Unknown'),
            resume_data.get('skills', [])
        )
        
        # Combine all analyses
        analysis_result = {
            "skill_gap_analysis": skill_gap_analysis,
            "salary_projection": salary_projection,
            "career_growth_analysis": career_growth_analysis,
            "location_growth_analysis": location_growth_analysis,
            "ai_insights": {
                "extraction_method": resume_data.get('extraction_method', 'ai_powered'),
                "confidence_score": resume_data.get('confidence_score', 0.0),
                "ai_powered": True,
                "analysis_timestamp": datetime.now().isoformat(),
                "personalized": True
            },
            "resume_summary": {
                "name": resume_data.get('name', 'Unknown'),
                "role": resume_data.get('role', 'Unknown'),
                "experience_years": resume_data.get('experience', {}).get('total_years', 0),
                "skills_count": len(resume_data.get('skills', [])),
                "location": resume_data.get('location', 'Unknown'),
                "education": resume_data.get('education', [])
            }
        }
        
        logger.info("✅ AI career analysis completed successfully")
        return analysis_result
        
    except Exception as e:
        logger.error(f"❌ Error in AI career analysis: {e}")
        return {"error": f"AI analysis error: {str(e)}"}
    
# Removed all helper functions for AI analysis

def analyze_fresher_career_based_on_resume(resume_data):
    """AI-powered fresher career analysis with personalized path"""
    try:
        logger.info("🤖 Starting AI-powered fresher career analysis...")
        
        # Use simple AI analyzer for comprehensive analysis (guaranteed to work)
        comprehensive_analysis = simple_ai_analyzer.analyze_resume(resume_data)
        
        # Extract specific components for fresher analysis
        skill_gap_analysis = comprehensive_analysis.get('skill_gap_analysis', {})
        salary_projection = comprehensive_analysis.get('salary_analysis', {})
        career_growth_analysis = comprehensive_analysis.get('career_path_analysis', {})
        location_growth_analysis = comprehensive_analysis.get('industry_analysis', {})
        
        # Generate fresher-specific career path
        fresher_career_path = {
            "entry_level_path": "Intern → Junior Developer → Mid Developer → Senior Developer",
            "skill_development": "Learn fundamentals → Build projects → Gain experience → Specialize",
            "recommended_skills": ["Python", "JavaScript", "Git", "SQL", "Problem Solving"],
            "certifications": ["AWS Certified Developer", "Google Cloud Associate", "Microsoft Azure Fundamentals"],
            "next_steps": [
                "Complete 2-3 personal projects",
                "Contribute to open source",
                "Build a strong GitHub profile",
                "Practice coding problems daily",
                "Learn version control (Git)",
                "Understand basic system design"
            ]
        }
        
        # Combine fresher-specific analyses
        fresher_analysis = {
            "fresher_career_path": fresher_career_path,
            "skill_gap_analysis": skill_gap_analysis,
            "salary_projection": salary_projection,
            "career_growth_analysis": career_growth_analysis,
            "location_growth_analysis": location_growth_analysis,
            "ai_insights": {
                "extraction_method": resume_data.get('extraction_method', 'ai_powered'),
                "confidence_score": resume_data.get('confidence_score', 0.0),
                "ai_powered": True,
                "personalized": True,
                "fresher_focused": True,
                "analysis_timestamp": datetime.now().isoformat()
            },
            "resume_summary": {
                "name": resume_data.get('name', 'Unknown'),
                "role": resume_data.get('role', 'Unknown'),
                "experience_years": resume_data.get('experience', {}).get('total_years', 0),
                "skills_count": len(resume_data.get('skills', [])),
                "location": resume_data.get('location', 'Unknown'),
                "education": resume_data.get('education', [])
            }
        }
        
        logger.info("✅ AI fresher analysis completed successfully")
        return fresher_analysis
        
    except Exception as e:
        logger.error(f"❌ Error in AI fresher analysis: {e}")
        return {"error": f"AI fresher analysis error: {str(e)}"}

# In-memory storage for demo (no database required)
users_db = {}
jobs_db = {}
applications_db = {}
resumes_db = {}

# Email configuration
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_USERNAME = "your-email@gmail.com"  # Replace with actual email
EMAIL_PASSWORD = "your-app-password"     # Replace with actual app password

# MongoDB configuration
MONGODB_URL = "mongodb://localhost:27017"  # Local MongoDB
# MONGODB_URL = "mongodb+srv://username:password@cluster.mongodb.net/jobportal"  # MongoDB Atlas
DATABASE_NAME = "jobportal"

# Persistent storage for resumes
RESUMES_FILE = "persistent_resumes.json"
USERS_FILE = "persistent_users.json"
APPLICATIONS_FILE = "persistent_applications.json"
JOBS_FILE = "persistent_jobs.json"

def save_persistent_data():
    """Save data to persistent storage"""
    try:
        # Save resumes
        with open(RESUMES_FILE, 'w') as f:
            json.dump(resumes_db, f, indent=2, default=str)
        
        # Save users
        with open(USERS_FILE, 'w') as f:
            json.dump(users_db, f, indent=2, default=str)
        
        # Save applications
        with open(APPLICATIONS_FILE, 'w') as f:
            json.dump(applications_db, f, indent=2, default=str)
        
        # Save jobs
        with open(JOBS_FILE, 'w') as f:
            json.dump(jobs_db, f, indent=2, default=str)
        
        logger.info("✅ Persistent data saved successfully")
    except Exception as e:
        logger.error(f"❌ Error saving persistent data: {e}")

def load_persistent_data():
    """Load data from persistent storage"""
    global resumes_db, users_db, applications_db, jobs_db
    
    try:
        # Load resumes
        if os.path.exists(RESUMES_FILE):
            with open(RESUMES_FILE, 'r') as f:
                resumes_db = json.load(f)
            logger.info(f"✅ Loaded {len(resumes_db)} resumes from persistent storage")
            
            # Clear any cached analysis results to force fresh analysis
            for email, resume_data in resumes_db.items():
                if 'analysis_result' in resume_data:
                    del resume_data['analysis_result']
                    logger.info(f"🧹 Cleared cached analysis for {email}")
        
        # Load users
        if os.path.exists(USERS_FILE):
            with open(USERS_FILE, 'r') as f:
                users_db = json.load(f)
            logger.info(f"✅ Loaded {len(users_db)} users from persistent storage")
            
        # Load applications
        if os.path.exists(APPLICATIONS_FILE):
            with open(APPLICATIONS_FILE, 'r') as f:
                applications_db = json.load(f)
            logger.info(f"✅ Loaded {len(applications_db)} applications from persistent storage")
        
        # Load jobs
        if os.path.exists(JOBS_FILE):
            with open(JOBS_FILE, 'r') as f:
                jobs_db = json.load(f)
            logger.info(f"✅ Loaded {len(jobs_db)} jobs from persistent storage")
            
    except Exception as e:
        logger.error(f"❌ Error loading persistent data: {e}")
        # Initialize empty if loading fails
        resumes_db = {}
        users_db = {}
        applications_db = {}
        jobs_db = {}

def clear_cached_extraction_data():
    """Clear cached extraction data to force fresh extraction"""
    global resumes_db, users_db
    
    try:
        logger.info("🧹 Clearing cached extraction data...")
        
        # Clear resume data for all users
        for email in list(resumes_db.keys()):
            if email in resumes_db:
                del resumes_db[email]
                logger.info(f"🧹 Cleared resume data for {email}")
        
        # Clear user profile data (keep login info)
        for email in list(users_db.keys()):
            if email in users_db:
                user_data = users_db[email]
                # Keep only essential login data
                users_db[email] = {
                    'email': user_data.get('email', email),
                    'password': user_data.get('password', ''),
                    'role': user_data.get('role', 'user')
                }
                logger.info(f"🧹 Cleared profile data for {email}")
        
        # Save cleared data
        save_persistent_data()
        logger.info("✅ Cached extraction data cleared successfully")
        
    except Exception as e:
        logger.error(f"❌ Error clearing cached data: {e}")

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

# Static files
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Pydantic models
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: str = "candidate"
    phone: str = None

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
    """Get MongoDB database connection"""
    try:
        client = MongoClient(MONGODB_URL)
        db = client[DATABASE_NAME]
        return db
    except Exception as e:
        logger.error(f"❌ MongoDB connection failed: {e}")
        return None

def get_collection(collection_name: str):
    """Get MongoDB collection"""
    db = get_db_connection()
    if db:
        return db[collection_name]
    return None

def init_database():
    """Initialize in-memory database with sample data"""
    global users_db, jobs_db, applications_db, resumes_db
    
    # Load persistent data first
    load_persistent_data()
    
    # No sample users - users must register
    
    # No fake jobs - jobs will be added by authorized users only

# Authentication functions
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password: str, hashed: str) -> bool:
    return hash_password(password) == hashed

async def send_application_notification(user_email: str, job_id: int):
    """Send email notification when user applies for a job"""
    try:
        # Get job details
        job_key = str(job_id)
        job_data = jobs_db.get(job_key, {})
        if not job_data:
            logger.warning(f"Job {job_id} not found for email notification")
            return
        
        # Get user details
        user_data = users_db.get(user_email, {})
        user_name = user_data.get('name', 'User')
        
        # Create email content
        subject = f"Application Submitted Successfully - {job_data.get('title', 'Job')}"
        
        html_content = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <h2 style="color: #2563eb;">Application Submitted Successfully!</h2>
                
                <p>Dear {user_name},</p>
                
                <p>Thank you for applying to the position. Your application has been submitted successfully.</p>
                
                <div style="background-color: #f8fafc; padding: 20px; border-radius: 8px; margin: 20px 0;">
                    <h3 style="color: #1e40af; margin-top: 0;">Job Details:</h3>
                    <p><strong>Position:</strong> {job_data.get('title', 'N/A')}</p>
                    <p><strong>Company:</strong> {job_data.get('company', 'N/A')}</p>
                    <p><strong>Location:</strong> {job_data.get('location', 'N/A')}</p>
                    <p><strong>Salary Range:</strong> {job_data.get('salary_range', 'N/A')}</p>
                </div>
                
                <p>Your application is now under review. We will contact you if you are selected for the next round.</p>
                
                <p>Best regards,<br>
                Job Portal Team</p>
                
                <hr style="margin: 30px 0; border: none; border-top: 1px solid #e5e7eb;">
                <p style="font-size: 12px; color: #6b7280;">
                    This is an automated message. Please do not reply to this email.
                </p>
            </div>
        </body>
        </html>
        """
        
        # Create message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = EMAIL_USERNAME
        msg['To'] = user_email
        
        # Add HTML content
        html_part = MIMEText(html_content, 'html')
        msg.attach(html_part)
        
        # Send email
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_USERNAME, EMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()
        
        logger.info(f"✅ Email notification sent to {user_email} for job {job_id}")
        
    except Exception as e:
        logger.error(f"❌ Failed to send email notification: {e}")
        raise e

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
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token signature")
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid token")

# Routes
@app.get("/", response_class=HTMLResponse)
async def read_root():
    return templates.TemplateResponse("index_final_v3.html", {"request": {}})

@app.get("/test")
async def test_upload():
    return FileResponse("test_upload.html")

@app.post("/api/register")
async def register(user: UserCreate):
    if user.email in users_db:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    users_db[user.email] = {
        'name': user.name,
        'email': user.email,
        'password': hash_password(user.password),
        'role': user.role,
        'phone': user.phone,
        'resume_file_path': None,
        'resume_filename': None,
        'resume_upload_date': None
    }
    
    # Save to persistent storage
    save_persistent_data()
    
    return {"message": "User registered successfully"}

@app.post("/api/login")
async def login(user: UserLogin):
    if user.email not in users_db:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    stored_user = users_db[user.email]
    # Check if password field exists in stored user data
    if 'password' not in stored_user:
        raise HTTPException(status_code=401, detail="User data corrupted - please re-register")
    
    if not verify_password(user.password, stored_user['password']):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token = create_access_token(data={"sub": user.email})
    
    # Return user data for frontend
    user_data = {
        "email": user.email,
        "name": stored_user.get('name', ''),
        "role": stored_user.get('role', 'candidate')
    }
    
    return {
        "access_token": access_token, 
        "token_type": "bearer",
        "user": user_data
    }

@app.get("/api/jobs")
async def get_jobs(
    search: str = None,
    location: str = None,
    company: str = None,
    min_salary: int = None,
    max_salary: int = None,
    job_type: str = None
):
    """Get jobs with search and filter options"""
    try:
        jobs = list(jobs_db.values())
        
        # Apply search filter
        if search:
            search_lower = search.lower()
            jobs = [job for job in jobs if 
                   search_lower in job.get('title', '').lower() or
                   search_lower in job.get('description', '').lower() or
                   search_lower in job.get('requirements', '').lower() or
                   search_lower in job.get('company', '').lower()]
        
        # Apply location filter
        if location:
            location_lower = location.lower()
            jobs = [job for job in jobs if location_lower in job.get('location', '').lower()]
        
        # Apply company filter
        if company:
            company_lower = company.lower()
            jobs = [job for job in jobs if company_lower in job.get('company', '').lower()]
        
        # Apply salary filters
        if min_salary is not None:
            jobs = [job for job in jobs if _extract_salary_min(job.get('salary_range', '')) >= min_salary]
        
        if max_salary is not None:
            jobs = [job for job in jobs if _extract_salary_max(job.get('salary_range', '')) <= max_salary]
        
        # Apply job type filter
        if job_type:
            job_type_lower = job_type.lower()
            jobs = [job for job in jobs if job_type_lower in job.get('job_type', '').lower()]
        
        return {"jobs": jobs, "total": len(jobs)}
    except Exception as e:
        logger.error(f"Error filtering jobs: {e}")
        return {"jobs": list(jobs_db.values()), "total": len(jobs_db)}

def _extract_salary_min(salary_range: str) -> int:
    """Extract minimum salary from salary range string"""
    try:
        import re
        # Extract numbers from salary range (e.g., "50,000 - 80,000" -> 50000)
        numbers = re.findall(r'[\d,]+', salary_range.replace(',', ''))
        if numbers:
            return int(numbers[0])
        return 0
    except:
        return 0

def _extract_salary_max(salary_range: str) -> int:
    """Extract maximum salary from salary range string"""
    try:
        import re
        # Extract numbers from salary range (e.g., "50,000 - 80,000" -> 80000)
        numbers = re.findall(r'[\d,]+', salary_range.replace(',', ''))
        if len(numbers) > 1:
            return int(numbers[1])
        elif len(numbers) == 1:
            return int(numbers[0])
        return 999999
    except:
        return 999999

@app.get("/api/debug-resume/{email}")
async def debug_resume_data(email: str = Depends(verify_token)):
    """Debug endpoint to check resume data"""
    try:
        if email not in resumes_db:
            return {"error": "No resume found"}
        
        resume_data = resumes_db[email]
        return {
            "email": email,
            "resume_keys": list(resume_data.keys()),
            "skills": resume_data.get('skills', []),
            "role": resume_data.get('role', 'Unknown'),
            "experience": resume_data.get('experience', {}),
            "name": resume_data.get('name', 'Unknown')
        }
    except Exception as e:
        return {"error": str(e)}

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
        
        # Get resume data from resumes_db (persistent storage)
        if email not in resumes_db:
            raise HTTPException(status_code=404, detail="No resume uploaded. Please upload a resume first.")
        
        resume_data = resumes_db[email]
        
        # Debug: Log the resume data structure
        logger.info(f"🔍 Debug - Resume data keys: {list(resume_data.keys())}")
        logger.info(f"🔍 Debug - Skills in resume_data: {resume_data.get('skills', 'NOT_FOUND')}")
        logger.info(f"🔍 Debug - Skills type: {type(resume_data.get('skills', []))}")
        logger.info(f"🔍 Debug - Role: {resume_data.get('role', 'NOT_FOUND')}")
        
        # Perform AI analysis using simple analyzer (guaranteed to work)
        analysis_result = simple_ai_analyzer.analyze_resume(resume_data)
        
        logger.info("✅ AI resume analysis completed successfully")
        return analysis_result
        
    except Exception as e:
        logger.error(f"❌ AI resume analysis error: {e}")
        logger.error(f"❌ Error type: {type(e).__name__}")
        logger.error(f"❌ Error details: {str(e)}")
        import traceback
        logger.error(f"❌ Traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Analysis error: {str(e)}")

@app.post("/api/admin/ai-resume-analysis")
async def admin_ai_resume_analysis(request: dict, email: str = Depends(verify_token)):
    """Admin AI-powered resume analysis for any user"""
    try:
        # Check if user is admin
        user = users_db.get(email, {})
        if user.get('role') != 'admin':
            raise HTTPException(status_code=403, detail="Admin access required")
        
        target_email = request.get('email')
        if not target_email:
            raise HTTPException(status_code=400, detail="Target email is required")
        
        logger.info(f"🤖 Admin AI analysis for user: {target_email}")
        
        # Get target user profile
        user_profile = users_db.get(target_email, {})
        if not user_profile:
            raise HTTPException(status_code=404, detail="Target user not found")
        
        # Get resume data
        if target_email not in resumes_db:
            raise HTTPException(status_code=404, detail="No resume found for this user")
        
        resume_data = resumes_db[target_email]
        
        # Debug: Log the resume data structure
        logger.info(f"🔍 Debug - Resume data keys: {list(resume_data.keys())}")
        logger.info(f"🔍 Debug - Resume data text key exists: {'text' in resume_data}")
        logger.info(f"🔍 Debug - Name: {resume_data.get('name', 'N/A')}")
        logger.info(f"🔍 Debug - Email: {resume_data.get('email', 'N/A')}")
        logger.info(f"🔍 Debug - Role: {resume_data.get('role', 'N/A')}")
        logger.info(f"🔍 Debug - Experience: {resume_data.get('experience', 'N/A')}")
        logger.info(f"🔍 Debug - Skills: {resume_data.get('skills', 'N/A')}")
        
        if 'text' in resume_data:
            logger.info(f"🔍 Debug - Resume text length: {len(resume_data['text'])}")
            logger.info(f"🔍 Debug - Resume text preview: {resume_data['text'][:200]}")
        
        # Perform AI analysis using simple analyzer (guaranteed to work)
        analysis_result = simple_ai_analyzer.analyze_resume(resume_data)
        
        # Add resume text to analysis result for frontend extraction
        resume_text = resume_data.get('text', '') or resume_data.get('raw_text', '') or resume_data.get('content', '')
        
        # If no resume text found, try to extract from file directly
        if not resume_text and 'resume_file_path' in resume_data:
            try:
                import PyPDF2
                with open(resume_data['resume_file_path'], 'rb') as file:
                    pdf_reader = PyPDF2.PdfReader(file)
                    resume_text = ""
                    for page in pdf_reader.pages:
                        resume_text += page.extract_text()
                logger.info(f"🔍 Extracted resume text from PDF file: {len(resume_text)} characters")
            except Exception as e:
                logger.error(f"❌ Error extracting text from PDF: {e}")
        
        analysis_result['resume_text'] = resume_text
        
        # Enhanced AI scoring
        enhanced_score = calculate_enhanced_ai_score(analysis_result, user_profile, resume_data)
        
        # Add enhanced score to the result
        analysis_result['ai_insights']['confidence'] = enhanced_score
        # Calculate individual scores safely
        skills_data = analysis_result.get('skills', {})
        if isinstance(skills_data, dict):
            skills_list = skills_data.get('extracted', [])
        elif isinstance(skills_data, list):
            skills_list = skills_data
        else:
            skills_list = []
        
        skills_count = len(skills_list) if isinstance(skills_list, list) else 0
        
        # Extract experience safely - prioritize AI analysis data
        experience_years = 0
        if analysis_result.get('experience') and analysis_result['experience'].get('years'):
            experience_years = analysis_result['experience']['years']
        elif user_profile.get('experience'):
            experience_years = user_profile.get('experience')
        
        if not isinstance(experience_years, (int, float)):
            experience_years = 0
        
        resume_text = resume_data.get('text', '')
        if not isinstance(resume_text, str):
            resume_text = str(resume_text)
        resume_text = resume_text.lower()
        
        # Calculate individual scores using dynamic analysis
        # Extract skills dynamically from the actual skills list
        core_skill_matches = len([skill for skill in skills_list if any(keyword in skill.lower() for keyword in ['java', 'spring', 'javascript', 'html', 'css', 'mysql', 'oracle', 'git', 'maven', 'jquery', 'json', 'bootstrap'])])
        advanced_skill_matches = len([skill for skill in skills_list if any(keyword in skill.lower() for keyword in ['microservices', 'docker', 'kubernetes', 'aws', 'azure', 'react', 'angular', 'node', 'typescript', 'rest', 'api'])])
        skill_diversity_bonus = min(skills_count * 1.5, 15) if skills_count > 3 else min(skills_count * 1.0, 10)
        skills_score = min((core_skill_matches * 4) + (advanced_skill_matches * 3) + skill_diversity_bonus, 40)
        
        # Experience scoring (more generous)
        if experience_years >= 5:
            experience_score = 35
        elif experience_years >= 3:
            experience_score = 30
        elif experience_years >= 2:
            experience_score = 25
        elif experience_years >= 1:
            experience_score = 20
        else:
            experience_score = 15  # Freshers get decent score
        
        if 'intern' in resume_text or 'internship' in resume_text:
            experience_score += 5
        if 'senior' in resume_text or 'lead' in resume_text:
            experience_score += 5
        if 'project' in resume_text or 'development' in resume_text:
            experience_score += 3
        experience_score = min(experience_score, 35)
        
        # Domain scoring using dynamic keyword detection
        # Extract domain keywords dynamically from resume content
        fullstack_matches = len([keyword for keyword in ['full stack', 'fullstack', 'frontend', 'backend', 'web development', 'web application'] if keyword in resume_text])
        java_matches = len([keyword for keyword in ['java', 'spring', 'spring boot', 'hibernate', 'maven', 'gradle', 'junit', 'tomcat'] if keyword in resume_text])
        db_matches = len([keyword for keyword in ['mysql', 'oracle', 'postgresql', 'mongodb', 'sql', 'database', 'jdbc'] if keyword in resume_text])
        programming_matches = len([keyword for keyword in ['programming', 'coding', 'development', 'software', 'application'] if keyword in resume_text])
        domain_score = min((fullstack_matches * 5) + (java_matches * 3) + (db_matches * 2) + (programming_matches * 2), 25)
        
        # Role scoring using dynamic keyword detection
        role_matches = len([keyword for keyword in ['developer', 'engineer', 'programmer', 'software', 'application', 'system'] if keyword in resume_text])
        leadership_matches = len([keyword for keyword in ['lead', 'senior', 'principal', 'architect', 'manager', 'mentor', 'team'] if keyword in resume_text])
        tech_matches = len([keyword for keyword in ['technical', 'it', 'computer', 'technology', 'coding'] if keyword in resume_text])
        role_score = min((role_matches * 3) + (leadership_matches * 4) + (tech_matches * 2), 20)
        
        analysis_result['enhanced_score'] = {
            'overall_score': enhanced_score,
            'skills_score': skills_score,
            'experience_score': experience_score,
            'domain_score': domain_score,
            'role_score': role_score,
            'core_skills_matched': core_skill_matches,
            'advanced_skills_matched': advanced_skill_matches,
            'total_skills_count': skills_count
        }
        
        # Add enhanced_score at top level for frontend compatibility
        analysis_result['enhanced_score'] = enhanced_score
        
        # Extract email from resume text
        extracted_email = None
        # Use the same resume text that was processed above
        logger.info(f"🔍 Email extraction - Resume text length: {len(resume_text) if resume_text else 0}")
        logger.info(f"🔍 Email extraction - Resume text preview: {resume_text[:200] if resume_text else 'No text'}")
        if resume_text:
            import re
            # Look for email patterns in resume text
            email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            email_matches = re.findall(email_pattern, resume_text)
            logger.info(f"🔍 Email extraction - Found matches: {email_matches}")
            if email_matches:
                extracted_email = email_matches[0]  # Take the first email found
                logger.info(f"✅ Email extracted from resume: {extracted_email}")
            else:
                logger.info("❌ No email found in resume text")
        else:
            logger.info("❌ No resume text available for email extraction")
        
        # Add extracted data to the result for frontend compatibility - USE ACTUAL RESUME DATA
        analysis_result['extracted_skills'] = resume_data.get('skills', [])
        analysis_result['extracted_experience'] = resume_data.get('experience', {}).get('total_years', 0)
        analysis_result['extracted_role'] = resume_data.get('role', 'Developer')
        analysis_result['extracted_email'] = resume_data.get('email', extracted_email)
        analysis_result['extracted_name'] = resume_data.get('name', 'Unknown')
        analysis_result['extracted_phone'] = resume_data.get('phone', 'N/A')
        analysis_result['extracted_location'] = resume_data.get('location', 'N/A')
        
        logger.info(f"✅ Admin AI analysis completed - Score: {enhanced_score}")
        logger.info(f"📤 Sending to frontend - extracted_email: {extracted_email}")
        return analysis_result
        
    except Exception as e:
        logger.error(f"❌ Admin AI analysis error: {e}")
        raise HTTPException(status_code=500, detail=f"Analysis error: {str(e)}")

def calculate_enhanced_ai_score(analysis_result, user_data, resume_data):
    """Calculate enhanced AI score based on ACTUAL resume data - skills, role, domain, experience"""
    try:
        # Use ACTUAL resume data instead of AI analysis results
        actual_skills = resume_data.get('skills', [])
        actual_role = resume_data.get('role', '')
        actual_experience = resume_data.get('experience', {})
        actual_email = resume_data.get('email', '')
        actual_name = resume_data.get('name', '')
        
        # Extract resume text safely
        resume_text = resume_data.get('text', '') or resume_data.get('raw_text', '') or resume_data.get('content', '')
        if not isinstance(resume_text, str):
            resume_text = str(resume_text)
        resume_text = resume_text.lower()
        
        # Use ACTUAL skills from resume data
        skills_list = actual_skills if isinstance(actual_skills, list) else []
        skills_count = len(skills_list)
        
        # Extract experience from ACTUAL resume data
        experience_years = 0
        if isinstance(actual_experience, dict):
            experience_years = actual_experience.get('total_years', 0)
        elif isinstance(actual_experience, (int, float)):
            experience_years = actual_experience
        
        if not isinstance(experience_years, (int, float)):
            experience_years = 0
        experience_years = int(experience_years)
        
        # 1. ENHANCED SKILLS ASSESSMENT (0-100 points) - More comprehensive skill analysis
        if skills_count == 0:
            skills_score = 0
        else:
            # Core technical skills (Java, Spring, Web technologies)
            core_skills = ['java', 'spring', 'spring boot', 'javascript', 'html', 'css', 'mysql', 'oracle', 'git', 'maven', 'jquery', 'json', 'bootstrap']
            core_matches = len([skill for skill in skills_list if any(core in skill.lower() for core in core_skills)])
            
            # Advanced skills (Cloud, DevOps, Modern frameworks)
            advanced_skills = ['docker', 'kubernetes', 'aws', 'azure', 'react', 'angular', 'node', 'typescript', 'microservices', 'rest', 'api']
            advanced_matches = len([skill for skill in skills_list if any(adv in skill.lower() for adv in advanced_skills)])
            
            # Programming languages
            languages = ['python', 'java', 'javascript', 'c', 'c++', 'c#', 'php', 'ruby', 'go', 'rust', 'swift', 'kotlin']
            language_matches = len([skill for skill in skills_list if any(lang in skill.lower() for lang in languages)])
            
            # Database skills
            database_skills = ['mysql', 'postgresql', 'mongodb', 'oracle', 'sql server', 'redis', 'elasticsearch', 'cassandra']
            db_matches = len([skill for skill in skills_list if any(db in skill.lower() for db in database_skills)])
            
            # Testing and Quality Assurance
            testing_skills = ['junit', 'testng', 'selenium', 'cypress', 'jest', 'mocha', 'pytest', 'unittest']
            testing_matches = len([skill for skill in skills_list if any(test in skill.lower() for test in testing_skills)])
            
            # Soft skills and methodologies
            soft_skills = ['agile', 'scrum', 'kanban', 'devops', 'ci/cd', 'jenkins', 'gitlab', 'github actions']
            soft_matches = len([skill for skill in skills_list if any(soft in skill.lower() for soft in soft_skills)])
            
            # Base score: 3 points per skill (reduced to allow more room for quality bonuses)
            base_score = min(skills_count * 3, 30)
            
            # Quality bonuses (more granular scoring)
            core_bonus = core_matches * 10  # 10 points per core skill
            advanced_bonus = advanced_matches * 12  # 12 points per advanced skill
            language_bonus = language_matches * 8  # 8 points per programming language
            db_bonus = db_matches * 6  # 6 points per database skill
            testing_bonus = testing_matches * 5  # 5 points per testing skill
            soft_bonus = soft_matches * 4  # 4 points per soft skill
            
            # Diversity bonus for having multiple skill categories
            categories = [core_matches, advanced_matches, language_matches, db_matches, testing_matches, soft_matches]
            active_categories = len([cat for cat in categories if cat > 0])
            diversity_bonus = min(active_categories * 3, 15)
            
            # Specialization bonus - if candidate has deep knowledge in one area
            max_category = max(categories) if categories else 0
            specialization_bonus = min(max_category * 2, 10) if max_category >= 3 else 0
        
            skills_score = min(base_score + core_bonus + advanced_bonus + language_bonus + 
                             db_bonus + testing_bonus + soft_bonus + diversity_bonus + specialization_bonus, 100)
        
        # 2. ENHANCED EXPERIENCE ASSESSMENT (0-100 points) - More nuanced experience evaluation
        if experience_years == 0:
            # Fresher - check for internship/learning experience
            fresher_keywords = ['intern', 'internship', 'training', 'learning', 'student', 'fresher', 'graduate', 'entry level']
            fresher_matches = len([keyword for keyword in fresher_keywords if keyword in resume_text])
            
            if fresher_matches > 0:
                # Base score for freshers with some experience indicators
                experience_score = 25 + (fresher_matches * 5)  # 25-50 points for freshers
                
                # Additional bonuses for freshers
                if 'project' in resume_text or 'portfolio' in resume_text:
                    experience_score += 10
                if 'certification' in resume_text or 'certified' in resume_text:
                    experience_score += 8
                if 'github' in resume_text or 'git' in resume_text:
                    experience_score += 5
            else:
                experience_score = 15  # Very low score for no experience indicators
        else:
            # Experienced candidates - more sophisticated scoring
            base_score = min(experience_years * 15, 70)  # 15 points per year, max 70
            
            # Quality bonuses based on actual experience depth
            quality_bonus = 0
            
            # Leadership and seniority indicators
            leadership_keywords = ['senior', 'lead', 'principal', 'architect', 'manager', 'director', 'head of']
            leadership_matches = len([keyword for keyword in leadership_keywords if keyword in resume_text])
            quality_bonus += leadership_matches * 8
            
            # Technical depth indicators
            technical_keywords = ['project', 'development', 'implementation', 'design', 'architecture', 'system']
            technical_matches = len([keyword for keyword in technical_keywords if keyword in resume_text])
            quality_bonus += min(technical_matches * 3, 15)
            
            # Team and collaboration indicators
            team_keywords = ['team', 'collaboration', 'mentor', 'coach', 'cross-functional']
            team_matches = len([keyword for keyword in team_keywords if keyword in resume_text])
            quality_bonus += team_matches * 4
            
            # Industry and domain expertise
            domain_keywords = ['enterprise', 'scalable', 'performance', 'optimization', 'security', 'compliance']
            domain_matches = len([keyword for keyword in domain_keywords if keyword in resume_text])
            quality_bonus += domain_matches * 3
            
            # Experience progression bonus
            if experience_years >= 5:
                quality_bonus += 10  # Senior level bonus
            if experience_years >= 8:
                quality_bonus += 5   # Expert level bonus
            
            experience_score = min(base_score + quality_bonus, 100)
        
        # 3. ENHANCED DOMAIN RELEVANCE (0-100 points) - More comprehensive domain analysis
        role_lower = actual_role.lower()
        domain_score = 0
        
        # Role-based scoring with more granular categories
        if any(role in role_lower for role in ['developer', 'engineer', 'programmer']):
            domain_score += 35  # Base score for developer roles
            if 'full stack' in role_lower or 'fullstack' in role_lower:
                domain_score += 10  # Full stack bonus
            elif 'frontend' in role_lower or 'front-end' in role_lower:
                domain_score += 8   # Frontend specialization
            elif 'backend' in role_lower or 'back-end' in role_lower:
                domain_score += 8   # Backend specialization
        elif any(role in role_lower for role in ['analyst', 'consultant', 'specialist']):
            domain_score += 30
        elif any(role in role_lower for role in ['manager', 'lead', 'director', 'head']):
            domain_score += 25
        elif any(role in role_lower for role in ['architect', 'principal', 'senior']):
            domain_score += 40  # High-level technical roles
        else:
            domain_score += 20  # Base score for other roles
        
        # Technology domain bonuses based on actual skills (more comprehensive)
        domain_bonuses = 0
        
        # Programming language domains
        if any('java' in skill.lower() for skill in skills_list):
            domain_bonuses += 12  # Java domain
        if any('python' in skill.lower() for skill in skills_list):
            domain_bonuses += 10  # Python domain
        if any('javascript' in skill.lower() for skill in skills_list):
            domain_bonuses += 10  # Web development
        if any('c#' in skill.lower() or 'csharp' in skill.lower() for skill in skills_list):
            domain_bonuses += 8   # .NET domain
        if any('php' in skill.lower() for skill in skills_list):
            domain_bonuses += 6   # PHP domain
        
        # Framework and technology domains
        if any('spring' in skill.lower() for skill in skills_list):
            domain_bonuses += 8   # Spring framework
        if any('react' in skill.lower() for skill in skills_list):
            domain_bonuses += 8   # React ecosystem
        if any('angular' in skill.lower() for skill in skills_list):
            domain_bonuses += 8   # Angular ecosystem
        if any('node' in skill.lower() for skill in skills_list):
            domain_bonuses += 8   # Node.js ecosystem
        
        # Database and data domains
        if any('sql' in skill.lower() or 'mysql' in skill.lower() or 'oracle' in skill.lower() for skill in skills_list):
            domain_bonuses += 8   # Relational database skills
        if any('mongodb' in skill.lower() or 'nosql' in skill.lower() for skill in skills_list):
            domain_bonuses += 6   # NoSQL database skills
        if any('data' in skill.lower() for skill in skills_list):
            domain_bonuses += 5   # Data domain
        
        # Cloud and DevOps domains
        if any('aws' in skill.lower() for skill in skills_list):
            domain_bonuses += 10  # AWS cloud
        if any('azure' in skill.lower() for skill in skills_list):
            domain_bonuses += 8   # Azure cloud
        if any('docker' in skill.lower() for skill in skills_list):
            domain_bonuses += 6   # Containerization
        if any('kubernetes' in skill.lower() for skill in skills_list):
            domain_bonuses += 8   # Orchestration
        if any('devops' in skill.lower() for skill in skills_list):
            domain_bonuses += 6   # DevOps practices
        
        # Mobile and emerging domains
        if any('mobile' in skill.lower() or 'android' in skill.lower() or 'ios' in skill.lower() for skill in skills_list):
            domain_bonuses += 8   # Mobile development
        if any('machine learning' in skill.lower() or 'ml' in skill.lower() or 'ai' in skill.lower() for skill in skills_list):
            domain_bonuses += 10  # AI/ML domain
        if any('blockchain' in skill.lower() for skill in skills_list):
            domain_bonuses += 6   # Blockchain domain
        
        domain_score += min(domain_bonuses, 40)  # Cap domain bonuses at 40 points
        domain_score = min(domain_score, 100)
        
        # 4. ENHANCED ROLE ALIGNMENT (0-100 points) - More sophisticated role analysis
        role_score = 0
        
        # Role specificity scoring
        if actual_role and actual_role.strip():
            role_score += 40  # Base score for having a role
            
            # Role level scoring with more granular categories
            if any(level in role_lower for level in ['senior', 'lead', 'principal', 'architect']):
                role_score += 25  # Senior/Lead level
            elif any(level in role_lower for level in ['junior', 'associate', 'entry', 'trainee']):
                role_score += 15  # Junior level
            elif any(level in role_lower for level in ['mid', 'intermediate']):
                role_score += 20  # Mid level
            else:
                role_score += 18  # Default level
            
            # Role type scoring with more categories
            if 'full stack' in role_lower or 'fullstack' in role_lower:
                role_score += 20  # Full stack bonus
            elif 'frontend' in role_lower or 'front-end' in role_lower:
                role_score += 15  # Frontend specialization
            elif 'backend' in role_lower or 'back-end' in role_lower:
                role_score += 15  # Backend specialization
            elif 'devops' in role_lower or 'cloud' in role_lower:
                role_score += 18  # DevOps/Cloud bonus
            elif 'data' in role_lower or 'analyst' in role_lower:
                role_score += 12  # Data roles
            elif 'mobile' in role_lower:
                role_score += 12  # Mobile development
            elif 'security' in role_lower:
                role_score += 15  # Security specialization
            
            # Role clarity bonus - well-defined roles get higher scores
            if len(actual_role.split()) >= 2:  # Multi-word roles are usually more specific
                role_score += 5
            
            # Role consistency with skills
            role_skill_alignment = 0
            if 'java' in role_lower and any('java' in skill.lower() for skill in skills_list):
                role_skill_alignment += 5
            if 'python' in role_lower and any('python' in skill.lower() for skill in skills_list):
                role_skill_alignment += 5
            if 'javascript' in role_lower and any('javascript' in skill.lower() for skill in skills_list):
                role_skill_alignment += 5
            if 'react' in role_lower and any('react' in skill.lower() for skill in skills_list):
                role_skill_alignment += 5
            
            role_score += min(role_skill_alignment, 10)
        else:
            role_score = 15  # Low score for no role specified
        
        role_score = min(role_score, 100)
        
        # 5. ENHANCED EDUCATION & CERTIFICATIONS (0-100 points) - More comprehensive education analysis
        education_data = resume_data.get('education', [])
        education_score = 0
        
        if education_data and len(education_data) > 0:
            education_score += 30  # Base score for having education
            
            # Check for degree levels with more granular scoring
            highest_degree_score = 0
            for edu in education_data:
                degree = edu.get('degree', '').lower()
                institution = edu.get('institution', '').lower()
                
                # Degree level scoring
                if any(level in degree for level in ['phd', 'doctorate', 'ph.d']):
                    degree_score = 40  # PhD
                elif any(level in degree for level in ['master', 'mtech', 'ms', 'mca', 'mba', 'm.sc', 'm.com']):
                    degree_score = 30  # Master's degree
                elif any(level in degree for level in ['bachelor', 'btech', 'be', 'bsc', 'ba', 'bca', 'b.com', 'bsc']):
                    degree_score = 25  # Bachelor's degree
                elif any(level in degree for level in ['diploma', 'certificate', 'pgdm']):
                    degree_score = 20  # Diploma/Certificate
        else:
            degree_score = 15  # Other education
            # Check for certifications in resume text if no formal education
            cert_keywords = ['certified', 'certification', 'certificate', 'aws', 'azure', 'google', 'microsoft', 'oracle']
            cert_matches = len([keyword for keyword in cert_keywords if keyword in resume_text])
            education_score = 10 + (cert_matches * 3)  # Minimal score + certification bonus
        
        # Institution quality bonus
        institution_bonus = 0
        if any(inst in institution for inst in ['iit', 'iim', 'nit', 'bits', 'vit', 'srm']):
            institution_bonus = 10  # Top tier institutions
        elif any(inst in institution for inst in ['university', 'college', 'institute']):
            institution_bonus = 5   # Recognized institutions
        
        # Technical field bonus
        field_bonus = 0
        if any(field in degree for field in ['computer', 'engineering', 'technology', 'science', 'mathematics']):
            field_bonus = 8  # Technical field
        elif any(field in degree for field in ['business', 'management', 'commerce']):
            field_bonus = 5  # Business field
        
        total_edu_score = degree_score + institution_bonus + field_bonus
        highest_degree_score = max(highest_degree_score, total_edu_score)
        
        education_score += highest_degree_score
        
        # Multiple degrees bonus
        if len(education_data) > 1:
            education_score += 5  # Multiple degrees show continuous learning
        
        # Recent education bonus (if graduation year is recent)
        for edu in education_data:
            if 'year' in edu or 'graduation' in edu:
                education_score += 3  # Recent education
                break
        
        education_score = min(education_score, 100)
        
        # 6. PROJECTS & ACHIEVEMENTS (0-100 points) - New factor for comprehensive assessment
        projects_score = 0
        
        # Project indicators in resume text
        project_keywords = ['project', 'portfolio', 'github', 'git', 'repository', 'developed', 'built', 'created', 'implemented']
        project_matches = len([keyword for keyword in project_keywords if keyword in resume_text])
        
        if project_matches > 0:
            projects_score += 30  # Base score for having project indicators
            
            # Project complexity indicators
            complexity_keywords = ['full stack', 'microservices', 'api', 'database', 'frontend', 'backend', 'mobile app', 'web application']
            complexity_matches = len([keyword for keyword in complexity_keywords if keyword in resume_text])
            projects_score += complexity_matches * 5
            
            # Technology stack indicators in projects
            tech_stack_keywords = ['react', 'angular', 'node', 'spring', 'django', 'flask', 'mysql', 'mongodb', 'aws', 'docker']
            tech_matches = len([keyword for keyword in tech_stack_keywords if keyword in resume_text])
            projects_score += tech_matches * 3
            
            # Achievement indicators
            achievement_keywords = ['achieved', 'improved', 'optimized', 'increased', 'reduced', 'solved', 'delivered', 'completed']
            achievement_matches = len([keyword for keyword in achievement_keywords if keyword in resume_text])
            projects_score += achievement_matches * 4
            
            # Open source and community involvement
            community_keywords = ['open source', 'contributed', 'collaborated', 'team', 'mentor', 'volunteer']
            community_matches = len([keyword for keyword in community_keywords if keyword in resume_text])
            projects_score += community_matches * 3
        
        projects_score = min(projects_score, 100)
        
        # 7. COMMUNICATION & PROFESSIONALISM (0-100 points) - New factor for soft skills
        communication_score = 0
        
        # Resume completeness and professionalism
        completeness_indicators = ['email', 'phone', 'linkedin', 'address', 'objective', 'summary']
        completeness_matches = len([indicator for indicator in completeness_indicators if indicator in resume_text])
        communication_score += completeness_matches * 8
        
        # Professional language and formatting
        professional_keywords = ['professional', 'experienced', 'skilled', 'proficient', 'expert', 'certified']
        professional_matches = len([keyword for keyword in professional_keywords if keyword in resume_text])
        communication_score += professional_matches * 5
        
        # Communication skills indicators
        comm_keywords = ['communication', 'presentation', 'documentation', 'reporting', 'client', 'stakeholder']
        comm_matches = len([keyword for keyword in comm_keywords if keyword in resume_text])
        communication_score += comm_matches * 6
        
        # Leadership and management indicators
        leadership_keywords = ['led', 'managed', 'coordinated', 'supervised', 'mentored', 'trained']
        leadership_matches = len([keyword for keyword in leadership_keywords if keyword in resume_text])
        communication_score += leadership_matches * 7
        
        communication_score = min(communication_score, 100)
        
        # Calculate ENHANCED FINAL SCORE with new factors
        # Updated weights: Skills (25%), Experience (20%), Domain (18%), Role (12%), Education (10%), Projects (10%), Communication (5%)
        total_score = (
            (skills_score * 0.25) +
            (experience_score * 0.20) +
            (domain_score * 0.18) +
            (role_score * 0.12) +
            (education_score * 0.10) +
            (projects_score * 0.10) +
            (communication_score * 0.05)
        )
        
        # Convert to 0-1 scale
        final_score = total_score / 100
        
        # Add bonus for exceptional candidates (score > 85%)
        if final_score > 0.85:
            final_score = min(final_score + 0.05, 1.0)  # 5% bonus for exceptional candidates
        
        # Log detailed scoring for debugging
        logger.info(f"🔍 Enhanced AI Scoring Details:")
        logger.info(f"   Skills: {skills_score}/100 (25% weight)")
        logger.info(f"   Experience: {experience_score}/100 (20% weight)")
        logger.info(f"   Domain: {domain_score}/100 (18% weight)")
        logger.info(f"   Role: {role_score}/100 (12% weight)")
        logger.info(f"   Education: {education_score}/100 (10% weight)")
        logger.info(f"   Projects: {projects_score}/100 (10% weight)")
        logger.info(f"   Communication: {communication_score}/100 (5% weight)")
        logger.info(f"   Total: {total_score:.1f}/100, Final: {final_score:.3f}")
        
        return final_score
        
    except Exception as e:
        logger.error(f"Error calculating enhanced score: {e}")
        return 0.8  # Default fallback score

def generate_ai_suggestion(resume_score: float) -> dict:
    """Generate AI suggestion based on resume score"""
    try:
        if resume_score >= 0.8:
            suggestion = "accept"
            confidence = "high"
            reason = "Excellent candidate with strong skills and experience match"
            color = "green"
        elif resume_score >= 0.6:
            suggestion = "under_review"
            confidence = "medium"
            reason = "Good candidate, worth reviewing in detail"
            color = "yellow"
        elif resume_score >= 0.4:
            suggestion = "under_review"
            confidence = "low"
            reason = "Moderate match, consider for specific roles"
            color = "orange"
        else:
            suggestion = "reject"
            confidence = "high"
            reason = "Poor match with job requirements"
            color = "red"
        
        return {
            "suggestion": suggestion,
            "confidence": confidence,
            "reason": reason,
            "color": color,
            "score": resume_score
        }
    except Exception as e:
        logger.error(f"Error generating AI suggestion: {e}")
        return {
            "suggestion": "under_review",
            "confidence": "low",
            "reason": "Unable to analyze, manual review recommended",
            "color": "gray",
            "score": resume_score
        }

def calculate_resume_job_match_score(user_email: str, job_id: int) -> float:
    """Calculate resume-job match score based on skills and role compatibility"""
    try:
        # Get resume data
        if user_email not in resumes_db:
            return 0.0
        
        resume_data = resumes_db[user_email]
        resume_skills = resume_data.get('skills', [])
        resume_role = resume_data.get('role', '').lower()
        resume_experience = resume_data.get('experience', {})
        experience_years = resume_experience.get('total_years', 0) if isinstance(resume_experience, dict) else 0
        
        # Get job data
        job_key = str(job_id)
        if job_key not in jobs_db:
            return 0.0
        
        job_data = jobs_db[job_key]
        job_title = job_data.get('title', '').lower()
        job_description = job_data.get('description', '').lower()
        job_requirements = job_data.get('requirements', '').lower()
        
        # Combine job text for analysis
        job_text = f"{job_title} {job_description} {job_requirements}"
        
        # 1. SKILLS MATCHING (40% weight)
        skills_score = 0.0
        if resume_skills:
            # Extract required skills from job description
            required_skills = []
            common_tech_skills = [
                'java', 'python', 'javascript', 'html', 'css', 'sql', 'mysql', 'oracle',
                'spring', 'spring boot', 'react', 'angular', 'node', 'express', 'django',
                'flask', 'git', 'docker', 'kubernetes', 'aws', 'azure', 'gcp',
                'linux', 'windows', 'networking', 'cisco', 'ccna', 'ccnp',
                'firewall', 'vpn', 'lan', 'wan', 'wireless', 'security'
            ]
            
            for skill in common_tech_skills:
                if skill in job_text:
                    required_skills.append(skill)
            
            # Calculate skills match
            if required_skills:
                matched_skills = []
                for req_skill in required_skills:
                    for resume_skill in resume_skills:
                        if req_skill in resume_skill.lower() or resume_skill.lower() in req_skill:
                            matched_skills.append(req_skill)
                            break
                
                skills_score = len(matched_skills) / len(required_skills)
            else:
                # If no specific skills mentioned, give base score for having skills
                skills_score = min(len(resume_skills) / 10, 1.0)  # Max 1.0 for 10+ skills
        
        # 2. ROLE MATCHING (30% weight)
        role_score = 0.0
        if resume_role and job_title:
            # Direct role match
            if resume_role in job_title or job_title in resume_role:
                role_score = 1.0
            else:
                # Partial role match
                role_keywords = ['engineer', 'developer', 'analyst', 'manager', 'admin', 'specialist']
                resume_role_words = resume_role.split()
                job_title_words = job_title.split()
                
                common_words = set(resume_role_words) & set(job_title_words) & set(role_keywords)
                if common_words:
                    role_score = len(common_words) / max(len(resume_role_words), len(job_title_words))
                else:
                    # Check for similar roles
                    if any(word in job_title for word in ['engineer', 'developer']) and any(word in resume_role for word in ['engineer', 'developer']):
                        role_score = 0.7
                    elif any(word in job_title for word in ['analyst', 'specialist']) and any(word in resume_role for word in ['analyst', 'specialist']):
                        role_score = 0.7
                    else:
                        role_score = 0.3  # Base score for any role
        
        # 3. EXPERIENCE MATCHING (20% weight)
        experience_score = 0.0
        if 'experience' in job_text or 'years' in job_text:
            # Extract required experience from job text
            import re
            exp_matches = re.findall(r'(\d+)[\s-]*(\d+)?\s*years?', job_text)
            if exp_matches:
                # Get the first experience requirement
                exp_range = exp_matches[0]
                if len(exp_range) == 2 and exp_range[1]:
                    min_exp = int(exp_range[0])
                    max_exp = int(exp_range[1])
                    if min_exp <= experience_years <= max_exp:
                        experience_score = 1.0
                    elif experience_years < min_exp:
                        experience_score = experience_years / min_exp
                    else:
                        experience_score = 0.8  # Overqualified but still good
                else:
                    required_exp = int(exp_range[0])
                    if experience_years >= required_exp:
                        experience_score = 1.0
                    else:
                        experience_score = experience_years / required_exp
            else:
                # No specific experience mentioned, give base score
                experience_score = 0.6
        else:
            # No experience requirement mentioned
            experience_score = 0.8
        
        # 4. EDUCATION MATCHING (10% weight)
        education_score = 0.0
        resume_education = resume_data.get('education', [])
        if resume_education:
            education_score = 0.8  # Base score for having education
            for edu in resume_education:
                degree = edu.get('degree', '').lower()
                if any(level in degree for level in ['bachelor', 'master', 'btech', 'mtech', 'be', 'me']):
                    education_score = 1.0
                    break
        else:
            education_score = 0.3
        
        # Calculate final weighted score
        final_score = (
            (skills_score * 0.40) +
            (role_score * 0.30) +
            (experience_score * 0.20) +
            (education_score * 0.10)
        )
        
        logger.info(f"🔍 Resume-Job Match Score for {user_email} -> Job {job_id}: "
                   f"Skills: {skills_score:.2f}, Role: {role_score:.2f}, "
                   f"Experience: {experience_score:.2f}, Education: {education_score:.2f}, "
                   f"Final: {final_score:.3f}")
        
        return round(final_score, 3)
        
    except Exception as e:
        logger.error(f"Error calculating resume-job match score: {e}")
        return 0.0

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
    
    # Save to persistent storage
    save_persistent_data()
    
    return {"message": "Job created successfully", "job_id": job_id}

@app.post("/api/apply/{job_id}")
async def apply_job(job_id: int, email: str = Depends(verify_token)):
    logger.info(f"Apply job request - Job ID: {job_id} (type: {type(job_id)}), Email: {email}")
    logger.info(f"Available jobs: {list(jobs_db.keys())}")
    
    # Convert job_id to string to match jobs_db keys
    job_key = str(job_id)
    if job_key not in jobs_db:
        logger.error(f"Job {job_id} not found in jobs_db. Available jobs: {list(jobs_db.keys())}")
        raise HTTPException(status_code=404, detail="Job not found")
    
    # Check if user already applied for this job
    for app_id, app_data in applications_db.items():
        if app_data.get('job_id') == job_id and app_data.get('user_email') == email:
            raise HTTPException(status_code=400, detail="You have already applied for this job")
    
    application_id = len(applications_db) + 1
    applications_db[application_id] = {
        'id': application_id,
        'job_id': job_id,
        'user_email': email,
        'status': 'applied',
        'applied_date': datetime.now().strftime('%Y-%m-%d')
    }
    
    # Save to persistent storage
    save_persistent_data()
    
    # Send email notification
    try:
        await send_application_notification(email, job_id)
    except Exception as e:
        logger.warning(f"Failed to send email notification: {e}")
    
    return {"message": "Application submitted successfully"}

@app.get("/api/user-applications")
async def get_user_applications(email: str = Depends(verify_token)):
    """Get applications for the current user"""
    try:
        user_applications = []
        for app_id, app_data in applications_db.items():
            if app_data.get('user_email') == email:
                # Convert job_id to string to match jobs_db keys
                job_key = str(app_data.get('job_id'))
                job_data = jobs_db.get(job_key, {})
                user_applications.append({
                    "id": app_id,
                    "job_id": app_data.get('job_id'),
                    "job_title": job_data.get('title', 'Unknown Job'),
                    "job_company": job_data.get('company', 'Unknown Company'),
                    "job_location": job_data.get('location', 'Unknown Location'),
                    "status": app_data.get('status', 'under_review') if app_data.get('status', 'under_review') != 'applied' else 'under_review',
                    "applied_date": app_data.get('applied_date'),
                    "updated_date": app_data.get('updated_date')
                })
        
        return {"applications": user_applications, "total": len(user_applications)}
    except Exception as e:
        logger.error(f"Error getting user applications: {e}")
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

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
    
    # Extract resume content using text extraction
    try:
        # Read file content
        async with aiofiles.open(file_path, 'rb') as f:
            file_content = await f.read()
        
        # Extract resume data using the accurate name and role extractor
        try:
            # Read the file content for text extraction
            with open(file_path, 'rb') as f:
                file_content = f.read()
            
            # Extract text from file
            if file_path.lower().endswith('.pdf'):
                import PyPDF2
                import io
                pdf_reader = PyPDF2.PdfReader(io.BytesIO(file_content))
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
            else:
                text = file_content.decode('utf-8', errors='ignore')
            
            # Use reliable extractor for guaranteed accuracy
            try:
                extracted_data = reliable_extractor.extract_resume_data(text, file.filename)
                logger.info("✅ Using reliable extraction results")
            except Exception as e:
                logger.error(f"❌ Error in reliable extraction: {e}")
                # If reliable extractor fails, return empty result
                logger.error("❌ Reliable extractor failed, returning empty result")
                extracted_data = {
                    'name': 'Name not found',
                    'email': 'Email not found',
                    'phone': 'Phone not found',
                    'skills': [],
                    'experience': {'total_years': 0, 'total_months': 0, 'display': 'Experience not found'},
                    'role': 'Role not found',
                    'location': 'Location not found',
                    'education': [],
                    'raw_text': '',
                    'extraction_method': 'reliable_extraction_failed',
                    'confidence_score': 0.0,
                    'extraction_timestamp': datetime.now().isoformat()
                }
            
            # Add additional fields that might be needed by the system
            if 'skills' not in extracted_data:
                extracted_data['skills'] = []
            if 'experience' not in extracted_data:
                extracted_data['experience'] = {'total_years': 0, 'total_months': 0, 'display': 'Experience not found'}
            if 'location' not in extracted_data:
                extracted_data['location'] = 'Location not found'
            if 'education' not in extracted_data:
                extracted_data['education'] = []
            
            logger.info("✅ Using accurate name and role extraction results")
            
        except Exception as e:
            logger.error(f"❌ Error in accurate extraction: {e}")
            # Fallback to deep text analyzer
            extracted_data = deep_text_analyzer.extract_resume_data_from_file(file_path)
            
            # If extraction failed, try filename-based extractor as final fallback
            if extracted_data.get('name') == 'Name not found' or extracted_data.get('confidence_score', 0) < 0.5:
                logger.info("🔄 Primary extraction failed, trying filename-based extractor...")
                filename_data = filename_based_extractor.extract_resume_data_from_file(file_path)
                
                # Use filename-based data if it's better
                if filename_data.get('name') != 'Name not found':
                    extracted_data = filename_data
                    logger.info("✅ Using filename-based extraction results")
        
        # Debug: Log extracted data
        logger.info(f"🔍 Extracted resume data: {extracted_data}")
        logger.info(f"🔍 Experience data: {extracted_data.get('experience', 'NOT_FOUND')}")
        logger.info(f"🔍 Skills data: {extracted_data.get('skills', 'NOT_FOUND')}")
        logger.info(f"🔍 Role data: {extracted_data.get('role', 'NOT_FOUND')}")
        
        if not extracted_data:
            logger.warning("⚠️ Failed to extract resume data from uploaded file")
            extracted_data = {
                'name': 'Extraction failed',
                'email': 'Extraction failed',
                'phone': 'Extraction failed',
                'skills': [],
                'experience': {'total_years': 0, 'total_months': 0, 'display': 'Extraction failed'},
                'role': 'Extraction failed',
                'location': 'Extraction failed',
                'education': [],
                'raw_text': '',
                'extraction_method': 'extraction_failed',
                'confidence_score': 0.0,
                'extraction_timestamp': datetime.now().isoformat()
            }
    except Exception as e:
        logger.error(f"❌ Error extracting text from file: {e}")
        extracted_data = {
            'name': 'Text extraction error',
            'email': 'Text extraction error',
            'phone': 'Text extraction error',
            'skills': [],
            'experience': {'total_years': 0, 'total_months': 0, 'display': 'Text extraction error'},
            'role': 'Text extraction error',
            'location': 'Text extraction error',
            'education': [],
            'raw_text': '',
            'extraction_method': 'text_extraction_error',
            'confidence_score': 0.0,
            'extraction_timestamp': datetime.now().isoformat()
        }
    
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
            'role': extracted_data.get('role', existing_profile.get('role')),
            'location': extracted_data.get('location', existing_profile.get('location')),
            'education': extracted_data.get('education', existing_profile.get('education', [])),
            'extraction_method': extracted_data.get('extraction_method', 'unknown'),
            'confidence_score': extracted_data.get('confidence_score', 0.0),
            'extraction_timestamp': extracted_data.get('extraction_timestamp', datetime.now().isoformat())
        })
        
        # Store in in-memory databases
        users_db[email] = existing_profile
        resumes_db[email] = extracted_data
        
        # Save to persistent storage
        save_persistent_data()
        
        return {
            "message": "Resume uploaded successfully",
            "extracted_data": extracted_data
        }
        
    except Exception as e:
        logger.error(f"Error processing resume: {e}")
        return {"message": f"Resume uploaded but processing failed: {str(e)}"}

@app.post("/api/clear-cache")
async def clear_cache(email: str = Depends(verify_token)):
    """Clear cached extraction data and force fresh extraction"""
    try:
        logger.info(f"🧹 Clearing cache for user: {email}")
        
        # Clear cached data for this user
        if email in resumes_db:
            del resumes_db[email]
            logger.info(f"🧹 Cleared resume data for {email}")
        
        if email in users_db:
            user_data = users_db[email]
            # Keep only essential login data
            users_db[email] = {
                'email': user_data.get('email', email),
                'password': user_data.get('password', ''),
                'role': user_data.get('role', 'user')
            }
            logger.info(f"🧹 Cleared profile data for {email}")
        
        # Save cleared data
        save_persistent_data()
        
        return {"message": "Cache cleared successfully", "status": "success"}
        
    except Exception as e:
        logger.error(f"❌ Error clearing cache: {e}")
        return {"message": f"Error clearing cache: {str(e)}", "status": "error"}

@app.get("/api/user-resume")
async def get_user_resume(email: str = Depends(verify_token)):
    """Get user's saved resume data"""
    try:
        # Check if user has a resume in in-memory storage
        if email not in resumes_db:
            # Check if resume file exists in uploads directory
            resume_files = glob.glob(f"uploads/{email}_*.pdf")
            if resume_files:
                # Resume file exists but not in database - extract it
                try:
                    file_path = resume_files[0]  # Get the most recent file
                    extracted_data = reliable_extractor.extract_resume_data_from_file(file_path)
                    
                    if extracted_data:
                        # Store in databases
                        resumes_db[email] = extracted_data
                        
                        # Update user profile
                        existing_profile = users_db.get(email, {})
                        existing_profile.update({
                            'resume_file_path': file_path,
                            'resume_filename': os.path.basename(file_path),
                            'role': extracted_data.get('role', 'User'),
                            'skills': extracted_data.get('skills', []),
                            'experience': extracted_data.get('experience', {}),
                            'location': extracted_data.get('location', ''),
                            'education': extracted_data.get('education', [])
                        })
                        users_db[email] = existing_profile
                        
                        # Save to persistent storage
                        save_persistent_data()
                        
                        return {
                            "has_resume": True,
                            "resume_data": extracted_data,
                            "role": extracted_data.get('role', 'User'),
                            "user_profile": {
                                "name": existing_profile.get('name', 'Unknown'),
                                "email": existing_profile.get('email', 'Unknown'),
                                "resume_filename": os.path.basename(file_path),
                                "resume_upload_date": int(os.path.getmtime(file_path))
                            }
                        }
                except Exception as e:
                    logger.error(f"Error extracting resume from file: {e}")
            
            return {"message": "No resume uploaded yet", "has_resume": False}
        
        resume_data = resumes_db[email]
        user_profile = users_db.get(email, {})
        
        return {
            "has_resume": True,
            "resume_data": resume_data,
            "role": user_profile.get('role', resume_data.get('role', 'User')),  # Priority: user_db role > resume_data role > default
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
        # Check if user has a resume
        if email not in resumes_db:
            return {"message": "No resume found to remove", "success": False}
        
        # Get file path before removing from database
        resume_data = resumes_db[email]
        file_path = resume_data.get('resume_file_path')
        
        # Remove from in-memory storage
        del resumes_db[email]
        
        # Delete the physical file
        if file_path and os.path.exists(file_path):
            try:
                os.remove(file_path)
                logger.info(f"✅ Deleted resume file: {file_path}")
            except OSError as e:
                logger.error(f"❌ Error deleting resume file {file_path}: {e}")
        
        # Also check for any files with user email pattern
        user_files = glob.glob(f"uploads/{email}_*.pdf")
        for file in user_files:
            try:
                os.remove(file)
                logger.info(f"✅ Deleted additional resume file: {file}")
            except OSError as e:
                logger.error(f"❌ Error deleting additional resume file {file}: {e}")
        
        # Update user profile - clear all resume-related data
        if email in users_db:
            users_db[email].update({
                'resume_file_path': None,
                'resume_filename': None,
                'resume_upload_date': None,
                'role': 'User',  # Reset role to default when resume is removed
                'skills': [],  # Clear extracted skills
                'experience': {
                    'total_years': 0,
                    'total_months': 0,
                    'display': '0 years',
                    'extraction_method': 'none'
                },
                'location': '',  # Clear extracted location
                'education': [],  # Clear extracted education
                'extraction_method': 'none',
                'confidence_score': 0.0,
                'extraction_timestamp': ''
            })
        
        # Save to persistent storage
        save_persistent_data()
        
        return {"message": "Resume removed successfully", "success": True}
        
    except Exception as e:
        logger.error(f"Error removing resume: {e}")
        return {"message": f"Error removing resume: {str(e)}", "success": False}

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

# Admin endpoints
@app.get("/api/admin/dashboard-stats")
async def get_admin_dashboard_stats(email: str = Depends(verify_token)):
    """Get admin dashboard statistics"""
    try:
        # Check if user is admin
        user = users_db.get(email, {})
        if user.get('role') != 'admin':
            raise HTTPException(status_code=403, detail="Admin access required")
        
        # Calculate statistics
        total_users = len(users_db)
        total_jobs = len(jobs_db)
        total_applications = len(applications_db)
        total_resumes = len(resumes_db)
        
        # Job statistics
        active_jobs = len([job for job in jobs_db.values() if job.get('status', 'active') == 'active'])
        
        # Application statistics
        application_status_breakdown = {
            'under_review': 0,
            'accepted': 0,
            'rejected': 0
        }
        
        for app in applications_db.values():
            status = app.get('status', 'under_review')
            # Convert 'applied' status to 'under_review' for display
            if status == 'applied':
                status = 'under_review'
            if status in application_status_breakdown:
                application_status_breakdown[status] += 1
        
        # User role distribution
        user_role_distribution = {
            'candidates': 0,
            'admins': 0
        }
        
        users_with_resumes = 0
        for user in users_db.values():
            role = user.get('role', 'candidate')
            if role == 'admin':
                user_role_distribution['admins'] += 1
            else:
                user_role_distribution['candidates'] += 1
            
            if user.get('has_resume', False):
                users_with_resumes += 1
        
        return {
            "total_users": total_users,
            "total_jobs": total_jobs,
            "total_applications": total_applications,
            "total_resumes": total_resumes,
            "active_jobs": active_jobs,
            "applications_by_status": application_status_breakdown,
            "user_role_distribution": user_role_distribution,
            "users_with_resumes": users_with_resumes
        }
        
    except Exception as e:
        logger.error(f"Error getting admin dashboard stats: {e}")
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@app.get("/api/admin/users")
async def get_all_users(
    search: str = None,
    experience_min: int = None,
    experience_max: int = None,
    skills: str = None,
    domain: str = None,
    job_role: str = None,
    email: str = Depends(verify_token)
):
    """Get all users for admin with search and filtering"""
    try:
        # Check if user is admin
        user = users_db.get(email, {})
        if user.get('role') != 'admin':
            raise HTTPException(status_code=403, detail="Admin access required")
        
        # Return user list without passwords
        users_list = []
        for user_email, user_data in users_db.items():
            # Check if user has resume file
            has_resume = user_email in resumes_db or user_data.get('resume_file_path')
            resume_filename = user_data.get('resume_filename')
            
            # Find the actual resume file if it exists
            if has_resume and user_data.get('resume_file_path'):
                # Extract filename from the stored path
                resume_filename = os.path.basename(user_data.get('resume_file_path'))
            
            # Get resume data for filtering
            resume_data = resumes_db.get(user_email, {})
            user_skills = resume_data.get('skills', [])
            user_experience = resume_data.get('experience', {})
            user_role = resume_data.get('role', '')
            user_domain = resume_data.get('domain', '')
            
            # Get comprehensive resume text for searching
            resume_text = resume_data.get('text', '') or resume_data.get('raw_text', '') or resume_data.get('content', '')
            if not resume_text and user_data.get('resume_file_path'):
                # Try to read resume file if text not available
                try:
                    import PyPDF2
                    with open(user_data['resume_file_path'], 'rb') as file:
                        pdf_reader = PyPDF2.PdfReader(file)
                        resume_text = ""
                        for page in pdf_reader.pages:
                            resume_text += page.extract_text()
                    # Store the extracted text for future use
                    if user_email in resumes_db:
                        resumes_db[user_email]['text'] = resume_text
                    logger.info(f"✅ Extracted {len(resume_text)} characters from resume for {user_email}")
                except Exception as e:
                    logger.warning(f"Could not read resume file for {user_email}: {e}")
                    resume_text = ""
            
            # Extract experience years
            experience_years = 0
            if isinstance(user_experience, dict):
                experience_years = user_experience.get('total_years', 0)
            elif isinstance(user_experience, (int, float)):
                experience_years = user_experience
            
            # Apply filters
            include_user = True
            
            # Search filter - improved to better handle skills with debugging
            if search:
                search_lower = search.lower()
                search_found = False
                
                logger.info(f"🔍 General search - Searching for: '{search_lower}' in user {user_email}")
                logger.info(f"🔍 User skills: {user_skills}")
                
                # Check name
                if search_lower in user_data.get('name', '').lower():
                    search_found = True
                    logger.info(f"✅ Search match in name: {user_data.get('name', '')}")
                
                # Check email
                if not search_found and search_lower in user_email.lower():
                    search_found = True
                    logger.info(f"✅ Search match in email: {user_email}")
                
                # Check role
                if not search_found and search_lower in user_role.lower():
                    search_found = True
                    logger.info(f"✅ Search match in role: {user_role}")
                
                # Check skills with better matching
                if not search_found:
                    for skill in user_skills:
                        if isinstance(skill, str):
                            if (search_lower == skill.lower() or 
                                search_lower in skill.lower() or 
                                skill.lower() in search_lower):
                                search_found = True
                                logger.info(f"✅ Search match in skill: '{search_lower}' matches '{skill}'")
                                break
                
                # Check location
                if not search_found and search_lower in resume_data.get('location', '').lower():
                    search_found = True
                    logger.info(f"✅ Search match in location: {resume_data.get('location', '')}")
                
                # Check resume content - COMPREHENSIVE SEARCH
                if not search_found and resume_text:
                    if search_lower in resume_text.lower():
                        search_found = True
                        logger.info(f"✅ Search match in resume content: '{search_lower}' found in resume text")
                
                if not search_found:
                    logger.info(f"❌ No search match for user {user_email}")
                    include_user = False
            
            # Experience filter
            if experience_min is not None and experience_years < experience_min:
                include_user = False
            if experience_max is not None and experience_years > experience_max:
                include_user = False
            
            # Skills filter - improved logic with debugging
            if skills:
                skills_list = [s.strip().lower() for s in skills.split(',')]
                skills_found = False
                
                logger.info(f"🔍 Skills filter - Searching for: {skills_list}")
                logger.info(f"🔍 User {user_email} skills: {user_skills}")
                
                # Check if any of the searched skills match any user skills
                for searched_skill in skills_list:
                    for user_skill in user_skills:
                        if isinstance(user_skill, str):
                            # Check for exact match or partial match
                            if (searched_skill == user_skill.lower() or 
                                searched_skill in user_skill.lower() or 
                                user_skill.lower() in searched_skill):
                                skills_found = True
                                logger.info(f"✅ Skills match found: '{searched_skill}' matches '{user_skill}'")
                                break
                    if skills_found:
                        break
                
                # If no match in extracted skills, search in resume content
                if not skills_found and resume_text:
                    for searched_skill in skills_list:
                        if searched_skill in resume_text.lower():
                            skills_found = True
                            logger.info(f"✅ Skills match found in resume content: '{searched_skill}' found in resume text")
                            break
                
                if not skills_found:
                    logger.info(f"❌ No skills match for user {user_email}")
                    include_user = False
            
            # Domain filter - includes resume content search
            if domain:
                domain_lower = domain.lower()
                domain_found = False
                
                # Check structured data first
                if (domain_lower in user_domain.lower() or 
                    domain_lower in user_role.lower() or
                    any(domain_lower in skill.lower() for skill in user_skills)):
                    domain_found = True
                
                # Check resume content if not found in structured data
                if not domain_found and resume_text and domain_lower in resume_text.lower():
                    domain_found = True
                    logger.info(f"✅ Domain match found in resume content: '{domain_lower}' found in resume text")
                
                if not domain_found:
                    include_user = False
            
            # Job role filter - simplified logic
            if job_role:
                job_role_lower = job_role.lower()
                if not (job_role_lower in user_role.lower() or
                       any(job_role_lower in skill.lower() for skill in user_skills)):
                    include_user = False
            
            if include_user:
                users_list.append({
                    "email": user_email,
                    "name": user_data.get('name', 'Unknown'),
                    "role": user_data.get('role', 'candidate'),
                    "resume_role": user_role,
                    "experience_years": experience_years,
                    "skills": user_skills,
                    "domain": user_domain,
                    "has_resume": has_resume,
                    "resume_filename": resume_filename,
                    "resume_upload_date": user_data.get('resume_upload_date'),
                    "location": resume_data.get('location', 'Unknown')
                })
        
        logger.info(f"✅ User search completed - Found {len(users_list)} users out of {len(users_db)} total users")
        if search:
            logger.info(f"🔍 Search term: '{search}'")
        if skills:
            logger.info(f"🔍 Skills filter: '{skills}'")
        if domain:
            logger.info(f"🔍 Domain filter: '{domain}'")
        if job_role:
            logger.info(f"🔍 Job role filter: '{job_role}'")
        
        return {"users": users_list, "total": len(users_list)}
        
    except Exception as e:
        logger.error(f"Error getting users: {e}")
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@app.delete("/api/admin/users/{user_email}")
async def delete_user(user_email: str, email: str = Depends(verify_token)):
    """Delete a user (admin only)"""
    try:
        # Check if user is admin
        user = users_db.get(email, {})
        if user.get('role') != 'admin':
            raise HTTPException(status_code=403, detail="Admin access required")
        
        if user_email not in users_db:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Don't allow admin to delete themselves
        if user_email == email:
            raise HTTPException(status_code=400, detail="Cannot delete your own account")
        
        # Remove user data
        del users_db[user_email]
        if user_email in resumes_db:
            del resumes_db[user_email]
        
        # Remove user's applications
        applications_to_remove = []
        for app_id, app_data in applications_db.items():
            if app_data.get('user_email') == user_email:
                applications_to_remove.append(app_id)
        
        for app_id in applications_to_remove:
            del applications_db[app_id]
        
        # Save to persistent storage
        save_persistent_data()
        
        return {"message": "User deleted successfully"}
        
    except Exception as e:
        logger.error(f"Error deleting user: {e}")
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@app.get("/api/admin/applications")
async def get_all_applications(
    search: str = None,
    status: str = None,
    job_id: int = None,
    email: str = Depends(verify_token)
):
    """Get all applications for admin with search and filtering"""
    try:
        # Check if user is admin
        user = users_db.get(email, {})
        if user.get('role') != 'admin':
            raise HTTPException(status_code=403, detail="Admin access required")
        
        # Return applications with job and user details
        applications_list = []
        for app_id, app_data in applications_db.items():
            job_id_app = app_data.get('job_id')
            job_key = str(job_id_app)  # Convert to string for lookup
            job_data = jobs_db.get(job_key, {})
            user_data = users_db.get(app_data.get('user_email'), {})
            resume_data = resumes_db.get(app_data.get('user_email'), {})
            
            # Apply filters
            include_app = True
            
            # Search filter
            if search:
                search_lower = search.lower()
                if not (search_lower in user_data.get('name', '').lower() or 
                       search_lower in app_data.get('user_email', '').lower() or
                       search_lower in job_data.get('title', '').lower() or
                       search_lower in job_data.get('company', '').lower()):
                    include_app = False
            
            # Status filter
            current_status = app_data.get('status', 'under_review') if app_data.get('status', 'under_review') != 'applied' else 'under_review'
            if status and current_status != status:
                include_app = False
            
            # Job ID filter
            if job_id and job_id_app != job_id:
                include_app = False
            
            if include_app:
                # Get user's resume information
                user_skills = resume_data.get('skills', [])
                user_experience = resume_data.get('experience', {})
                user_role = resume_data.get('role', '')
                
                # Extract experience years
                experience_years = 0
                if isinstance(user_experience, dict):
                    experience_years = user_experience.get('total_years', 0)
                elif isinstance(user_experience, (int, float)):
                    experience_years = user_experience
            
            applications_list.append({
                "id": app_id,
                    "job_id": job_id_app,
                "job_title": job_data.get('title', 'Unknown Job'),
                "job_company": job_data.get('company', 'Unknown Company'),
                    "job_location": job_data.get('location', 'Unknown Location'),
                "user_email": app_data.get('user_email'),
                "user_name": user_data.get('name', 'Unknown User'),
                    "user_role": user_role,
                    "user_skills": user_skills,
                    "user_experience_years": experience_years,
                "status": app_data.get('status', 'under_review') if app_data.get('status', 'under_review') != 'applied' else 'under_review',
                "applied_date": app_data.get('applied_date'),
                    "updated_date": app_data.get('updated_date'),
                    "has_resume": app_data.get('user_email') in resumes_db,
                    "resume_filename": user_data.get('resume_filename', 'N/A')
            })
        
        # Add resume scores for each application
        for app in applications_list:
            app['resume_score'] = calculate_resume_job_match_score(
                app['user_email'], 
                app['job_id']
            )
        
        # Add AI suggestions for each application
        for app in applications_list:
            app['ai_suggestion'] = generate_ai_suggestion(app['resume_score'])
            logger.info(f"🔍 Added AI suggestion for app {app['id']}: {app['ai_suggestion']}")
        
        return {"applications": applications_list, "total": len(applications_list)}
        
    except Exception as e:
        logger.error(f"Error getting applications: {e}")
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.put("/api/admin/applications/{application_id}/status")
async def update_application_status(
    application_id: int,
    status_update: dict,
    email: str = Depends(verify_token)
):
    """Update application status"""
    try:
        # Check if user is admin
        user = users_db.get(email, {})
        if user.get('role') != 'admin':
            raise HTTPException(status_code=403, detail="Admin access required")
        
        # Convert application_id to string for lookup
        app_key = str(application_id)
        if app_key not in applications_db:
            raise HTTPException(status_code=404, detail="Application not found")
        
        new_status = status_update.get('status')
        if new_status not in ['under_review', 'accepted', 'rejected']:
            raise HTTPException(status_code=400, detail="Invalid status")
        
        applications_db[app_key]['status'] = new_status
        applications_db[app_key]['updated_date'] = datetime.now().strftime('%Y-%m-%d')
        
        # Save to persistent storage
        save_persistent_data()
        
        return {"message": "Application status updated successfully"}
        
    except Exception as e:
        logger.error(f"Error updating application status: {e}")
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@app.put("/api/update-profile")
async def update_profile(
    profile_data: dict,
    email: str = Depends(verify_token)
):
    """Update user profile information"""
    try:
        if email not in users_db:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Update user data
        user_data = users_db[email]
        
        # Update allowed fields
        if 'name' in profile_data:
            user_data['name'] = profile_data['name']
        if 'phone' in profile_data:
            user_data['phone'] = profile_data['phone']
        if 'location' in profile_data:
            user_data['location'] = profile_data['location']
        
        # Save persistent data
        save_persistent_data()
        
        logger.info(f"✅ Profile updated for user: {email}")
        return {
            "message": "Profile updated successfully",
            "user": {
                "email": email,
                "name": user_data.get('name', ''),
                "phone": user_data.get('phone', ''),
                "location": user_data.get('location', ''),
                "role": user_data.get('role', 'candidate')
            }
        }
        
    except Exception as e:
        logger.error(f"Error updating profile: {e}")
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.get("/api/admin/resume-files/{user_email}")
async def get_user_resume_files(user_email: str, pattern: str = None, admin_email: str = Depends(verify_token)):
    """Get resume files for a specific user (admin only)"""
    try:
        # Check if user is admin
        admin_user = users_db.get(admin_email, {})
        if admin_user.get('role') != 'admin':
            raise HTTPException(status_code=403, detail="Admin access required")
        
        # Look for resume files in uploads directory
        import glob
        filenames = []
        
        # If pattern is provided, use it
        if pattern:
            # Replace wildcards with actual glob patterns
            search_pattern = pattern.replace('*', '*')
            resume_files = glob.glob(f"uploads/{search_pattern}")
            filenames = [os.path.basename(file) for file in resume_files]
        else:
            # Try multiple patterns
            patterns = [
                f"{user_email}_*.pdf",
                f"*{user_email}*.pdf",
                f"{user_email.replace('@', '_').replace('.', '_')}*.pdf"
            ]
            
            for pat in patterns:
                resume_files = glob.glob(f"uploads/{pat}")
                if resume_files:
                    filenames = [os.path.basename(file) for file in resume_files]
                    break
        
        # If no files found, check if user has resume data but no file
        if not filenames and user_email in resumes_db:
            user_data = users_db.get(user_email, {})
            if user_data.get('resume_filename'):
                filenames = [user_data['resume_filename']]
            elif user_data.get('resume_file_path'):
                filenames = [os.path.basename(user_data['resume_file_path'])]
        
        return {"files": filenames}
        
    except Exception as e:
        logger.error(f"Error getting resume files: {e}")
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.get("/api/admin/view-resume/{user_email}")
async def view_user_resume(user_email: str, admin_email: str = Depends(verify_token)):
    """View resume file for a specific user (admin only)"""
    try:
        # Check if user is admin
        admin_user = users_db.get(admin_email, {})
        if admin_user.get('role') != 'admin':
            raise HTTPException(status_code=403, detail="Admin access required")
        
        # Check if target user exists
        if user_email not in users_db:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Look for resume file
        import glob
        resume_files = glob.glob(f"uploads/{user_email}_*.pdf")
        
        if not resume_files:
            # Try alternative patterns
            patterns = [
                f"*{user_email}*.pdf",
                f"{user_email.replace('@', '_').replace('.', '_')}*.pdf"
            ]
            for pat in patterns:
                resume_files = glob.glob(f"uploads/{pat}")
                if resume_files:
                    break
        
        if not resume_files:
            raise HTTPException(status_code=404, detail="Resume file not found")
        
        # Return the most recent resume file
        resume_file = max(resume_files, key=os.path.getmtime)
        
        # Check if file exists
        if not os.path.exists(resume_file):
            raise HTTPException(status_code=404, detail="Resume file not accessible")
        
        # Return file response
        return FileResponse(
            path=resume_file,
            media_type='application/pdf',
            filename=os.path.basename(resume_file)
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error viewing resume: {e}")
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.get("/api/admin/resume-data/{user_email}")
async def get_user_resume_data(user_email: str, admin_email: str = Depends(verify_token)):
    """Get resume data for a specific user (admin only)"""
    try:
        # Check if user is admin
        admin_user = users_db.get(admin_email, {})
        if admin_user.get('role') != 'admin':
            raise HTTPException(status_code=403, detail="Admin access required")
        
        # Check if target user exists
        if user_email not in users_db:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Get resume data
        if user_email not in resumes_db:
            raise HTTPException(status_code=404, detail="No resume data found")
        
        resume_data = resumes_db[user_email]
        user_data = users_db[user_email]
        
        # Return comprehensive resume data
        return {
            "user_info": {
                "email": user_email,
                "name": user_data.get('name', 'Unknown'),
                "phone": user_data.get('phone', 'N/A'),
                "role": user_data.get('role', 'candidate')
            },
            "resume_data": {
                "name": resume_data.get('name', 'Unknown'),
                "email": resume_data.get('email', 'N/A'),
                "phone": resume_data.get('phone', 'N/A'),
                "role": resume_data.get('role', 'Unknown'),
                "location": resume_data.get('location', 'Unknown'),
                "skills": resume_data.get('skills', []),
                "experience": resume_data.get('experience', {}),
                "education": resume_data.get('education', []),
                "extraction_method": resume_data.get('extraction_method', 'unknown'),
                "confidence_score": resume_data.get('confidence_score', 0.0),
                "extraction_timestamp": resume_data.get('extraction_timestamp', '')
            },
            "file_info": {
                "resume_filename": user_data.get('resume_filename', 'N/A'),
                "resume_upload_date": user_data.get('resume_upload_date', 'N/A'),
                "has_resume_file": bool(user_data.get('resume_file_path'))
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting resume data: {e}")
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8005)
