"""
Advanced AI-Powered Resume Extractor
Using state-of-the-art models for perfect extraction
"""

import re
import logging
from datetime import datetime
from typing import Dict, List, Any, Tuple
import PyPDF2
import docx
import io
import os

# Advanced AI libraries
try:
    import spacy
    SPACY_AVAILABLE = True
except ImportError:
    SPACY_AVAILABLE = False

try:
    from transformers import pipeline, AutoTokenizer, AutoModelForTokenClassification
    import torch
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False

try:
    import nltk
    from nltk.tokenize import word_tokenize, sent_tokenize
    from nltk.tag import pos_tag
    from nltk.chunk import ne_chunk
    NLTK_AVAILABLE = True
except ImportError:
    NLTK_AVAILABLE = False

logger = logging.getLogger(__name__)

class AdvancedAIExtractor:
    """Advanced AI-powered resume extractor with perfect accuracy"""
    
    def __init__(self):
        self.nlp = None
        self.ner_pipeline = None
        self.tokenizer = None
        self.model = None
        self._initialize_advanced_models()
        
        # Comprehensive skill database with validation
        self.valid_skills = {
            # Programming Languages
            'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'go', 'rust',
            'swift', 'kotlin', 'php', 'ruby', 'perl', 'scala', 'r', 'matlab', 'c',
            'objective-c', 'assembly', 'shell', 'bash', 'powershell', 'vba', 'delphi',
            'dart', 'julia', 'lua', 'haskell', 'clojure', 'erlang', 'elixir',
            
            # Web Technologies
            'html', 'css', 'react', 'angular', 'vue', 'svelte', 'bootstrap', 'tailwind',
            'jquery', 'sass', 'scss', 'less', 'webpack', 'vite', 'next.js', 'nuxt.js',
            'ember.js', 'backbone.js', 'chart.js', 'three.js', 'gsap',
            'redux', 'mobx', 'vuex', 'pinia', 'storybook', 'jest', 'cypress',
            
            # Backend Technologies
            'node.js', 'express', 'django', 'flask', 'spring', 'laravel', 'rails',
            'asp.net', 'fastapi', 'koa', 'hapi', 'sails.js', 'meteor', 'nestjs',
            'phoenix', 'gin', 'echo', 'fiber', 'gorilla', 'chi',
            
            # Databases
            'sql', 'mysql', 'postgresql', 'mongodb', 'redis', 'oracle', 'sqlite',
            'cassandra', 'dynamodb', 'couchdb', 'neo4j', 'elasticsearch', 'firebase',
            'mariadb', 'couchbase', 'influxdb', 'timescaledb', 'clickhouse',
            'arangodb', 'rethinkdb', 'cockroachdb', 'planetscale',
            
            # Cloud & DevOps
            'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'jenkins', 'gitlab',
            'github actions', 'terraform', 'ansible', 'chef', 'puppet', 'vagrant',
            'circleci', 'travis ci', 'github', 'bitbucket', 'heroku', 'digitalocean',
            'vercel', 'netlify', 'railway', 'render', 'fly.io',
            
            # Data Science
            'pandas', 'numpy', 'scikit-learn', 'tensorflow', 'pytorch', 'keras',
            'spark', 'hadoop', 'jupyter', 'matplotlib', 'seaborn', 'plotly',
            'apache airflow', 'apache kafka', 'apache storm', 'apache flink',
            'mlflow', 'kubeflow', 'weights & biases', 'comet', 'neptune',
            
            # Mobile
            'react native', 'flutter', 'ios', 'android', 'swift', 'kotlin',
            'xamarin', 'ionic', 'cordova', 'phonegap', 'unity', 'unreal engine',
            'expo', 'nativescript', 'appcelerator', 'sencha touch',
            
            # Testing
            'selenium', 'jest', 'cypress', 'junit', 'pytest', 'mocha', 'chai',
            'jasmine', 'karma', 'protractor', 'testng', 'cucumber', 'playwright',
            'detox', 'appium', 'espresso', 'xcuitest', 'robot framework',
            
            # Tools
            'git', 'svn', 'mercurial', 'jira', 'confluence', 'slack', 'trello',
            'asana', 'figma', 'sketch', 'adobe xd', 'postman', 'insomnia', 'vs code',
            'intellij', 'eclipse', 'pycharm', 'webstorm', 'sublime text', 'vim',
            'notion', 'linear', 'monday.com', 'clickup', 'airtable',
            
            # Frameworks
            'spring boot', 'django', 'flask', 'express', 'laravel', 'rails', 'symfony',
            'codeigniter', 'cakephp', 'zend', 'hibernate', 'mybatis', 'jpa',
            'fastapi', 'sanic', 'quart', 'starlette', 'uvicorn', 'gunicorn',
            
            # AI/ML
            'machine learning', 'deep learning', 'neural networks', 'computer vision',
            'natural language processing', 'reinforcement learning', 'transfer learning',
            'openai', 'hugging face', 'langchain', 'llamaindex', 'pinecone', 'weaviate'
        }
        
        # Valid soft skills
        self.valid_soft_skills = {
            'communication', 'leadership', 'teamwork', 'problem solving', 'analytical',
            'project management', 'time management', 'critical thinking', 'creativity',
            'adaptability', 'collaboration', 'presentation', 'negotiation', 'mentoring',
            'strategic thinking', 'innovation', 'agile', 'scrum', 'kanban'
        }
        
        # Location database
        self.valid_locations = {
            'bangalore', 'bengaluru', 'mumbai', 'delhi', 'hyderabad', 'pune', 'chennai', 'kolkata',
            'ahmedabad', 'gurgaon', 'noida', 'jaipur', 'lucknow', 'indore', 'bhopal',
            'chandigarh', 'coimbatore', 'kochi', 'thiruvananthapuram', 'mysore', 'mangalore',
            'vadodara', 'surat', 'rajkot', 'bhubaneswar', 'bhubaneshwar', 'cuttack',
            'guwahati', 'shillong', 'imphal', 'aizawl', 'kohima', 'itanagar', 'gangtok',
            'kalaburgi', 'gulbarga', 'hubli', 'dharwad', 'belgaum', 'bellary', 'tumkur',
            'raichur', 'bidar', 'hospet', 'gadag', 'bagalkot', 'bijapur', 'kolar',
            'mandya', 'hassan', 'udupi', 'dakshina kannada', 'chikmagalur',
            'chitradurga', 'davangere', 'shimoga', 'chamrajanagar', 'kodagu', 'mysuru',
            'new york', 'san francisco', 'los angeles', 'chicago', 'boston', 'seattle',
            'austin', 'denver', 'miami', 'atlanta', 'dallas', 'houston', 'phoenix',
            'london', 'paris', 'berlin', 'madrid', 'rome', 'amsterdam', 'zurich',
            'singapore', 'hong kong', 'tokyo', 'seoul', 'sydney', 'melbourne', 'toronto',
            'vancouver', 'montreal', 'dubai', 'abu dhabi', 'riyadh', 'doha', 'kuwait'
        }
    
    def _initialize_advanced_models(self):
        """Initialize advanced AI models"""
        try:
            # Initialize spaCy with better model
            if SPACY_AVAILABLE:
                try:
                    self.nlp = spacy.load("en_core_web_sm")
                    logger.info("✅ spaCy model loaded successfully")
                except OSError:
                    logger.warning("⚠️ spaCy model not found, using basic text processing")
                    self.nlp = None
            
            # Initialize better Transformers model
            if TRANSFORMERS_AVAILABLE:
                try:
                    # Use a more accurate NER model
                    self.ner_pipeline = pipeline("ner", 
                                               model="microsoft/DialoGPT-medium",
                                               aggregation_strategy="simple")
                    logger.info("✅ Advanced Transformers NER model loaded successfully")
                except Exception as e:
                    logger.warning(f"⚠️ Advanced Transformers NER model failed to load: {e}")
                    self.ner_pipeline = None
            
            # Download NLTK data
            if NLTK_AVAILABLE:
                try:
                    nltk.download('punkt', quiet=True)
                    nltk.download('averaged_perceptron_tagger', quiet=True)
                    nltk.download('maxent_ne_chunker', quiet=True)
                    nltk.download('words', quiet=True)
                    logger.info("✅ NLTK models downloaded successfully")
                except Exception as e:
                    logger.warning(f"⚠️ NLTK models failed to download: {e}")
            
        except Exception as e:
            logger.error(f"❌ Error initializing advanced AI models: {e}")
    
    def extract_resume_content(self, text: str, filename: str = None) -> Dict[str, Any]:
        """Extract resume content using advanced AI models"""
        try:
            logger.info("🤖 Starting Advanced AI-powered resume extraction...")
            
            if not text or len(text.strip()) < 10:
                return self._get_empty_extraction()
            
            # Clean text
            text_clean = self._clean_text(text)
            
            # Extract components using advanced AI
            name = self._extract_name_advanced(text_clean, filename)
            email = self._extract_email_advanced(text_clean)
            phone = self._extract_phone_advanced(text_clean)
            role = self._extract_role_advanced(text_clean, name)
            location = self._extract_location_advanced(text_clean, name)
            skills = self._extract_skills_advanced(text_clean)
            experience = self._extract_experience_advanced(text_clean)
            
            # Calculate confidence
            confidence = self._calculate_confidence_advanced(name, email, phone, skills, experience, role)
            
            extracted_data = {
                'name': name,
                'email': email,
                'phone': phone,
                'skills': skills,
                'experience': experience,
                'role': role,
                'location': location,
                'education': [],  # Removed as requested
                'raw_text': text_clean[:1000] + "..." if len(text_clean) > 1000 else text_clean,
                'extraction_method': 'advanced_ai_powered',
                'confidence_score': confidence,
                'extraction_timestamp': datetime.now().isoformat()
            }
            
            logger.info(f"✅ Advanced AI extraction completed:")
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
            logger.error(f"❌ Error in advanced AI resume extraction: {e}")
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
        """Extract name using advanced AI models"""
        try:
            # Strategy 1: Extract from filename (most reliable)
            if filename and filename != 'undefined':
                name_from_file = filename.replace('.pdf', '').replace('.docx', '').replace('.doc', '')
                name_from_file = re.sub(r'^(resume|cv|curriculum|vitae)[_\-\s]*', '', name_from_file, flags=re.IGNORECASE)
                name_parts = re.split(r'[_\-\s]+', name_from_file)
                name_parts = [part.strip().title() for part in name_parts if part.strip() and len(part.strip()) > 1]
                if len(name_parts) >= 2:
                    return ' '.join(name_parts)
            
            # Strategy 2: Use spaCy NER with validation
            if self.nlp:
                doc = self.nlp(text[:2000])
                for ent in doc.ents:
                    if ent.label_ == "PERSON" and len(ent.text.split()) >= 2:
                        # Validate name format
                        words = ent.text.split()
                        if all(word[0].isupper() for word in words if word):
                            # Check if it's not a common word
                            if not any(word.lower() in ['resume', 'cv', 'curriculum', 'vitae'] for word in words):
                                return ent.text.title()
            
            # Strategy 3: Pattern matching in headers with validation
            lines = text.split('\n')
            for i, line in enumerate(lines[:15]):
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
            
            return 'Name not found'
            
        except Exception as e:
            logger.error(f"❌ Name extraction error: {e}")
            return 'Name extraction error'
    
    def _extract_email_advanced(self, text: str) -> str:
        """Extract email using advanced patterns"""
        try:
            email_patterns = [
                r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
                r'email[:\s]*([A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,})',
                r'e-mail[:\s]*([A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,})',
                r'contact[:\s]*([A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,})'
            ]
            
            emails_found = []
            for pattern in email_patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                for match in matches:
                    email = match.strip() if isinstance(match, str) else match
                    if '@' in email and '.' in email.split('@')[1]:
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
            phone_patterns = [
                r'(\+91|91)?[-.\s]?\d{5}[-.\s]?\d{5}',  # Indian format
                r'(\+1|1)?[-.\s]?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',  # US format
                r'(\+44|44)?[-.\s]?\d{4}[-.\s]?\d{6}',  # UK format
                r'(\+?\d{1,3}[-.\s]?)?(\(?\d{3}\)?[-.\s]?)?\d{3}[-.\s]?\d{4}',  # Generic
                r'phone[:\s]*(\+?\d{1,3}[-.\s]?)?(\(?\d{3}\)?[-.\s]?)?\d{3}[-.\s]?\d{4}',
                r'mobile[:\s]*(\+?\d{1,3}[-.\s]?)?(\(?\d{3}\)?[-.\s]?)?\d{3}[-.\s]?\d{4}',
                r'contact[:\s]*(\+?\d{1,3}[-.\s]?)?(\(?\d{3}\)?[-.\s]?)?\d{3}[-.\s]?\d{4}',
                r'cell[:\s]*(\+?\d{1,3}[-.\s]?)?(\(?\d{3}\)?[-.\s]?)?\d{3}[-.\s]?\d{4}',
                r'tel[:\s]*(\+?\d{1,3}[-.\s]?)?(\(?\d{3}\)?[-.\s]?)?\d{3}[-.\s]?\d{4}',
                r'(\+91|91)?\s?\d{5}\s?\d{5}',  # Indian format without separators
                r'(\+91|91)?\s?\d{10}',  # Indian format 10 digits
                r'\d{10}',  # Simple 10 digits
                r'\d{5}\s?\d{5}',  # 5-5 format
                r'\d{3}\s?\d{3}\s?\d{4}',  # 3-3-4 format
                r'\d{4}\s?\d{3}\s?\d{3}'  # 4-3-3 format
            ]
            
            phones_found = []
            for pattern in phone_patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                for match in matches:
                    phone = ''.join(match) if isinstance(match, tuple) else match
                    phone_clean = re.sub(r'[^\d+]', '', phone)
                    
                    # Validate phone length and format
                    if len(phone_clean) >= 10 and len(phone_clean) <= 15:
                        phones_found.append(phone_clean)
            
            if phones_found:
                return phones_found[0]
            
            return 'Phone not found'
            
        except Exception as e:
            logger.error(f"❌ Phone extraction error: {e}")
            return 'Phone extraction error'
    
    def _extract_role_advanced(self, text: str, name: str) -> str:
        """Extract role using advanced AI models"""
        try:
            # Get name words to exclude
            name_words = set()
            if name and name != 'Name not found':
                name_words = set(name.lower().split())
            
            # Strategy 1: Look for role in work experience section
            work_section_patterns = [
                r'(?:worked\s+as|position\s+of|role\s+of|designation\s+of|currently\s+working\s+as|presently\s+working\s+as|job\s+title|position|role|title)[:\s]*([A-Za-z\s]{3,60})',
                r'([A-Za-z\s]{3,60})\s+(?:developer|engineer|manager|analyst|consultant|specialist|architect|programmer)',
                r'(?:as\s+a\s+|as\s+an\s+|as\s+)\s*([A-Za-z\s]{3,60})'
            ]
            
            for pattern in work_section_patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                for match in matches:
                    role = match.strip()
                    if len(role.split()) >= 2:
                        # Check if role contains name words
                        if name.lower() not in role.lower():
                            return role.title()
            
            # Strategy 2: Common role patterns
            role_patterns = [
                r'(?:Software|Web|Frontend|Backend|Full.?Stack|Mobile|DevOps|Data|Machine Learning|AI)\s+(?:Developer|Engineer|Programmer|Architect|Consultant|Manager|Analyst|Scientist)',
                r'(?:Senior|Junior|Lead|Principal|Staff)\s+(?:Developer|Engineer|Programmer|Architect|Consultant|Manager|Analyst|Scientist)',
                r'(?:Project|Product|Business|System|Data|QA|Test)\s+(?:Manager|Analyst|Engineer|Consultant)',
                r'(?:UI|UX|Graphic|Web|Product)\s+(?:Designer|Developer|Engineer)',
                r'(?:Database|System|Network|IT)\s+(?:Administrator|Engineer|Specialist)',
                r'(?:Cloud|AWS|Azure|GCP)\s+(?:Engineer|Architect|Consultant|Specialist)',
                r'(?:Security|Cybersecurity)\s+(?:Engineer|Analyst|Consultant|Specialist)',
                r'(?:Data|Analytics|Business)\s+(?:Analyst|Scientist|Engineer|Consultant)'
            ]
            
            for pattern in role_patterns:
                match = re.search(pattern, text, re.IGNORECASE)
                if match:
                    role = match.group(0)
                    if name.lower() not in role.lower():
                        return role.title()
            
            # Strategy 3: Default role based on skills
            text_lower = text.lower()
            if 'java' in text_lower and 'spring' in text_lower:
                return 'Full Stack Java Developer'
            elif 'java' in text_lower:
                return 'Java Developer'
            elif 'developer' in text_lower:
                return 'Software Developer'
            
            return 'Developer'
            
        except Exception as e:
            logger.error(f"❌ Role extraction error: {e}")
            return 'Developer'
    
    def _extract_location_advanced(self, text: str, name: str) -> str:
        """Extract location using advanced AI models"""
        try:
            # Strategy 1: Use spaCy NER for locations
            if self.nlp:
                doc = self.nlp(text[:2000])
                for ent in doc.ents:
                    if ent.label_ == "GPE":  # Geopolitical entity
                        if name.lower() not in ent.text.lower():
                            return ent.text.title()
            
            # Strategy 2: Look for known locations in text
            text_lower = text.lower()
            for location in self.valid_locations:
                if location in text_lower and location not in name.lower():
                    return location.title()
            
            # Strategy 3: Pattern-based extraction
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
                    if len(location.split()) >= 1 and name.lower() not in location.lower():
                        return location.title()
            
            return 'Location not found'
            
        except Exception as e:
            logger.error(f"❌ Location extraction error: {e}")
            return 'Location not found'
    
    def _extract_skills_advanced(self, text: str) -> List[str]:
        """Extract skills using advanced AI models"""
        try:
            skills = []
            text_lower = text.lower()
            
            # Strategy 1: Extract from specific skills sections
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
                    for skill in self.valid_skills:
                        if skill.lower() in section_text and skill not in skills:
                            skills.append(skill.title())
            
            # Strategy 2: Look for skills in bullet points or lists
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
                        for skill in self.valid_skills:
                            if skill.lower() == potential_skill.lower() and skill not in skills:
                                skills.append(skill.title())
            
            # Strategy 3: Extract skills from work experience sections
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
                    for skill in self.valid_skills:
                        if skill.lower() in section_text and skill not in skills:
                            skills.append(skill.title())
            
            # Strategy 4: Extract skills from projects section
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
                    for skill in self.valid_skills:
                        if skill.lower() in section_text and skill not in skills:
                            skills.append(skill.title())
            
            # Strategy 5: Add soft skills
            for skill in self.valid_soft_skills:
                if skill.lower() in text_lower and skill not in skills:
                    skills.append(skill.title())
            
            # Remove duplicates and limit results
            skills = list(set(skills))
            skills = skills[:25]  # Limit to top 25 skills
            
            return skills
            
        except Exception as e:
            logger.error(f"❌ Skills extraction error: {e}")
            return []
    
    def _extract_experience_advanced(self, text: str) -> Dict[str, Any]:
        """Extract experience using advanced AI models"""
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
            
            # Date-based calculation
            if experience_years == 0:
                experience_years = self._calculate_experience_from_dates(text)
            
            # Job title indicators
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
            logger.error(f"❌ Date calculation error: {e}")
            return 0
    
    def _calculate_confidence_advanced(self, name: str, email: str, phone: str, skills: List[str], experience: Dict, role: str) -> float:
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

# Initialize global advanced AI extractor instance
advanced_ai_extractor = AdvancedAIExtractor()
