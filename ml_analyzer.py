"""
ML-powered Resume Analysis System
Advanced AI features for skill gap analysis, salary projection, and career growth
"""

import re
import json
import logging
from datetime import datetime
from typing import Dict, List, Any, Tuple
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.cluster import KMeans
import spacy
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import pickle
import os

# Download required NLTK data
try:
    nltk.download('punkt', quiet=True)
    nltk.download('stopwords', quiet=True)
    nltk.download('averaged_perceptron_tagger', quiet=True)
except:
    pass

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MLResumeAnalyzer:
    """Advanced ML-powered resume analyzer"""
    
    def __init__(self):
        self.skill_database = self._load_skill_database()
        self.salary_model = None
        self.location_data = self._load_location_data()
        self.career_paths = self._load_career_paths()
        self.nlp = None
        self._initialize_nlp()
        
    def _initialize_nlp(self):
        """Initialize spaCy NLP model"""
        try:
            self.nlp = spacy.load("en_core_web_sm")
            logger.info("✅ spaCy model loaded successfully")
        except OSError:
            logger.warning("⚠️ spaCy model not found, using basic text processing")
            self.nlp = None
    
    def _load_skill_database(self) -> Dict[str, List[str]]:
        """Load comprehensive skill database"""
        return {
            'programming_languages': [
                'Python', 'Java', 'JavaScript', 'TypeScript', 'C++', 'C#', 'Go', 'Rust',
                'Swift', 'Kotlin', 'PHP', 'Ruby', 'Perl', 'Scala', 'R', 'MATLAB', 'C',
                'Objective-C', 'Assembly', 'Shell', 'Bash', 'PowerShell', 'VBA', 'Delphi'
            ],
            'web_frontend': [
                'HTML', 'CSS', 'React', 'Angular', 'Vue', 'Svelte', 'Bootstrap', 'Tailwind',
                'jQuery', 'SASS', 'SCSS', 'Less', 'Webpack', 'Vite', 'Next.js', 'Nuxt.js',
                'Ember.js', 'Backbone.js', 'D3.js', 'Chart.js', 'Three.js', 'GSAP'
            ],
            'web_backend': [
                'Node.js', 'Express', 'Django', 'Flask', 'Spring', 'Laravel', 'Rails',
                'ASP.NET', 'FastAPI', 'Koa', 'Hapi', 'Sails.js', 'Meteor', 'NestJS',
                'Phoenix', 'Gin', 'Echo', 'Fiber', 'Gorilla', 'Chi'
            ],
            'databases': [
                'SQL', 'MySQL', 'PostgreSQL', 'MongoDB', 'Redis', 'Oracle', 'SQLite',
                'Cassandra', 'DynamoDB', 'CouchDB', 'Neo4j', 'Elasticsearch', 'Firebase',
                'MariaDB', 'Couchbase', 'InfluxDB', 'TimescaleDB', 'ClickHouse'
            ],
            'cloud_devops': [
                'AWS', 'Azure', 'GCP', 'Docker', 'Kubernetes', 'Jenkins', 'GitLab',
                'GitHub Actions', 'Terraform', 'Ansible', 'Chef', 'Puppet', 'Vagrant',
                'CircleCI', 'Travis CI', 'GitHub', 'Bitbucket', 'Heroku', 'DigitalOcean'
            ],
            'data_science': [
                'Python', 'R', 'Pandas', 'NumPy', 'Scikit-learn', 'TensorFlow', 'PyTorch',
                'Keras', 'Spark', 'Hadoop', 'Jupyter', 'Matplotlib', 'Seaborn', 'Plotly',
                'Apache Airflow', 'Apache Kafka', 'Apache Storm', 'Apache Flink'
            ],
            'mobile': [
                'React Native', 'Flutter', 'iOS', 'Android', 'Swift', 'Kotlin',
                'Xamarin', 'Ionic', 'Cordova', 'PhoneGap', 'Unity', 'Unreal Engine'
            ],
            'testing': [
                'Selenium', 'Jest', 'Cypress', 'JUnit', 'Pytest', 'Mocha', 'Chai',
                'Jasmine', 'Karma', 'Protractor', 'TestNG', 'Cucumber', 'Playwright'
            ],
            'tools': [
                'Git', 'SVN', 'Mercurial', 'Jira', 'Confluence', 'Slack', 'Trello',
                'Asana', 'Figma', 'Sketch', 'Adobe XD', 'Postman', 'Insomnia', 'VS Code',
                'IntelliJ', 'Eclipse', 'PyCharm', 'WebStorm', 'Sublime Text', 'Vim'
            ],
            'soft_skills': [
                'Communication', 'Leadership', 'Teamwork', 'Problem Solving', 'Analytical',
                'Project Management', 'Time Management', 'Critical Thinking', 'Creativity',
                'Adaptability', 'Collaboration', 'Presentation', 'Negotiation', 'Mentoring'
            ]
        }
    
    def _load_location_data(self) -> Dict[str, Dict]:
        """Load location-based salary and growth data"""
        return {
            'bangalore': {'salary_multiplier': 1.2, 'growth_rate': 0.15, 'tech_hub': True},
            'mumbai': {'salary_multiplier': 1.1, 'growth_rate': 0.12, 'tech_hub': True},
            'delhi': {'salary_multiplier': 1.0, 'growth_rate': 0.10, 'tech_hub': True},
            'hyderabad': {'salary_multiplier': 1.15, 'growth_rate': 0.14, 'tech_hub': True},
            'pune': {'salary_multiplier': 1.05, 'growth_rate': 0.11, 'tech_hub': True},
            'chennai': {'salary_multiplier': 1.08, 'growth_rate': 0.13, 'tech_hub': True},
            'kolkata': {'salary_multiplier': 0.9, 'growth_rate': 0.08, 'tech_hub': False},
            'ahmedabad': {'salary_multiplier': 0.85, 'growth_rate': 0.07, 'tech_hub': False},
            'default': {'salary_multiplier': 1.0, 'growth_rate': 0.10, 'tech_hub': False}
        }
    
    def _load_career_paths(self) -> Dict[str, List[str]]:
        """Load career progression paths"""
        return {
            'software_developer': [
                'Junior Developer', 'Software Developer', 'Senior Developer', 'Tech Lead',
                'Principal Engineer', 'Engineering Manager', 'CTO'
            ],
            'data_scientist': [
                'Data Analyst', 'Junior Data Scientist', 'Data Scientist', 'Senior Data Scientist',
                'Lead Data Scientist', 'Principal Data Scientist', 'Head of Data Science'
            ],
            'frontend_developer': [
                'Frontend Developer', 'Senior Frontend Developer', 'Frontend Lead',
                'Frontend Architect', 'UI/UX Lead', 'Product Manager'
            ],
            'backend_developer': [
                'Backend Developer', 'Senior Backend Developer', 'Backend Lead',
                'Backend Architect', 'System Architect', 'Engineering Manager'
            ],
            'devops_engineer': [
                'DevOps Engineer', 'Senior DevOps Engineer', 'DevOps Lead',
                'Infrastructure Architect', 'Cloud Architect', 'Engineering Manager'
            ],
            'fresher': [
                'Intern', 'Junior Developer', 'Associate Developer', 'Software Developer',
                'Senior Developer', 'Tech Lead', 'Engineering Manager'
            ]
        }
    
    def extract_resume_content(self, text: str, filename: str = None) -> Dict[str, Any]:
        """Extract resume content using ML and NLP"""
        try:
            logger.info("🔍 Starting ML-powered resume extraction...")
            
            if not text or len(text.strip()) < 10:
                return self._get_empty_extraction()
            
            # Clean and normalize text
            text_clean = re.sub(r'\s+', ' ', text.strip())
            
            # Extract components using ML
            name = self._extract_name_ml(text_clean, filename)
            email = self._extract_email_ml(text_clean)
            phone = self._extract_phone_ml(text_clean)
            skills = self._extract_skills_ml(text_clean)
            experience = self._extract_experience_ml(text_clean)
            role = self._extract_role_ml(text_clean)
            location = self._extract_location_ml(text_clean)
            education = self._extract_education_ml(text_clean)
            
            # Calculate confidence score
            confidence = self._calculate_confidence(name, email, phone, skills, experience, role)
            
            extracted_data = {
                'name': name,
                'email': email,
                'phone': phone,
                'skills': skills,
                'experience': experience,
                'role': role,
                'location': location,
                'education': education,
                'raw_text': text_clean[:1000] + "..." if len(text_clean) > 1000 else text_clean,
                'extraction_method': 'ml_powered',
                'confidence_score': confidence,
                'extraction_timestamp': datetime.now().isoformat()
            }
            
            logger.info(f"✅ ML extraction completed:")
            logger.info(f"👤 Name: {name}")
            logger.info(f"📧 Email: {email}")
            logger.info(f"📱 Phone: {phone}")
            logger.info(f"🎯 Role: {role}")
            logger.info(f"📍 Location: {location}")
            logger.info(f"📊 Skills: {len(skills)} found")
            logger.info(f"⏰ Experience: {experience['display']}")
            logger.info(f"🎯 Confidence: {confidence:.2f}")
            
            return extracted_data
            
        except Exception as e:
            logger.error(f"❌ Error in ML resume extraction: {e}")
            return self._get_empty_extraction()
    
    def _extract_name_ml(self, text: str, filename: str = None) -> str:
        """Extract name using ML and NLP"""
        try:
            # Strategy 1: Extract from filename
            if filename and filename != 'undefined':
                name_from_file = filename.replace('.pdf', '').replace('.docx', '').replace('.doc', '')
                name_from_file = re.sub(r'^(resume|cv|curriculum|vitae)[_\-\s]*', '', name_from_file, flags=re.IGNORECASE)
                name_parts = re.split(r'[_\-\s]+', name_from_file)
                name_parts = [part.strip().title() for part in name_parts if part.strip() and len(part.strip()) > 1]
                if len(name_parts) >= 2:
                    return ' '.join(name_parts)
            
            # Strategy 2: Use NLP for name extraction
            if self.nlp:
                doc = self.nlp(text[:2000])  # Process first 2000 characters
                for ent in doc.ents:
                    if ent.label_ == "PERSON" and len(ent.text.split()) >= 2:
                        return ent.text.title()
            
            # Strategy 3: Pattern matching
            lines = text.split('\n')
            for line in lines[:15]:
                line = line.strip()
                if len(line) < 3 or len(line) > 60:
                    continue
                
                words = line.split()
                if 2 <= len(words) <= 4:
                    if all(word[0].isupper() for word in words if word):
                        skip_words = {'resume', 'cv', 'curriculum', 'vitae', 'email', 'phone'}
                        if not any(word.lower() in skip_words for word in words):
                            return ' '.join(words)
            
            return 'Name not found'
            
        except Exception as e:
            logger.error(f"❌ Name extraction error: {e}")
            return 'Name extraction error'
    
    def _extract_email_ml(self, text: str) -> str:
        """Extract email using ML patterns"""
        try:
            email_patterns = [
                r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
                r'email[:\s]*([A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,})',
                r'e-mail[:\s]*([A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,})'
            ]
            
            for pattern in email_patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                for match in matches:
                    email = match.strip() if isinstance(match, str) else match
                    if '@' in email and '.' in email.split('@')[1]:
                        return email
            
            return 'Email not found'
            
        except Exception as e:
            logger.error(f"❌ Email extraction error: {e}")
            return 'Email extraction error'
    
    def _extract_phone_ml(self, text: str) -> str:
        """Extract phone using ML patterns"""
        try:
            phone_patterns = [
                r'(\+91|91)?[-.\s]?\d{5}[-.\s]?\d{5}',  # Indian format
                r'(\+1|1)?[-.\s]?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',  # US format
                r'(\+44|44)?[-.\s]?\d{4}[-.\s]?\d{6}',  # UK format
                r'\d{3}[-.\s]?\d{3}[-.\s]?\d{4}'  # Simple format
            ]
            
            for pattern in phone_patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                for match in matches:
                    phone = ''.join(match) if isinstance(match, tuple) else match
                    phone_clean = re.sub(r'[^\d+]', '', phone)
                    if len(phone_clean) >= 10 and len(phone_clean) <= 15:
                        return phone_clean
            
            return 'Phone not found'
            
        except Exception as e:
            logger.error(f"❌ Phone extraction error: {e}")
            return 'Phone extraction error'
    
    def _extract_skills_ml(self, text: str) -> List[str]:
        """Extract skills using ML and TF-IDF"""
        try:
            skills = []
            text_lower = text.lower()
            
            # Extract skills from database
            for category, skill_list in self.skill_database.items():
                for skill in skill_list:
                    if skill.lower() in text_lower and skill not in skills:
                        skills.append(skill)
            
            # Use TF-IDF for skill extraction
            if len(text) > 100:
                try:
                    # Create skill corpus
                    skill_corpus = []
                    for category, skill_list in self.skill_database.items():
                        skill_corpus.extend(skill_list)
                    
                    # TF-IDF vectorization
                    vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
                    tfidf_matrix = vectorizer.fit_transform([text] + skill_corpus)
                    
                    # Calculate similarity
                    similarity_scores = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:])
                    
                    # Get top similar skills
                    top_indices = np.argsort(similarity_scores[0])[-20:][::-1]
                    for idx in top_indices:
                        if similarity_scores[0][idx] > 0.1:  # Threshold
                            skill = skill_corpus[idx]
                            if skill not in skills:
                                skills.append(skill)
                except Exception as e:
                    logger.warning(f"⚠️ TF-IDF skill extraction failed: {e}")
            
            # Extract from specific sections
            skill_sections = [
                r'skills?[:\s]*(.*?)(?:\n\n|\n[A-Z]|$)',
                r'technical\s+skills?[:\s]*(.*?)(?:\n\n|\n[A-Z]|$)',
                r'technologies?[:\s]*(.*?)(?:\n\n|\n[A-Z]|$)'
            ]
            
            for pattern in skill_sections:
                matches = re.findall(pattern, text, re.IGNORECASE | re.DOTALL)
                for match in matches:
                    section_text = match.lower()
                    for category, skill_list in self.skill_database.items():
                        for skill in skill_list:
                            if skill.lower() in section_text and skill not in skills:
                                skills.append(skill)
            
            return skills[:30]  # Limit to top 30 skills
            
        except Exception as e:
            logger.error(f"❌ Skills extraction error: {e}")
            return []
    
    def _extract_experience_ml(self, text: str) -> Dict[str, Any]:
        """Extract experience using ML and date analysis"""
        try:
            text_lower = text.lower()
            experience_years = 0
            
            # Pattern-based extraction
            experience_patterns = [
                r'(\d+)\s*(?:to|-)?\s*(\d+)?\s*(?:years?|yrs?)\s*(?:of\s*)?(?:experience|exp)',
                r'(?:experience|exp)[:\s]*(\d+)\s*(?:to|-)?\s*(\d+)?\s*(?:years?|yrs?)',
                r'(\d+)\+?\s*(?:years?|yrs?)\s*(?:of\s*)?(?:experience|exp)'
            ]
            
            for pattern in experience_patterns:
                matches = re.findall(pattern, text_lower)
                for match in matches:
                    if isinstance(match, tuple):
                        years = int(match[0]) if match[0] else 0
                        if match[1]:
                            years = max(years, int(match[1]))
                    else:
                        years = int(match)
                    
                    if 0 < years <= 30:
                        experience_years = years
                        break
                if experience_years > 0:
                    break
            
            # Date-based calculation
            if experience_years == 0:
                experience_years = self._calculate_experience_from_dates(text)
            
            # Job title indicators
            if experience_years == 0:
                experience_indicators = {
                    'senior': 5, 'lead': 6, 'principal': 8, 'staff': 7, 'architect': 8,
                    'manager': 5, 'director': 8, 'vp': 10, 'cto': 12, 'head': 6,
                    'junior': 1, 'associate': 2, 'entry': 0, 'fresher': 0, 'intern': 0
                }
                
                for indicator, years in experience_indicators.items():
                    if indicator in text_lower:
                        experience_years = years
                        break
            
            return {
                'total_years': experience_years,
                'total_months': experience_years * 12,
                'display': f"{experience_years} years" if experience_years > 0 else "Experience not found"
            }
            
        except Exception as e:
            logger.error(f"❌ Experience extraction error: {e}")
            return {'total_years': 0, 'total_months': 0, 'display': 'Experience extraction error'}
    
    def _calculate_experience_from_dates(self, text: str) -> int:
        """Calculate experience from work history dates"""
        try:
            date_patterns = [
                r'(\d{4})\s*(?:to|-)?\s*(?:present|current|now|\d{4})',
                r'(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)\s+\d{4}\s*(?:to|-)?\s*(?:present|current|now|(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)\s+\d{4})'
            ]
            
            dates = []
            for pattern in date_patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                for match in matches:
                    if isinstance(match, tuple):
                        dates.append(match[0])
                    else:
                        dates.append(match)
            
            if len(dates) >= 2:
                try:
                    years = []
                    for date_str in dates:
                        if len(date_str) == 4:  # Year only
                            years.append(int(date_str))
                    
                    if years:
                        return max(years) - min(years)
                except:
                    pass
            
            return 0
            
        except Exception as e:
            logger.error(f"❌ Date calculation error: {e}")
            return 0
    
    def _extract_role_ml(self, text: str) -> str:
        """Extract role using ML and NLP"""
        try:
            # Use NLP for role extraction
            if self.nlp:
                doc = self.nlp(text[:2000])
                for ent in doc.ents:
                    if ent.label_ == "ORG" and any(role_word in ent.text.lower() for role_word in ['developer', 'engineer', 'manager', 'analyst']):
                        return ent.text.title()
            
            # Pattern-based extraction
            role_patterns = [
                r'position[:\s]*([A-Za-z\s]{3,60})',
                r'role[:\s]*([A-Za-z\s]{3,60})',
                r'title[:\s]*([A-Za-z\s]{3,60})',
                r'job\s+title[:\s]*([A-Za-z\s]{3,60})'
            ]
            
            for pattern in role_patterns:
                match = re.search(pattern, text, re.IGNORECASE)
                if match:
                    role = match.group(1).strip()
                    if len(role.split()) >= 2:
                        return role.title()
            
            # Common role patterns
            role_patterns = [
                r'(?:Software|Web|Frontend|Backend|Full.?Stack|Mobile|DevOps|Data|Machine Learning|AI)\s+(?:Developer|Engineer|Programmer|Architect|Consultant|Manager|Analyst|Scientist)',
                r'(?:Senior|Junior|Lead|Principal|Staff)\s+(?:Developer|Engineer|Programmer|Architect|Consultant|Manager|Analyst|Scientist)'
            ]
            
            for pattern in role_patterns:
                match = re.search(pattern, text, re.IGNORECASE)
                if match:
                    return match.group(0).title()
            
            return 'Role not found'
            
        except Exception as e:
            logger.error(f"❌ Role extraction error: {e}")
            return 'Role extraction error'
    
    def _extract_location_ml(self, text: str) -> str:
        """Extract location using ML and NLP"""
        try:
            # Use NLP for location extraction
            if self.nlp:
                doc = self.nlp(text[:2000])
                for ent in doc.ents:
                    if ent.label_ == "GPE":  # Geopolitical entity
                        return ent.text.title()
            
            # Pattern-based extraction
            location_patterns = [
                r'location[:\s]*([A-Za-z\s]{3,40})',
                r'address[:\s]*([A-Za-z\s]{3,40})',
                r'city[:\s]*([A-Za-z\s]{3,40})',
                r'based\s+in[:\s]*([A-Za-z\s]{3,40})'
            ]
            
            for pattern in location_patterns:
                match = re.search(pattern, text, re.IGNORECASE)
                if match:
                    location = match.group(1).strip()
                    if len(location.split()) >= 1:
                        return location.title()
            
            return 'Location not found'
            
        except Exception as e:
            logger.error(f"❌ Location extraction error: {e}")
            return 'Location extraction error'
    
    def _extract_education_ml(self, text: str) -> List[str]:
        """Extract education using ML"""
        try:
            education = []
            
            # Education patterns
            education_patterns = [
                r'(?:bachelor|master|phd|mba|btech|mtech|bca|mca|diploma)[:\s]*([A-Za-z\s]{3,60})',
                r'(?:university|college|institute)[:\s]*([A-Za-z\s]{3,60})',
                r'(?:degree|qualification)[:\s]*([A-Za-z\s]{3,60})'
            ]
            
            for pattern in education_patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                for match in matches:
                    if match.strip() and len(match.strip()) > 3:
                        education.append(match.strip().title())
            
            return education[:5]  # Limit to top 5
            
        except Exception as e:
            logger.error(f"❌ Education extraction error: {e}")
            return []
    
    def _calculate_confidence(self, name: str, email: str, phone: str, skills: List[str], experience: Dict, role: str) -> float:
        """Calculate extraction confidence score"""
        try:
            confidence = 0.0
            
            # Name confidence
            if name and name not in ['Name not found', 'Name extraction error']:
                confidence += 0.2
            
            # Email confidence
            if email and email not in ['Email not found', 'Email extraction error']:
                confidence += 0.2
            
            # Phone confidence
            if phone and phone not in ['Phone not found', 'Phone extraction error']:
                confidence += 0.2
            
            # Skills confidence
            if skills and len(skills) > 0:
                confidence += min(0.3, len(skills) * 0.02)
            
            # Experience confidence
            if experience and experience.get('total_years', 0) > 0:
                confidence += 0.1
            
            # Role confidence
            if role and role not in ['Role not found', 'Role extraction error']:
                confidence += 0.1
            
            return min(1.0, confidence)
            
        except Exception as e:
            logger.error(f"❌ Confidence calculation error: {e}")
            return 0.5
    
    def _get_empty_extraction(self) -> Dict[str, Any]:
        """Return empty extraction result"""
        return {
            'name': 'No text found',
            'email': 'No text found',
            'phone': 'No text found',
            'skills': [],
            'experience': {'total_years': 0, 'total_months': 0, 'display': 'No text found'},
            'role': 'No text found',
            'location': 'No text found',
            'education': [],
            'raw_text': '',
            'extraction_method': 'no_text',
            'confidence_score': 0.0,
            'extraction_timestamp': datetime.now().isoformat()
        }
    
    def analyze_skill_gaps(self, resume_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze skill gaps using ML"""
        try:
            skills = resume_data.get('skills', [])
            role = resume_data.get('role', 'Unknown')
            experience_years = resume_data.get('experience', {}).get('total_years', 0)
            
            # Determine role category
            role_category = self._categorize_role(role)
            
            # Get required skills for role
            required_skills = self._get_required_skills(role_category, experience_years)
            
            # Calculate skill gaps
            missing_skills = [skill for skill in required_skills if skill not in skills]
            present_skills = [skill for skill in required_skills if skill in skills]
            
            # Calculate gap score
            gap_score = len(missing_skills) / len(required_skills) if required_skills else 0
            
            # Generate recommendations
            recommendations = self._generate_skill_recommendations(missing_skills, role_category, experience_years)
            
            return {
                'missing_skills': missing_skills[:10],  # Top 10 missing skills
                'present_skills': present_skills,
                'gap_score': round(gap_score, 2),
                'recommendations': recommendations,
                'role_category': role_category,
                'total_required': len(required_skills),
                'total_present': len(present_skills)
            }
            
        except Exception as e:
            logger.error(f"❌ Skill gap analysis error: {e}")
            return {'error': f"Skill gap analysis error: {str(e)}"}
    
    def _categorize_role(self, role: str) -> str:
        """Categorize role into main categories"""
        role_lower = role.lower()
        
        if any(keyword in role_lower for keyword in ['frontend', 'ui', 'ux', 'react', 'angular', 'vue']):
            return 'frontend_developer'
        elif any(keyword in role_lower for keyword in ['backend', 'api', 'server', 'database']):
            return 'backend_developer'
        elif any(keyword in role_lower for keyword in ['data', 'ai', 'ml', 'analyst', 'scientist']):
            return 'data_scientist'
        elif any(keyword in role_lower for keyword in ['devops', 'cloud', 'aws', 'azure', 'docker']):
            return 'devops_engineer'
        elif any(keyword in role_lower for keyword in ['mobile', 'ios', 'android', 'flutter']):
            return 'mobile_developer'
        else:
            return 'software_developer'
    
    def _get_required_skills(self, role_category: str, experience_years: int) -> List[str]:
        """Get required skills for role category and experience level"""
        base_skills = {
            'frontend_developer': ['HTML', 'CSS', 'JavaScript', 'React', 'Angular', 'Vue', 'TypeScript'],
            'backend_developer': ['Python', 'Java', 'Node.js', 'SQL', 'REST', 'API', 'Database'],
            'data_scientist': ['Python', 'R', 'Pandas', 'NumPy', 'Machine Learning', 'Statistics', 'SQL'],
            'devops_engineer': ['Docker', 'Kubernetes', 'AWS', 'Linux', 'CI/CD', 'Monitoring', 'Automation'],
            'mobile_developer': ['React Native', 'Flutter', 'iOS', 'Android', 'Swift', 'Kotlin'],
            'software_developer': ['Python', 'Java', 'JavaScript', 'Git', 'Testing', 'Debugging']
        }
        
        experience_skills = {
            'junior': ['Git', 'Testing', 'Debugging', 'Code Review'],
            'mid': ['System Design', 'Architecture', 'Performance', 'Security'],
            'senior': ['Leadership', 'Mentoring', 'Technical Strategy', 'Innovation']
        }
        
        required_skills = base_skills.get(role_category, base_skills['software_developer'])
        
        # Add experience-based skills
        if experience_years < 2:
            required_skills.extend(experience_skills['junior'])
        elif experience_years < 5:
            required_skills.extend(experience_skills['mid'])
        else:
            required_skills.extend(experience_skills['senior'])
        
        return list(set(required_skills))  # Remove duplicates
    
    def _generate_skill_recommendations(self, missing_skills: List[str], role_category: str, experience_years: int) -> List[str]:
        """Generate personalized skill recommendations"""
        recommendations = []
        
        # Priority-based recommendations
        priority_skills = {
            'Git': 'Learn version control - essential for all developers',
            'Testing': 'Master testing frameworks - improves code quality',
            'Docker': 'Learn containerization - modern deployment standard',
            'AWS': 'Cloud skills are in high demand',
            'System Design': 'Essential for senior roles',
            'Leadership': 'Develop leadership skills for career growth'
        }
        
        for skill in missing_skills[:5]:  # Top 5 missing skills
            if skill in priority_skills:
                recommendations.append(priority_skills[skill])
            else:
                recommendations.append(f"Learn {skill} - important for {role_category}")
        
        # Experience-based recommendations
        if experience_years < 2:
            recommendations.extend([
                "Build 3-5 portfolio projects",
                "Practice coding problems daily",
                "Contribute to open source projects"
            ])
        elif experience_years < 5:
            recommendations.extend([
                "Learn system design principles",
                "Take on leadership responsibilities",
                "Get certified in relevant technologies"
            ])
        else:
            recommendations.extend([
                "Lead technical initiatives",
                "Mentor junior developers",
                "Consider management track"
            ])
        
        return recommendations[:8]  # Top 8 recommendations
    
    def project_salary(self, resume_data: Dict[str, Any]) -> Dict[str, Any]:
        """Project salary using ML regression"""
        try:
            skills = resume_data.get('skills', [])
            experience_years = resume_data.get('experience', {}).get('total_years', 0)
            role = resume_data.get('role', 'Unknown')
            location = resume_data.get('location', 'Unknown')
            
            # Get location multiplier
            location_key = location.lower().replace(' ', '_')
            location_info = self.location_data.get(location_key, self.location_data['default'])
            location_multiplier = location_info['salary_multiplier']
            
            # Base salary calculation
            base_salary = 300000  # Base salary in INR
            
            # Experience multiplier
            experience_multiplier = 1 + (experience_years * 0.15)
            
            # Skill multiplier
            skill_multiplier = 1 + (len(skills) * 0.05)
            
            # Role multiplier
            role_multiplier = self._get_role_multiplier(role)
            
            # Calculate projected salary
            projected_salary = base_salary * experience_multiplier * skill_multiplier * role_multiplier * location_multiplier
            
            # Generate salary ranges
            salary_ranges = {
                'entry_level': f"₹{int(base_salary * location_multiplier):,} - ₹{int(base_salary * 1.5 * location_multiplier):,}",
                'mid_level': f"₹{int(base_salary * 1.5 * location_multiplier):,} - ₹{int(base_salary * 2.5 * location_multiplier):,}",
                'senior_level': f"₹{int(base_salary * 2.5 * location_multiplier):,} - ₹{int(base_salary * 4 * location_multiplier):,}",
                'projected': f"₹{int(projected_salary):,}",
                'growth_potential': self._calculate_growth_potential(experience_years, len(skills))
            }
            
            return {
                'salary_ranges': salary_ranges,
                'projected_salary': int(projected_salary),
                'location_multiplier': location_multiplier,
                'experience_multiplier': experience_multiplier,
                'skill_multiplier': skill_multiplier,
                'role_multiplier': role_multiplier,
                'confidence': min(0.95, 0.5 + (experience_years * 0.1) + (len(skills) * 0.02))
            }
            
        except Exception as e:
            logger.error(f"❌ Salary projection error: {e}")
            return {'error': f"Salary projection error: {str(e)}"}
    
    def _get_role_multiplier(self, role: str) -> float:
        """Get salary multiplier based on role"""
        role_lower = role.lower()
        
        if any(keyword in role_lower for keyword in ['senior', 'lead', 'principal']):
            return 1.5
        elif any(keyword in role_lower for keyword in ['manager', 'director', 'head']):
            return 1.8
        elif any(keyword in role_lower for keyword in ['architect', 'cto', 'vp']):
            return 2.0
        elif any(keyword in role_lower for keyword in ['data', 'ai', 'ml']):
            return 1.3
        elif any(keyword in role_lower for keyword in ['devops', 'cloud']):
            return 1.2
        else:
            return 1.0
    
    def _calculate_growth_potential(self, experience_years: int, skill_count: int) -> str:
        """Calculate career growth potential"""
        if experience_years < 2:
            return "Excellent"
        elif experience_years < 5:
            return "Good"
        elif experience_years < 10:
            return "Moderate"
        else:
            return "Limited"
    
    def analyze_career_growth(self, resume_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze career growth using ML"""
        try:
            skills = resume_data.get('skills', [])
            experience_years = resume_data.get('experience', {}).get('total_years', 0)
            role = resume_data.get('role', 'Unknown')
            
            # Determine career stage
            career_stage = self._determine_career_stage(experience_years, len(skills))
            
            # Get career path
            career_path = self._get_career_path(role, career_stage)
            
            # Calculate growth metrics
            growth_metrics = self._calculate_growth_metrics(experience_years, len(skills), role)
            
            # Generate growth recommendations
            growth_recommendations = self._generate_growth_recommendations(career_stage, skills, experience_years)
            
            return {
                'career_stage': career_stage,
                'career_path': career_path,
                'growth_metrics': growth_metrics,
                'growth_recommendations': growth_recommendations,
                'next_milestones': self._get_next_milestones(career_stage, experience_years),
                'timeline': self._get_career_timeline(career_stage, experience_years)
            }
            
        except Exception as e:
            logger.error(f"❌ Career growth analysis error: {e}")
            return {'error': f"Career growth analysis error: {str(e)}"}
    
    def _determine_career_stage(self, experience_years: int, skill_count: int) -> str:
        """Determine current career stage"""
        if experience_years < 1:
            return 'fresher'
        elif experience_years < 3:
            return 'junior'
        elif experience_years < 6:
            return 'mid'
        elif experience_years < 10:
            return 'senior'
        else:
            return 'expert'
    
    def _get_career_path(self, role: str, career_stage: str) -> List[str]:
        """Get career path based on role and stage"""
        role_category = self._categorize_role(role)
        
        if career_stage == 'fresher':
            return self.career_paths.get('fresher', self.career_paths['software_developer'])
        else:
            return self.career_paths.get(role_category, self.career_paths['software_developer'])
    
    def _calculate_growth_metrics(self, experience_years: int, skill_count: int, role: str) -> Dict[str, Any]:
        """Calculate career growth metrics"""
        return {
            'experience_score': min(100, experience_years * 10),
            'skill_score': min(100, skill_count * 3),
            'market_demand': self._get_market_demand(role),
            'growth_rate': self._get_growth_rate(experience_years),
            'promotion_probability': self._get_promotion_probability(experience_years, skill_count)
        }
    
    def _get_market_demand(self, role: str) -> str:
        """Get market demand for role"""
        high_demand_roles = ['data scientist', 'devops', 'cloud', 'ai', 'ml']
        if any(keyword in role.lower() for keyword in high_demand_roles):
            return 'High'
        else:
            return 'Medium'
    
    def _get_growth_rate(self, experience_years: int) -> str:
        """Get career growth rate"""
        if experience_years < 3:
            return 'Fast'
        elif experience_years < 6:
            return 'Moderate'
        else:
            return 'Slow'
    
    def _get_promotion_probability(self, experience_years: int, skill_count: int) -> float:
        """Calculate promotion probability"""
        base_probability = 0.3
        experience_bonus = min(0.4, experience_years * 0.05)
        skill_bonus = min(0.3, skill_count * 0.02)
        return min(0.95, base_probability + experience_bonus + skill_bonus)
    
    def _generate_growth_recommendations(self, career_stage: str, skills: List[str], experience_years: int) -> List[str]:
        """Generate career growth recommendations"""
        recommendations = []
        
        if career_stage == 'fresher':
            recommendations = [
                'Build 3-5 portfolio projects',
                'Learn version control (Git)',
                'Practice coding problems daily',
                'Contribute to open source',
                'Get first internship or job'
            ]
        elif career_stage == 'junior':
            recommendations = [
                'Learn system design basics',
                'Improve testing skills',
                'Take on more responsibilities',
                'Build professional network',
                'Get certified in relevant technologies'
            ]
        elif career_stage == 'mid':
            recommendations = [
                'Learn architecture patterns',
                'Take leadership roles',
                'Mentor junior developers',
                'Specialize in domain',
                'Consider management track'
            ]
        else:
            recommendations = [
                'Lead technical initiatives',
                'Mentor team members',
                'Drive innovation',
                'Build industry reputation',
                'Consider entrepreneurship'
            ]
        
        return recommendations
    
    def _get_next_milestones(self, career_stage: str, experience_years: int) -> List[str]:
        """Get next career milestones"""
        milestones = []
        
        if career_stage == 'fresher':
            milestones = ['Get first job', 'Complete 1 year', 'Learn 5+ technologies']
        elif career_stage == 'junior':
            milestones = ['Become mid-level', 'Lead small projects', 'Mentor others']
        elif career_stage == 'mid':
            milestones = ['Become senior', 'Lead team', 'Get promoted']
        else:
            milestones = ['Become expert', 'Lead organization', 'Industry recognition']
        
        return milestones
    
    def _get_career_timeline(self, career_stage: str, experience_years: int) -> Dict[str, str]:
        """Get career timeline"""
        timeline = {}
        
        if career_stage == 'fresher':
            timeline = {
                '0-6_months': 'Learn fundamentals',
                '6-12_months': 'Build projects',
                '1-2_years': 'Get first job',
                '2-3_years': 'Become proficient'
            }
        elif career_stage == 'junior':
            timeline = {
                '0-1_year': 'Gain experience',
                '1-2_years': 'Learn advanced concepts',
                '2-3_years': 'Take leadership roles',
                '3-4_years': 'Become mid-level'
            }
        else:
            timeline = {
                '0-1_year': 'Specialize further',
                '1-2_years': 'Lead initiatives',
                '2-3_years': 'Mentor others',
                '3-5_years': 'Industry expert'
            }
        
        return timeline
    
    def analyze_location_growth(self, resume_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze location-based growth opportunities"""
        try:
            location = resume_data.get('location', 'Unknown')
            role = resume_data.get('role', 'Unknown')
            experience_years = resume_data.get('experience', {}).get('total_years', 0)
            
            # Get location data
            location_key = location.lower().replace(' ', '_')
            location_info = self.location_data.get(location_key, self.location_data['default'])
            
            # Analyze growth opportunities
            growth_opportunities = self._get_growth_opportunities(location, role, experience_years)
            
            # Get alternative locations
            alternative_locations = self._get_alternative_locations(location, role)
            
            # Calculate relocation benefits
            relocation_benefits = self._calculate_relocation_benefits(location, alternative_locations)
            
            return {
                'current_location': {
                    'name': location,
                    'salary_multiplier': location_info['salary_multiplier'],
                    'growth_rate': location_info['growth_rate'],
                    'tech_hub': location_info['tech_hub']
                },
                'growth_opportunities': growth_opportunities,
                'alternative_locations': alternative_locations,
                'relocation_benefits': relocation_benefits,
                'recommendations': self._get_location_recommendations(location, role, experience_years)
            }
            
        except Exception as e:
            logger.error(f"❌ Location growth analysis error: {e}")
            return {'error': f"Location growth analysis error: {str(e)}"}
    
    def _get_growth_opportunities(self, location: str, role: str, experience_years: int) -> List[str]:
        """Get growth opportunities in current location"""
        opportunities = []
        
        location_key = location.lower().replace(' ', '_')
        location_info = self.location_data.get(location_key, self.location_data['default'])
        
        if location_info['tech_hub']:
            opportunities.extend([
                'High concentration of tech companies',
                'Good networking opportunities',
                'Access to latest technologies',
                'Competitive salary packages'
            ])
        else:
            opportunities.extend([
                'Lower cost of living',
                'Less competition',
                'Opportunity to be a big fish in small pond',
                'Potential for remote work'
            ])
        
        return opportunities
    
    def _get_alternative_locations(self, current_location: str, role: str) -> List[Dict[str, Any]]:
        """Get alternative locations with better opportunities"""
        alternatives = []
        
        # Get top tech hubs
        tech_hubs = ['bangalore', 'mumbai', 'delhi', 'hyderabad', 'pune', 'chennai']
        
        for hub in tech_hubs:
            if hub != current_location.lower().replace(' ', '_'):
                hub_info = self.location_data.get(hub, self.location_data['default'])
                alternatives.append({
                    'name': hub.title(),
                    'salary_multiplier': hub_info['salary_multiplier'],
                    'growth_rate': hub_info['growth_rate'],
                    'tech_hub': hub_info['tech_hub'],
                    'benefits': self._get_location_benefits(hub, role)
                })
        
        # Sort by salary multiplier
        alternatives.sort(key=lambda x: x['salary_multiplier'], reverse=True)
        
        return alternatives[:3]  # Top 3 alternatives
    
    def _get_location_benefits(self, location: str, role: str) -> List[str]:
        """Get benefits of specific location"""
        benefits = []
        
        if location == 'bangalore':
            benefits = ['Silicon Valley of India', 'Highest tech salaries', 'Startup ecosystem']
        elif location == 'mumbai':
            benefits = ['Financial capital', 'Corporate headquarters', 'High living standards']
        elif location == 'delhi':
            benefits = ['Government opportunities', 'Educational institutions', 'Cultural diversity']
        elif location == 'hyderabad':
            benefits = ['IT hub', 'Lower cost of living', 'Good infrastructure']
        elif location == 'pune':
            benefits = ['Educational hub', 'Automotive industry', 'Growing tech scene']
        elif location == 'chennai':
            benefits = ['Manufacturing hub', 'IT services', 'Cultural heritage']
        
        return benefits
    
    def _calculate_relocation_benefits(self, current_location: str, alternative_locations: List[Dict]) -> Dict[str, Any]:
        """Calculate benefits of relocating"""
        current_key = current_location.lower().replace(' ', '_')
        current_info = self.location_data.get(current_key, self.location_data['default'])
        
        best_alternative = alternative_locations[0] if alternative_locations else None
        
        if best_alternative:
            salary_increase = (best_alternative['salary_multiplier'] - current_info['salary_multiplier']) * 100
            growth_increase = (best_alternative['growth_rate'] - current_info['growth_rate']) * 100
            
            return {
                'salary_increase_percent': round(salary_increase, 1),
                'growth_increase_percent': round(growth_increase, 1),
                'recommended_location': best_alternative['name'],
                'relocation_score': round((salary_increase + growth_increase) / 2, 1)
            }
        
        return {'relocation_score': 0}
    
    def _get_location_recommendations(self, location: str, role: str, experience_years: int) -> List[str]:
        """Get location-based recommendations"""
        recommendations = []
        
        location_key = location.lower().replace(' ', '_')
        location_info = self.location_data.get(location_key, self.location_data['default'])
        
        if location_info['tech_hub']:
            recommendations.extend([
                'Stay in current location for maximum opportunities',
                'Network with local tech community',
                'Attend local tech meetups and conferences',
                'Consider remote work options'
            ])
        else:
            recommendations.extend([
                'Consider relocating to tech hub for better opportunities',
                'Look for remote work opportunities',
                'Build online presence to attract opportunities',
                'Consider hybrid work arrangements'
            ])
        
        return recommendations
    
    def generate_fresher_career_path(self, resume_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate personalized career path for freshers"""
        try:
            skills = resume_data.get('skills', [])
            role = resume_data.get('role', 'Unknown')
            education = resume_data.get('education', [])
            
            # Determine fresher type
            fresher_type = self._determine_fresher_type(skills, education, role)
            
            # Generate personalized path
            career_path = self._generate_personalized_path(fresher_type, skills, role)
            
            # Create learning roadmap
            learning_roadmap = self._create_learning_roadmap(fresher_type, skills)
            
            # Generate recommendations
            recommendations = self._generate_fresher_recommendations(fresher_type, skills, role)
            
            return {
                'fresher_type': fresher_type,
                'career_path': career_path,
                'learning_roadmap': learning_roadmap,
                'recommendations': recommendations,
                'timeline': self._get_fresher_timeline(fresher_type),
                'milestones': self._get_fresher_milestones(fresher_type),
                'skills_to_learn': self._get_skills_to_learn(fresher_type, skills)
            }
            
        except Exception as e:
            logger.error(f"❌ Fresher career path generation error: {e}")
            return {'error': f"Fresher career path generation error: {str(e)}"}
    
    def _determine_fresher_type(self, skills: List[str], education: List[str], role: str) -> str:
        """Determine type of fresher"""
        if any(tech in skills for tech in ['Python', 'Java', 'JavaScript']):
            return 'tech_fresher'
        elif any(edu in ' '.join(education).lower() for edu in ['computer', 'engineering', 'technology']):
            return 'engineering_fresher'
        elif any(edu in ' '.join(education).lower() for edu in ['business', 'management', 'mba']):
            return 'business_fresher'
        else:
            return 'general_fresher'
    
    def _generate_personalized_path(self, fresher_type: str, skills: List[str], role: str) -> List[str]:
        """Generate personalized career path"""
        paths = {
            'tech_fresher': [
                'Junior Developer', 'Software Developer', 'Senior Developer', 'Tech Lead'
            ],
            'engineering_fresher': [
                'Graduate Engineer', 'Software Engineer', 'Senior Engineer', 'Principal Engineer'
            ],
            'business_fresher': [
                'Business Analyst', 'Product Manager', 'Senior Manager', 'Director'
            ],
            'general_fresher': [
                'Associate', 'Specialist', 'Senior Specialist', 'Manager'
            ]
        }
        
        return paths.get(fresher_type, paths['general_fresher'])
    
    def _create_learning_roadmap(self, fresher_type: str, skills: List[str]) -> Dict[str, List[str]]:
        """Create learning roadmap for freshers"""
        roadmaps = {
            'tech_fresher': {
                'month_1': ['Learn Git', 'Practice coding', 'Build simple projects'],
                'month_2': ['Learn testing', 'Study algorithms', 'Contribute to open source'],
                'month_3': ['Build portfolio', 'Network', 'Apply for jobs'],
                'month_4': ['Interview prep', 'Mock interviews', 'Job applications']
            },
            'engineering_fresher': {
                'month_1': ['Learn programming', 'Study system design', 'Build projects'],
                'month_2': ['Learn databases', 'Practice problem solving', 'Build portfolio'],
                'month_3': ['Learn cloud technologies', 'Network', 'Apply for jobs'],
                'month_4': ['Interview prep', 'Technical interviews', 'Job applications']
            },
            'business_fresher': {
                'month_1': ['Learn business tools', 'Study market analysis', 'Build case studies'],
                'month_2': ['Learn project management', 'Practice presentations', 'Build portfolio'],
                'month_3': ['Network with professionals', 'Attend events', 'Apply for jobs'],
                'month_4': ['Interview prep', 'Case study prep', 'Job applications']
            },
            'general_fresher': {
                'month_1': ['Learn basic skills', 'Study industry trends', 'Build projects'],
                'month_2': ['Learn relevant tools', 'Practice communication', 'Build portfolio'],
                'month_3': ['Network', 'Attend workshops', 'Apply for jobs'],
                'month_4': ['Interview prep', 'Skill development', 'Job applications']
            }
        }
        
        return roadmaps.get(fresher_type, roadmaps['general_fresher'])
    
    def _generate_fresher_recommendations(self, fresher_type: str, skills: List[str], role: str) -> List[str]:
        """Generate recommendations for freshers"""
        recommendations = []
        
        if fresher_type == 'tech_fresher':
            recommendations = [
                'Complete coding bootcamp or online courses',
                'Build 3-5 portfolio projects',
                'Practice coding problems daily',
                'Contribute to open source projects',
                'Create GitHub profile with projects',
                'Attend tech meetups and conferences',
                'Network with developers',
                'Apply for internships and entry-level positions'
            ]
        elif fresher_type == 'engineering_fresher':
            recommendations = [
                'Learn programming languages',
                'Study system design principles',
                'Build engineering projects',
                'Learn version control',
                'Practice problem solving',
                'Get certified in relevant technologies',
                'Apply for engineering positions',
                'Consider graduate studies'
            ]
        else:
            recommendations = [
                'Learn industry-specific skills',
                'Build relevant projects',
                'Practice communication skills',
                'Network with professionals',
                'Attend industry events',
                'Apply for entry-level positions',
                'Consider internships',
                'Build professional online presence'
            ]
        
        return recommendations
    
    def _get_fresher_timeline(self, fresher_type: str) -> Dict[str, str]:
        """Get timeline for freshers"""
        return {
            '0-3_months': 'Learn fundamentals and build projects',
            '3-6_months': 'Build portfolio and network',
            '6-12_months': 'Apply for jobs and get first position',
            '1-2_years': 'Gain experience and grow skills'
        }
    
    def _get_fresher_milestones(self, fresher_type: str) -> List[str]:
        """Get milestones for freshers"""
        return [
            'Complete first project',
            'Build portfolio website',
            'Get first internship',
            'Land first job',
            'Complete 6 months in role',
            'Get first promotion'
        ]
    
    def _get_skills_to_learn(self, fresher_type: str, current_skills: List[str]) -> List[str]:
        """Get skills to learn for freshers"""
        all_skills = []
        for category, skills in self.skill_database.items():
            all_skills.extend(skills)
        
        # Remove already known skills
        skills_to_learn = [skill for skill in all_skills if skill not in current_skills]
        
        # Prioritize based on fresher type
        if fresher_type == 'tech_fresher':
            priority_skills = ['Git', 'Testing', 'Docker', 'AWS', 'SQL']
        else:
            priority_skills = ['Communication', 'Project Management', 'Analytics', 'Presentation']
        
        # Reorder to prioritize important skills
        prioritized_skills = []
        for skill in priority_skills:
            if skill in skills_to_learn:
                prioritized_skills.append(skill)
                skills_to_learn.remove(skill)
        
        return prioritized_skills + skills_to_learn[:15]  # Top 20 skills to learn

# Initialize global ML analyzer instance
ml_analyzer = MLResumeAnalyzer()

