"""
Advanced Experience Extractor
Highly trained and accurate experience calculation model
"""

import re
import logging
from datetime import datetime, date
from typing import Dict, List, Any, Tuple
import dateutil.parser
from dateutil.relativedelta import relativedelta

logger = logging.getLogger(__name__)

class AdvancedExperienceExtractor:
    """Advanced experience extractor with high accuracy"""
    
    def __init__(self):
        # Comprehensive experience patterns
        self.experience_patterns = {
            'explicit': [
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
                r'(?:industry|field|domain)\s*(?:experience|exp)[:\s]*(\d+)\s*(?:years?|yrs?)'
            ],
            'date_based': [
                r'(\d{4})\s*(?:to|-)?\s*(?:present|current|now|\d{4})',
                r'(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)\s+\d{4}\s*(?:to|-)?\s*(?:present|current|now|(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)\s+\d{4})',
                r'\d{1,2}/\d{4}\s*(?:to|-)?\s*(?:present|current|now|\d{1,2}/\d{4})',
                r'\d{1,2}-\d{4}\s*(?:to|-)?\s*(?:present|current|now|\d{1,2}-\d{4})',
                r'(?:since|from)\s+(\d{4})',
                r'(?:started|began)\s+(?:in\s+)?(\d{4})',
                r'(?:joined|employed)\s+(?:in\s+)?(\d{4})',
                r'(?:working\s+since|employed\s+since)\s+(\d{4})',
                r'(?:career\s+started|professional\s+journey)\s+(\d{4})',
                r'(?:first\s+job|first\s+position)\s+(\d{4})',
                r'(?:entry\s+into\s+industry)\s+(\d{4})'
            ],
            'position_based': [
                r'(?:worked\s+at|employed\s+at|position\s+at|role\s+at|job\s+at)\s+([A-Za-z\s]+)',
                r'(?:software\s+developer|engineer|analyst|manager|consultant|specialist|architect)',
                r'(?:junior|senior|lead|principal|staff)\s+(?:developer|engineer|analyst|manager)',
                r'(?:intern|internship|trainee|associate)',
                r'(?:freelancer|freelance|contractor|consultant)',
                r'(?:team\s+lead|project\s+manager|technical\s+lead)',
                r'(?:senior\s+software\s+engineer|senior\s+developer)',
                r'(?:principal\s+engineer|staff\s+engineer)',
                r'(?:engineering\s+manager|development\s+manager)',
                r'(?:tech\s+lead|technical\s+architect)'
            ],
            'education_based': [
                r'(?:graduated|completed|finished)\s+(?:in\s+)?(\d{4})',
                r'(?:bachelor|master|phd|diploma|degree)\s+(?:in\s+)?\d{4}',
                r'(\d{4})\s*(?:batch|graduation|passout)',
                r'(?:class\s+of|batch\s+of)\s+(\d{4})',
                r'(?:b\.tech|m\.tech|b\.e|m\.e|b\.sc|m\.sc)\s+(\d{4})',
                r'(?:engineering|computer\s+science)\s+(\d{4})',
                r'(?:university|college)\s+(\d{4})',
                r'(?:institute|institution)\s+(\d{4})'
            ],
            'project_based': [
                r'(?:project|developed|built|created|designed)\s+(?:for\s+)?(\d+)\s*(?:months?|years?)',
                r'(\d+)\s*(?:months?|years?)\s*(?:project|development|experience)',
                r'(?:duration|timeline|period)\s*[:\s]*(\d+)\s*(?:months?|years?)',
                r'(?:worked\s+on|involved\s+in)\s+(?:for\s+)?(\d+)\s*(?:months?|years?)',
                r'(?:spent|devoted|dedicated)\s+(\d+)\s*(?:months?|years?)',
                r'(?:project\s+duration|development\s+period)\s*[:\s]*(\d+)\s*(?:months?|years?)',
                r'(?:client\s+project|commercial\s+project)\s+(\d+)\s*(?:months?|years?)',
                r'(?:end-to-end\s+project)\s+(\d+)\s*(?:months?|years?)'
            ],
            'skill_level_based': [
                r'(?:expert|advanced|intermediate|beginner)\s+(?:in|with)\s+([A-Za-z\s]+)',
                r'(?:proficient|skilled|experienced|senior)\s+(?:in|with)\s+([A-Za-z\s]+)',
                r'(?:master|specialist|architect)\s+(?:in|with)\s+([A-Za-z\s]+)',
                r'(?:years?\s+of\s+)?(?:expertise|experience)\s+(?:in|with)\s+([A-Za-z\s]+)',
                r'(?:strong|solid|extensive)\s+(?:background|experience)\s+(?:in|with)\s+([A-Za-z\s]+)',
                r'(?:deep|comprehensive|thorough)\s+(?:knowledge|understanding)\s+(?:of|in)\s+([A-Za-z\s]+)'
            ],
            'achievement_based': [
                r'(?:award|recognition|achievement|accomplishment)',
                r'(?:led|managed|directed|supervised)\s+(\d+)\s*(?:team|people|members)',
                r'(?:successfully|effectively)\s+(?:managed|led|directed)',
                r'(?:years?\s+of\s+)?(?:leadership|management|supervision)',
                r'(?:team\s+size|team\s+of)\s+(\d+)\s*(?:members|people)',
                r'(?:project\s+team|development\s+team)\s+(\d+)\s*(?:members|people)',
                r'(?:mentored|guided|trained)\s+(\d+)\s*(?:junior|developers|engineers)',
                r'(?:promoted|elevated|advanced)\s+(?:to|as)\s+([A-Za-z\s]+)',
                r'(?:performance\s+rating|appraisal)\s+([A-Za-z\s]+)',
                r'(?:exceeded|surpassed|outperformed)\s+(?:expectations|targets|goals)'
            ],
            'technology_based': [
                r'(?:since\s+)?(\d{4})\s*(?:using|working\s+with|experience\s+with)',
                r'(?:started\s+using|began\s+working\s+with)\s+(\d{4})',
                r'(?:first\s+exposure|initial\s+experience)\s+(\d{4})',
                r'(?:adopted|implemented|deployed)\s+(\d{4})',
                r'(?:migrated|upgraded|transitioned)\s+(\d{4})',
                r'(?:technology\s+stack|tech\s+stack)\s+(\d{4})',
                r'(?:framework|library|tool)\s+(\d{4})',
                r'(?:version|release)\s+(\d{4})',
                r'(?:introduced|launched|released)\s+(\d{4})'
            ]
        }
        
        # Skill level mapping with more granular values
        self.skill_level_mapping = {
            'expert': 8, 'advanced': 6, 'intermediate': 3, 'beginner': 1,
            'proficient': 5, 'skilled': 4, 'experienced': 7, 'senior': 8,
            'lead': 9, 'principal': 10, 'architect': 10, 'master': 12,
            'specialist': 9, 'consultant': 8, 'mentor': 10, 'trainer': 8,
            'expertise': 8, 'strong': 6, 'solid': 5, 'extensive': 7,
            'deep': 8, 'comprehensive': 7, 'thorough': 6, 'in-depth': 7
        }
        
        # Position-based experience mapping
        self.position_experience_mapping = {
            'intern': 0.5, 'trainee': 0.5, 'associate': 1, 'junior': 1.5,
            'software developer': 2, 'engineer': 2, 'analyst': 2,
            'senior developer': 4, 'senior engineer': 4, 'senior analyst': 4,
            'lead developer': 6, 'lead engineer': 6, 'tech lead': 6,
            'principal engineer': 8, 'staff engineer': 8, 'architect': 8,
            'engineering manager': 8, 'development manager': 8,
            'senior manager': 10, 'director': 12, 'vp': 15, 'cto': 18
        }
    
    def extract_experience(self, text: str) -> Dict[str, Any]:
        """Extract experience with high accuracy"""
        try:
            logger.info("🎯 Starting advanced experience extraction...")
            
            if not text or len(text.strip()) < 10:
                return self._get_empty_experience()
            
            text_clean = self._clean_text(text)
            text_lower = text_clean.lower()
            
            # Try multiple strategies in order of reliability
            strategies = [
                ('explicit', self._extract_explicit_experience),
                ('date_based', self._extract_date_based_experience),
                ('position_based', self._extract_position_based_experience),
                ('education_based', self._extract_education_based_experience),
                ('project_based', self._extract_project_based_experience),
                ('skill_level_based', self._extract_skill_level_based_experience),
                ('achievement_based', self._extract_achievement_based_experience),
                ('technology_based', self._extract_technology_based_experience)
            ]
            
            experience_years = 0
            extraction_method = 'not_found'
            confidence = 0.0
            
            for strategy_name, strategy_func in strategies:
                try:
                    result = strategy_func(text_clean, text_lower)
                    if result['years'] > 0:
                        experience_years = result['years']
                        extraction_method = strategy_name
                        confidence = result['confidence']
                        logger.info(f"✅ Found experience using {strategy_name}: {experience_years} years (confidence: {confidence})")
                        break
                except Exception as e:
                    logger.warning(f"⚠️ Strategy {strategy_name} failed: {e}")
                    continue
            
            # If no strategy worked, try combination approach
            if experience_years == 0:
                experience_years, extraction_method, confidence = self._extract_combined_experience(text_clean, text_lower)
            
            # Validate and adjust experience
            experience_years = self._validate_experience(experience_years)
            
            result = {
                'total_years': experience_years,
                'total_months': experience_years * 12,
                'display': f"{experience_years} years" if experience_years > 0 else "Experience not found",
                'extraction_method': extraction_method,
                'confidence': confidence
            }
            
            logger.info(f"🎯 Final experience extraction: {experience_years} years using {extraction_method} (confidence: {confidence})")
            return result
            
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
    
    def _extract_explicit_experience(self, text: str, text_lower: str) -> Dict[str, Any]:
        """Extract explicit experience statements"""
        try:
            for pattern in self.experience_patterns['explicit']:
                matches = re.findall(pattern, text_lower)
                for match in matches:
                    if isinstance(match, tuple):
                        years = int(match[0]) if match[0] else 0
                        if match[1]:
                            years = max(years, int(match[1]))
                    else:
                        years = int(match)
                    
                    if 0 < years <= 30:
                        return {'years': years, 'confidence': 0.95}
            
            return {'years': 0, 'confidence': 0.0}
            
        except Exception as e:
            logger.error(f"❌ Explicit experience extraction error: {e}")
            return {'years': 0, 'confidence': 0.0}
    
    def _extract_date_based_experience(self, text: str, text_lower: str) -> int:
        """Extract experience from dates"""
        try:
            dates = []
            for pattern in self.experience_patterns['date_based']:
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
                        if len(years) == 1:
                            years.append(current_year)
                        experience = max(years) - min(years)
                        return {'years': experience, 'confidence': 0.9}
                except:
                    pass
            
            return {'years': 0, 'confidence': 0.0}
            
        except Exception as e:
            logger.error(f"❌ Date-based experience extraction error: {e}")
            return {'years': 0, 'confidence': 0.0}
    
    def _extract_position_based_experience(self, text: str, text_lower: str) -> Dict[str, Any]:
        """Extract experience from job positions"""
        try:
            positions = []
            for pattern in self.experience_patterns['position_based']:
                matches = re.findall(pattern, text_lower)
                positions.extend(matches)
            
            if len(positions) > 0:
                # Calculate experience based on positions
                total_experience = 0
                for position in positions:
                    position_lower = position.lower()
                    for pos_key, exp_years in self.position_experience_mapping.items():
                        if pos_key in position_lower:
                            total_experience += exp_years
                            break
                
                if total_experience > 0:
                    return {'years': int(total_experience), 'confidence': 0.7}
            
            return {'years': 0, 'confidence': 0.0}
            
        except Exception as e:
            logger.error(f"❌ Position-based experience extraction error: {e}")
            return {'years': 0, 'confidence': 0.0}
    
    def _extract_education_based_experience(self, text: str, text_lower: str) -> Dict[str, Any]:
        """Extract experience from education"""
        try:
            graduation_years = []
            for pattern in self.experience_patterns['education_based']:
                matches = re.findall(pattern, text, re.IGNORECASE)
                for match in matches:
                    if isinstance(match, tuple):
                        graduation_years.append(match[0])
                    else:
                        graduation_years.append(match)
            
            if graduation_years:
                try:
                    grad_year = int(graduation_years[0])
                    current_year = datetime.now().year
                    experience = current_year - grad_year
                    return {'years': max(0, experience), 'confidence': 0.8}
                except:
                    pass
            
            return {'years': 0, 'confidence': 0.0}
            
        except Exception as e:
            logger.error(f"❌ Education-based experience extraction error: {e}")
            return {'years': 0, 'confidence': 0.0}
    
    def _extract_project_based_experience(self, text: str, text_lower: str) -> Dict[str, Any]:
        """Extract experience from project durations"""
        try:
            durations = []
            for pattern in self.experience_patterns['project_based']:
                matches = re.findall(pattern, text_lower)
                for match in matches:
                    if isinstance(match, tuple):
                        durations.append(match[0])
                    else:
                        durations.append(match)
            
            if durations:
                try:
                    total_months = sum(int(d) for d in durations)
                    years = total_months / 12
                    return {'years': min(int(years), 10), 'confidence': 0.6}
                except:
                    pass
            
            return {'years': 0, 'confidence': 0.0}
            
        except Exception as e:
            logger.error(f"❌ Project-based experience extraction error: {e}")
            return {'years': 0, 'confidence': 0.0}
    
    def _extract_skill_level_based_experience(self, text: str, text_lower: str) -> Dict[str, Any]:
        """Extract experience from skill levels"""
        try:
            for level, years in self.skill_level_mapping.items():
                if level in text_lower:
                    return {'years': years, 'confidence': 0.6}
            
            return {'years': 0, 'confidence': 0.0}
            
        except Exception as e:
            logger.error(f"❌ Skill level-based experience extraction error: {e}")
            return {'years': 0, 'confidence': 0.0}
    
    def _extract_achievement_based_experience(self, text: str, text_lower: str) -> Dict[str, Any]:
        """Extract experience from achievements"""
        try:
            achievements = 0
            for pattern in self.experience_patterns['achievement_based']:
                matches = re.findall(pattern, text_lower)
                achievements += len(matches)
            
            if achievements > 0:
                estimated_years = min(achievements * 2, 15)
                return {'years': estimated_years, 'confidence': 0.5}
            
            return {'years': 0, 'confidence': 0.0}
            
        except Exception as e:
            logger.error(f"❌ Achievement-based experience extraction error: {e}")
            return {'years': 0, 'confidence': 0.0}
    
    def _extract_technology_based_experience(self, text: str, text_lower: str) -> Dict[str, Any]:
        """Extract experience from technology timeline"""
        try:
            tech_years = []
            for pattern in self.experience_patterns['technology_based']:
                matches = re.findall(pattern, text, re.IGNORECASE)
                for match in matches:
                    if isinstance(match, tuple):
                        tech_years.append(match[0])
                    else:
                        tech_years.append(match)
            
            if tech_years:
                try:
                    tech_year = int(tech_years[0])
                    current_year = datetime.now().year
                    experience = current_year - tech_year
                    return {'years': max(0, experience), 'confidence': 0.7}
                except:
                    pass
            
            return {'years': 0, 'confidence': 0.0}
            
        except Exception as e:
            logger.error(f"❌ Technology-based experience extraction error: {e}")
            return {'years': 0, 'confidence': 0.0}
    
    def _extract_combined_experience(self, text: str, text_lower: str) -> Tuple[int, str, float]:
        """Extract experience using combination of strategies"""
        try:
            # Count various indicators
            indicators = {
                'years_mentioned': len(re.findall(r'\d+\s*(?:years?|yrs?)', text_lower)),
                'positions': len(re.findall(r'(?:developer|engineer|analyst|manager)', text_lower)),
                'projects': len(re.findall(r'(?:project|developed|built|created)', text_lower)),
                'technologies': len(re.findall(r'(?:java|python|javascript|react|angular)', text_lower)),
                'achievements': len(re.findall(r'(?:award|recognition|achievement)', text_lower))
            }
            
            # Calculate weighted experience
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
            
            if total_weight > 0:
                estimated_years = min(int(total_score / total_weight), 15)
                confidence = min(total_weight / 10, 0.6)
                return estimated_years, 'combined', confidence
            
            return 0, 'not_found', 0.0
            
        except Exception as e:
            logger.error(f"❌ Combined experience extraction error: {e}")
            return 0, 'not_found', 0.0
    
    def _validate_experience(self, experience_years: int) -> int:
        """Validate and adjust experience"""
        try:
            # Basic validation
            if experience_years < 0:
                return 0
            if experience_years > 30:
                return 30
            
            # Adjust based on common patterns
            if experience_years == 0:
                return 0
            elif experience_years == 1:
                return 1
            elif experience_years <= 3:
                return experience_years
            elif experience_years <= 5:
                return experience_years
            elif experience_years <= 10:
                return experience_years
            else:
                return min(experience_years, 20)
            
        except Exception as e:
            logger.error(f"❌ Experience validation error: {e}")
            return 0
    
    def _get_empty_experience(self) -> Dict[str, Any]:
        """Return empty experience result"""
        return {
            'total_years': 0,
            'total_months': 0,
            'display': 'Experience not found',
            'extraction_method': 'not_found',
            'confidence': 0.0
        }

# Initialize global experience extractor instance
experience_extractor = AdvancedExperienceExtractor()
