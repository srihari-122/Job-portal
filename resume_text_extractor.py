"""
Resume Text Extractor
Accurate text extraction from resume files
"""

import re
import logging
import os
from typing import Dict, List, Any
import PyPDF2
import docx
import io
from trained_extractor import trained_extractor
from location_extractor import location_extractor
from improved_experience_extractor import improved_experience_extractor

logger = logging.getLogger(__name__)

class ResumeTextExtractor:
    """Accurate text extraction from resume files"""
    
    def __init__(self):
        # Email pattern
        self.email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        
        # Phone patterns
        self.phone_patterns = [
            r'\b\d{10}\b',  # 10 digits
            r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',  # XXX-XXX-XXXX
            r'\b\+91[-.]?\d{10}\b',  # +91-XXXXXXXXXX
            r'\b\d{4}[-.]?\d{3}[-.]?\d{3}\b'  # XXXX-XXX-XXX
        ]
        
        # Name patterns
        self.name_patterns = [
            r'^([A-Z][a-z]+ [A-Z][a-z]+)',  # First Last
            r'^([A-Z][a-z]+ [A-Z][a-z]+ [A-Z][a-z]+)',  # First Middle Last
            r'Name[:\s]*([A-Z][a-z]+ [A-Z][a-z]+)',  # Name: First Last
            r'Full Name[:\s]*([A-Z][a-z]+ [A-Z][a-z]+)',  # Full Name: First Last
        ]
        
        
        # Role patterns - more specific to avoid capturing names
        self.role_patterns = [
            r'(?:Position|Title|Role|Job Title|Designation|Current Role|Professional Title)[:\s]*([A-Za-z\s]{3,30})',
            r'(?:Working as|Currently|Role)[:\s]*([A-Za-z\s]{3,30})',
            r'(?:I am|I\'m)[:\s]*([A-Za-z\s]{3,30})',
            r'(?:As a|Being a)[:\s]*([A-Za-z\s]{3,30})',
            r'(?:Experienced|Skilled)[:\s]*([A-Za-z\s]{3,30})',
            r'(?:Passionate|Dedicated)[:\s]*([A-Za-z\s]{3,30})'
        ]
    
    def extract_text_from_file(self, file_content: bytes, filename: str) -> str:
        """Extract text from uploaded file"""
        try:
            logger.info(f"📄 Extracting text from file: {filename}")
            
            if filename.lower().endswith('.pdf'):
                return self._extract_from_pdf(file_content)
            elif filename.lower().endswith('.docx'):
                return self._extract_from_docx(file_content)
            elif filename.lower().endswith('.txt'):
                return self._extract_from_txt(file_content)
            else:
                logger.error(f"❌ Unsupported file format: {filename}")
                return ""
                
        except Exception as e:
            logger.error(f"❌ Text extraction error: {e}")
            return ""
    
    def extract_resume_data_from_file(self, file_path: str) -> Dict[str, Any]:
        """Extract resume data from file path"""
        try:
            logger.info(f"📄 Extracting resume data from file: {file_path}")
            
            # Read file content
            with open(file_path, 'rb') as file:
                file_content = file.read()
            
            # Extract text
            filename = os.path.basename(file_path)
            text = self.extract_text_from_file(file_content, filename)
            
            if not text:
                logger.error(f"❌ No text extracted from file: {file_path}")
                return {}
            
            # Extract resume data from text
            resume_data = self.extract_resume_data(text)
            logger.info("✅ Resume data extraction completed")
            return resume_data
            
        except Exception as e:
            logger.error(f"❌ Resume data extraction error: {e}")
            return {}
    
    def _extract_from_pdf(self, file_content: bytes) -> str:
        """Extract text from PDF"""
        try:
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(file_content))
            text = ""
            
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            
            return text.strip()
        except Exception as e:
            logger.error(f"❌ PDF extraction error: {e}")
            return ""
    
    def _extract_from_docx(self, file_content: bytes) -> str:
        """Extract text from DOCX"""
        try:
            doc = docx.Document(io.BytesIO(file_content))
            text = ""
            
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            
            return text.strip()
        except Exception as e:
            logger.error(f"❌ DOCX extraction error: {e}")
            return ""
    
    def _extract_from_txt(self, file_content: bytes) -> str:
        """Extract text from TXT"""
        try:
            return file_content.decode('utf-8').strip()
        except Exception as e:
            logger.error(f"❌ TXT extraction error: {e}")
            return ""
    
    def extract_resume_data(self, text: str) -> Dict[str, Any]:
        """Extract all resume data from text"""
        try:
            logger.info("🔍 Starting resume data extraction...")
            
            if not text or len(text.strip()) < 10:
                return self._get_empty_result()
            
            # Clean text
            text_clean = self._clean_text(text)
            
            # Extract individual components
            name = self._extract_name(text_clean)
            email = self._extract_email(text_clean)
            phone = self._extract_phone(text_clean)
            role = self._extract_role(text_clean)
            
            # Use trained extractors for location, experience and skills
            location = location_extractor.extract_location(text_clean, name)
            experience = improved_experience_extractor.extract_experience(text_clean)
            skills = trained_extractor.extract_skills(text_clean)
            
            result = {
                'name': name,
                'email': email,
                'phone': phone,
                'location': location,
                'experience': experience,
                'role': role,
                'skills': skills,
                'raw_text': text_clean[:500] if text_clean else '',
                'extraction_method': 'text_extraction',
                'extraction_timestamp': '2024-01-01T00:00:00'
            }
            
            logger.info("✅ Resume data extraction completed")
            logger.info(f"🔍 Extracted data - Name: '{name}', Role: '{role}', Experience: {experience}, Skills: {len(skills)}, Location: '{location}'")
            logger.info(f"🔍 Skills list: {skills}")
            return result
            
        except Exception as e:
            logger.error(f"❌ Resume data extraction error: {e}")
            return self._get_empty_result()
    
    def _extract_name(self, text: str) -> str:
        """Extract name from text"""
        try:
            lines = text.split('\n')
            
            # Check first few lines for name patterns
            for line in lines[:5]:
                line = line.strip()
                if len(line) > 5 and len(line) < 50:
                    for pattern in self.name_patterns:
                        match = re.search(pattern, line, re.IGNORECASE)
                        if match:
                            return match.group(1).strip()
            
            # Fallback: look for common name patterns
            for pattern in self.name_patterns:
                match = re.search(pattern, text, re.IGNORECASE)
                if match:
                    return match.group(1).strip()
            
            # Additional fallback: look for capitalized words at the beginning
            first_line = lines[0].strip() if lines else ""
            if first_line and len(first_line.split()) >= 2:
                words = first_line.split()
                if all(word[0].isupper() for word in words[:2]):
                    return " ".join(words[:2])
            
            return 'Name not found'
        except Exception as e:
            logger.error(f"❌ Name extraction error: {e}")
            return 'Name not found'
    
    def _extract_email(self, text: str) -> str:
        """Extract email from text"""
        try:
            match = re.search(self.email_pattern, text)
            if match:
                return match.group(0).strip()
            return 'Email not found'
        except Exception as e:
            logger.error(f"❌ Email extraction error: {e}")
            return 'Email not found'
    
    def _extract_phone(self, text: str) -> str:
        """Extract phone from text"""
        try:
            for pattern in self.phone_patterns:
                match = re.search(pattern, text)
                if match:
                    return match.group(0).strip()
            return 'Phone not found'
        except Exception as e:
            logger.error(f"❌ Phone extraction error: {e}")
            return 'Phone not found'
    
    
    
    def _extract_role(self, text: str) -> str:
        """Extract role from text with improved specificity"""
        try:
            logger.info(f"🔍 Starting role extraction from text")
            logger.info(f"📝 Original text: {text[:200]}...")
            
            # First, look for exact role patterns in the text
            exact_role_patterns = [
                # Full Stack Developer patterns
                r'\b(Full\s*Stack\s*(?:Java|Python|JavaScript|\.NET|PHP)\s*Developer)\b',
                r'\b(Full\s*Stack\s*Developer)\b',
                # Specific technology + Developer patterns
                r'\b(Java\s*Developer)\b',
                r'\b(Python\s*Developer)\b',
                r'\b(JavaScript\s*Developer)\b',
                r'\b(React\s*Developer)\b',
                r'\b(Angular\s*Developer)\b',
                r'\b(Node\.js\s*Developer)\b',
                r'\b(Spring\s*Boot\s*Developer)\b',
                # Seniority + Technology patterns
                r'\b(Senior\s*(?:Full\s*Stack|Java|Python|JavaScript|React|Angular)\s*Developer)\b',
                r'\b(Lead\s*(?:Full\s*Stack|Java|Python|JavaScript|React|Angular)\s*Developer)\b',
                # Other specific roles
                r'\b(Software\s*Engineer)\b',
                r'\b(Web\s*Developer)\b',
                r'\b(Frontend\s*Developer)\b',
                r'\b(Backend\s*Developer)\b',
                r'\b(Mobile\s*Developer)\b',
                r'\b(Data\s*Scientist)\b',
                r'\b(Data\s*Analyst)\b',
                r'\b(DevOps\s*Engineer)\b',
                r'\b(QA\s*Engineer)\b',
                r'\b(UI\/UX\s*Designer)\b',
            ]
            
            # Try exact role patterns first
            for i, pattern in enumerate(exact_role_patterns):
                matches = re.findall(pattern, text, re.IGNORECASE)
                if matches:
                    role = matches[0].strip()
                    logger.info(f"✅ Exact role extracted with pattern {i+1}: {role}")
                    return role.title()
            
            # Fallback: look for complete role phrases in the original text
            complete_role_patterns = [
                # Look for complete role descriptions
                r'\b([A-Z][a-z\s]*(?:Full\s*Stack|Frontend|Backend|Mobile|Web|Data|Cloud|Security|DevOps|QA|UI|UX|Software|Machine\s*Learning|Artificial\s*Intelligence|Network|Database|Game|Embedded|System|Platform|Product|Technical)\s*[A-Za-z\s]*(?:Developer|Engineer|Analyst|Manager|Consultant|Specialist|Architect|Lead|Designer))\b',
                # Look for Java/Python/JavaScript specific roles
                r'\b([A-Z][a-z\s]*(?:Java|Python|JavaScript|React|Angular|Node\.js|Spring|Django|Flask|Express)\s*[A-Za-z\s]*(?:Developer|Engineer|Specialist))\b',
                # Look for seniority + technology combinations
                r'\b([A-Z][a-z\s]*(?:Senior|Junior|Lead|Principal|Staff)\s*[A-Za-z\s]*(?:Full\s*Stack|Frontend|Backend|Mobile|Web|Data|Cloud|Security|DevOps|QA|UI|UX|Software|Machine\s*Learning|Artificial\s*Intelligence|Network|Database|Game|Embedded|System|Platform|Product|Technical)\s*[A-Za-z\s]*(?:Developer|Engineer|Analyst|Manager|Consultant|Specialist|Architect|Lead|Designer))\b',
            ]
            
            # Try complete role patterns first
            for i, pattern in enumerate(complete_role_patterns):
                matches = re.findall(pattern, text, re.IGNORECASE)
                if matches:
                    for match in matches:
                        role = match.strip()
                        role = self._clean_role_text(role)
                        if self._is_valid_role(role) and len(role.split()) >= 2:  # Ensure it's specific enough
                            logger.info(f"✅ Complete role extracted with pattern {i+1}: {role}")
                            return role.title()
            
            # If no complete role found, try partial patterns
            partial_patterns = [
                r'\b([A-Za-z\s]*(?:Full\s*Stack|Frontend|Backend|Mobile|Web|Data|Cloud|Security|DevOps|QA|UI|UX|Software|Machine\s*Learning|Artificial\s*Intelligence|Network|Database|Game|Embedded|System|Platform|Product|Technical)\s*[A-Za-z\s]*(?:Developer|Engineer|Analyst|Manager|Consultant|Specialist|Architect|Lead|Designer))\b',
                r'\b([A-Za-z\s]*(?:Java|Python|JavaScript|React|Angular|Node\.js|Spring|Django|Flask|Express)\s*[A-Za-z\s]*(?:Developer|Engineer|Specialist))\b',
            ]
            
            for i, pattern in enumerate(partial_patterns):
                matches = re.findall(pattern, text, re.IGNORECASE)
                if matches:
                    for match in matches:
                        role = match.strip()
                        role = self._clean_role_text(role)
                        if self._is_valid_role(role):
                            logger.info(f"✅ Partial role extracted with pattern {i+1}: {role}")
                            return role.title()
            
            # Fallback: look for specific role combinations in order of specificity
            specific_roles = [
                'full stack java developer', 'full stack python developer', 'full stack javascript developer',
                'java full stack developer', 'python full stack developer', 'javascript full stack developer',
                'senior full stack developer', 'lead full stack developer', 'principal full stack developer',
                'full stack developer', 'frontend developer', 'backend developer',
                'java developer', 'python developer', 'javascript developer',
                'react developer', 'angular developer', 'node.js developer',
                'spring boot developer', 'django developer', 'flask developer',
                'data scientist', 'data analyst', 'machine learning engineer',
                'devops engineer', 'qa engineer', 'ui designer', 'ux designer',
                'mobile developer', 'web developer', 'software engineer',
                'cloud engineer', 'security engineer', 'database administrator',
                'product manager', 'project manager', 'technical lead',
                'solution architect', 'system architect', 'platform engineer'
            ]
            
            text_lower = text.lower()
            for role in specific_roles:
                if role in text_lower:
                    logger.info(f"✅ Role found in specific roles: {role}")
                    return role.title()
            
            logger.warning(f"⚠️ No valid role found in text")
            return 'Role not found'
            
        except Exception as e:
            logger.error(f"❌ Role extraction error: {e}")
            return 'Role not found'
    
    def _preprocess_text_for_role_extraction(self, text: str) -> str:
        """Preprocess text to remove names and irrelevant content before role extraction"""
        # Convert to lowercase for processing
        text_lower = text.lower()
        
        # Remove common name patterns
        text_lower = re.sub(r'\b[a-z]+ [a-z]+\b', '', text_lower)  # Remove "first last" patterns
        
        # Remove specific names that might appear
        common_names = [
            'manjari', 'madyalkar', 'john', 'jane', 'smith', 'johnson', 'williams', 'brown', 'jones',
            'garcia', 'miller', 'davis', 'rodriguez', 'martinez', 'hernandez', 'lopez', 'gonzalez',
            'wilson', 'anderson', 'thomas', 'taylor', 'moore', 'jackson', 'martin', 'lee', 'perez',
            'thompson', 'white', 'harris', 'sanchez', 'clark', 'ramirez', 'lewis', 'robinson', 'walker',
            'young', 'allen', 'king', 'wright', 'scott', 'torres', 'nguyen', 'hill', 'flores', 'green',
            'adams', 'nelson', 'baker', 'hall', 'rivera', 'campbell', 'mitchell', 'carter', 'roberts'
        ]
        
        for name in common_names:
            text_lower = re.sub(r'\b' + name + r'\b', '', text_lower)
        
        # Remove common prefixes
        text_lower = re.sub(r'\b(mr|mrs|ms|dr|prof)\s+', '', text_lower)
        
        # Remove extra whitespace
        text_lower = re.sub(r'\s+', ' ', text_lower.strip())
        
        return text_lower
    
    def _is_valid_role(self, role: str) -> bool:
        """Check if the extracted role is valid"""
        if not role or len(role.strip()) < 3:
            return False
        
        # Check if role contains job-related keywords
        job_keywords = [
            'developer', 'engineer', 'analyst', 'manager', 'designer', 'architect', 
            'specialist', 'consultant', 'lead', 'senior', 'junior', 'associate', 
            'intern', 'trainee', 'coordinator', 'supervisor', 'director', 'executive',
            'programmer', 'coder', 'technician', 'administrator', 'officer'
        ]
        
        role_lower = role.lower()
        has_job_keyword = any(keyword in role_lower for keyword in job_keywords)
        
        # Check if role contains technology keywords
        tech_keywords = [
            'java', 'python', 'javascript', 'react', 'angular', 'node', 'spring',
            'sql', 'mongodb', 'aws', 'azure', 'docker', 'kubernetes', 'git',
            'html', 'css', 'bootstrap', 'jquery', 'express', 'django', 'flask'
        ]
        
        has_tech_keyword = any(keyword in role_lower for keyword in tech_keywords)
        
        # Role is valid if it has job keywords or tech keywords
        return has_job_keyword or has_tech_keyword
    
    def _clean_role_text(self, role: str) -> str:
        """Clean role text to remove names and irrelevant content"""
        # Remove common name patterns more aggressively
        role = re.sub(r'\b[A-Z][a-z]+ [A-Z][a-z]+\b', '', role)  # Remove "First Last" patterns
        role = re.sub(r'\b[A-Z][a-z]+\b(?=\s+[A-Z][a-z]+)', '', role)  # Remove first name if followed by last name
        
        # Remove specific name patterns that might appear in roles
        role = re.sub(r'\b(manjari|madyalkar|john|jane|smith|johnson|williams|brown|jones|garcia|miller|davis|rodriguez|martinez|hernandez|lopez|gonzalez|wilson|anderson|thomas|taylor|moore|jackson|martin|lee|perez|thompson|white|harris|sanchez|clark|ramirez|lewis|robinson|walker|young|allen|king|wright|scott|torres|nguyen|hill|flores|green|adams|nelson|baker|hall|rivera|campbell|mitchell|carter|roberts)\b', '', role, flags=re.IGNORECASE)
        
        # Remove common prefixes that might be names
        role = re.sub(r'^(mr|mrs|ms|dr|prof)\s+', '', role, flags=re.IGNORECASE)
        
        # Remove extra whitespace
        role = re.sub(r'\s+', ' ', role.strip())
        
        return role
    
    def _find_role_context(self, text: str, keyword: str) -> str:
        """Find the context around a role keyword"""
        # Find the position of the keyword
        pos = text.find(keyword)
        if pos == -1:
            return None
        
        # Extract context around the keyword (50 characters before and after)
        start = max(0, pos - 50)
        end = min(len(text), pos + len(keyword) + 50)
        context = text[start:end]
        
        # Look for role patterns in the context
        role_patterns = [
            r'([a-z\s]*(?:senior|junior|lead|principal|staff)?\s*[a-z\s]*' + keyword + r'[a-z\s]*)',
            r'([a-z\s]*(?:full\s*stack|frontend|backend|mobile|web|data|cloud|security|devops|qa|ui|ux)\s*[a-z\s]*' + keyword + r'[a-z\s]*)',
            r'([a-z\s]*(?:software|data|machine\s*learning|artificial\s*intelligence|cloud|security|network|database|web|mobile|game|embedded|system|platform|product|technical)\s*[a-z\s]*' + keyword + r'[a-z\s]*)'
        ]
        
        for pattern in role_patterns:
            match = re.search(pattern, context, re.IGNORECASE)
            if match:
                role = match.group(1).strip()
                role = self._clean_role_text(role)
                if len(role) > 3 and len(role) < 30:
                    return role
        
        return keyword
    
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text.strip())
        
        # Remove special characters but keep basic punctuation
        text = re.sub(r'[^\w\s@\.\-\+\(\)]', ' ', text)
        
        # Normalize line breaks
        text = re.sub(r'\n+', '\n', text)
        
        return text
    
    def _get_empty_result(self) -> Dict[str, Any]:
        """Return empty result"""
        return {
            'name': 'Name not found',
            'email': 'Email not found',
            'phone': 'Phone not found',
            'location': 'Location not found',
            'experience': {
                'total_years': 0,
                'total_months': 0,
                'display': 'Experience not found'
            },
            'role': 'Role not found',
            'skills': [],
            'raw_text': '',
            'extraction_method': 'text_extraction',
            'extraction_timestamp': '2024-01-01T00:00:00'
        }

    def _clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text.strip())
        
        # Remove special characters but keep basic punctuation
        text = re.sub(r'[^\w\s@\.\-\+\(\)]', ' ', text)
        
        # Normalize line breaks
        text = re.sub(r'\n+', '\n', text)
        
        return text
    
    def _get_empty_result(self) -> Dict[str, Any]:
        """Return empty result"""
        return {
            'name': 'Name not found',
            'email': 'Email not found',
            'phone': 'Phone not found',
            'location': 'Location not found',
            'experience': {
                'total_years': 0,
                'total_months': 0,
                'display': 'Experience not found'
            },
            'role': 'Role not found',
            'skills': [],
            'raw_text': '',
            'extraction_method': 'text_extraction',
            'extraction_timestamp': '2024-01-01T00:00:00'
        }

# Initialize global resume text extractor
resume_text_extractor = ResumeTextExtractor()

