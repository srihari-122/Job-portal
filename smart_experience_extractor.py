"""
Smart Experience Extractor
Dynamic experience extraction without hardcoding
"""

import re
import logging
from typing import Dict, List, Any

logger = logging.getLogger(__name__)

class SmartExperienceExtractor:
    """Smart experience extractor that learns from resume content"""
    
    def __init__(self):
        # Dynamic experience patterns
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
        
        # Dynamic position indicators
        self.position_indicators = {
            'senior': ['senior', 'sr', 'lead', 'principal', 'staff', 'architect'],
            'mid': ['mid', 'intermediate', 'experienced', 'skilled'],
            'junior': ['junior', 'jr', 'associate', 'entry'],
            'fresher': ['fresher', 'fresh', 'new', 'intern', 'trainee', 'beginner']
        }
        
        # Dynamic skill indicators
        self.skill_indicators = {
            'expert': ['expert', 'master', 'advanced', 'proficient', 'specialist'],
            'intermediate': ['intermediate', 'comfortable', 'familiar', 'working'],
            'beginner': ['beginner', 'learning', 'basic', 'introduction']
        }
    
    def extract_experience(self, text: str) -> Dict[str, Any]:
        """Extract experience dynamically from resume content"""
        try:
            logger.info("🧠 Starting smart experience extraction...")
            
            if not text or len(text.strip()) < 10:
                return self._get_fresher_result()
            
            text_clean = self._clean_text(text)
            text_lower = text_clean.lower()
            
            # Strategy 1: Direct experience statements
            explicit_experience = self._extract_explicit_experience(text_lower)
            if explicit_experience:
                logger.info(f"✅ Found explicit experience: {explicit_experience['total_years']} years")
                return explicit_experience
            
            # Strategy 2: Position-based analysis
            position_experience = self._analyze_position_level(text_lower)
            if position_experience:
                logger.info(f"✅ Analyzed position experience: {position_experience['total_years']} years")
                return position_experience
            
            # Strategy 3: Skill-based analysis
            skill_experience = self._analyze_skill_level(text_lower)
            if skill_experience:
                logger.info(f"✅ Analyzed skill experience: {skill_experience['total_years']} years")
                return skill_experience
            
            # Strategy 4: Context-based analysis
            context_experience = self._analyze_context(text_lower)
            if context_experience:
                logger.info(f"✅ Analyzed context experience: {context_experience['total_years']} years")
                return context_experience
            
            # If no experience found, declare as fresher
            logger.info("⚠️ No experience found - declaring as fresher")
            return self._get_fresher_result()
            
        except Exception as e:
            logger.error(f"❌ Smart experience extraction error: {e}")
            return self._get_fresher_result()
    
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
    
    def _analyze_position_level(self, text_lower: str) -> Dict[str, Any]:
        """Analyze experience based on position level"""
        try:
            position_scores = []
            
            # Check for position indicators
            for level, indicators in self.position_indicators.items():
                for indicator in indicators:
                    if indicator in text_lower:
                        if level == 'senior':
                            position_scores.append(6)
                        elif level == 'mid':
                            position_scores.append(3)
                        elif level == 'junior':
                            position_scores.append(1)
                        elif level == 'fresher':
                            position_scores.append(0)
            
            if position_scores:
                avg_experience = sum(position_scores) / len(position_scores)
                years = int(avg_experience)
                
                return {
                    'total_years': years,
                    'total_months': years * 12,
                    'display': f"{years} years" if years > 0 else "Fresher",
                    'extraction_method': 'position_analysis',
                    'is_fresher': years == 0
                }
            
            return None
        except Exception as e:
            logger.error(f"❌ Position analysis error: {e}")
            return None
    
    def _analyze_skill_level(self, text_lower: str) -> Dict[str, Any]:
        """Analyze experience based on skill level"""
        try:
            skill_scores = []
            
            # Check for skill indicators
            for level, indicators in self.skill_indicators.items():
                for indicator in indicators:
                    if indicator in text_lower:
                        if level == 'expert':
                            skill_scores.append(8)
                        elif level == 'intermediate':
                            skill_scores.append(4)
                        elif level == 'beginner':
                            skill_scores.append(1)
            
            if skill_scores:
                avg_experience = sum(skill_scores) / len(skill_scores)
                years = int(avg_experience)
                
                return {
                    'total_years': years,
                    'total_months': years * 12,
                    'display': f"{years} years" if years > 0 else "Fresher",
                    'extraction_method': 'skill_analysis',
                    'is_fresher': years == 0
                }
            
            return None
        except Exception as e:
            logger.error(f"❌ Skill analysis error: {e}")
            return None
    
    def _analyze_context(self, text_lower: str) -> Dict[str, Any]:
        """Analyze experience based on contextual indicators"""
        try:
            # Count various indicators
            indicators = {
                'years_mentioned': len(re.findall(r'\d+\s*(?:years?|yrs?)', text_lower)),
                'positions': len(re.findall(r'(?:developer|engineer|analyst|manager)', text_lower)),
                'projects': len(re.findall(r'(?:project|developed|built|created)', text_lower)),
                'technologies': len(re.findall(r'(?:java|python|javascript|react|angular)', text_lower)),
                'achievements': len(re.findall(r'(?:award|recognition|achievement)', text_lower)),
                'companies': len(re.findall(r'(?:company|corporation|inc|ltd)', text_lower))
            }
            
            # Calculate experience based on indicators
            total_score = 0
            total_weight = 0
            
            if indicators['years_mentioned'] > 0:
                total_score += indicators['years_mentioned'] * 2
                total_weight += 2
            
            if indicators['positions'] > 0:
                total_score += indicators['positions'] * 1.5
                total_weight += 1.5
            
            if indicators['projects'] > 0:
                total_score += indicators['projects'] * 1
                total_weight += 1
            
            if indicators['technologies'] > 0:
                total_score += indicators['technologies'] * 0.5
                total_weight += 0.5
            
            if indicators['achievements'] > 0:
                total_score += indicators['achievements'] * 1
                total_weight += 1
            
            if indicators['companies'] > 0:
                total_score += indicators['companies'] * 1
                total_weight += 1
            
            if total_weight > 0:
                estimated_years = min(int(total_score / total_weight), 15)
                
                return {
                    'total_years': estimated_years,
                    'total_months': estimated_years * 12,
                    'display': f"{estimated_years} years" if estimated_years > 0 else "Fresher",
                    'extraction_method': 'context_analysis',
                    'is_fresher': estimated_years == 0
                }
            
            return None
        except Exception as e:
            logger.error(f"❌ Context analysis error: {e}")
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

# Initialize global smart experience extractor
smart_experience_extractor = SmartExperienceExtractor()

