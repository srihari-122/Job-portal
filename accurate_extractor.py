"""
Accurate Location and Experience Extractor
Ultra-precise extraction for location and experience
"""

import re
import logging
from datetime import datetime
from typing import Dict, List, Any, Tuple
from perfect_extractor import perfect_extractor

logger = logging.getLogger(__name__)

class AccurateExtractor:
    """Accurate extractor for location and experience"""
    
    def __init__(self):
        # Comprehensive Indian cities and locations
        self.indian_cities = {
            'bangalore', 'bengaluru', 'mumbai', 'delhi', 'hyderabad', 'pune', 'chennai', 'kolkata',
            'ahmedabad', 'gurgaon', 'noida', 'jaipur', 'lucknow', 'indore', 'bhopal',
            'chandigarh', 'coimbatore', 'kochi', 'thiruvananthapuram', 'mysore', 'mangalore',
            'vadodara', 'surat', 'rajkot', 'bhubaneswar', 'bhubaneshwar', 'cuttack',
            'guwahati', 'shillong', 'imphal', 'aizawl', 'kohima', 'itanagar', 'gangtok',
            'kalaburgi', 'gulbarga', 'hubli', 'dharwad', 'belgaum', 'bellary', 'tumkur',
            'raichur', 'bidar', 'hospet', 'gadag', 'bagalkot', 'bijapur', 'kolar',
            'mandya', 'hassan', 'udupi', 'dakshina kannada', 'chikmagalur',
            'chitradurga', 'davangere', 'shimoga', 'chamrajanagar', 'kodagu', 'mysuru',
            'bangalore urban', 'bangalore rural', 'bangalore city', 'bangalore metro',
            'mumbai city', 'mumbai suburban', 'greater mumbai', 'mumbai metro',
            'delhi ncr', 'new delhi', 'delhi metro', 'ncr', 'gurugram', 'faridabad',
            'hyderabad city', 'greater hyderabad', 'hyderabad metro',
            'pune city', 'greater pune', 'pune metro',
            'chennai city', 'greater chennai', 'chennai metro',
            'kolkata city', 'greater kolkata', 'kolkata metro'
        }
        
        # International cities
        self.international_cities = {
            'new york', 'san francisco', 'los angeles', 'chicago', 'boston', 'seattle',
            'austin', 'denver', 'miami', 'atlanta', 'dallas', 'houston', 'phoenix',
            'london', 'paris', 'berlin', 'madrid', 'rome', 'amsterdam', 'zurich',
            'singapore', 'hong kong', 'tokyo', 'seoul', 'sydney', 'melbourne', 'toronto',
            'vancouver', 'montreal', 'dubai', 'abu dhabi', 'riyadh', 'doha', 'kuwait'
        }
        
        # Experience patterns with high accuracy
        self.experience_patterns = [
            # Direct experience statements
            r'(\d+)\s*(?:to|-)?\s*(\d+)?\s*(?:years?|yrs?)\s*(?:of\s*)?(?:experience|exp)',
            r'(?:experience|exp)[:\s]*(\d+)\s*(?:to|-)?\s*(\d+)?\s*(?:years?|yrs?)',
            r'(\d+)\+?\s*(?:years?|yrs?)\s*(?:of\s*)?(?:experience|exp)',
            r'(?:total|overall)\s*(?:experience|exp)[:\s]*(\d+)\s*(?:years?|yrs?)',
            r'(\d+)\s*(?:to|-)?\s*(\d+)?\s*(?:years?|yrs?)\s*(?:of\s*)?(?:work|professional)',
            r'(?:work|professional)\s*(?:experience|exp)[:\s]*(\d+)\s*(?:to|-)?\s*(\d+)?\s*(?:years?|yrs?)',
            r'(\d+)\s*(?:to|-)?\s*(\d+)?\s*(?:years?|yrs?)\s*(?:in\s*)?(?:software|development|engineering)',
            r'(?:software|development|engineering)\s*(?:experience|exp)[:\s]*(\d+)\s*(?:to|-)?\s*(\d+)?\s*(?:years?|yrs?)',
            r'(?:over|more\s+than)\s+(\d+)\s*(?:years?|yrs?)',
            r'(\d+)\s*(?:years?|yrs?)\s*(?:plus|and\s+above)',
            r'(?:around|approximately|about)\s+(\d+)\s*(?:years?|yrs?)',
            r'(\d+)\s*(?:years?|yrs?)\s*(?:of\s*)?(?:industry|field|domain)',
            r'(?:industry|field|domain)\s*(?:experience|exp)[:\s]*(\d+)\s*(?:years?|yrs?)',
            
            # Date-based patterns
            r'(\d{4})\s*(?:to|-)?\s*(?:present|current|now|\d{4})',
            r'(?:since|from)\s+(\d{4})',
            r'(?:started|began)\s+(?:in\s+)?(\d{4})',
            r'(?:joined|employed)\s+(?:in\s+)?(\d{4})',
            r'(?:working\s+since|employed\s+since)\s+(\d{4})',
            r'(?:career\s+started|professional\s+journey)\s+(\d{4})',
            r'(?:first\s+job|first\s+position)\s+(\d{4})',
            r'(?:entry\s+into\s+industry)\s+(\d{4})',
            
            # Graduation-based patterns
            r'(?:graduated|completed|finished)\s+(?:in\s+)?(\d{4})',
            r'(?:bachelor|master|phd|diploma|degree)\s+(?:in\s+)?\d{4}',
            r'(\d{4})\s*(?:batch|graduation|passout)',
            r'(?:class\s+of|batch\s+of)\s+(\d{4})',
            r'(?:b\.tech|m\.tech|b\.e|m\.e|b\.sc|m\.sc)\s+(\d{4})',
            r'(?:engineering|computer\s+science)\s+(\d{4})',
            
            # Position-based patterns
            r'(?:senior|lead|principal|staff)\s+(?:developer|engineer|analyst|manager)',
            r'(?:junior|associate|intern|trainee)',
            r'(?:software\s+developer|engineer|analyst|manager|consultant|specialist|architect)',
            r'(?:team\s+lead|project\s+manager|technical\s+lead)',
            r'(?:engineering\s+manager|development\s+manager)',
            r'(?:tech\s+lead|technical\s+architect)',
            
            # Skill level patterns
            r'(?:expert|advanced|intermediate|beginner)',
            r'(?:proficient|skilled|experienced|senior)',
            r'(?:master|specialist|architect)',
            r'(?:years?\s+of\s+)?(?:expertise|experience)',
            r'(?:strong|solid|extensive)\s+(?:background|experience)',
            r'(?:deep|comprehensive|thorough)\s+(?:knowledge|understanding)'
        ]
        
        # Location patterns
        self.location_patterns = [
            r'location[:\s]*([A-Za-z\s]{3,40})',
            r'address[:\s]*([A-Za-z\s]{3,40})',
            r'city[:\s]*([A-Za-z\s]{3,40})',
            r'based\s+in[:\s]*([A-Za-z\s]{3,40})',
            r'located\s+in[:\s]*([A-Za-z\s]{3,40})',
            r'residing\s+in[:\s]*([A-Za-z\s]{3,40})',
            r'from[:\s]*([A-Za-z\s]{3,40})',
            r'lives\s+in[:\s]*([A-Za-z\s]{3,40})',
            r'stays\s+in[:\s]*([A-Za-z\s]{3,40})',
            r'current\s+location[:\s]*([A-Za-z\s]{3,40})',
            r'present\s+location[:\s]*([A-Za-z\s]{3,40})',
            r'work\s+location[:\s]*([A-Za-z\s]{3,40})',
            r'office\s+location[:\s]*([A-Za-z\s]{3,40})',
            r'job\s+location[:\s]*([A-Za-z\s]{3,40})',
            r'employment\s+location[:\s]*([A-Za-z\s]{3,40})',
            r'residence[:\s]*([A-Za-z\s]{3,40})',
            r'domicile[:\s]*([A-Za-z\s]{3,40})',
            r'permanent\s+address[:\s]*([A-Za-z\s]{3,40})',
            r'current\s+address[:\s]*([A-Za-z\s]{3,40})',
            r'contact\s+address[:\s]*([A-Za-z\s]{3,40})'
        ]
    
    def extract_location(self, text: str, name: str = None) -> str:
        """Extract location using perfect extractor"""
        try:
            logger.info("📍 Starting accurate location extraction...")
            
            # Use perfect extractor for maximum accuracy
            location = perfect_extractor.extract_location(text, name)
            
            logger.info(f"✅ Accurate location extraction completed: {location}")
            return location
            
        except Exception as e:
            logger.error(f"❌ Location extraction error: {e}")
            return 'Location extraction error'
    
    def extract_experience(self, text: str) -> Dict[str, Any]:
        """Extract experience using perfect extractor"""
        try:
            logger.info("🤖 Starting accurate experience extraction...")
            
            # Use perfect extractor for maximum accuracy
            experience_result = perfect_extractor.extract_experience(text)
            
            logger.info(f"✅ Accurate experience extraction completed: {experience_result['total_years']} years")
            return experience_result
            
        except Exception as e:
            logger.error(f"❌ Experience extraction error: {e}")
            return self._get_empty_experience()
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text.strip())
        
        # Remove special characters but keep basic punctuation
        text = re.sub(r'[^\w\s@\.\-\+\(\)]', ' ', text)
        
        # Normalize line breaks
        text = re.sub(r'\n+', '\n', text)
        
        return text
    
    def _get_empty_experience(self) -> Dict[str, Any]:
        """Return empty experience result"""
        return {
            'total_years': 0,
            'total_months': 0,
            'display': 'Experience not found',
            'extraction_method': 'not_found',
            'confidence': 0.0
        }

# Initialize global accurate extractor instance
accurate_extractor = AccurateExtractor()
