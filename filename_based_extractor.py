import os
import re
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class FilenameBasedExtractor:
    def __init__(self):
        self.logger = logger
    
    def extract_resume_data_from_file(self, file_path):
        """Extract resume data using filename as fallback when text extraction fails"""
        try:
            self.logger.info(f"📄 Extracting resume data from file: {file_path}")
            
            # Extract text first
            text = self._extract_text_from_file(file_path)
            if not text:
                return self._get_empty_result()
            
            # Try to extract data from text
            extracted_data = self._extract_from_text(text, file_path)
            
            # If name extraction failed, try filename
            if extracted_data.get('name') == 'Name not found':
                filename_name = self._extract_name_from_filename(file_path)
                if filename_name:
                    extracted_data['name'] = filename_name
                    extracted_data['extraction_method'] = 'filename_based_extraction'
                    self.logger.info(f"✅ Name extracted from filename: {filename_name}")
            
            # If email extraction failed, try to find it in text
            if extracted_data.get('email') == 'Email not found':
                email = self._extract_email_from_text(text)
                if email:
                    extracted_data['email'] = email
                    self.logger.info(f"✅ Email extracted: {email}")
            
            # If phone extraction failed, try to find it in text
            if extracted_data.get('phone') == 'Phone not found':
                phone = self._extract_phone_from_text(text)
                if phone:
                    extracted_data['phone'] = phone
                    self.logger.info(f"✅ Phone extracted: {phone}")
            
            # If role extraction failed, try to find it in text
            if extracted_data.get('role') == 'Role not found':
                role = self._extract_role_from_text(text)
                if role:
                    extracted_data['role'] = role
                    self.logger.info(f"✅ Role extracted: {role}")
            
            # Add metadata
            extracted_data['extraction_timestamp'] = datetime.now().isoformat()
            extracted_data['confidence_score'] = 0.95 if extracted_data.get('name') != 'Name not found' else 0.3
            
            self.logger.info("✅ Filename-based extraction completed")
            return extracted_data
            
        except Exception as e:
            self.logger.error(f"❌ Filename-based extraction error: {str(e)}")
            return self._get_empty_result()
    
    def _extract_text_from_file(self, file_path):
        """Extract text from file"""
        try:
            if file_path.endswith('.pdf'):
                return self._extract_from_pdf(file_path)
            elif file_path.endswith('.docx'):
                return self._extract_from_docx(file_path)
            elif file_path.endswith('.txt'):
                return self._extract_from_txt(file_path)
            else:
                return ""
        except Exception as e:
            self.logger.error(f"❌ Text extraction error: {str(e)}")
            return ""
    
    def _extract_from_pdf(self, file_path):
        """Extract text from PDF"""
        try:
            import PyPDF2
            with open(file_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                text = ""
                for page in reader.pages:
                    text += page.extract_text() + "\n"
                return text
        except Exception as e:
            self.logger.error(f"❌ PDF extraction error: {str(e)}")
            return ""
    
    def _extract_from_docx(self, file_path):
        """Extract text from DOCX"""
        try:
            import docx
            doc = docx.Document(file_path)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text
        except Exception as e:
            self.logger.error(f"❌ DOCX extraction error: {str(e)}")
            return ""
    
    def _extract_from_txt(self, file_path):
        """Extract text from TXT"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except Exception as e:
            self.logger.error(f"❌ TXT extraction error: {str(e)}")
            return ""
    
    def _extract_name_from_filename(self, file_path):
        """Extract name from filename"""
        try:
            filename = os.path.basename(file_path)
            self.logger.info(f"🔍 Extracting name from filename: {filename}")
            
            # Remove file extension
            name_part = filename.replace('.pdf', '').replace('.docx', '').replace('.txt', '')
            
            # Remove email and timestamp parts
            name_part = re.sub(r'_\d+_', '_', name_part)  # Remove timestamp
            name_part = re.sub(r'@[^_]+_', '_', name_part)  # Remove email part
            
            # Split by underscores and take the last part (usually the actual filename)
            parts = name_part.split('_')
            if len(parts) > 1:
                # Take the last part which should be the resume name
                potential_name = parts[-1]
                
                # Clean up the name
                potential_name = potential_name.replace('_', ' ').replace('-', ' ')
                potential_name = re.sub(r'\s+', ' ', potential_name).strip()
                
                # Check if it looks like a name (contains letters and spaces)
                if re.match(r'^[A-Za-z\s]+$', potential_name) and len(potential_name.split()) >= 2:
                    return potential_name.title()
            
            return None
            
        except Exception as e:
            self.logger.error(f"❌ Filename name extraction error: {str(e)}")
            return None
    
    def _extract_from_text(self, text, file_path):
        """Extract data from text using basic patterns"""
        try:
            # Basic extraction
            name = self._extract_name_from_text(text)
            email = self._extract_email_from_text(text)
            phone = self._extract_phone_from_text(text)
            role = self._extract_role_from_text(text)
            location = self._extract_location_from_text(text)
            skills = self._extract_skills_from_text(text)
            experience = self._extract_experience_from_text(text)
            education = self._extract_education_from_text(text)
            
            return {
                'name': name,
                'email': email,
                'phone': phone,
                'role': role,
                'location': location,
                'skills': skills,
                'experience': experience,
                'education': education,
                'raw_text': text[:500] + "..." if len(text) > 500 else text,
                'extraction_method': 'filename_based_extraction'
            }
            
        except Exception as e:
            self.logger.error(f"❌ Text extraction error: {str(e)}")
            return self._get_empty_result()
    
    def _extract_name_from_text(self, text):
        """Extract name from text"""
        try:
            # Look for name patterns in the first few lines
            lines = text.split('\n')[:10]
            for line in lines:
                line = line.strip()
                if len(line) > 5 and len(line) < 50:
                    # Check if it looks like a name
                    if re.match(r'^[A-Z][a-z]+\s+[A-Z][a-z]+', line):
                        return line
            return 'Name not found'
        except:
            return 'Name not found'
    
    def _extract_email_from_text(self, text):
        """Extract email from text"""
        try:
            email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            match = re.search(email_pattern, text)
            return match.group() if match else 'Email not found'
        except:
            return 'Email not found'
    
    def _extract_phone_from_text(self, text):
        """Extract phone from text"""
        try:
            phone_patterns = [
                r'\b\d{10}\b',
                r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
                r'\b\+?\d{1,3}[-.]?\d{3,4}[-.]?\d{3,4}[-.]?\d{3,4}\b'
            ]
            for pattern in phone_patterns:
                match = re.search(pattern, text)
                if match:
                    return match.group()
            return 'Phone not found'
        except:
            return 'Phone not found'
    
    def _extract_role_from_text(self, text):
        """Extract role from text"""
        try:
            # Look for common role patterns
            role_patterns = [
                r'(?:Software|Full Stack|Frontend|Backend|Java|Python|React|Angular|Node\.js|MERN|MEAN)\s+(?:Developer|Engineer|Programmer)',
                r'(?:Developer|Engineer|Programmer|Analyst|Consultant|Manager|Lead|Senior|Junior)',
                r'(?:Data|Machine Learning|AI|DevOps|Cloud|Security|QA|Test)\s+(?:Engineer|Scientist|Analyst|Developer)'
            ]
            
            for pattern in role_patterns:
                match = re.search(pattern, text, re.IGNORECASE)
                if match:
                    return match.group().title()
            
            return 'Role not found'
        except:
            return 'Role not found'
    
    def _extract_location_from_text(self, text):
        """Extract location from text"""
        try:
            # Look for common Indian cities
            cities = ['Bangalore', 'Mumbai', 'Delhi', 'Chennai', 'Hyderabad', 'Pune', 'Kolkata', 'Ahmedabad']
            for city in cities:
                if city.lower() in text.lower():
                    return city
            return 'Location not found'
        except:
            return 'Location not found'
    
    def _extract_skills_from_text(self, text):
        """Extract skills from text"""
        try:
            # Common skills
            skills = ['Java', 'Python', 'JavaScript', 'React', 'Angular', 'Node.js', 'SQL', 'HTML', 'CSS', 'Git', 'AWS', 'Docker', 'Kubernetes', 'MongoDB', 'MySQL', 'PostgreSQL', 'Spring', 'Django', 'Flask', 'Express']
            found_skills = []
            text_lower = text.lower()
            
            for skill in skills:
                if skill.lower() in text_lower:
                    found_skills.append(skill)
            
            return found_skills[:20]  # Limit to 20 skills
        except:
            return []
    
    def _extract_experience_from_text(self, text):
        """Extract experience from text"""
        try:
            # Look for experience patterns
            exp_patterns = [
                r'(\d+)\s*years?\s*(?:of\s*)?experience',
                r'experience\s*:\s*(\d+)\s*years?',
                r'(\d+)\+?\s*years?\s*in'
            ]
            
            for pattern in exp_patterns:
                match = re.search(pattern, text, re.IGNORECASE)
                if match:
                    years = int(match.group(1))
                    return {
                        'total_years': years,
                        'total_months': years * 12,
                        'display': f'{years} years',
                        'is_fresher': years == 0,
                        'experience_periods': [],
                        'extraction_method': 'filename_based_extraction'
                    }
            
            return {
                'total_years': 0,
                'total_months': 0,
                'display': 'No experience found',
                'is_fresher': True,
                'experience_periods': [],
                'extraction_method': 'no_experience_found'
            }
        except:
            return {
                'total_years': 0,
                'total_months': 0,
                'display': 'No experience found',
                'is_fresher': True,
                'experience_periods': [],
                'extraction_method': 'no_experience_found'
            }
    
    def _extract_education_from_text(self, text):
        """Extract education from text"""
        try:
            # Look for education patterns
            education = []
            lines = text.split('\n')
            for line in lines:
                line = line.strip()
                if any(degree in line.lower() for degree in ['bachelor', 'master', 'phd', 'b.tech', 'm.tech', 'bca', 'mca', 'be', 'me']):
                    education.append(line)
            return education[:5]  # Limit to 5 entries
        except:
            return []
    
    def _get_empty_result(self):
        """Return empty result structure"""
        return {
            'name': 'Name not found',
            'email': 'Email not found',
            'phone': 'Phone not found',
            'role': 'Role not found',
            'location': 'Location not found',
            'skills': [],
            'experience': {
                'total_years': 0,
                'total_months': 0,
                'display': 'No experience found',
                'is_fresher': True,
                'experience_periods': [],
                'extraction_method': 'no_experience_found'
            },
            'education': [],
            'raw_text': '',
            'extraction_method': 'filename_based_extraction',
            'confidence_score': 0.1,
            'extraction_timestamp': datetime.now().isoformat()
        }

# Create instance
filename_based_extractor = FilenameBasedExtractor()
