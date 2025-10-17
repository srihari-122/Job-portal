"""
Advanced Resume Extraction System
Using state-of-the-art NLP models for accurate resume parsing
"""

import re
import json
import logging
from datetime import datetime
from typing import Dict, List, Any, Tuple
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import spacy
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.chunk import ne_chunk
from nltk.tag import pos_tag
import PyPDF2
import docx
import io
import os

# Download required NLTK data
try:
    nltk.download('punkt', quiet=True)
    nltk.download('stopwords', quiet=True)
    nltk.download('averaged_perceptron_tagger', quiet=True)
    nltk.download('maxent_ne_chunker', quiet=True)
    nltk.download('words', quiet=True)
except:
    pass

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AdvancedResumeExtractor:
    """Advanced resume extractor using multiple NLP techniques"""
    
    def __init__(self):
        self.nlp = None
        self.skill_database = self._load_comprehensive_skill_database()
        self.education_keywords = self._load_education_keywords()
        self.experience_patterns = self._load_experience_patterns()
        self.location_database = self._load_location_database()
        self._initialize_nlp()
        
    def _initialize_nlp(self):
        """Initialize spaCy NLP model"""
        try:
            self.nlp = spacy.load("en_core_web_sm")
            logger.info("✅ spaCy model loaded successfully")
        except OSError:
            logger.warning("⚠️ spaCy model not found, using basic text processing")
            self.nlp = None
    
    def _load_comprehensive_skill_database(self) -> Dict[str, List[str]]:
        """Load comprehensive skill database"""
        return {
            'programming_languages': [
                'Python', 'Java', 'JavaScript', 'TypeScript', 'C++', 'C#', 'Go', 'Rust',
                'Swift', 'Kotlin', 'PHP', 'Ruby', 'Perl', 'Scala', 'R', 'MATLAB', 'C',
                'Objective-C', 'Assembly', 'Shell', 'Bash', 'PowerShell', 'VBA', 'Delphi',
                'Dart', 'Julia', 'Lua', 'Haskell', 'Clojure', 'Erlang', 'Elixir'
            ],
            'web_frontend': [
                'HTML', 'CSS', 'React', 'Angular', 'Vue', 'Svelte', 'Bootstrap', 'Tailwind',
                'jQuery', 'SASS', 'SCSS', 'Less', 'Webpack', 'Vite', 'Next.js', 'Nuxt.js',
                'Ember.js', 'Backbone.js', 'D3.js', 'Chart.js', 'Three.js', 'GSAP',
                'Redux', 'MobX', 'Vuex', 'Pinia', 'Storybook', 'Jest', 'Cypress'
            ],
            'web_backend': [
                'Node.js', 'Express', 'Django', 'Flask', 'Spring', 'Laravel', 'Rails',
                'ASP.NET', 'FastAPI', 'Koa', 'Hapi', 'Sails.js', 'Meteor', 'NestJS',
                'Phoenix', 'Gin', 'Echo', 'Fiber', 'Gorilla', 'Chi', 'Gin', 'Echo'
            ],
            'databases': [
                'SQL', 'MySQL', 'PostgreSQL', 'MongoDB', 'Redis', 'Oracle', 'SQLite',
                'Cassandra', 'DynamoDB', 'CouchDB', 'Neo4j', 'Elasticsearch', 'Firebase',
                'MariaDB', 'Couchbase', 'InfluxDB', 'TimescaleDB', 'ClickHouse',
                'ArangoDB', 'RethinkDB', 'CockroachDB', 'PlanetScale'
            ],
            'cloud_devops': [
                'AWS', 'Azure', 'GCP', 'Docker', 'Kubernetes', 'Jenkins', 'GitLab',
                'GitHub Actions', 'Terraform', 'Ansible', 'Chef', 'Puppet', 'Vagrant',
                'CircleCI', 'Travis CI', 'GitHub', 'Bitbucket', 'Heroku', 'DigitalOcean',
                'Vercel', 'Netlify', 'Railway', 'Render', 'Fly.io'
            ],
            'data_science': [
                'Python', 'R', 'Pandas', 'NumPy', 'Scikit-learn', 'TensorFlow', 'PyTorch',
                'Keras', 'Spark', 'Hadoop', 'Jupyter', 'Matplotlib', 'Seaborn', 'Plotly',
                'Apache Airflow', 'Apache Kafka', 'Apache Storm', 'Apache Flink',
                'MLflow', 'Kubeflow', 'Weights & Biases', 'Comet', 'Neptune'
            ],
            'mobile': [
                'React Native', 'Flutter', 'iOS', 'Android', 'Swift', 'Kotlin',
                'Xamarin', 'Ionic', 'Cordova', 'PhoneGap', 'Unity', 'Unreal Engine',
                'Expo', 'NativeScript', 'Appcelerator', 'Sencha Touch'
            ],
            'testing': [
                'Selenium', 'Jest', 'Cypress', 'JUnit', 'Pytest', 'Mocha', 'Chai',
                'Jasmine', 'Karma', 'Protractor', 'TestNG', 'Cucumber', 'Playwright',
                'Detox', 'Appium', 'Espresso', 'XCUITest', 'Robot Framework'
            ],
            'tools': [
                'Git', 'SVN', 'Mercurial', 'Jira', 'Confluence', 'Slack', 'Trello',
                'Asana', 'Figma', 'Sketch', 'Adobe XD', 'Postman', 'Insomnia', 'VS Code',
                'IntelliJ', 'Eclipse', 'PyCharm', 'WebStorm', 'Sublime Text', 'Vim',
                'Notion', 'Linear', 'Monday.com', 'ClickUp', 'Airtable'
            ],
            'soft_skills': [
                'Communication', 'Leadership', 'Teamwork', 'Problem Solving', 'Analytical',
                'Project Management', 'Time Management', 'Critical Thinking', 'Creativity',
                'Adaptability', 'Collaboration', 'Presentation', 'Negotiation', 'Mentoring',
                'Strategic Thinking', 'Innovation', 'Agile', 'Scrum', 'Kanban'
            ],
            'frameworks': [
                'Spring Boot', 'Django', 'Flask', 'Express', 'Laravel', 'Rails', 'Symfony',
                'CodeIgniter', 'CakePHP', 'Zend', 'Hibernate', 'MyBatis', 'JPA',
                'FastAPI', 'Sanic', 'Quart', 'Starlette', 'Uvicorn', 'Gunicorn'
            ],
            'ai_ml': [
                'Machine Learning', 'Deep Learning', 'Neural Networks', 'Computer Vision',
                'Natural Language Processing', 'Reinforcement Learning', 'Transfer Learning',
                'OpenAI', 'Hugging Face', 'LangChain', 'LlamaIndex', 'Pinecone', 'Weaviate'
            ]
        }
    
    def _load_education_keywords(self) -> List[str]:
        """Load education-related keywords"""
        return [
            'bachelor', 'master', 'phd', 'mba', 'btech', 'mtech', 'bca', 'mca', 'diploma',
            'university', 'college', 'institute', 'degree', 'qualification', 'certification',
            'bachelor of', 'master of', 'doctor of', 'associate', 'graduate', 'postgraduate',
            'engineering', 'computer science', 'information technology', 'business administration',
            'electrical', 'mechanical', 'civil', 'chemical', 'aerospace', 'biomedical'
        ]
    
    def _load_experience_patterns(self) -> List[str]:
        """Load experience-related patterns"""
        return [
            r'(\d+)\s*(?:to|-)?\s*(\d+)?\s*(?:years?|yrs?)\s*(?:of\s*)?(?:experience|exp)',
            r'(?:experience|exp)[:\s]*(\d+)\s*(?:to|-)?\s*(\d+)?\s*(?:years?|yrs?)',
            r'(\d+)\+?\s*(?:years?|yrs?)\s*(?:of\s*)?(?:experience|exp)',
            r'(?:total|overall)\s*(?:experience|exp)[:\s]*(\d+)\s*(?:years?|yrs?)',
            r'(\d+)\s*(?:to|-)?\s*(\d+)?\s*(?:years?|yrs?)\s*(?:of\s*)?(?:work|professional)',
            r'(?:work|professional)\s*(?:experience|exp)[:\s]*(\d+)\s*(?:to|-)?\s*(\d+)?\s*(?:years?|yrs?)',
            r'(\d+)\s*(?:to|-)?\s*(\d+)?\s*(?:years?|yrs?)\s*(?:in\s*)?(?:software|development|engineering)',
            r'(?:software|development|engineering)\s*(?:experience|exp)[:\s]*(\d+)\s*(?:to|-)?\s*(\d+)?\s*(?:years?|yrs?)'
        ]
    
    def _load_location_database(self) -> List[str]:
        """Load location database"""
        return [
            'bangalore', 'mumbai', 'delhi', 'hyderabad', 'pune', 'chennai', 'kolkata',
            'ahmedabad', 'gurgaon', 'noida', 'jaipur', 'lucknow', 'indore', 'bhopal',
            'chandigarh', 'coimbatore', 'kochi', 'thiruvananthapuram', 'mysore', 'mangalore',
            'vadodara', 'surat', 'rajkot', 'bhubaneswar', 'bhubaneshwar', 'cuttack',
            'guwahati', 'shillong', 'imphal', 'aizawl', 'kohima', 'itanagar', 'gangtok',
            'new york', 'san francisco', 'los angeles', 'chicago', 'boston', 'seattle',
            'austin', 'denver', 'miami', 'atlanta', 'dallas', 'houston', 'phoenix',
            'london', 'paris', 'berlin', 'madrid', 'rome', 'amsterdam', 'zurich',
            'singapore', 'hong kong', 'tokyo', 'seoul', 'sydney', 'melbourne', 'toronto',
            'vancouver', 'montreal', 'dubai', 'abu dhabi', 'riyadh', 'doha', 'kuwait'
        ]
    
    def extract_resume_content(self, text: str, filename: str = None) -> Dict[str, Any]:
        """Extract resume content using advanced NLP techniques"""
        try:
            logger.info("🚀 Starting advanced resume extraction...")
            
            if not text or len(text.strip()) < 10:
                return self._get_empty_extraction()
            
            # Clean and normalize text
            text_clean = self._clean_text(text)
            
            # Extract components using multiple techniques
            name = self._extract_name_advanced(text_clean, filename)
            email = self._extract_email_advanced(text_clean)
            phone = self._extract_phone_advanced(text_clean)
            skills = self._extract_skills_advanced(text_clean)
            experience = self._extract_experience_advanced(text_clean)
            role = self._extract_role_advanced(text_clean)
            location = self._extract_location_advanced(text_clean)
            education = self._extract_education_advanced(text_clean)
            
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
                'extraction_method': 'advanced_nlp',
                'confidence_score': confidence,
                'extraction_timestamp': datetime.now().isoformat()
            }
            
            logger.info(f"✅ Advanced extraction completed:")
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
            logger.error(f"❌ Error in advanced resume extraction: {e}")
            return self._get_empty_extraction()
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text.strip())
        
        # Remove special characters but keep basic punctuation
        text = re.sub(r'[^\w\s@\.\-\+\(\)]', ' ', text)
        
        # Normalize line breaks
        text = re.sub(r'\n+', '\n', text)
        
        return text
    
    def _extract_name_advanced(self, text: str, filename: str = None) -> str:
        """Extract name using advanced NLP techniques"""
        try:
            # Strategy 1: Extract from filename (most reliable)
            if filename and filename != 'undefined':
                name_from_file = filename.replace('.pdf', '').replace('.docx', '').replace('.doc', '')
                name_from_file = re.sub(r'^(resume|cv|curriculum|vitae)[_\-\s]*', '', name_from_file, flags=re.IGNORECASE)
                name_parts = re.split(r'[_\-\s]+', name_from_file)
                name_parts = [part.strip().title() for part in name_parts if part.strip() and len(part.strip()) > 1]
                if len(name_parts) >= 2:
                    return ' '.join(name_parts)
            
            # Strategy 2: Use spaCy NER
            if self.nlp:
                doc = self.nlp(text[:2000])  # Process first 2000 characters
                for ent in doc.ents:
                    if ent.label_ == "PERSON" and len(ent.text.split()) >= 2:
                        # Validate name format
                        words = ent.text.split()
                        if all(word[0].isupper() for word in words if word):
                            return ent.text.title()
            
            # Strategy 3: Use NLTK NER
            try:
                sentences = sent_tokenize(text[:1000])
                for sentence in sentences:
                    words = word_tokenize(sentence)
                    pos_tags = pos_tag(words)
                    chunks = ne_chunk(pos_tags)
                    
                    for chunk in chunks:
                        if hasattr(chunk, 'label') and chunk.label() == 'PERSON':
                            name = ' '.join([token for token, pos in chunk.leaves()])
                            if len(name.split()) >= 2:
                                return name.title()
            except:
                pass
            
            # Strategy 4: Pattern matching in headers
            lines = text.split('\n')
            for i, line in enumerate(lines[:15]):  # Check first 15 lines
                line = line.strip()
                if len(line) < 3 or len(line) > 60:
                    continue
                
                # Look for name patterns (2-4 words, proper case)
                words = line.split()
                if 2 <= len(words) <= 4:
                    # Check if all words are proper nouns
                    if all(word[0].isupper() for word in words if word):
                        # Skip common non-name words
                        skip_words = {
                            'resume', 'cv', 'curriculum', 'vitae', 'email', 'phone', 'address',
                            'linkedin', 'github', 'objective', 'summary', 'profile', 'experience',
                            'education', 'skills', 'projects', 'certifications', 'contact',
                            'software', 'engineer', 'developer', 'manager', 'analyst'
                        }
                        if not any(word.lower() in skip_words for word in words):
                            return ' '.join(words)
            
            # Strategy 5: Look for "Name:" pattern
            name_patterns = [
                r'name[:\s]+([A-Za-z\s]{2,40})',
                r'full\s*name[:\s]+([A-Za-z\s]{2,40})',
                r'candidate[:\s]+([A-Za-z\s]{2,40})',
                r'first\s*name[:\s]+([A-Za-z\s]{2,40})',
                r'last\s*name[:\s]+([A-Za-z\s]{2,40})'
            ]
            
            for pattern in name_patterns:
                match = re.search(pattern, text, re.IGNORECASE)
                if match:
                    name = match.group(1).strip()
                    if len(name.split()) >= 2:
                        return name.title()
            
            return 'Name not found'
            
        except Exception as e:
            logger.error(f"❌ Name extraction error: {e}")
            return 'Name extraction error'
    
    def _extract_email_advanced(self, text: str) -> str:
        """Extract email using advanced patterns"""
        try:
            # Multiple email patterns
            email_patterns = [
                r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
                r'email[:\s]*([A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,})',
                r'e-mail[:\s]*([A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,})',
                r'contact[:\s]*([A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,})',
                r'mail[:\s]*([A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,})',
                r'id[:\s]*([A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,})'
            ]
            
            emails_found = []
            for pattern in email_patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                for match in matches:
                    email = match.strip() if isinstance(match, str) else match
                    if '@' in email and '.' in email.split('@')[1]:
                        # Validate email format
                        if len(email.split('@')[0]) > 0 and len(email.split('@')[1]) > 0:
                            emails_found.append(email)
            
            if emails_found:
                return emails_found[0]
            
            return 'Email not found'
            
        except Exception as e:
            logger.error(f"❌ Email extraction error: {e}")
            return 'Email extraction error'
    
    def _extract_phone_advanced(self, text: str) -> str:
        """Extract phone using advanced patterns"""
        try:
            # Multiple phone patterns
            phone_patterns = [
                r'(\+91|91)?[-.\s]?\d{5}[-.\s]?\d{5}',  # Indian format
                r'(\+1|1)?[-.\s]?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',  # US format
                r'(\+44|44)?[-.\s]?\d{4}[-.\s]?\d{6}',  # UK format
                r'(\+?\d{1,3}[-.\s]?)?(\(?\d{3}\)?[-.\s]?)?\d{3}[-.\s]?\d{4}',  # Generic
                r'phone[:\s]*(\+?\d{1,3}[-.\s]?)?(\(?\d{3}\)?[-.\s]?)?\d{3}[-.\s]?\d{4}',
                r'mobile[:\s]*(\+?\d{1,3}[-.\s]?)?(\(?\d{3}\)?[-.\s]?)?\d{3}[-.\s]?\d{4}',
                r'contact[:\s]*(\+?\d{1,3}[-.\s]?)?(\(?\d{3}\)?[-.\s]?)?\d{3}[-.\s]?\d{4}',
                r'cell[:\s]*(\+?\d{1,3}[-.\s]?)?(\(?\d{3}\)?[-.\s]?)?\d{3}[-.\s]?\d{4}',
                r'tel[:\s]*(\+?\d{1,3}[-.\s]?)?(\(?\d{3}\)?[-.\s]?)?\d{3}[-.\s]?\d{4}'
            ]
            
            phones_found = []
            for pattern in phone_patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                for match in matches:
                    phone = ''.join(match) if isinstance(match, tuple) else match
                    phone_clean = re.sub(r'[^\d+]', '', phone)  # Keep only digits and +
                    
                    # Validate phone length and format
                    if len(phone_clean) >= 10 and len(phone_clean) <= 15:
                        phones_found.append(phone_clean)
            
            if phones_found:
                return phones_found[0]
            
            return 'Phone not found'
            
        except Exception as e:
            logger.error(f"❌ Phone extraction error: {e}")
            return 'Phone extraction error'
    
    def _extract_skills_advanced(self, text: str) -> List[str]:
        """Extract skills using advanced NLP techniques - only from resume content"""
        try:
            skills = []
            text_lower = text.lower()
            
            # Extract from specific skills sections first (most reliable)
            skill_sections = [
                r'skills?[:\s]*(.*?)(?:\n\n|\n[A-Z]|$)',
                r'technical\s+skills?[:\s]*(.*?)(?:\n\n|\n[A-Z]|$)',
                r'technologies?[:\s]*(.*?)(?:\n\n|\n[A-Z]|$)',
                r'tools?\s+and\s+technologies?[:\s]*(.*?)(?:\n\n|\n[A-Z]|$)',
                r'programming\s+languages?[:\s]*(.*?)(?:\n\n|\n[A-Z]|$)',
                r'frameworks?[:\s]*(.*?)(?:\n\n|\n[A-Z]|$)',
                r'libraries?[:\s]*(.*?)(?:\n\n|\n[A-Z]|$)',
                r'software\s+skills?[:\s]*(.*?)(?:\n\n|\n[A-Z]|$)',
                r'core\s+competencies?[:\s]*(.*?)(?:\n\n|\n[A-Z]|$)',
                r'expertise[:\s]*(.*?)(?:\n\n|\n[A-Z]|$)',
                r'competencies?[:\s]*(.*?)(?:\n\n|\n[A-Z]|$)',
                r'proficiencies?[:\s]*(.*?)(?:\n\n|\n[A-Z]|$)'
            ]
            
            for pattern in skill_sections:
                matches = re.findall(pattern, text, re.IGNORECASE | re.DOTALL)
                for match in matches:
                    section_text = match.lower()
                    for category, skill_list in self.skill_database.items():
                        for skill in skill_list:
                            if skill.lower() in section_text and skill not in skills:
                                skills.append(skill)
            
            # Look for skills in bullet points or lists
            bullet_patterns = [
                r'[•\-\*]\s*([A-Za-z0-9\s\.]+)',
                r'\d+\.\s*([A-Za-z0-9\s\.]+)',
                r'[•\-\*]\s*([A-Za-z0-9\s\.]+)'
            ]
            
            for pattern in bullet_patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                for match in matches:
                    potential_skill = match.strip()
                    if len(potential_skill) > 2 and len(potential_skill) < 30:
                        for category, skill_list in self.skill_database.items():
                            for skill in skill_list:
                                if skill.lower() == potential_skill.lower() and skill not in skills:
                                    skills.append(skill)
            
            # Extract skills from work experience sections
            work_sections = [
                r'work\s+experience[:\s]*(.*?)(?:\n\n|\n[A-Z]|$)',
                r'professional\s+experience[:\s]*(.*?)(?:\n\n|\n[A-Z]|$)',
                r'employment\s+history[:\s]*(.*?)(?:\n\n|\n[A-Z]|$)',
                r'career\s+history[:\s]*(.*?)(?:\n\n|\n[A-Z]|$)',
                r'job\s+history[:\s]*(.*?)(?:\n\n|\n[A-Z]|$)'
            ]
            
            for pattern in work_sections:
                matches = re.findall(pattern, text, re.IGNORECASE | re.DOTALL)
                for match in matches:
                    section_text = match.lower()
                    for category, skill_list in self.skill_database.items():
                        for skill in skill_list:
                            if skill.lower() in section_text and skill not in skills:
                                skills.append(skill)
            
            # Extract skills from projects section
            project_sections = [
                r'projects?[:\s]*(.*?)(?:\n\n|\n[A-Z]|$)',
                r'personal\s+projects?[:\s]*(.*?)(?:\n\n|\n[A-Z]|$)',
                r'academic\s+projects?[:\s]*(.*?)(?:\n\n|\n[A-Z]|$)',
                r'professional\s+projects?[:\s]*(.*?)(?:\n\n|\n[A-Z]|$)'
            ]
            
            for pattern in project_sections:
                matches = re.findall(pattern, text, re.IGNORECASE | re.DOTALL)
                for match in matches:
                    section_text = match.lower()
                    for category, skill_list in self.skill_database.items():
                        for skill in skill_list:
                            if skill.lower() in section_text and skill not in skills:
                                skills.append(skill)
            
            # Only extract from resume content, not random text
            # Remove skills that appear in education sections (likely not technical skills)
            education_sections = [
                r'education[:\s]*(.*?)(?:\n\n|\n[A-Z]|$)',
                r'academic\s+qualifications?[:\s]*(.*?)(?:\n\n|\n[A-Z]|$)',
                r'degrees?[:\s]*(.*?)(?:\n\n|\n[A-Z]|$)',
                r'qualifications?[:\s]*(.*?)(?:\n\n|\n[A-Z]|$)'
            ]
            
            education_text = ""
            for pattern in education_sections:
                matches = re.findall(pattern, text, re.IGNORECASE | re.DOTALL)
                for match in matches:
                    education_text += match.lower() + " "
            
            # Filter out skills that appear only in education sections
            filtered_skills = []
            for skill in skills:
                skill_lower = skill.lower()
                # Check if skill appears in non-education sections
                non_education_text = text_lower.replace(education_text, "")
                if skill_lower in non_education_text:
                    filtered_skills.append(skill)
            
            skills = filtered_skills
            
            # Remove duplicates and limit results
            skills = list(set(skills))
            skills = skills[:25]  # Reduced limit to focus on actual skills
            
            return skills
            
        except Exception as e:
            logger.error(f"❌ Skills extraction error: {e}")
            return []
    
    def _extract_experience_advanced(self, text: str) -> Dict[str, Any]:
        """Extract experience using advanced techniques - improved accuracy"""
        try:
            text_lower = text.lower()
            experience_years = 0
            
            # Enhanced pattern-based extraction
            enhanced_patterns = [
                r'(\d+)\s*(?:to|-)?\s*(\d+)?\s*(?:years?|yrs?)\s*(?:of\s*)?(?:experience|exp)',
                r'(?:experience|exp)[:\s]*(\d+)\s*(?:to|-)?\s*(\d+)?\s*(?:years?|yrs?)',
                r'(\d+)\+?\s*(?:years?|yrs?)\s*(?:of\s*)?(?:experience|exp)',
                r'(?:total|overall)\s*(?:experience|exp)[:\s]*(\d+)\s*(?:years?|yrs?)',
                r'(\d+)\s*(?:to|-)?\s*(\d+)?\s*(?:years?|yrs?)\s*(?:of\s*)?(?:work|professional)',
                r'(?:work|professional)\s*(?:experience|exp)[:\s]*(\d+)\s*(?:to|-)?\s*(\d+)?\s*(?:years?|yrs?)',
                r'(\d+)\s*(?:to|-)?\s*(\d+)?\s*(?:years?|yrs?)\s*(?:in\s*)?(?:software|development|engineering)',
                r'(?:software|development|engineering)\s*(?:experience|exp)[:\s]*(\d+)\s*(?:to|-)?\s*(\d+)?\s*(?:years?|yrs?)',
                r'(?:since|from)\s+\d{4}.*?(?:years?|yrs?)',
                r'(?:over|more\s+than)\s+(\d+)\s*(?:years?|yrs?)',
                r'(\d+)\s*(?:years?|yrs?)\s*(?:plus|and\s+above)'
            ]
            
            for pattern in enhanced_patterns:
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
            
            # Date-based calculation (improved)
            if experience_years == 0:
                experience_years = self._calculate_experience_from_dates_enhanced(text)
            
            # Job title indicators (improved)
            if experience_years == 0:
                experience_indicators = {
                    'senior': 5, 'lead': 6, 'principal': 8, 'staff': 7, 'architect': 8,
                    'manager': 5, 'director': 8, 'vp': 10, 'cto': 12, 'head': 6,
                    'junior': 1, 'associate': 2, 'entry': 0, 'fresher': 0, 'intern': 0,
                    'trainee': 0, 'graduate': 0, 'new grad': 0, 'student': 0
                }
                
                for indicator, years in experience_indicators.items():
                    if indicator in text_lower:
                        experience_years = years
                        break
            
            # Look for experience in work history sections
            if experience_years == 0:
                experience_years = self._extract_experience_from_work_history(text)
            
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
                r'(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)\s+\d{4}\s*(?:to|-)?\s*(?:present|current|now|(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)\s+\d{4})',
                r'\d{1,2}/\d{4}\s*(?:to|-)?\s*(?:present|current|now|\d{1,2}/\d{4})',
                r'\d{1,2}-\d{4}\s*(?:to|-)?\s*(?:present|current|now|\d{1,2}-\d{4})'
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
    
    def _calculate_experience_from_dates_enhanced(self, text: str) -> int:
        """Enhanced experience calculation from work history dates"""
        try:
            # Enhanced date patterns
            date_patterns = [
                r'(\d{4})\s*(?:to|-)?\s*(?:present|current|now|\d{4})',
                r'(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)\s+\d{4}\s*(?:to|-)?\s*(?:present|current|now|(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)\s+\d{4})',
                r'\d{1,2}/\d{4}\s*(?:to|-)?\s*(?:present|current|now|\d{1,2}/\d{4})',
                r'\d{1,2}-\d{4}\s*(?:to|-)?\s*(?:present|current|now|\d{1,2}-\d{4})',
                r'(?:since|from)\s+(\d{4})',
                r'(?:started|began)\s+(?:in\s+)?(\d{4})',
                r'(?:joined|employed)\s+(?:in\s+)?(\d{4})'
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
                        current_year = datetime.now().year
                        # If no end date, assume current year
                        if len(years) == 1:
                            years.append(current_year)
                        return max(years) - min(years)
                except:
                    pass
            
            return 0
            
        except Exception as e:
            logger.error(f"❌ Enhanced date calculation error: {e}")
            return 0
    
    def _extract_experience_from_work_history(self, text: str) -> int:
        """Extract experience from work history sections"""
        try:
            # Look for work experience sections
            work_sections = [
                r'work\s+experience[:\s]*(.*?)(?:\n\n|\n[A-Z]|$)',
                r'professional\s+experience[:\s]*(.*?)(?:\n\n|\n[A-Z]|$)',
                r'employment\s+history[:\s]*(.*?)(?:\n\n|\n[A-Z]|$)',
                r'career\s+history[:\s]*(.*?)(?:\n\n|\n[A-Z]|$)',
                r'job\s+history[:\s]*(.*?)(?:\n\n|\n[A-Z]|$)'
            ]
            
            for pattern in work_sections:
                matches = re.findall(pattern, text, re.IGNORECASE | re.DOTALL)
                for match in matches:
                    section_text = match.lower()
                    # Count years mentioned in this section
                    year_matches = re.findall(r'\b(19|20)\d{2}\b', section_text)
                    if len(year_matches) >= 2:
                        years = [int(year) for year in year_matches]
                        return max(years) - min(years)
            
            return 0
            
        except Exception as e:
            logger.error(f"❌ Work history extraction error: {e}")
            return 0
    
    def _extract_role_advanced(self, text: str) -> str:
        """Extract role using advanced NLP techniques - fixed to avoid name contamination"""
        try:
            # First, extract potential names to exclude them from role extraction
            potential_names = set()
            
            # Extract names using spaCy
            if self.nlp:
                doc = self.nlp(text[:2000])
                for ent in doc.ents:
                    if ent.label_ == "PERSON":
                        potential_names.add(ent.text.lower())
            
            # Extract names using NLTK
            try:
                sentences = sent_tokenize(text[:1000])
                for sentence in sentences:
                    words = word_tokenize(sentence)
                    pos_tags = pos_tag(words)
                    chunks = ne_chunk(pos_tags)
                    
                    for chunk in chunks:
                        if hasattr(chunk, 'label') and chunk.label() == 'PERSON':
                            name = ' '.join([token for token, pos in chunk.leaves()])
                            potential_names.add(name.lower())
            except:
                pass
            
            # Look for role in work experience section first (most reliable)
            work_section_patterns = [
                r'(?:worked\s+as|position\s+of|role\s+of|designation\s+of|currently\s+working\s+as|presently\s+working\s+as)\s+([A-Za-z\s]{3,60})',
                r'([A-Za-z\s]{3,60})\s+(?:developer|engineer|manager|analyst|consultant|specialist|architect|programmer)',
                r'(?:as\s+a\s+|as\s+an\s+|as\s+)\s*([A-Za-z\s]{3,60})',
                r'(?:job\s+title|position|role|title)[:\s]*([A-Za-z\s]{3,60})'
            ]
            
            for pattern in work_section_patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                for match in matches:
                    role = match.strip()
                    if len(role.split()) >= 2:
                        # Check if role contains a potential name
                        role_words = role.lower().split()
                        if not any(word in potential_names for word in role_words):
                            return role.title()
            
            # Common role patterns (excluding names)
            role_patterns = [
                r'(?:Software|Web|Frontend|Backend|Full.?Stack|Mobile|DevOps|Data|Machine Learning|AI)\s+(?:Developer|Engineer|Programmer|Architect|Consultant|Manager|Analyst|Scientist)',
                r'(?:Senior|Junior|Lead|Principal|Staff)\s+(?:Developer|Engineer|Programmer|Architect|Consultant|Manager|Analyst|Scientist)',
                r'(?:Project|Product|Business|System|Data|QA|Test)\s+(?:Manager|Analyst|Engineer|Consultant)',
                r'(?:UI|UX|Graphic|Web|Product)\s+(?:Designer|Developer|Engineer)',
                r'(?:Database|System|Network|IT)\s+(?:Administrator|Engineer|Specialist)',
                r'(?:Cloud|AWS|Azure|GCP)\s+(?:Engineer|Architect|Consultant|Specialist)',
                r'(?:Security|Cybersecurity)\s+(?:Engineer|Analyst|Consultant|Specialist)',
                r'(?:Data|Analytics|Business)\s+(?:Analyst|Scientist|Engineer|Consultant)',
                r'(?:Sales|Marketing|Business)\s+(?:Manager|Executive|Representative|Specialist)',
                r'(?:HR|Human Resources)\s+(?:Manager|Specialist|Executive|Consultant)',
                r'(?:Finance|Accounting)\s+(?:Manager|Analyst|Specialist|Consultant)',
                r'(?:Operations|Operations)\s+(?:Manager|Specialist|Analyst|Consultant)'
            ]
            
            for pattern in role_patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                for match in matches:
                    # Check if match contains a potential name
                    match_words = match.lower().split()
                    if not any(word in potential_names for word in match_words):
                        return match.title()
            
            # Look for role in job titles or headers (excluding names)
            lines = text.split('\n')
            for line in lines[:20]:  # Check first 20 lines
                line = line.strip()
                if len(line) < 5 or len(line) > 80:
                    continue
                    
                # Check if line contains role indicators
                role_indicators = [
                    'developer', 'engineer', 'manager', 'analyst', 'consultant', 'specialist',
                    'architect', 'scientist', 'designer', 'programmer', 'administrator'
                ]
                
                line_lower = line.lower()
                if any(indicator in line_lower for indicator in role_indicators):
                    # Check if it's a proper role format
                    words = line.split()
                    if 2 <= len(words) <= 6:
                        # Check if it starts with a capital letter and doesn't contain names
                        if words[0][0].isupper():
                            line_words = line.lower().split()
                            if not any(word in potential_names for word in line_words):
                                return line.title()
            
            return 'Role not found'
            
        except Exception as e:
            logger.error(f"❌ Role extraction error: {e}")
            return 'Role extraction error'
    
    def _extract_location_advanced(self, text: str) -> str:
        """Extract location using advanced NLP techniques - improved accuracy"""
        try:
            # First, extract potential names to exclude them from location extraction
            potential_names = set()
            
            # Extract names using spaCy
            if self.nlp:
                doc = self.nlp(text[:2000])
                for ent in doc.ents:
                    if ent.label_ == "PERSON":
                        potential_names.add(ent.text.lower())
            
            # Use spaCy NER for locations
            if self.nlp:
                doc = self.nlp(text[:2000])
                for ent in doc.ents:
                    if ent.label_ == "GPE":  # Geopolitical entity
                        # Check if it's not a person's name
                        if ent.text.lower() not in potential_names:
                            return ent.text.title()
            
            # Use NLTK NER
            try:
                sentences = sent_tokenize(text[:1000])
                for sentence in sentences:
                    words = word_tokenize(sentence)
                    pos_tags = pos_tag(words)
                    chunks = ne_chunk(pos_tags)
                    
                    for chunk in chunks:
                        if hasattr(chunk, 'label') and chunk.label() == 'GPE':
                            location = ' '.join([token for token, pos in chunk.leaves()])
                            if location.lower() in self.location_database and location.lower() not in potential_names:
                                return location.title()
            except:
                pass
            
            # Pattern-based extraction (improved)
            location_patterns = [
                r'location[:\s]*([A-Za-z\s]{3,40})',
                r'address[:\s]*([A-Za-z\s]{3,40})',
                r'city[:\s]*([A-Za-z\s]{3,40})',
                r'based\s+in[:\s]*([A-Za-z\s]{3,40})',
                r'located\s+in[:\s]*([A-Za-z\s]{3,40})',
                r'residing\s+in[:\s]*([A-Za-z\s]{3,40})',
                r'from[:\s]*([A-Za-z\s]{3,40})',
                r'lives\s+in[:\s]*([A-Za-z\s]{3,40})',
                r'stays\s+in[:\s]*([A-Za-z\s]{3,40})'
            ]
            
            for pattern in location_patterns:
                match = re.search(pattern, text, re.IGNORECASE)
                if match:
                    location = match.group(1).strip()
                    if len(location.split()) >= 1:
                        # Check if it's not a person's name
                        if location.lower() not in potential_names:
                            return location.title()
            
            # Look for known locations in text (excluding names)
            text_lower = text.lower()
            for location in self.location_database:
                if location in text_lower and location not in potential_names:
                    return location.title()
            
            # Look for location in contact information section
            contact_sections = [
                r'contact\s+information[:\s]*(.*?)(?:\n\n|\n[A-Z]|$)',
                r'personal\s+information[:\s]*(.*?)(?:\n\n|\n[A-Z]|$)',
                r'address[:\s]*(.*?)(?:\n\n|\n[A-Z]|$)'
            ]
            
            for pattern in contact_sections:
                matches = re.findall(pattern, text, re.IGNORECASE | re.DOTALL)
                for match in matches:
                    section_text = match.lower()
                    for location in self.location_database:
                        if location in section_text and location not in potential_names:
                            return location.title()
            
            return 'Location not found'
            
        except Exception as e:
            logger.error(f"❌ Location extraction error: {e}")
            return 'Location extraction error'
    
    def _extract_education_advanced(self, text: str) -> List[str]:
        """Extract education using advanced techniques - removed as requested"""
        try:
            # Return empty list as education extraction is not needed
            return []
            
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
                confidence += min(0.3, len(skills) * 0.01)
            
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

# Initialize global advanced extractor instance
advanced_extractor = AdvancedResumeExtractor()
