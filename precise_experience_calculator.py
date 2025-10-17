"""
Precise Experience Calculator
Ultra-accurate experience calculation from resume dates
"""

import re
import logging
from datetime import datetime, date
from typing import Dict, List, Any, Tuple
import calendar
from direct_experience_extractor import direct_experience_extractor

logger = logging.getLogger(__name__)

class PreciseExperienceCalculator:
    """Precise experience calculator with maximum accuracy"""
    
    def __init__(self):
        # Comprehensive date patterns
        self.date_patterns = [
            # Full date patterns
            r'(\d{1,2})[/-](\d{1,2})[/-](\d{4})',  # DD/MM/YYYY or DD-MM-YYYY
            r'(\d{4})[/-](\d{1,2})[/-](\d{1,2})',  # YYYY/MM/DD or YYYY-MM-DD
            r'(\d{1,2})\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+(\d{4})',  # DD Month YYYY
            r'(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+(\d{1,2}),?\s+(\d{4})',  # Month DD, YYYY
            r'(\d{4})\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+(\d{1,2})',  # YYYY Month DD
            
            # Year only patterns
            r'\b(\d{4})\b',  # Any 4-digit year
            
            # Month-Year patterns
            r'(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+(\d{4})',  # Month YYYY
            r'(\d{1,2})[/-](\d{4})',  # MM/YYYY or MM-YYYY
        ]
        
        # Month name mapping
        self.month_names = {
            'jan': 1, 'january': 1, 'feb': 2, 'february': 2, 'mar': 3, 'march': 3,
            'apr': 4, 'april': 4, 'may': 5, 'jun': 6, 'june': 6, 'jul': 7, 'july': 7,
            'aug': 8, 'august': 8, 'sep': 9, 'september': 9, 'oct': 10, 'october': 10,
            'nov': 11, 'november': 11, 'dec': 12, 'december': 12
        }
        
        # Employment keywords
        self.employment_keywords = [
            'started', 'began', 'joined', 'employed', 'working', 'since', 'from',
            'experience', 'career', 'professional', 'work', 'employment', 'job',
            'position', 'role', 'appointed', 'hired', 'recruited', 'onboarded'
        ]
        
        # Company keywords
        self.company_keywords = [
            'company', 'corporation', 'inc', 'ltd', 'pvt', 'limited', 'technologies',
            'solutions', 'services', 'consulting', 'software', 'systems', 'enterprises'
        ]
        
        # Duration keywords
        self.duration_keywords = [
            'years', 'yrs', 'months', 'mos', 'year', 'month', 'duration', 'period',
            'tenure', 'service', 'employment', 'work'
        ]
    
    def calculate_experience(self, text: str) -> Dict[str, Any]:
        """Calculate experience using direct extraction"""
        try:
            logger.info("🎯 Starting precise experience calculation...")
            
            # Use direct experience extractor for maximum accuracy
            experience_result = direct_experience_extractor.extract_experience(text)
            
            logger.info(f"✅ Precise experience calculation completed: {experience_result['total_years']} years")
            return experience_result
            
        except Exception as e:
            logger.error(f"❌ Precise experience calculation error: {e}")
            return self._get_empty_experience()
    
    def _extract_all_dates(self, text: str) -> List[Dict[str, Any]]:
        """Extract all dates from text with context"""
        try:
            dates = []
            text_lower = text.lower()
            
            # Extract dates using patterns
            for pattern in self.date_patterns:
                matches = re.finditer(pattern, text, re.IGNORECASE)
                for match in matches:
                    date_info = self._parse_date_match(match, text_lower)
                    if date_info:
                        dates.append(date_info)
            
            # Remove duplicates and sort
            unique_dates = []
            seen_dates = set()
            for date_info in dates:
                date_key = f"{date_info['year']}-{date_info['month']}-{date_info['day']}"
                if date_key not in seen_dates:
                    seen_dates.add(date_key)
                    unique_dates.append(date_info)
            
            # Sort by date
            unique_dates.sort(key=lambda x: (x['year'], x['month'], x['day']))
            
            logger.info(f"📅 Extracted {len(unique_dates)} unique dates")
            return unique_dates
            
        except Exception as e:
            logger.error(f"❌ Date extraction error: {e}")
            return []
    
    def _parse_date_match(self, match, text_lower: str) -> Dict[str, Any]:
        """Parse a date match into structured format"""
        try:
            groups = match.groups()
            pattern = match.re.pattern
            
            # Full date patterns
            if r'(\d{1,2})[/-](\d{1,2})[/-](\d{4})' in pattern:
                day, month, year = int(groups[0]), int(groups[1]), int(groups[2])
                return {'year': year, 'month': month, 'day': day, 'type': 'full_date'}
            
            elif r'(\d{4})[/-](\d{1,2})[/-](\d{1,2})' in pattern:
                year, month, day = int(groups[0]), int(groups[1]), int(groups[2])
                return {'year': year, 'month': month, 'day': day, 'type': 'full_date'}
            
            # Month name patterns
            elif r'(\d{1,2})\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+(\d{4})' in pattern:
                day, year = int(groups[0]), int(groups[1])
                month_name = match.group(0).split()[1].lower()
                month = self.month_names.get(month_name, 1)
                return {'year': year, 'month': month, 'day': day, 'type': 'month_name'}
            
            elif r'(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+(\d{1,2}),?\s+(\d{4})' in pattern:
                day, year = int(groups[0]), int(groups[1])
                month_name = match.group(0).split()[0].lower()
                month = self.month_names.get(month_name, 1)
                return {'year': year, 'month': month, 'day': day, 'type': 'month_name'}
            
            elif r'(\d{4})\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+(\d{1,2})' in pattern:
                year, day = int(groups[0]), int(groups[1])
                month_name = match.group(0).split()[1].lower()
                month = self.month_names.get(month_name, 1)
                return {'year': year, 'month': month, 'day': day, 'type': 'month_name'}
            
            # Year only patterns
            elif r'\b(\d{4})\b' in pattern:
                year = int(groups[0])
                if 1950 <= year <= datetime.now().year:
                    return {'year': year, 'month': 1, 'day': 1, 'type': 'year_only'}
            
            # Month-Year patterns
            elif r'(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+(\d{4})' in pattern:
                year = int(groups[0])
                month_name = match.group(0).split()[0].lower()
                month = self.month_names.get(month_name, 1)
                return {'year': year, 'month': month, 'day': 1, 'type': 'month_year'}
            
            elif r'(\d{1,2})[/-](\d{4})' in pattern:
                month, year = int(groups[0]), int(groups[1])
                if 1 <= month <= 12 and 1950 <= year <= datetime.now().year:
                    return {'year': year, 'month': month, 'day': 1, 'type': 'month_year'}
            
            return None
            
        except Exception as e:
            logger.error(f"❌ Date parsing error: {e}")
            return None
    
    def _calculate_employment_experience(self, dates: List[Dict[str, Any]], text: str) -> Dict[str, Any]:
        """Calculate experience from employment start dates"""
        try:
            employment_dates = []
            text_lower = text.lower()
            
            # Find employment start dates
            for date_info in dates:
                date_str = f"{date_info['year']}-{date_info['month']:02d}-{date_info['day']:02d}"
                
                # Find context around the date
                date_pattern = re.escape(date_str)
                context_match = re.search(rf'.{{0,200}}{date_pattern}.{{0,200}}', text, re.IGNORECASE)
                
                if context_match:
                    context = context_match.group(0).lower()
                    
                    # Check for employment indicators
                    employment_score = 0
                    for keyword in self.employment_keywords:
                        if keyword in context:
                            employment_score += 1
                    
                    if employment_score > 0:
                        employment_dates.append({
                            'date': date_info,
                            'score': employment_score,
                            'context': context
                        })
            
            if employment_dates:
                # Sort by score and date
                employment_dates.sort(key=lambda x: (-x['score'], x['date']['year'], x['date']['month']))
                start_date = employment_dates[0]['date']
                
                current_date = datetime.now()
                total_months = self._calculate_months_between(
                    start_date['year'], start_date['month'], start_date['day'],
                    current_date.year, current_date.month, current_date.day
                )
                
                years = total_months // 12
                months = total_months % 12
                
                return {
                    'total_years': years,
                    'total_months': months,
                    'display': f"{years} years {months} months" if months > 0 else f"{years} years",
                    'extraction_method': 'employment_dates',
                    'start_date': f"{start_date['year']}-{start_date['month']:02d}-{start_date['day']:02d}",
                    'confidence': 0.95
                }
            
            return None
            
        except Exception as e:
            logger.error(f"❌ Employment experience calculation error: {e}")
            return None
    
    def _calculate_graduation_experience(self, dates: List[Dict[str, Any]], text: str) -> Dict[str, Any]:
        """Calculate experience from graduation date"""
        try:
            graduation_keywords = [
                'graduated', 'completed', 'finished', 'degree', 'bachelor', 'master',
                'phd', 'diploma', 'certificate', 'education', 'university', 'college',
                'institute', 'passout', 'batch'
            ]
            
            text_lower = text.lower()
            
            # Find graduation dates
            for date_info in dates:
                date_str = f"{date_info['year']}-{date_info['month']:02d}-{date_info['day']:02d}"
                
                # Find context around the date
                date_pattern = re.escape(date_str)
                context_match = re.search(rf'.{{0,200}}{date_pattern}.{{0,200}}', text, re.IGNORECASE)
                
                if context_match:
                    context = context_match.group(0).lower()
                    
                    # Check for graduation indicators
                    graduation_score = 0
                    for keyword in graduation_keywords:
                        if keyword in context:
                            graduation_score += 1
                    
                    if graduation_score > 0:
                        current_date = datetime.now()
                        total_months = self._calculate_months_between(
                            date_info['year'], date_info['month'], date_info['day'],
                            current_date.year, current_date.month, current_date.day
                        )
                        
                        years = total_months // 12
                        months = total_months % 12
                        
                        return {
                            'total_years': years,
                            'total_months': months,
                            'display': f"{years} years {months} months" if months > 0 else f"{years} years",
                            'extraction_method': 'graduation_date',
                            'graduation_date': f"{date_info['year']}-{date_info['month']:02d}-{date_info['day']:02d}",
                            'confidence': 0.9
                        }
            
            return None
            
        except Exception as e:
            logger.error(f"❌ Graduation experience calculation error: {e}")
            return None
    
    def _calculate_range_experience(self, dates: List[Dict[str, Any]], text: str) -> Dict[str, Any]:
        """Calculate experience from date range"""
        try:
            if len(dates) >= 2:
                # Look for date ranges in text
                text_lower = text.lower()
                range_patterns = [
                    r'(\d{4})\s*(?:to|-)\s*(\d{4})',
                    r'(\d{4})\s*(?:to|-)\s*(?:present|current|now)',
                    r'(?:from|since)\s+(\d{4})\s*(?:to|-)\s*(\d{4})',
                    r'(?:from|since)\s+(\d{4})\s*(?:to|-)\s*(?:present|current|now)'
                ]
                
                for pattern in range_patterns:
                    matches = re.findall(pattern, text_lower)
                    for match in matches:
                        if len(match) == 2:
                            start_year, end_year = int(match[0]), int(match[1])
                        else:
                            start_year, end_year = int(match[0]), datetime.now().year
                        
                        if 1950 <= start_year <= datetime.now().year and 1950 <= end_year <= datetime.now().year:
                            total_months = (end_year - start_year) * 12
                            years = total_months // 12
                            months = total_months % 12
                            
                            return {
                                'total_years': years,
                                'total_months': months,
                                'display': f"{years} years {months} months" if months > 0 else f"{years} years",
                                'extraction_method': 'date_range',
                                'start_year': start_year,
                                'end_year': end_year,
                                'confidence': 0.8
                            }
            
            return None
            
        except Exception as e:
            logger.error(f"❌ Range experience calculation error: {e}")
            return None
    
    def _calculate_explicit_experience(self, text: str) -> Dict[str, Any]:
        """Calculate experience from explicit statements"""
        try:
            text_lower = text.lower()
            
            # Explicit experience patterns
            patterns = [
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
            
            for pattern in patterns:
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
                            'confidence': 0.95
                        }
            
            return None
            
        except Exception as e:
            logger.error(f"❌ Explicit experience calculation error: {e}")
            return None
    
    def _calculate_position_experience(self, text: str) -> Dict[str, Any]:
        """Calculate experience from position levels"""
        try:
            text_lower = text.lower()
            
            # Position-based experience mapping
            position_experience = {
                'intern': 0.5, 'trainee': 0.5, 'associate': 1, 'junior': 1.5,
                'software developer': 2, 'engineer': 2, 'analyst': 2,
                'senior developer': 4, 'senior engineer': 4, 'senior analyst': 4,
                'lead developer': 6, 'lead engineer': 6, 'tech lead': 6,
                'principal engineer': 8, 'staff engineer': 8, 'architect': 8,
                'engineering manager': 8, 'development manager': 8,
                'senior manager': 10, 'director': 12, 'vp': 15, 'cto': 18
            }
            
            for position, years in position_experience.items():
                if position in text_lower:
                    return {
                        'total_years': int(years),
                        'total_months': int(years * 12),
                        'display': f"{int(years)} years",
                        'extraction_method': 'position_estimation',
                        'confidence': 0.7
                    }
            
            return None
            
        except Exception as e:
            logger.error(f"❌ Position experience calculation error: {e}")
            return None
    
    def _select_best_result(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Select the most accurate result from multiple calculations"""
        try:
            if not results:
                return self._get_empty_experience()
            
            # Sort by confidence and method priority
            method_priority = {
                'explicit_statement': 1,
                'employment_dates': 2,
                'graduation_date': 3,
                'date_range': 4,
                'position_estimation': 5
            }
            
            results.sort(key=lambda x: (
                -x.get('confidence', 0),
                method_priority.get(x.get('extraction_method', ''), 6)
            ))
            
            return results[0]
            
        except Exception as e:
            logger.error(f"❌ Best result selection error: {e}")
            return results[0] if results else self._get_empty_experience()
    
    def _calculate_months_between(self, start_year: int, start_month: int, start_day: int,
                                 end_year: int, end_month: int, end_day: int) -> int:
        """Calculate months between two dates"""
        try:
            start_date = date(start_year, start_month, start_day)
            end_date = date(end_year, end_month, end_day)
            
            # Calculate total months
            total_months = (end_year - start_year) * 12 + (end_month - start_month)
            
            # Adjust for day difference
            if end_day < start_day:
                total_months -= 1
            
            return max(0, total_months)
            
        except Exception as e:
            logger.error(f"❌ Month calculation error: {e}")
            return 0
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text.strip())
        
        # Remove special characters but keep basic punctuation
        text = re.sub(r'[^\w\s@\.\-\+\(\)\/]', ' ', text)
        
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

# Initialize global precise experience calculator
precise_experience_calculator = PreciseExperienceCalculator()
