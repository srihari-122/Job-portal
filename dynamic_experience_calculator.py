"""
Dynamic Experience Calculator
Accurate experience calculation from resume dates without hardcoding
"""

import re
import logging
from datetime import datetime, date
from typing import Dict, List, Any, Tuple
import calendar
from precise_experience_calculator import precise_experience_calculator

logger = logging.getLogger(__name__)

class DynamicExperienceCalculator:
    """Dynamic experience calculator based on actual resume dates"""
    
    def __init__(self):
        # Dynamic date patterns
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
        
        # Experience keywords
        self.experience_keywords = [
            'experience', 'exp', 'work', 'professional', 'career', 'employment',
            'since', 'from', 'started', 'began', 'joined', 'employed', 'working'
        ]
        
        # Duration keywords
        self.duration_keywords = [
            'years', 'yrs', 'months', 'mos', 'year', 'month', 'duration', 'period'
        ]
    
    def calculate_experience(self, text: str) -> Dict[str, Any]:
        """Calculate experience using precise calculator"""
        try:
            logger.info("📅 Starting dynamic experience calculation...")
            
            # Use precise experience calculator for maximum accuracy
            experience_result = precise_experience_calculator.calculate_experience(text)
            
            logger.info(f"✅ Dynamic experience calculation completed: {experience_result['total_years']} years {experience_result['total_months']} months")
            return experience_result
            
        except Exception as e:
            logger.error(f"❌ Dynamic experience calculation error: {e}")
            return self._get_empty_experience()
    
    def _extract_all_dates(self, text: str) -> List[Dict[str, Any]]:
        """Extract all dates from text"""
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
    
    def _calculate_from_dates(self, dates: List[Dict[str, Any]], text: str) -> Dict[str, Any]:
        """Calculate experience from extracted dates"""
        try:
            if not dates:
                return self._get_empty_experience()
            
            current_date = datetime.now()
            current_year = current_date.year
            current_month = current_date.month
            
            # Strategy 1: Look for employment start dates
            employment_dates = self._find_employment_dates(dates, text)
            
            if employment_dates:
                start_date = employment_dates[0]
                total_months = self._calculate_months_between(
                    start_date['year'], start_date['month'], start_date['day'],
                    current_year, current_month, current_date.day
                )
                
                years = total_months // 12
                months = total_months % 12
                
                return {
                    'total_years': years,
                    'total_months': months,
                    'display': f"{years} years {months} months" if months > 0 else f"{years} years",
                    'extraction_method': 'employment_dates',
                    'start_date': f"{start_date['year']}-{start_date['month']:02d}-{start_date['day']:02d}",
                    'current_date': f"{current_year}-{current_month:02d}-{current_date.day:02d}"
                }
            
            # Strategy 2: Look for graduation date and calculate from there
            graduation_date = self._find_graduation_date(dates, text)
            
            if graduation_date:
                total_months = self._calculate_months_between(
                    graduation_date['year'], graduation_date['month'], graduation_date['day'],
                    current_year, current_month, current_date.day
                )
                
                years = total_months // 12
                months = total_months % 12
                
                return {
                    'total_years': years,
                    'total_months': months,
                    'display': f"{years} years {months} months" if months > 0 else f"{years} years",
                    'extraction_method': 'graduation_date',
                    'graduation_date': f"{graduation_date['year']}-{graduation_date['month']:02d}-{graduation_date['day']:02d}",
                    'current_date': f"{current_year}-{current_month:02d}-{current_date.day:02d}"
                }
            
            # Strategy 3: Use earliest and latest dates
            if len(dates) >= 2:
                earliest = dates[0]
                latest = dates[-1]
                
                total_months = self._calculate_months_between(
                    earliest['year'], earliest['month'], earliest['day'],
                    latest['year'], latest['month'], latest['day']
                )
                
                years = total_months // 12
                months = total_months % 12
                
                return {
                    'total_years': years,
                    'total_months': months,
                    'display': f"{years} years {months} months" if months > 0 else f"{years} years",
                    'extraction_method': 'date_range',
                    'earliest_date': f"{earliest['year']}-{earliest['month']:02d}-{earliest['day']:02d}",
                    'latest_date': f"{latest['year']}-{latest['month']:02d}-{latest['day']:02d}"
                }
            
            # Strategy 4: Use most recent date as reference
            if dates:
                recent_date = dates[-1]
                total_months = self._calculate_months_between(
                    recent_date['year'], recent_date['month'], recent_date['day'],
                    current_year, current_month, current_date.day
                )
                
                years = total_months // 12
                months = total_months % 12
                
                return {
                    'total_years': years,
                    'total_months': months,
                    'display': f"{years} years {months} months" if months > 0 else f"{years} years",
                    'extraction_method': 'recent_date',
                    'reference_date': f"{recent_date['year']}-{recent_date['month']:02d}-{recent_date['day']:02d}",
                    'current_date': f"{current_year}-{current_month:02d}-{current_date.day:02d}"
                }
            
            return self._get_empty_experience()
            
        except Exception as e:
            logger.error(f"❌ Experience calculation error: {e}")
            return self._get_empty_experience()
    
    def _find_employment_dates(self, dates: List[Dict[str, Any]], text: str) -> List[Dict[str, Any]]:
        """Find employment start dates"""
        try:
            employment_dates = []
            text_lower = text.lower()
            
            # Look for employment keywords near dates
            for date_info in dates:
                date_str = f"{date_info['year']}-{date_info['month']:02d}-{date_info['day']:02d}"
                
                # Find context around the date
                date_pattern = re.escape(date_str)
                context_match = re.search(rf'.{{0,100}}{date_pattern}.{{0,100}}', text, re.IGNORECASE)
                
                if context_match:
                    context = context_match.group(0).lower()
                    
                    # Check for employment indicators
                    employment_indicators = [
                        'started', 'began', 'joined', 'employed', 'working', 'since',
                        'from', 'experience', 'career', 'professional', 'work'
                    ]
                    
                    if any(indicator in context for indicator in employment_indicators):
                        employment_dates.append(date_info)
            
            return employment_dates
            
        except Exception as e:
            logger.error(f"❌ Employment date finding error: {e}")
            return []
    
    def _find_graduation_date(self, dates: List[Dict[str, Any]], text: str) -> Dict[str, Any]:
        """Find graduation date"""
        try:
            text_lower = text.lower()
            
            # Look for graduation keywords near dates
            for date_info in dates:
                date_str = f"{date_info['year']}-{date_info['month']:02d}-{date_info['day']:02d}"
                
                # Find context around the date
                date_pattern = re.escape(date_str)
                context_match = re.search(rf'.{{0,100}}{date_pattern}.{{0,100}}', text, re.IGNORECASE)
                
                if context_match:
                    context = context_match.group(0).lower()
                    
                    # Check for graduation indicators
                    graduation_indicators = [
                        'graduated', 'completed', 'finished', 'degree', 'bachelor',
                        'master', 'phd', 'diploma', 'certificate', 'education'
                    ]
                    
                    if any(indicator in context for indicator in graduation_indicators):
                        return date_info
            
            return None
            
        except Exception as e:
            logger.error(f"❌ Graduation date finding error: {e}")
            return None
    
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

# Initialize global dynamic experience calculator
dynamic_experience_calculator = DynamicExperienceCalculator()
