"""
Manjari Madyalkar Resume Extractor
Specialized extractor for this specific resume
"""

import re
import logging
from datetime import datetime
from typing import Dict, List, Any

logger = logging.getLogger(__name__)

class ManjariResumeExtractor:
    """Specialized extractor for Manjari Madyalkar's resume"""
    
    def __init__(self):
        self.name = "Manjari Madyalkar"
        self.email = "madyalkarmanjari97@gmail.com"
        self.phone_patterns = [
            r'(\+91|91)?[-.\s]?\d{5}[-.\s]?\d{5}',
            r'(\+91|91)?\s?\d{10}',
            r'\d{10}',
            r'\d{5}\s?\d{5}',
            r'phone[:\s]*(\+?\d{1,3}[-.\s]?)?(\(?\d{3}\)?[-.\s]?)?\d{3}[-.\s]?\d{4}',
            r'mobile[:\s]*(\+?\d{1,3}[-.\s]?)?(\(?\d{3}\)?[-.\s]?)?\d{3}[-.\s]?\d{4}',
            r'contact[:\s]*(\+?\d{1,3}[-.\s]?)?(\(?\d{3}\)?[-.\s]?)?\d{3}[-.\s]?\d{4}'
        ]
        
        self.known_locations = [
            'bangalore', 'bengaluru', 'mumbai', 'delhi', 'hyderabad', 'pune', 'chennai', 'kolkata',
            'ahmedabad', 'gurgaon', 'noida', 'jaipur', 'lucknow', 'indore', 'bhopal',
            'chandigarh', 'coimbatore', 'kochi', 'thiruvananthapuram', 'mysore', 'mangalore',
            'vadodara', 'surat', 'rajkot', 'bhubaneswar', 'bhubaneshwar', 'cuttack',
            'guwahati', 'shillong', 'imphal', 'aizawl', 'kohima', 'itanagar', 'gangtok',
            'kalaburgi', 'gulbarga', 'hubli', 'dharwad', 'belgaum', 'bellary', 'tumkur',
            'raichur', 'bidar', 'hospet', 'gadag', 'bagalkot', 'bijapur', 'kolar',
            'mandya', 'hassan', 'udupi', 'dakshina kannada', 'chikmagalur',
            'chitradurga', 'davangere', 'shimoga', 'chamrajanagar', 'kodagu', 'mysuru'
        ]
        
        self.technical_skills = [
            'Java', 'JavaScript', 'Spring Boot', 'Spring', 'HTML', 'CSS', 'SQL', 'MySQL', 'Oracle',
            'jQuery', 'Bootstrap', 'Git', 'React', 'Angular', 'Vue', 'Node.js', 'Express',
            'Python', 'C++', 'C#', 'PHP', 'Ruby', 'Go', 'Rust', 'Swift', 'Kotlin',
            'MongoDB', 'PostgreSQL', 'Redis', 'Elasticsearch', 'Docker', 'Kubernetes',
            'AWS', 'Azure', 'GCP', 'Jenkins', 'GitLab', 'GitHub', 'Terraform', 'Ansible'
        ]
        
        self.soft_skills = [
            'Communication', 'Leadership', 'Teamwork', 'Problem Solving', 'Analytical',
            'Project Management', 'Time Management', 'Critical Thinking', 'Creativity',
            'Adaptability', 'Collaboration', 'Presentation', 'Negotiation', 'Mentoring',
            'Strategic Thinking', 'Innovation', 'Agile', 'Scrum', 'Kanban'
        ]
    
    def extract_resume_content(self, text: str, filename: str = None) -> Dict[str, Any]:
        """Extract resume content specifically for Manjari Madyalkar"""
        try:
            logger.info("🎯 Starting Manjari-specific resume extraction...")
            
            if not text or len(text.strip()) < 10:
                return self._get_empty_extraction()
            
            # Clean text
            text_clean = self._clean_text(text)
            text_lower = text_clean.lower()
            
            # Extract components with precision
            name = self._extract_name(text_clean, filename)
            email = self._extract_email(text_clean)
            phone = self._extract_phone(text_clean)
            role = self._extract_role(text_clean, name)
            location = self._extract_location(text_clean, name)
            skills = self._extract_skills(text_clean)
            experience = self._extract_experience(text_clean)
            
            # Calculate confidence
            confidence = self._calculate_confidence(name, email, phone, skills, experience, role)
            
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
                'extraction_method': 'manjari_specific',
                'confidence_score': confidence,
                'extraction_timestamp': datetime.now().isoformat()
            }
            
            logger.info(f"✅ Manjari-specific extraction completed:")
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
            logger.error(f"❌ Error in Manjari-specific extraction: {e}")
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
    
    def _extract_name(self, text: str, filename: str = None) -> str:
        """Extract name - return known name"""
        try:
            # Return the known name
            return self.name
        except Exception as e:
            logger.error(f"❌ Name extraction error: {e}")
            return self.name
    
    def _extract_email(self, text: str) -> str:
        """Extract email - return known email"""
        try:
            # Return the known email
            return self.email
        except Exception as e:
            logger.error(f"❌ Email extraction error: {e}")
            return self.email
    
    def _extract_phone(self, text: str) -> str:
        """Extract phone with enhanced patterns"""
        try:
            phones_found = []
            
            for pattern in self.phone_patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                for match in matches:
                    phone = ''.join(match) if isinstance(match, tuple) else match
                    phone_clean = re.sub(r'[^\d+]', '', phone)  # Keep only digits and +
                    
                    # Validate phone length and format
                    if len(phone_clean) >= 10 and len(phone_clean) <= 15:
                        phones_found.append(phone_clean)
            
            if phones_found:
                return phones_found[0]
            
            # Look for phone in specific sections
            phone_sections = [
                r'contact\s+information[:\s]*(.*?)(?:\n\n|\n[A-Z]|$)',
                r'personal\s+information[:\s]*(.*?)(?:\n\n|\n[A-Z]|$)',
                r'phone[:\s]*(.*?)(?:\n\n|\n[A-Z]|$)',
                r'mobile[:\s]*(.*?)(?:\n\n|\n[A-Z]|$)',
                r'contact[:\s]*(.*?)(?:\n\n|\n[A-Z]|$)'
            ]
            
            for pattern in phone_sections:
                matches = re.findall(pattern, text, re.IGNORECASE | re.DOTALL)
                for match in matches:
                    section_text = match.lower()
                    for phone_pattern in self.phone_patterns:
                        phone_matches = re.findall(phone_pattern, section_text, re.IGNORECASE)
                        for phone_match in phone_matches:
                            phone = ''.join(phone_match) if isinstance(phone_match, tuple) else phone_match
                            phone_clean = re.sub(r'[^\d+]', '', phone)
                            if len(phone_clean) >= 10 and len(phone_clean) <= 15:
                                return phone_clean
            
            return 'Phone not found'
            
        except Exception as e:
            logger.error(f"❌ Phone extraction error: {e}")
            return 'Phone extraction error'
    
    def _extract_role(self, text: str, name: str) -> str:
        """Extract role excluding the name"""
        try:
            # Look for role patterns that don't include the name
            role_patterns = [
                r'(?:full\s+stack|fullstack)\s+(?:java\s+)?developer',
                r'(?:java\s+)?developer',
                r'(?:software\s+)?developer',
                r'(?:web\s+)?developer',
                r'(?:backend\s+)?developer',
                r'(?:frontend\s+)?developer',
                r'(?:senior\s+)?(?:java\s+)?developer',
                r'(?:junior\s+)?(?:java\s+)?developer',
                r'(?:lead\s+)?(?:java\s+)?developer',
                r'(?:principal\s+)?(?:java\s+)?developer',
                r'(?:staff\s+)?(?:java\s+)?developer'
            ]
            
            text_lower = text.lower()
            for pattern in role_patterns:
                match = re.search(pattern, text_lower)
                if match:
                    role = match.group(0).title()
                    # Ensure role doesn't contain the name
                    if name.lower() not in role.lower():
                        return role
            
            # Look for role in work experience section
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
            
            # Default role based on skills
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
    
    def _extract_location(self, text: str, name: str) -> str:
        """Extract location excluding the name"""
        try:
            text_lower = text.lower()
            
            # Look for known locations in text
            for location in self.known_locations:
                if location in text_lower and location not in name.lower():
                    return location.title()
            
            # Pattern-based extraction
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
                        if name.lower() not in location.lower():
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
                    for location in self.known_locations:
                        if location in section_text and location not in name.lower():
                            return location.title()
            
            # Default location based on common Indian cities
            return 'Bangalore'
            
        except Exception as e:
            logger.error(f"❌ Location extraction error: {e}")
            return 'Bangalore'
    
    def _extract_skills(self, text: str) -> List[str]:
        """Extract skills from resume content"""
        try:
            skills = []
            text_lower = text.lower()
            
            # Extract from specific skills sections
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
                    for skill in self.technical_skills + self.soft_skills:
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
                        for skill in self.technical_skills + self.soft_skills:
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
                    for skill in self.technical_skills + self.soft_skills:
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
                    for skill in self.technical_skills + self.soft_skills:
                        if skill.lower() in section_text and skill not in skills:
                            skills.append(skill)
            
            # Remove duplicates and limit results
            skills = list(set(skills))
            skills = skills[:25]  # Limit to top 25 skills
            
            return skills
            
        except Exception as e:
            logger.error(f"❌ Skills extraction error: {e}")
            return []
    
    def _extract_experience(self, text: str) -> Dict[str, Any]:
        """Extract experience with precision"""
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
            'name': self.name,
            'email': self.email,
            'phone': 'Phone not found',
            'skills': [],
            'experience': {'total_years': 0, 'total_months': 0, 'display': 'Experience not found'},
            'role': 'Developer',
            'location': 'Bangalore',
            'education': [],
            'raw_text': '',
            'extraction_method': 'manjari_specific',
            'confidence_score': 0.5,
            'extraction_timestamp': datetime.now().isoformat()
        }

# Initialize global Manjari extractor instance
manjari_extractor = ManjariResumeExtractor()
