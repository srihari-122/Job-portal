"""
Dynamic Resume Extractor
Real-time extraction without hardcoded data
"""

import logging
import re
from datetime import datetime
from typing import Dict, List, Any

logger = logging.getLogger(__name__)

class DirectResumeExtractor:
    """Dynamic extractor that analyzes resume content in real-time"""
    
    def __init__(self):
        self.skill_keywords = [
            'python', 'java', 'javascript', 'react', 'angular', 'vue', 'node.js', 'express',
            'spring', 'spring boot', 'django', 'flask', 'sql', 'mysql', 'postgresql', 'mongodb',
            'redis', 'docker', 'kubernetes', 'aws', 'azure', 'gcp', 'git', 'jenkins', 'ci/cd',
            'html', 'css', 'bootstrap', 'jquery', 'typescript', 'php', 'laravel', 'symfony',
            'c#', '.net', 'ruby', 'rails', 'go', 'rust', 'swift', 'kotlin', 'android', 'ios'
        ]
    
    def extract_resume_content(self, text: str, filename: str = None) -> Dict[str, Any]:
        """Extract resume content dynamically from text"""
        try:
            logger.info("🎯 Starting dynamic resume extraction...")
            
            # Extract name (first line or common patterns)
            name = self._extract_name(text)
            
            # Extract email
            email = self._extract_email(text)
            
            # Extract phone
            phone = self._extract_phone(text)
            
            # Extract skills
            skills = self._extract_skills(text)
            
            # Extract experience
            experience = self._extract_experience(text)
            
            # Extract role/title
            role = self._extract_role(text)
            
            # Extract location
            location = self._extract_location(text)
            
            # Extract education
            education = self._extract_education(text)
            
            extracted_data = {
                'name': name,
                'email': email,
                'phone': phone,
                'skills': skills,
                'experience': experience,
                'role': role,
                'location': location,
                'education': education,
                'raw_text': text[:1000] + "..." if text else '',
                'extraction_method': 'dynamic_extraction',
                'confidence_score': 0.85,  # Dynamic extraction confidence
                'extraction_timestamp': datetime.now().isoformat()
            }
            
            logger.info(f"✅ Direct extraction completed:")
            logger.info(f"👤 Name: {extracted_data['name']}")
            logger.info(f"📧 Email: {extracted_data['email']}")
            logger.info(f"📱 Phone: {extracted_data['phone']}")
            logger.info(f"🎯 Role: {extracted_data['role']}")
            logger.info(f"📍 Location: {extracted_data['location']}")
            logger.info(f"📊 Skills: {len(extracted_data['skills'])} found")
            logger.info(f"⏰ Experience: {extracted_data['experience']['display']}")
            logger.info(f"🎯 Confidence: {extracted_data['confidence_score']:.2f}")
            
            return extracted_data
            
        except Exception as e:
            logger.error(f"❌ Error in dynamic extraction: {e}")
            return self._get_empty_result()
    
    def _extract_name(self, text: str) -> str:
        """Extract name from resume text"""
        lines = text.split('\n')
        
        # Look for name patterns in the first few lines
        for i, line in enumerate(lines[:5]):
            line = line.strip()
            
            # Skip empty lines
            if not line:
                continue
                
            # Skip lines with common resume keywords
            skip_keywords = ['email', 'phone', 'experience', 'skills', 'education', 'summary', 'objective', 'developer', 'engineer', 'analyst', 'manager']
            if any(keyword in line.lower() for keyword in skip_keywords):
                continue
                
            # Look for name pattern: First Last or First Middle Last (all caps or title case)
            # Name should be 2-4 words, each starting with capital letter
            name_pattern = r'^[A-Z][A-Z\s]+[A-Z]$|^[A-Z][a-z]+(?:\s+[A-Z][a-z]+){1,3}$'
            if re.match(name_pattern, line) and len(line.split()) >= 2 and len(line.split()) <= 4:
                # Additional validation: should not contain numbers or special chars
                if not re.search(r'[0-9@#\$%^&*()_+=\[\]{}|\\:";\'<>?,./]', line):
                    return line
                    
        # Fallback: look for the first line that looks like a name
        for line in lines[:3]:
            line = line.strip()
            if line and len(line.split()) >= 2 and len(line.split()) <= 4:
                # Check if it's all caps (common in resumes)
                if line.isupper() and not any(char.isdigit() for char in line):
                    return line
                    
        return ''
    
    def _extract_email(self, text: str) -> str:
        """Extract email from resume text"""
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, text)
        return emails[0] if emails else ''
    
    def _extract_phone(self, text: str) -> str:
        """Extract phone number from resume text"""
        # Look for phone patterns in the text
        phone_patterns = [
            r'91[\s-]?[6-9]\d{9}',        # 91-8095716480 format
            r'\+91[\s-]?[6-9]\d{9}',      # +91-8095716480 format
            r'(\+?91[\s-]?)?[6-9]\d{9}',  # General Indian format
            r'[6-9]\d{9}',                # Simple 10-digit
        ]
        
        for pattern in phone_patterns:
            matches = re.findall(pattern, text)
            if matches:
                # Get the full match, not just the group
                full_match = re.search(pattern, text)
                if full_match:
                    phone = full_match.group(0)
                    # Clean up the phone number but keep the format
                    phone = phone.strip()
                    return phone
                
        return ''
    
    def _extract_skills(self, text: str) -> List[str]:
        """Extract skills from resume text"""
        text_lower = text.lower()
        found_skills = []
        
        # First, look for skills in the predefined list
        for skill in self.skill_keywords:
            if skill in text_lower:
                found_skills.append(skill.title())
        
        # Also look for skills in common sections
        skill_sections = [
            r'skills?\s*:?\s*(.*?)(?:\n\n|\n[A-Z]|$)',
            r'technical\s+skills?\s*:?\s*(.*?)(?:\n\n|\n[A-Z]|$)',
            r'technologies?\s*:?\s*(.*?)(?:\n\n|\n[A-Z]|$)',
            r'tools?\s*:?\s*(.*?)(?:\n\n|\n[A-Z]|$)',
        ]
        
        for pattern in skill_sections:
            matches = re.findall(pattern, text_lower, re.DOTALL | re.IGNORECASE)
            for match in matches:
                # Split by common separators and clean up
                skills_in_section = re.split(r'[,;|\n•]', match)
                for skill in skills_in_section:
                    skill = skill.strip()
                    if len(skill) > 2 and skill not in [s.lower() for s in found_skills]:
                        # Check if it's a valid skill (not too long, contains letters)
                        if len(skill) < 30 and re.search(r'[a-zA-Z]', skill):
                            found_skills.append(skill.title())
        
        # Remove duplicates and return
        return list(set(found_skills))
    
    def _extract_experience(self, text: str) -> Dict[str, Any]:
        """Extract experience from resume text"""
        # Look for experience patterns including decimal values
        exp_patterns = [
            r'(\d+\.?\d*)\s*years?\s*(?:of\s*)?experience',
            r'experience\s*:\s*(\d+\.?\d*)\s*years?',
            r'(\d+\.?\d*)\s*years?\s*in',
            r'(\d+\.?\d*)\s*years?\s*experience',
            r'(\d+\.?\d*)\+?\s*years?\s*(?:of\s*)?(?:software\s*)?(?:development\s*)?(?:experience\s*)?',
            r'(\d+\.?\d*)\s*years?\s*(?:of\s*)?(?:professional\s*)?(?:work\s*)?(?:experience\s*)?',
        ]
        
        text_lower = text.lower()
        for pattern in exp_patterns:
            match = re.search(pattern, text_lower)
            if match:
                years_str = match.group(1)
                try:
                    years = float(years_str)
                    years_int = int(years) if years.is_integer() else years
                    return {
                        'total_years': years_int,
                        'total_months': int(years * 12),
                        'display': f'{years_int} years' if isinstance(years_int, int) else f'{years} years'
                    }
                except ValueError:
                    continue
        
        return {'total_years': 0, 'total_months': 0, 'display': '0 years'}
    
    def _extract_role(self, text: str) -> str:
        """Extract role/title from resume text"""
        lines = text.split('\n')
        
        # Look for role patterns in the first few lines (after name)
        for i, line in enumerate(lines[:8]):
            line = line.strip()
            if not line:
                continue
                
            # Skip if it looks like a name (all caps)
            if re.match(r'^[A-Z][A-Z\s]+[A-Z]$', line):
                continue
                
            # Skip if it looks like contact info
            if '@' in line or re.search(r'91[\s-]?[6-9]\d{9}', line) or 'linkedin' in line.lower():
                continue
                
            # Skip if it's just a single word or too short
            if len(line.split()) < 2:
                continue
                
            # Look for specific role patterns first
            role_patterns = [
                r'Full Stack\s+Java\s+Developer',
                r'Full Stack\s+Developer', 
                r'Java\s+Developer',
                r'Software\s+Developer',
                r'Web\s+Developer',
                r'Frontend\s+Developer',
                r'Backend\s+Developer',
                r'Mobile\s+Developer',
                r'Data\s+Scientist',
                r'DevOps\s+Engineer',
            ]
            
            # Check for exact role matches first
            for pattern in role_patterns:
                match = re.search(pattern, line, re.IGNORECASE)
                if match:
                    return match.group(0).title()
                    
            # Check if line contains role keywords
            role_keywords = ['developer', 'engineer', 'analyst', 'manager', 'consultant', 'specialist', 'architect']
            line_lower = line.lower()
            
            for keyword in role_keywords:
                if keyword in line_lower:
                    # Return the full line as role, but clean it up
                    role = line.strip()
                    # Remove common prefixes
                    role = re.sub(r'^(i am|i\'m|working as|currently|role|position|title)[:\s]*', '', role.lower())
                    # Remove trailing punctuation
                    role = re.sub(r'[:\s]*$', '', role)
                    # Capitalize properly
                    return role.title()
                    
        # Fallback: search the entire text for role patterns
        text_lower = text.lower()
        fallback_patterns = [
            r'full stack\s+java\s+developer',
            r'full stack\s+developer',
            r'java\s+developer',
            r'software\s+developer',
        ]
        
        for pattern in fallback_patterns:
            match = re.search(pattern, text_lower)
            if match:
                return match.group(0).title()
                
        return ''
    
    def _extract_location(self, text: str) -> str:
        """Extract location from resume text"""
        location_keywords = ['bangalore', 'mumbai', 'delhi', 'hyderabad', 'chennai', 'pune', 'kolkata']
        text_lower = text.lower()
        for location in location_keywords:
            if location in text_lower:
                return location.title()
        return ''
    
    def _extract_education(self, text: str) -> List[str]:
        """Extract education from resume text"""
        education_keywords = ['bachelor', 'master', 'phd', 'diploma', 'degree', 'university', 'college']
        education = []
        text_lower = text.lower()
        for keyword in education_keywords:
            if keyword in text_lower:
                # Find the line containing education
                lines = text.split('\n')
                for line in lines:
                    if keyword in line.lower():
                        education.append(line.strip())
        return education
    
    def _get_empty_result(self) -> Dict[str, Any]:
        """Return empty extraction result"""
        return {
            'name': '',
            'email': '',
            'phone': '',
            'skills': [],
            'experience': {'total_years': 0, 'total_months': 0, 'display': '0 years'},
            'role': '',
            'location': '',
            'education': [],
            'raw_text': '',
            'extraction_method': 'dynamic_extraction',
            'confidence_score': 0.0,
            'extraction_timestamp': datetime.now().isoformat()
        }

# Initialize global direct extractor instance
direct_extractor = DirectResumeExtractor()
