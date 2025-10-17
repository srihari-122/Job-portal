"""
Reliable Resume Extractor - Simple and Accurate
"""

import re
import logging
import os
from typing import Dict, List, Any, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

class ReliableExtractor:
    """Simple and reliable extractor that always works"""
    
    def __init__(self):
        pass
    
    def extract_resume_data_from_file(self, file_path: str) -> Dict[str, Any]:
        """Extract resume data from file"""
        try:
            import PyPDF2
            import os
            
            logger.info(f"📄 Extracting resume data from file: {file_path}")
            
            # Extract text from PDF
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
            
            # Get filename from path
            filename = os.path.basename(file_path)
            
            # Extract data using the main method
            return self.extract_resume_data(text, filename)
            
        except Exception as e:
            logger.error(f"❌ Error extracting from file {file_path}: {e}")
            return self._get_empty_result()
    
    def extract_resume_data(self, text: str, filename: str = None) -> Dict[str, Any]:
        """Extract resume data reliably"""
        try:
            logger.info("🚀 Starting reliable resume extraction...")
            
            if not text or len(text.strip()) < 10:
                return self._get_empty_result()
            
            # Extract all data
            name = self._extract_name(text, filename)
            role = self._extract_role(text)
            email = self._extract_email(text)
            phone = self._extract_phone(text)
            skills = self._extract_skills(text)
            experience = self._extract_experience(text)
            location = self._extract_location(text)
            education = self._extract_education(text)
            
            result = {
                'name': name,
                'role': role,
                'email': email,
                'phone': phone,
                'skills': skills,
                'experience': experience,
                'location': location,
                'education': education,
                'raw_text': text[:500] if text else '',
                'extraction_method': 'reliable_extraction',
                'confidence_score': 1.0,
                'extraction_timestamp': datetime.now().isoformat()
            }
            
            logger.info("✅ Reliable extraction completed")
            logger.info(f"👤 Name: {name}")
            logger.info(f"🎯 Role: {role}")
            logger.info(f"⏰ Experience: {experience.get('display', 'Not found')}")
            logger.info(f"🛠️ Skills: {len(skills)} skills found")
            
            return result
            
        except Exception as e:
            logger.error(f"❌ Reliable extraction error: {e}")
            return self._get_empty_result()
    
    def _extract_name(self, text: str, filename: str = None) -> str:
        """Extract name reliably"""
        try:
            # Strategy 1: Filename extraction
            if filename:
                name_from_file = self._extract_name_from_filename(filename)
                if name_from_file:
                    logger.info(f"✅ Name from filename: {name_from_file}")
                    return name_from_file
            
            # Strategy 2: First line extraction
            lines = text.split('\n')
            for line in lines[:5]:
                line = line.strip()
                if line and self._is_likely_name(line):
                    logger.info(f"✅ Name from first lines: {line}")
                    return line.title()
            
            return 'Name not found'
            
        except Exception as e:
            logger.error(f"❌ Name extraction error: {e}")
            return 'Name not found'
    
    def _extract_name_from_filename(self, filename: str) -> str:
        """Extract name from filename"""
        try:
            name_part = os.path.splitext(filename)[0]
            
            # Try different patterns
            patterns = [
                r'([A-Z][a-z]+_[A-Z][a-z]+)',  # Underscore names
                r'([A-Z][a-z]+ [A-Z][a-z]+)',  # Space names
                r'([A-Z][a-z]+-[A-Z][a-z]+)',  # Hyphen names
            ]
            
            for pattern in patterns:
                match = re.search(pattern, name_part)
                if match:
                    name = match.group(1).strip()
                    name = name.replace('_', ' ').replace('-', ' ')
                    name = ' '.join(word.capitalize() for word in name.split())
                    return name
            
            return None
            
        except Exception as e:
            logger.error(f"❌ Filename name extraction error: {e}")
            return None
    
    def _is_likely_name(self, text: str) -> bool:
        """Check if text is likely a name"""
        if not text or len(text) < 3 or len(text) > 50:
            return False
        
        words = text.split()
        if len(words) < 2 or len(words) > 4:
            return False
        
        # Check if all words start with capital letters
        if not all(word[0].isupper() for word in words if word):
            return False
        
        # Check if it contains only letters and spaces
        if not all(c.isalpha() or c.isspace() for c in text):
            return False
        
        # Exclude common non-name words
        exclude_words = ['resume', 'cv', 'curriculum', 'vitae', 'profile', 'summary', 'objective']
        if any(word.lower() in exclude_words for word in words):
            return False
        
        return True
    
    def _extract_role(self, text: str) -> str:
        """Extract role reliably"""
        try:
            # Look for specific role patterns
            role_patterns = [
                r'\b(Full Stack Java Developer|Java Developer|Software Engineer|Software Developer|Full Stack Developer|Frontend Developer|Backend Developer|Web Developer|Mobile Developer|DevOps Engineer|Data Scientist|Data Analyst|Machine Learning Engineer|AI Engineer|Cloud Engineer|Security Engineer|QA Engineer|Test Engineer|UI/UX Designer|Product Manager|Project Manager|Technical Lead|Team Lead|Solution Architect|System Architect|Database Administrator|Network Administrator|System Administrator|Business Analyst|System Analyst|Technical Writer|Scrum Master|Agile Coach|Engineering Manager|Development Manager|IT Manager)\b',
                r'\b(Senior|Lead|Principal|Staff|Junior|Entry Level|Associate|Mid Level)\s+(Developer|Engineer|Programmer|Analyst|Consultant|Specialist|Architect|Manager|Director)\b',
                r'\b(Java|Python|JavaScript|React|Angular|Vue|Node\.js|Spring|Django|Flask|Laravel|Ruby on Rails|PHP|C#|C\+\+|Go|Rust|Swift|Kotlin|Flutter|React Native|Android|iOS)\s+(Developer|Engineer|Programmer|Specialist)\b',
            ]
            
            for pattern in role_patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                if matches:
                    role = matches[0].strip()
                    if self._is_valid_role(role):
                        logger.info(f"✅ Role found: {role}")
                        return role.title()
            
            return 'Role not found'
            
        except Exception as e:
            logger.error(f"❌ Role extraction error: {e}")
            return 'Role not found'
    
    def _is_valid_role(self, role: str) -> bool:
        """Check if role is valid"""
        if not role or len(role.strip()) < 3:
            return False
        
        role = role.strip()
        
        # Check if it contains job keywords
        job_keywords = [
            'developer', 'engineer', 'programmer', 'analyst', 'consultant', 'specialist',
            'architect', 'manager', 'director', 'lead', 'coordinator', 'administrator',
            'designer', 'writer', 'editor', 'researcher', 'scientist', 'technician'
        ]
        
        role_lower = role.lower()
        return any(keyword in role_lower for keyword in job_keywords)
    
    def _extract_email(self, text: str) -> str:
        """Extract email reliably"""
        try:
            email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            matches = re.findall(email_pattern, text)
            if matches:
                return matches[0]
            return 'Email not found'
        except Exception as e:
            logger.error(f"❌ Email extraction error: {e}")
            return 'Email not found'
    
    def _extract_phone(self, text: str) -> str:
        """Extract phone reliably"""
        try:
            phone_patterns = [
                r'\b\d{10}\b',  # 10 digits
                r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',  # US format
                r'\b\+\d{1,3}[-.\s]?\d{1,4}[-.\s]?\d{1,4}[-.\s]?\d{1,9}\b',  # International
            ]
            
            for pattern in phone_patterns:
                matches = re.findall(pattern, text)
                if matches:
                    return matches[0]
            return 'Phone not found'
        except Exception as e:
            logger.error(f"❌ Phone extraction error: {e}")
            return 'Phone not found'
    
    def _extract_skills(self, text: str) -> List[str]:
        """Extract skills reliably"""
        try:
            # Common technical skills
            common_skills = [
                'Java', 'Python', 'JavaScript', 'React', 'Angular', 'Vue', 'Node.js',
                'Spring', 'Django', 'Flask', 'Laravel', 'Ruby on Rails', 'PHP',
                'C#', 'C++', 'Go', 'Rust', 'Swift', 'Kotlin', 'Flutter',
                'React Native', 'Android', 'iOS', 'HTML', 'CSS', 'Bootstrap',
                'SQL', 'MySQL', 'PostgreSQL', 'MongoDB', 'Redis', 'Elasticsearch',
                'AWS', 'Azure', 'GCP', 'Docker', 'Kubernetes', 'Jenkins',
                'Git', 'GitHub', 'GitLab', 'Jira', 'Confluence', 'Agile',
                'Scrum', 'DevOps', 'CI/CD', 'REST API', 'GraphQL', 'Microservices',
                'Machine Learning', 'Data Science', 'TensorFlow', 'PyTorch',
                'Power BI', 'Tableau', 'Excel', 'R', 'SAS', 'SPSS'
            ]
            
            text_lower = text.lower()
            found_skills = []
            
            for skill in common_skills:
                if skill.lower() in text_lower:
                    found_skills.append(skill)
            
            return found_skills
            
        except Exception as e:
            logger.error(f"❌ Skills extraction error: {e}")
            return []
    
    def _extract_experience(self, text: str) -> Dict[str, Any]:
        """Extract experience reliably"""
        try:
            # Look for experience patterns with decimal support
            experience_patterns = [
                r'(\d+\.?\d*)\s*years?\s*(?:of\s*)?experience',
                r'experience\s*(?:of\s*)?(\d+\.?\d*)\s*years?',
                r'(\d+\.?\d*)\s*years?\s*(?:in|with)',
                r'(\d+\.?\d*)\s*years?\s*(?:of\s*)?(?:professional|work|industry)',
                r'(\d+\.?\d*)\s*years?\s*(?:of\s*)?(?:software|development|engineering)',
            ]
            
            for pattern in experience_patterns:
                match = re.search(pattern, text, re.IGNORECASE)
                if match:
                    years_str = match.group(1)
                    years = float(years_str)
                    months = int(years * 12)
                    
                    # Format display based on decimal or whole number
                    if years == int(years):
                        display = f'{int(years)} years'
                    else:
                        display = f'{years} years'
                    
                    return {
                        'total_years': years,
                        'total_months': months,
                        'display': display,
                        'is_fresher': years == 0,
                        'experience_periods': [],
                        'extraction_method': 'pattern_matching'
                    }
            
            # Default to fresher if no experience found
            return {
                'total_years': 0,
                'total_months': 0,
                'display': 'Fresher (0 years)',
                'is_fresher': True,
                'experience_periods': [],
                'extraction_method': 'fresher_detection'
            }
            
        except Exception as e:
            logger.error(f"❌ Experience extraction error: {e}")
            return {
                'total_years': 0,
                'total_months': 0,
                'display': 'Experience not found',
                'is_fresher': True,
                'experience_periods': [],
                'extraction_method': 'error'
            }
    
    def _extract_location(self, text: str) -> str:
        """Extract location reliably"""
        try:
            # Common location patterns
            location_patterns = [
                r'\b(?:located in|based in|from|lives in|resides in)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)',
                r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s*,\s*[A-Z]{2}\b',  # City, State
                r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s*,\s*[A-Z][a-z]+\b',  # City, Country
            ]
            
            for pattern in location_patterns:
                match = re.search(pattern, text, re.IGNORECASE)
                if match:
                    return match.group(1).strip()
            
            return 'Location not found'
            
        except Exception as e:
            logger.error(f"❌ Location extraction error: {e}")
            return 'Location not found'
    
    def _extract_education(self, text: str) -> List[Dict[str, str]]:
        """Extract education reliably"""
        try:
            education = []
            
            # Look for degree patterns
            degree_patterns = [
                r'\b(Bachelor|Master|PhD|Doctorate|Associate|Diploma|Certificate)\s+(?:of|in)\s+([A-Za-z\s]+)',
                r'\b([A-Za-z\s]+)\s+(?:Bachelor|Master|PhD|Doctorate|Associate|Diploma|Certificate)',
            ]
            
            for pattern in degree_patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                for match in matches:
                    education.append({
                        'degree': match[0] if len(match) > 1 else match,
                        'institution': 'Not specified',
                        'year': 'Not specified'
                    })
            
            return education if education else [{
                'degree': 'Not specified',
                'institution': 'Not specified',
                'year': 'Not specified'
            }]
            
        except Exception as e:
            logger.error(f"❌ Education extraction error: {e}")
            return [{
                'degree': 'Not specified',
                'institution': 'Not specified',
                'year': 'Not specified'
            }]
    
    def _get_empty_result(self) -> Dict[str, Any]:
        """Return empty result structure"""
        return {
            'name': 'Name not found',
            'email': 'Email not found',
            'phone': 'Phone not found',
            'skills': [],
            'experience': {'total_years': 0, 'total_months': 0, 'display': 'Experience not found'},
            'role': 'Role not found',
            'location': 'Location not found',
            'education': [],
            'raw_text': '',
            'extraction_method': 'reliable_extraction_error',
            'confidence_score': 0.0,
            'extraction_timestamp': datetime.now().isoformat()
        }

# Initialize the extractor
reliable_extractor = ReliableExtractor()
