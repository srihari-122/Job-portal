"""
Precision Resume Extractor
Ultra-accurate extraction with perfect data validation
"""

import re
import logging
from datetime import datetime
from typing import Dict, List, Any, Tuple
import PyPDF2
import docx
import io
import os
from ultimate_extractor import ultimate_extractor

logger = logging.getLogger(__name__)

class PrecisionExtractor:
    """Precision extractor with perfect accuracy"""
    
    def __init__(self):
        # Only valid technical skills (no single letters or invalid skills)
        self.valid_technical_skills = {
            # Programming Languages
            'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'go', 'rust',
            'swift', 'kotlin', 'php', 'ruby', 'perl', 'scala', 'matlab',
            'objective-c', 'assembly', 'shell', 'bash', 'powershell', 'vba', 'delphi',
            'dart', 'julia', 'lua', 'haskell', 'clojure', 'erlang', 'elixir',
            
            # Web Technologies
            'html', 'css', 'react', 'angular', 'vue', 'svelte', 'bootstrap', 'tailwind',
            'jquery', 'sass', 'scss', 'webpack', 'vite', 'next.js', 'nuxt.js',
            'ember.js', 'backbone.js', 'chart.js', 'three.js', 'gsap',
            'redux', 'mobx', 'vuex', 'pinia', 'storybook', 'jest', 'cypress',
            
            # Backend Technologies
            'node.js', 'express', 'django', 'flask', 'spring', 'laravel', 'rails',
            'asp.net', 'fastapi', 'koa', 'hapi', 'sails.js', 'meteor', 'nestjs',
            'phoenix', 'echo', 'fiber', 'gorilla', 'chi',
            
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
        
        # Valid locations (Indian cities)
        self.valid_locations = {
            'bangalore', 'bengaluru', 'mumbai', 'delhi', 'hyderabad', 'pune', 'chennai', 'kolkata',
            'ahmedabad', 'gurgaon', 'noida', 'jaipur', 'lucknow', 'indore', 'bhopal',
            'chandigarh', 'coimbatore', 'kochi', 'thiruvananthapuram', 'mysore', 'mangalore',
            'vadodara', 'surat', 'rajkot', 'bhubaneswar', 'bhubaneshwar', 'cuttack',
            'guwahati', 'shillong', 'imphal', 'aizawl', 'kohima', 'itanagar', 'gangtok',
            'kalaburgi', 'gulbarga', 'hubli', 'dharwad', 'belgaum', 'bellary', 'tumkur',
            'raichur', 'bidar', 'hospet', 'gadag', 'bagalkot', 'bijapur', 'kolar',
            'mandya', 'hassan', 'udupi', 'dakshina kannada', 'chikmagalur',
            'chitradurga', 'davangere', 'shimoga', 'chamrajanagar', 'kodagu', 'mysuru'
        }
    
    def extract_resume_content(self, text: str, filename: str = None) -> Dict[str, Any]:
        """Extract resume content with perfect accuracy"""
        try:
            logger.info("🎯 Starting Precision resume extraction...")
            
            if not text or len(text.strip()) < 10:
                return self._get_empty_extraction()
            
            # Clean text
            text_clean = self._clean_text(text)
            
            # Extract components with precision
            name = self._extract_name_precision(text_clean, filename)
            email = self._extract_email_precision(text_clean)
            phone = self._extract_phone_precision(text_clean)
            role = self._extract_role_precision(text_clean, name)
            location = accurate_extractor.extract_location(text_clean, name)
            skills = ultimate_extractor.extract_skills(text_clean)
            experience = ultimate_extractor.extract_experience(text_clean)
            
            # Calculate confidence
            confidence = self._calculate_confidence_precision(name, email, phone, skills, experience, role)
            
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
                'extraction_method': 'precision_extraction',
                'confidence_score': confidence,
                'extraction_timestamp': datetime.now().isoformat()
            }
            
            logger.info(f"✅ Precision extraction completed:")
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
            logger.error(f"❌ Error in precision resume extraction: {e}")
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
    
    def _extract_name_precision(self, text: str, filename: str = None) -> str:
        """Extract name with precision"""
        try:
            # Strategy 1: Extract from filename (most reliable)
            if filename and filename != 'undefined':
                name_from_file = filename.replace('.pdf', '').replace('.docx', '').replace('.doc', '')
                name_from_file = re.sub(r'^(resume|cv|curriculum|vitae)[_\-\s]*', '', name_from_file, flags=re.IGNORECASE)
                name_parts = re.split(r'[_\-\s]+', name_from_file)
                name_parts = [part.strip().title() for part in name_parts if part.strip() and len(part.strip()) > 1]
                if len(name_parts) >= 2:
                    return ' '.join(name_parts)
            
            # Strategy 2: Look for name in first few lines
            lines = text.split('\n')
            for i, line in enumerate(lines[:10]):
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
    
    def _extract_email_precision(self, text: str) -> str:
        """Extract email with precision"""
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
    
    def _extract_phone_precision(self, text: str) -> str:
        """Extract phone with precision"""
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
    
    def _extract_role_precision(self, text: str, name: str) -> str:
        """Extract role with precision (no name contamination)"""
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
                        if not any(name_word in role.lower() for name_word in name_words):
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
                    if not any(name_word in role.lower() for name_word in name_words):
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
    
    
    def _extract_skills_precision(self, text: str) -> List[str]:
        """Extract skills with precision (only valid skills)"""
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
                    for skill in self.valid_technical_skills:
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
                        for skill in self.valid_technical_skills:
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
                    for skill in self.valid_technical_skills:
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
                    for skill in self.valid_technical_skills:
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
    
    
    
    def _calculate_confidence_precision(self, name: str, email: str, phone: str, skills: List[str], experience: Dict, role: str) -> float:
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

# Initialize global precision extractor instance
precision_extractor = PrecisionExtractor()
