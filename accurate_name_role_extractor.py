"""
Accurate Name and Role Extractor
Unified system for precise name and role extraction from resumes
"""

import re
import logging
import os
from typing import Dict, List, Any, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

class AccurateNameRoleExtractor:
    """Accurate extractor focused on name and role precision"""
    
    def __init__(self):
        self.initialize_patterns()
        self.initialize_validation_rules()
        
    def initialize_patterns(self):
        """Initialize precise extraction patterns"""
        
        # PRECISE NAME PATTERNS - Priority order matters
        self.name_patterns = [
            # 1. Filename-based extraction (highest priority)
            r'^([A-Z][A-Z]+ [A-Z][A-Z]+)',  # ALL CAPS names from filename
            r'^([A-Z][a-z]+ [A-Z][a-z]+(?: [A-Z][a-z]+)?)',  # Title Case names from filename
            
            # 2. Header patterns (second priority)
            r'^([A-Z][A-Z]+ [A-Z][A-Z]+)\s*\n',  # ALL CAPS at start of text
            r'^([A-Z][a-z]+ [A-Z][a-z]+(?: [A-Z][a-z]+)?)\s*\n',  # Title Case at start
            
            # 3. Before common sections
            r'([A-Z][A-Z]+ [A-Z][A-Z]+)\s+(?:PROFILE|Profile|About|Summary|SKILLS|Skills|EDUCATION|Education|EXPERIENCE|Experience)',
            r'([A-Z][a-z]+ [A-Z][a-z]+(?: [A-Z][a-z]+)?)\s+(?:PROFILE|Profile|About|Summary|SKILLS|Skills|EDUCATION|Education|EXPERIENCE|Experience)',
            
            # 4. Contact section patterns
            r'(?:Name|Full Name|Contact Name)[:\s]*([A-Z][A-Z]+ [A-Z][A-Z]+)',
            r'(?:Name|Full Name|Contact Name)[:\s]*([A-Z][a-z]+ [A-Z][a-z]+(?: [A-Z][a-z]+)?)',
            
            # 5. General patterns in text
            r'\b([A-Z][A-Z]+ [A-Z][A-Z]+)\b',  # ALL CAPS anywhere
            r'\b([A-Z][a-z]+ [A-Z][a-z]+(?: [A-Z][a-z]+)?)\b',  # Title Case anywhere
        ]
        
        # PRECISE ROLE PATTERNS - Specific and comprehensive
        self.role_patterns = [
            # 1. Exact role matches (highest priority)
            r'\b(Full\s*Stack\s*Java\s*Developer)\b',
            r'\b(Full\s*Stack\s*Python\s*Developer)\b',
            r'\b(Full\s*Stack\s*JavaScript\s*Developer)\b',
            r'\b(Full\s*Stack\s*Developer)\b',
            
            # 2. Technology-specific roles
            r'\b(Java\s*Developer)\b',
            r'\b(Python\s*Developer)\b',
            r'\b(JavaScript\s*Developer)\b',
            r'\b(React\s*Developer)\b',
            r'\b(Angular\s*Developer)\b',
            r'\b(Node\.js\s*Developer)\b',
            r'\b(Spring\s*Boot\s*Developer)\b',
            r'\b(Django\s*Developer)\b',
            r'\b(Flask\s*Developer)\b',
            
            # 3. Seniority + Technology
            r'\b(Senior\s*Full\s*Stack\s*Developer)\b',
            r'\b(Senior\s*Java\s*Developer)\b',
            r'\b(Senior\s*Python\s*Developer)\b',
            r'\b(Senior\s*JavaScript\s*Developer)\b',
            r'\b(Lead\s*Full\s*Stack\s*Developer)\b',
            r'\b(Lead\s*Java\s*Developer)\b',
            r'\b(Principal\s*Full\s*Stack\s*Developer)\b',
            
            # 4. General developer roles
            r'\b(Software\s*Engineer)\b',
            r'\b(Web\s*Developer)\b',
            r'\b(Frontend\s*Developer)\b',
            r'\b(Backend\s*Developer)\b',
            r'\b(Mobile\s*Developer)\b',
            
            # 5. Other technical roles
            r'\b(Data\s*Scientist)\b',
            r'\b(Data\s*Analyst)\b',
            r'\b(Machine\s*Learning\s*Engineer)\b',
            r'\b(DevOps\s*Engineer)\b',
            r'\b(QA\s*Engineer)\b',
            r'\b(UI\/UX\s*Designer)\b',
            r'\b(Cloud\s*Engineer)\b',
            r'\b(Security\s*Engineer)\b',
            
            # 6. Management roles
            r'\b(Technical\s*Lead)\b',
            r'\b(Team\s*Lead)\b',
            r'\b(Project\s*Manager)\b',
            r'\b(Product\s*Manager)\b',
            r'\b(Solution\s*Architect)\b',
            r'\b(System\s*Architect)\b',
            
            # 7. Context-based patterns
            r'(?:Position|Title|Role|Job Title|Designation|Current Role|Professional Title)[:\s]*([A-Za-z\s]{3,50})',
            r'(?:Working as|Currently|Role)[:\s]*([A-Za-z\s]{3,50})',
            r'(?:I am|I\'m)[:\s]*([A-Za-z\s]{3,50})',
            r'(?:As a|Being a)[:\s]*([A-Za-z\s]{3,50})',
        ]
        
        # EMAIL PATTERNS
        self.email_patterns = [
            r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            r'(?:Email|E-mail|Mail|Contact)[:\s]*([A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,})',
        ]
        
        # PHONE PATTERNS
        self.phone_patterns = [
            r'\b(?:\+91[-.\s]?)?[6-9]\d{9}\b',
            r'\b(?:\+91[-.\s]?)?[6-9]\d{2}[-.\s]?\d{3}[-.\s]?\d{4}\b',
            r'(?:Phone|Mobile|Cell|Contact)[:\s]*([+]?[\d\s\-\(\)]{10,})',
            r'\+91[-.\s]?[6-9]\d{9}',
        ]
        
    def initialize_validation_rules(self):
        """Initialize validation rules for names and roles"""
        
        # FALSE POSITIVES for names (things that look like names but aren't)
        self.name_false_positives = [
            'resume', 'cv', 'curriculum vitae', 'personal information', 'contact information',
            'objective', 'summary', 'profile', 'about', 'contact', 'address', 'phone', 'email',
            'experience', 'education', 'skills', 'projects', 'certifications', 'achievements',
            'complete visitor management service', 'admin dashboard', 'visitor management',
            'the unauthenticated or unwanted visitors', 'user and system data logs',
            'system data logs', 'data logs', 'logs', 'to land', 'challenging job',
            'reputable company', 'broaden my knowledge', 'responsible career path',
            'make the most of my education', 'significantly contributing', 'organization',
            'growth', 'former assistant', 'assistant', 'former', 'current', 'present',
            'working', 'employed', 'job', 'position', 'role', 'title', 'designation'
        ]
        
        # VALID ROLE KEYWORDS
        self.valid_role_keywords = [
            'developer', 'engineer', 'analyst', 'manager', 'designer', 'architect',
            'specialist', 'consultant', 'lead', 'senior', 'junior', 'associate',
            'intern', 'trainee', 'coordinator', 'supervisor', 'director', 'executive',
            'programmer', 'coder', 'technician', 'administrator', 'officer', 'scientist'
        ]
        
        # VALID TECHNOLOGY KEYWORDS for roles
        self.valid_tech_keywords = [
            'java', 'python', 'javascript', 'react', 'angular', 'node', 'spring',
            'sql', 'mongodb', 'aws', 'azure', 'docker', 'kubernetes', 'git',
            'html', 'css', 'bootstrap', 'jquery', 'express', 'django', 'flask',
            'full stack', 'frontend', 'backend', 'mobile', 'web', 'data', 'cloud',
            'security', 'devops', 'qa', 'ui', 'ux', 'software', 'machine learning',
            'artificial intelligence', 'network', 'database', 'game', 'embedded',
            'system', 'platform', 'product', 'technical'
        ]
    
    def extract_resume_data(self, text: str, filename: str = None) -> Dict[str, Any]:
        """Extract resume data with focus on accurate name and role"""
        try:
            logger.info("🎯 Starting accurate name and role extraction...")
            
            if not text or len(text.strip()) < 10:
                return self._get_empty_result()
            
            # Clean text
            text_clean = self._clean_text(text)
            
            # Extract with high precision
            name = self._extract_name_accurate(text_clean, filename)
            role = self._extract_role_accurate(text_clean, name)
            email = self._extract_email_accurate(text_clean)
            phone = self._extract_phone_accurate(text_clean)
            
            # Calculate confidence
            confidence = self._calculate_confidence(name, email, phone, role)
            
            result = {
                'name': name,
                'email': email,
                'phone': phone,
                'role': role,
                'raw_text': text_clean[:500] + "..." if len(text_clean) > 500 else text_clean,
                'extraction_method': 'accurate_name_role_extraction',
                'confidence_score': confidence,
                'extraction_timestamp': datetime.now().isoformat()
            }
            
            logger.info("✅ Accurate extraction completed:")
            logger.info(f"👤 Name: {name}")
            logger.info(f"🎯 Role: {role}")
            logger.info(f"📧 Email: {email}")
            logger.info(f"📱 Phone: {phone}")
            logger.info(f"🎯 Confidence: {confidence:.2f}")
            
            return result
            
        except Exception as e:
            logger.error(f"❌ Accurate extraction error: {e}")
            return self._get_empty_result()
    
    def _extract_name_accurate(self, text: str, filename: str = None) -> str:
        """Extract name with high accuracy"""
        try:
            logger.info("🔍 Starting accurate name extraction...")
            
            # Strategy 1: Extract from filename (highest priority)
            if filename:
                name_from_file = self._extract_name_from_filename(filename)
                if name_from_file and self._is_valid_name(name_from_file):
                    logger.info(f"✅ Name from filename: {name_from_file}")
                    return name_from_file
            
            # Strategy 2: Try all name patterns in priority order
            for i, pattern in enumerate(self.name_patterns):
                matches = re.findall(pattern, text, re.IGNORECASE)
                if matches:
                    for match in matches:
                        name = match.strip()
                        if self._is_valid_name(name):
                            logger.info(f"✅ Name found with pattern {i+1}: {name}")
                            return name
            
            # Strategy 3: Look in first few lines
            lines = text.split('\n')
            for i, line in enumerate(lines[:10]):  # Check first 10 lines
                line = line.strip()
                if self._is_valid_name(line):
                    logger.info(f"✅ Name found on line {i+1}: {line}")
                    return line
            
            logger.warning("⚠️ No valid name found")
            return 'Name not found'
            
        except Exception as e:
            logger.error(f"❌ Name extraction error: {e}")
            return 'Name not found'
    
    def _extract_role_accurate(self, text: str, name: str = None) -> str:
        """Extract role with high accuracy"""
        try:
            logger.info("🔍 Starting accurate role extraction...")
            
            # Remove name from text to avoid false matches
            text_for_role = text
            if name and name != 'Name not found':
                text_for_role = text_for_role.replace(name, '')
            
            # Strategy 1: Try exact role patterns first
            for i, pattern in enumerate(self.role_patterns):
                matches = re.findall(pattern, text_for_role, re.IGNORECASE)
                if matches:
                    for match in matches:
                        role = match.strip()
                        if self._is_valid_role(role):
                            logger.info(f"✅ Role found with pattern {i+1}: {role}")
                            return role.title()
            
            # Strategy 2: Look for role keywords in context
            role_context = self._find_role_in_context(text_for_role)
            if role_context and self._is_valid_role(role_context):
                logger.info(f"✅ Role found in context: {role_context}")
                return role_context.title()
            
            # Strategy 3: Default based on skills/technologies mentioned
            default_role = self._infer_role_from_content(text_for_role)
            if default_role:
                logger.info(f"✅ Role inferred from content: {default_role}")
                return default_role
            
            logger.warning("⚠️ No valid role found")
            return 'Role not found'
            
        except Exception as e:
            logger.error(f"❌ Role extraction error: {e}")
            return 'Role not found'
    
    def _extract_email_accurate(self, text: str) -> str:
        """Extract email with high accuracy"""
        try:
            for pattern in self.email_patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                if matches:
                    email = matches[0].strip()
                    if self._is_valid_email(email):
                        logger.info(f"✅ Email extracted: {email}")
                        return email
            
            return 'Email not found'
            
        except Exception as e:
            logger.error(f"❌ Email extraction error: {e}")
            return 'Email not found'
    
    def _extract_phone_accurate(self, text: str) -> str:
        """Extract phone with high accuracy"""
        try:
            for pattern in self.phone_patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                if matches:
                    phone = matches[0].strip()
                    if self._is_valid_phone(phone):
                        logger.info(f"✅ Phone extracted: {phone}")
                        return phone
            
            return 'Phone not found'
            
        except Exception as e:
            logger.error(f"❌ Phone extraction error: {e}")
            return 'Phone not found'
    
    def _extract_name_from_filename(self, filename: str) -> Optional[str]:
        """Extract name from filename"""
        try:
            # Remove file extension
            name = filename.replace('.pdf', '').replace('.docx', '').replace('.txt', '')
            
            # Remove common prefixes/suffixes
            name = re.sub(r'^(resume|cv|curriculum_vitae)_?', '', name, flags=re.IGNORECASE)
            name = re.sub(r'_\d+$', '', name)  # Remove timestamps
            name = re.sub(r'_\d+_', '_', name)  # Remove middle timestamps
            
            # Convert underscores and hyphens to spaces
            name = re.sub(r'[_-]', ' ', name)
            
            # Check if it looks like a name
            if self._is_valid_name(name):
                return name
            
            return None
            
        except Exception as e:
            logger.error(f"❌ Error extracting name from filename: {e}")
            return None
    
    def _is_valid_name(self, name: str) -> bool:
        """Validate if text is likely a real name"""
        if not name or len(name.strip()) < 2:
            return False
        
        # Must contain only letters, spaces, dots, and hyphens
        if not re.match(r'^[A-Za-z\s\.\-]+$', name):
            return False
        
        # Must be reasonable length
        if len(name) > 50:
            return False
        
        # Must have at least 2 words
        words = name.split()
        if len(words) < 2:
            return False
        
        # Each word should start with uppercase
        for word in words:
            if not word[0].isupper():
                return False
        
        # Check for false positives
        name_lower = name.lower()
        for fp in self.name_false_positives:
            if fp in name_lower:
                return False
        
        # Additional validation: names shouldn't contain common job terms
        job_terms = ['developer', 'engineer', 'manager', 'analyst', 'assistant', 'former', 'current']
        for term in job_terms:
            if term in name_lower:
                return False
        
        return True
    
    def _is_valid_role(self, role: str) -> bool:
        """Validate if text is likely a real role"""
        if not role or len(role.strip()) < 3:
            return False
        
        role_lower = role.lower()
        
        # Check if role contains job-related keywords
        has_job_keyword = any(keyword in role_lower for keyword in self.valid_role_keywords)
        
        # Check if role contains technology keywords
        has_tech_keyword = any(keyword in role_lower for keyword in self.valid_tech_keywords)
        
        # Role is valid if it has job keywords or tech keywords
        return has_job_keyword or has_tech_keyword
    
    def _is_valid_email(self, email: str) -> bool:
        """Validate email format"""
        if not email or '@' not in email:
            return False
        
        email_pattern = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$'
        return re.match(email_pattern, email) is not None
    
    def _is_valid_phone(self, phone: str) -> bool:
        """Validate phone format"""
        if not phone:
            return False
        
        # Remove all non-digit characters
        digits_only = re.sub(r'\D', '', phone)
        
        # Check if it has reasonable length
        return 10 <= len(digits_only) <= 15
    
    def _find_role_in_context(self, text: str) -> Optional[str]:
        """Find role by looking for context around role keywords"""
        try:
            # Look for role keywords and extract surrounding context
            for keyword in self.valid_role_keywords:
                pattern = rf'\b([A-Za-z\s]*(?:senior|junior|lead|principal|staff)?\s*[A-Za-z\s]*{keyword}[A-Za-z\s]*)\b'
                matches = re.findall(pattern, text, re.IGNORECASE)
                if matches:
                    for match in matches:
                        role = match.strip()
                        if len(role) > 3 and len(role) < 50:
                            return role
            
            return None
            
        except Exception as e:
            logger.error(f"❌ Error finding role in context: {e}")
            return None
    
    def _infer_role_from_content(self, text: str) -> Optional[str]:
        """Infer role from content analysis"""
        try:
            text_lower = text.lower()
            
            # Check for specific technology combinations
            if 'java' in text_lower and 'spring' in text_lower:
                return 'Full Stack Java Developer'
            elif 'java' in text_lower:
                return 'Java Developer'
            elif 'python' in text_lower and ('django' in text_lower or 'flask' in text_lower):
                return 'Full Stack Python Developer'
            elif 'python' in text_lower:
                return 'Python Developer'
            elif 'javascript' in text_lower and ('react' in text_lower or 'angular' in text_lower):
                return 'Full Stack JavaScript Developer'
            elif 'javascript' in text_lower:
                return 'JavaScript Developer'
            elif 'react' in text_lower:
                return 'React Developer'
            elif 'angular' in text_lower:
                return 'Angular Developer'
            elif 'developer' in text_lower:
                return 'Software Developer'
            elif 'engineer' in text_lower:
                return 'Software Engineer'
            
            return None
            
        except Exception as e:
            logger.error(f"❌ Error inferring role from content: {e}")
            return None
    
    def _calculate_confidence(self, name: str, email: str, phone: str, role: str) -> float:
        """Calculate extraction confidence score"""
        try:
            confidence = 0.0
            
            # Name confidence (40%)
            if name != 'Name not found':
                confidence += 0.4
            
            # Role confidence (30%)
            if role != 'Role not found':
                confidence += 0.3
            
            # Email confidence (20%)
            if email != 'Email not found':
                confidence += 0.2
            
            # Phone confidence (10%)
            if phone != 'Phone not found':
                confidence += 0.1
            
            return min(confidence, 1.0)
            
        except Exception as e:
            logger.error(f"❌ Error calculating confidence: {e}")
            return 0.5
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        try:
            # Remove extra whitespace
            text = re.sub(r'\s+', ' ', text.strip())
            
            # Remove special characters but keep basic punctuation
            text = re.sub(r'[^\w\s@\.\-\+\(\)\/]', ' ', text)
            
            # Normalize line breaks
            text = re.sub(r'\n+', '\n', text)
            
            return text
            
        except Exception as e:
            logger.error(f"❌ Error cleaning text: {e}")
            return text
    
    def _get_empty_result(self) -> Dict[str, Any]:
        """Return empty result"""
        return {
            'name': 'Name not found',
            'email': 'Email not found',
            'phone': 'Phone not found',
            'role': 'Role not found',
            'raw_text': '',
            'extraction_method': 'accurate_name_role_extraction',
            'confidence_score': 0.0,
            'extraction_timestamp': datetime.now().isoformat()
        }

# Initialize global accurate extractor
accurate_name_role_extractor = AccurateNameRoleExtractor()





