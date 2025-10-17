"""
Ultimate Extractor
Maximum accuracy for skills and experience extraction
"""

import re
import logging
from typing import Dict, List, Any

logger = logging.getLogger(__name__)

class UltimateExtractor:
    """Ultimate extractor for skills and experience"""
    
    def __init__(self):
        # Comprehensive skill database
        self.skill_database = {
            'programming': ['java', 'python', 'javascript', 'c++', 'c#', 'go', 'rust', 'kotlin', 'swift', 'php', 'ruby', 'scala', 'r', 'matlab'],
            'web': ['html', 'css', 'javascript', 'react', 'angular', 'vue', 'bootstrap', 'tailwind', 'sass', 'less', 'jquery', 'node.js', 'express'],
            'backend': ['spring', 'django', 'flask', 'fastapi', 'rails', 'laravel', 'express', 'asp.net', 'hibernate', 'jpa'],
            'database': ['mysql', 'postgresql', 'mongodb', 'redis', 'elasticsearch', 'oracle', 'sqlite', 'cassandra', 'dynamodb'],
            'cloud': ['aws', 'azure', 'gcp', 'docker', 'kubernetes', 'terraform', 'jenkins', 'gitlab', 'github actions'],
            'mobile': ['android', 'ios', 'react native', 'flutter', 'xamarin', 'ionic', 'cordova'],
            'ai_ml': ['tensorflow', 'pytorch', 'scikit-learn', 'pandas', 'numpy', 'opencv', 'keras', 'spark'],
            'devops': ['git', 'ci/cd', 'ansible', 'chef', 'puppet', 'monitoring', 'logging', 'microservices'],
            'testing': ['selenium', 'junit', 'testng', 'cypress', 'jest', 'mocha', 'pytest', 'jasmine'],
            'tools': ['git', 'maven', 'gradle', 'npm', 'yarn', 'webpack', 'babel', 'eslint', 'prettier']
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
            r'(?:around|approximately|about)\s+(\d+)\s*(?:years?|yrs?)'
        ]
    
    def extract_skills(self, text: str) -> List[str]:
        """Extract skills with maximum accuracy"""
        try:
            logger.info("🔧 Starting ultimate skills extraction...")
            
            if not text or len(text.strip()) < 10:
                return []
            
            text_clean = self._clean_text(text)
            text_lower = text_clean.lower()
            
            skills = []
            
            # Extract skills from database
            for category, skill_list in self.skill_database.items():
                for skill in skill_list:
                    if skill in text_lower:
                        skills.append(skill.title())
            
            # Remove duplicates and sort
            unique_skills = list(set(skills))
            unique_skills.sort()
            
            logger.info(f"✅ Ultimate skills extraction completed: {len(unique_skills)} skills")
            return unique_skills
            
        except Exception as e:
            logger.error(f"❌ Ultimate skills extraction error: {e}")
            return []
    
    def extract_experience(self, text: str) -> Dict[str, Any]:
        """Extract experience with maximum accuracy"""
        try:
            logger.info("⏰ Starting ultimate experience extraction...")
            
            if not text or len(text.strip()) < 10:
                return self._get_fresher_result()
            
            text_clean = self._clean_text(text)
            text_lower = text_clean.lower()
            
            # Strategy 1: Direct experience statements
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
                        logger.info(f"✅ Found direct experience: {years} years")
                        return {
                            'total_years': years,
                            'total_months': years * 12,
                            'display': f"{years} years",
                            'extraction_method': 'direct_statement',
                            'is_fresher': False
                        }
            
            # Strategy 2: Position-based analysis
            position_keywords = {
                'senior': 6, 'lead': 8, 'principal': 10, 'architect': 10,
                'manager': 8, 'director': 12, 'vp': 15, 'cto': 18,
                'mid': 3, 'intermediate': 3, 'experienced': 4,
                'junior': 1, 'associate': 1, 'entry': 0,
                'intern': 0, 'trainee': 0, 'fresher': 0
            }
            
            for keyword, years in position_keywords.items():
                if keyword in text_lower:
                    logger.info(f"✅ Found position-based experience: {years} years")
                    return {
                        'total_years': years,
                        'total_months': years * 12,
                        'display': f"{years} years" if years > 0 else "Fresher",
                        'extraction_method': 'position_based',
                        'is_fresher': years == 0
                    }
            
            # Strategy 3: Skill-based analysis
            skill_count = len(self.extract_skills(text))
            if skill_count > 0:
                # Estimate experience based on skill count
                if skill_count >= 15:
                    estimated_years = 8
                elif skill_count >= 10:
                    estimated_years = 5
                elif skill_count >= 5:
                    estimated_years = 3
                else:
                    estimated_years = 1
                
                logger.info(f"✅ Found skill-based experience: {estimated_years} years")
                return {
                    'total_years': estimated_years,
                    'total_months': estimated_years * 12,
                    'display': f"{estimated_years} years",
                    'extraction_method': 'skill_based',
                    'is_fresher': False
                }
            
            # Strategy 4: Context analysis
            context_indicators = {
                'projects': len(re.findall(r'(?:project|developed|built|created)', text_lower)),
                'companies': len(re.findall(r'(?:company|corporation|inc|ltd)', text_lower)),
                'technologies': len(re.findall(r'(?:java|python|javascript|react|angular)', text_lower)),
                'achievements': len(re.findall(r'(?:award|recognition|achievement)', text_lower))
            }
            
            total_indicators = sum(context_indicators.values())
            if total_indicators > 0:
                # Estimate experience based on context
                if total_indicators >= 10:
                    estimated_years = 6
                elif total_indicators >= 5:
                    estimated_years = 3
                else:
                    estimated_years = 1
                
                logger.info(f"✅ Found context-based experience: {estimated_years} years")
                return {
                    'total_years': estimated_years,
                    'total_months': estimated_years * 12,
                    'display': f"{estimated_years} years",
                    'extraction_method': 'context_based',
                    'is_fresher': False
                }
            
            # If no experience found, declare as fresher
            logger.info("⚠️ No experience found - declaring as fresher")
            return self._get_fresher_result()
            
        except Exception as e:
            logger.error(f"❌ Ultimate experience extraction error: {e}")
            return self._get_fresher_result()
    
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

# Initialize global ultimate extractor
ultimate_extractor = UltimateExtractor()

