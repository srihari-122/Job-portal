"""
Direct Experience Extractor
Extract experience directly from resume text without calculation
"""

import re
import logging
from typing import Dict, List, Any

logger = logging.getLogger(__name__)

class DirectExperienceExtractor:
    """Direct experience extractor - only extract, don't calculate"""
    
    def __init__(self):
        # Direct experience patterns
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
        
        # Fresher indicators
        self.fresher_indicators = [
            'fresher', 'fresh graduate', 'recent graduate', 'new graduate',
            'entry level', 'junior', 'intern', 'trainee', 'associate',
            'no experience', '0 years', 'zero experience', 'beginner',
            'starting career', 'career starter', 'first job', 'new to industry'
        ]
    
    def extract_experience(self, text: str) -> Dict[str, Any]:
        """Extract experience directly from resume text"""
        try:
            logger.info("🎯 Starting direct experience extraction...")
            
            if not text or len(text.strip()) < 10:
                return self._get_fresher_result()
            
            text_clean = self._clean_text(text)
            text_lower = text_clean.lower()
            
            # Check for fresher indicators first
            if self._is_fresher(text_lower):
                logger.info("✅ Identified as fresher")
                return self._get_fresher_result()
            
            # Extract explicit experience
            experience_result = self._extract_explicit_experience(text_lower)
            
            if experience_result:
                logger.info(f"✅ Direct experience extraction completed: {experience_result['total_years']} years")
                return experience_result
            
            # If no explicit experience found, check for implicit indicators
            implicit_experience = self._extract_implicit_experience(text_lower)
            
            if implicit_experience:
                logger.info(f"✅ Implicit experience extraction completed: {implicit_experience['total_years']} years")
                return implicit_experience
            
            # If no experience found at all, declare as fresher
            logger.info("⚠️ No experience found - declaring as fresher")
            return self._get_fresher_result()
            
        except Exception as e:
            logger.error(f"❌ Direct experience extraction error: {e}")
            return self._get_fresher_result()
    
    def _is_fresher(self, text_lower: str) -> bool:
        """Check if resume indicates fresher status"""
        try:
            for indicator in self.fresher_indicators:
                if indicator in text_lower:
                    return True
            return False
        except Exception as e:
            logger.error(f"❌ Fresher check error: {e}")
            return False
    
    def _extract_explicit_experience(self, text_lower: str) -> Dict[str, Any]:
        """Extract explicit experience statements"""
        try:
            for pattern in self.experience_patterns:
                matches = re.findall(pattern, text_lower)
                for match in matches:
                    if isinstance(match, tuple):
                        years = int(match[0]) if match[0] else 0
                        if match[1]:
                            years = max(years, int(match[1]))
                    else:
                        years = int(match)
                    
                    if 0 < years <= 30:
                        return {
                            'total_years': years,
                            'total_months': years * 12,
                            'display': f"{years} years",
                            'extraction_method': 'explicit_statement',
                            'is_fresher': False
                        }
            
            return None
        except Exception as e:
            logger.error(f"❌ Explicit experience extraction error: {e}")
            return None
    
    def _extract_implicit_experience(self, text_lower: str) -> Dict[str, Any]:
        """Extract implicit experience from position levels"""
        try:
            # Position-based experience mapping
            position_experience = {
                'senior manager': 10, 'director': 12, 'vp': 15, 'cto': 18,
                'principal engineer': 8, 'staff engineer': 8, 'architect': 8,
                'engineering manager': 8, 'development manager': 8,
                'lead developer': 6, 'lead engineer': 6, 'tech lead': 6,
                'senior developer': 4, 'senior engineer': 4, 'senior analyst': 4,
                'software developer': 2, 'engineer': 2, 'analyst': 2,
                'junior developer': 1, 'junior engineer': 1, 'junior analyst': 1,
                'associate': 1, 'intern': 0, 'trainee': 0
            }
            
            for position, years in position_experience.items():
                if position in text_lower:
                    return {
                        'total_years': years,
                        'total_months': years * 12,
                        'display': f"{years} years" if years > 0 else "Fresher",
                        'extraction_method': 'position_based',
                        'is_fresher': years == 0
                    }
            
            return None
        except Exception as e:
            logger.error(f"❌ Implicit experience extraction error: {e}")
            return None
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text.strip())
        
        # Remove special characters but keep basic punctuation
        text = re.sub(r'[^\w\s@\.\-\+\(\)]', ' ', text)
        
        # Normalize line breaks
        text = re.sub(r'\n+', '\n', text)
        
        return text
    
    def _get_fresher_result(self) -> Dict[str, Any]:
        """Return fresher result"""
        return {
            'total_years': 0,
            'total_months': 0,
            'display': 'Fresher',
            'extraction_method': 'fresher_identified',
            'is_fresher': True
        }

# Initialize global direct experience extractor
direct_experience_extractor = DirectExperienceExtractor()

