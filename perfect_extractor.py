"""
Perfect Extractor
Ultra-accurate extraction for location and experience
"""

import re
import logging
from typing import Dict, List, Any
from smart_experience_extractor import smart_experience_extractor

logger = logging.getLogger(__name__)

class PerfectExtractor:
    """Perfect extractor for location and experience"""
    
    def __init__(self):
        # Comprehensive Indian cities
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
        
        # Experience patterns
        self.experience_patterns = [
            r'(\d+)\s*(?:to|-)?\s*(\d+)?\s*(?:years?|yrs?)\s*(?:of\s*)?(?:experience|exp)',
            r'(?:experience|exp)[:\s]*(\d+)\s*(?:to|-)?\s*(\d+)?\s*(?:years?|yrs?)',
            r'(\d+)\+?\s*(?:years?|yrs?)\s*(?:of\s*)?(?:experience|exp)',
            r'(?:total|overall)\s*(?:experience|exp)[:\s]*(\d+)\s*(?:years?|yrs?)',
            r'(\d+)\s*(?:to|-)?\s*(\d+)?\s*(?:years?|yrs?)\s*(?:of\s*)?(?:work|professional)',
            r'(?:work|professional)\s*(?:experience|exp)[:\s]*(\d+)\s*(?:to|-)?\s*(\d+)?\s*(?:years?|yrs?)',
            r'(?:over|more\s+than)\s+(\d+)\s*(?:years?|yrs?)',
            r'(\d+)\s*(?:years?|yrs?)\s*(?:plus|and\s+above)',
            r'(?:around|approximately|about)\s+(\d+)\s*(?:years?|yrs?)',
            r'(\d+)\s*(?:years?|yrs?)\s*(?:of\s*)?(?:industry|field|domain)',
            r'(?:industry|field|domain)\s*(?:experience|exp)[:\s]*(\d+)\s*(?:years?|yrs?)',
            r'(\d+)\s*(?:years?|yrs?)\s*(?:in\s*)?(?:software|development|engineering)',
            r'(?:software|development|engineering)\s*(?:experience|exp)[:\s]*(\d+)\s*(?:to|-)?\s*(\d+)?\s*(?:years?|yrs?)'
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
        """Extract location with perfect accuracy"""
        try:
            logger.info("📍 Starting perfect location extraction...")
            
            if not text or len(text.strip()) < 10:
                return 'Location not found'
            
            text_clean = self._clean_text(text)
            text_lower = text_clean.lower()
            
            # Get name words to exclude
            name_words = set()
            if name and name != 'Name not found':
                name_words = set(name.lower().split())
            
            # Strategy 1: Look for known cities in text
            for city in self.indian_cities:
                if city in text_lower and not any(name_word in city for name_word in name_words):
                    logger.info(f"✅ Found Indian city: {city}")
                    return city.title()
            
            # Strategy 2: Pattern-based extraction
            for pattern in self.location_patterns:
                match = re.search(pattern, text_clean, re.IGNORECASE)
                if match:
                    location = match.group(1).strip()
                    if len(location.split()) >= 1 and not any(name_word in location.lower() for name_word in name_words):
                        # Validate if it's a real location
                        location_lower = location.lower()
                        if any(city in location_lower for city in self.indian_cities):
                            logger.info(f"✅ Found location via pattern: {location}")
                            return location.title()
            
            # Strategy 3: Look for state names
            indian_states = {
                'karnataka', 'maharashtra', 'tamil nadu', 'west bengal', 'gujarat',
                'rajasthan', 'uttar pradesh', 'madhya pradesh', 'andhra pradesh',
                'telangana', 'kerala', 'odisha', 'assam', 'punjab', 'haryana',
                'delhi', 'goa', 'himachal pradesh', 'uttarakhand', 'bihar',
                'jharkhand', 'chhattisgarh', 'meghalaya', 'manipur', 'mizoram',
                'nagaland', 'arunachal pradesh', 'sikkim', 'tripura'
            }
            
            for state in indian_states:
                if state in text_lower and not any(name_word in state for name_word in name_words):
                    logger.info(f"✅ Found Indian state: {state}")
                    return state.title()
            
            logger.info("⚠️ No location found in resume")
            return 'Location not found'
            
        except Exception as e:
            logger.error(f"❌ Location extraction error: {e}")
            return 'Location extraction error'
    
    def extract_experience(self, text: str) -> Dict[str, Any]:
        """Extract experience using smart extractor"""
        try:
            logger.info("⏰ Starting perfect experience extraction...")
            
            # Use smart experience extractor for dynamic analysis
            experience_result = smart_experience_extractor.extract_experience(text)
            
            logger.info(f"✅ Perfect experience extraction completed: {experience_result['total_years']} years")
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
            'extraction_method': 'not_found'
        }

# Initialize global perfect extractor
perfect_extractor = PerfectExtractor()