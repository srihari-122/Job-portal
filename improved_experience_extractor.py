"""
Improved Experience Extractor
Handles yyyy-yyyy format and calculates total experience accurately
"""

import re
import logging
from datetime import datetime
from typing import Dict, List, Any, Tuple
from dateutil.relativedelta import relativedelta

logger = logging.getLogger(__name__)

class ImprovedExperienceExtractor:
    """Improved experience extractor with yyyy-yyyy format support"""
    
    def __init__(self):
        # Experience patterns for yyyy-yyyy format
        self.experience_patterns = [
            # yyyy-yyyy format patterns
            r'(\d{4})\s*[-–—]\s*(\d{4})',  # 2020-2024, 2020 – 2024, 2020—2024
            r'(\d{4})\s*to\s*(\d{4})',     # 2020 to 2024
            r'(\d{4})\s*-\s*(\d{4})',      # 2020 - 2024
            r'(\d{4})\s*–\s*(\d{4})',      # 2020 – 2024
            r'(\d{4})\s*—\s*(\d{4})',      # 2020 — 2024
            
            # Month-Year format patterns
            r'([A-Za-z]{3,9})\s*(\d{4})\s*[-–—]\s*([A-Za-z]{3,9})\s*(\d{4})',  # Jan 2020 - Dec 2024
            r'([A-Za-z]{3,9})\s*(\d{4})\s*to\s*([A-Za-z]{3,9})\s*(\d{4})',     # Jan 2020 to Dec 2024
            r'(\d{1,2})[/-](\d{4})\s*[-–—]\s*(\d{1,2})[/-](\d{4})',            # 01/2020 - 12/2024
            r'(\d{1,2})[/-](\d{4})\s*to\s*(\d{1,2})[/-](\d{4})',               # 01/2020 to 12/2024
            
            # Present/Current patterns
            r'(\d{4})\s*[-–—]\s*(?:present|current|till\s+date|till\s+now)',    # 2020 - Present
            r'([A-Za-z]{3,9})\s*(\d{4})\s*[-–—]\s*(?:present|current|till\s+date|till\s+now)',  # Jan 2020 - Present
            r'(\d{1,2})[/-](\d{4})\s*[-–—]\s*(?:present|current|till\s+date|till\s+now)',       # 01/2020 - Present
            
            # Direct experience statements
            r'(?:total|overall|total\s+work)\s*(?:experience|exp)[:\s]*(\d+(?:\.\d+)?)\s*(?:to|-)?\s*(\d+(?:\.\d+)?)?\s*(?:years?|yrs?)',
            r'(?:experience|exp)[:\s]*(\d+(?:\.\d+)?)\s*(?:to|-)?\s*(\d+(?:\.\d+)?)?\s*(?:years?|yrs?)',
            r'(\d+(?:\.\d+)?)\s*(?:to|-)?\s*(\d+(?:\.\d+)?)?\s*(?:years?|yrs?)\s*(?:of\s*)?(?:experience|exp)',
        ]
        
        # Month name mappings
        self.month_names = {
            'january': 1, 'jan': 1,
            'february': 2, 'feb': 2,
            'march': 3, 'mar': 3,
            'april': 4, 'apr': 4,
            'may': 5,
            'june': 6, 'jun': 6,
            'july': 7, 'jul': 7,
            'august': 8, 'aug': 8,
            'september': 9, 'sep': 9, 'sept': 9,
            'october': 10, 'oct': 10,
            'november': 11, 'nov': 11,
            'december': 12, 'dec': 12
        }
        
        # Fresher keywords
        self.fresher_keywords = [
            'fresher', 'fresh graduate', 'recent graduate', 'new graduate', 'entry level',
            'junior', 'trainee', 'intern', 'internship', 'no experience', 'zero experience',
            'beginner', 'starter', 'newbie', 'rookie', 'novice', 'apprentice'
        ]
    
    def extract_experience(self, text: str) -> Dict[str, Any]:
        """Extract experience from resume text with yyyy-yyyy format support"""
        try:
            logger.info("⏰ Starting improved experience extraction...")
            
            text_lower = text.lower()
            
            # Check for fresher indicators first
            for keyword in self.fresher_keywords:
                if keyword in text_lower:
                    logger.info(f"✅ Fresher detected: {keyword}")
                    return {
                        'total_years': 0,
                        'total_months': 0,
                        'display': 'Fresher (0 years)',
                        'is_fresher': True,
                        'experience_periods': [],
                        'extraction_method': 'fresher_detection'
                    }
            
            # Extract experience periods
            experience_periods = self._extract_experience_periods(text)
            
            if not experience_periods:
                logger.info("⚠️ No experience periods found")
                return {
                    'total_years': 0,
                    'total_months': 0,
                    'display': 'No experience found',
                    'is_fresher': True,
                    'experience_periods': [],
                    'extraction_method': 'no_periods_found'
                }
            
            # Calculate total experience
            total_months = self._calculate_total_experience(experience_periods)
            total_years = total_months / 12
            
            # Determine if fresher
            is_fresher = total_years <= 1.0
            
            result = {
                'total_years': round(total_years, 1),
                'total_months': total_months,
                'display': f'{total_years:.1f} years' if total_years > 0 else 'Fresher (0 years)',
                'is_fresher': is_fresher,
                'experience_periods': experience_periods,
                'extraction_method': 'improved_extraction'
            }
            
            logger.info(f"✅ Experience extracted: {result['display']}")
            return result
            
        except Exception as e:
            logger.error(f"❌ Experience extraction error: {e}")
            return {
                'total_years': 0,
                'total_months': 0,
                'display': 'Experience extraction error',
                'is_fresher': True,
                'experience_periods': [],
                'extraction_method': 'error'
            }
    
    def _extract_experience_periods(self, text: str) -> List[Dict[str, Any]]:
        """Extract all experience periods from text"""
        periods = []
        
        try:
            # Try yyyy-yyyy patterns first
            for pattern in self.experience_patterns:
                matches = re.finditer(pattern, text, re.IGNORECASE)
                for match in matches:
                    period = self._parse_experience_match(match, pattern)
                    if period:
                        periods.append(period)
            
            # Remove duplicates and sort by start date
            periods = self._deduplicate_periods(periods)
            periods.sort(key=lambda x: x['start_date'])
            
            logger.info(f"📅 Found {len(periods)} experience periods")
            return periods
            
        except Exception as e:
            logger.error(f"❌ Error extracting experience periods: {e}")
            return []
    
    def _parse_experience_match(self, match, pattern: str) -> Dict[str, Any]:
        """Parse a single experience match"""
        try:
            groups = match.groups()
            
            # Handle yyyy-yyyy format
            if len(groups) >= 2 and groups[0].isdigit() and len(groups[0]) == 4:
                start_year = int(groups[0])
                end_year = int(groups[1]) if groups[1].isdigit() and len(groups[1]) == 4 else datetime.now().year
                
                return {
                    'start_date': datetime(start_year, 1, 1),
                    'end_date': datetime(end_year, 12, 31),
                    'start_year': start_year,
                    'end_year': end_year,
                    'pattern_type': 'yyyy-yyyy'
                }
            
            # Handle month-year format
            elif len(groups) >= 4:
                start_month = self._parse_month(groups[0])
                start_year = int(groups[1]) if groups[1].isdigit() else datetime.now().year
                
                if groups[2].lower() in ['present', 'current', 'till', 'date', 'now']:
                    end_month = datetime.now().month
                    end_year = datetime.now().year
                else:
                    end_month = self._parse_month(groups[2])
                    end_year = int(groups[3]) if groups[3].isdigit() else datetime.now().year
                
                return {
                    'start_date': datetime(start_year, start_month, 1),
                    'end_date': datetime(end_year, end_month, 28),  # Use 28 to avoid month-end issues
                    'start_year': start_year,
                    'end_year': end_year,
                    'pattern_type': 'month-year'
                }
            
            return None
            
        except Exception as e:
            logger.error(f"❌ Error parsing experience match: {e}")
            return None
    
    def _parse_month(self, month_str: str) -> int:
        """Parse month string to integer"""
        try:
            month_lower = month_str.lower()
            return self.month_names.get(month_lower, 1)
        except:
            return 1
    
    def _calculate_total_experience(self, periods: List[Dict[str, Any]]) -> int:
        """Calculate total experience in months"""
        try:
            if not periods:
                return 0
            
            # Merge overlapping periods
            merged_periods = self._merge_overlapping_periods(periods)
            
            total_months = 0
            for period in merged_periods:
                start_date = period['start_date']
                end_date = period['end_date']
                
                # Calculate months between dates
                delta = relativedelta(end_date, start_date)
                months = delta.years * 12 + delta.months
                total_months += max(0, months)  # Ensure non-negative
            
            return total_months
            
        except Exception as e:
            logger.error(f"❌ Error calculating total experience: {e}")
            return 0
    
    def _merge_overlapping_periods(self, periods: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Merge overlapping experience periods"""
        try:
            if not periods:
                return []
            
            # Sort by start date
            sorted_periods = sorted(periods, key=lambda x: x['start_date'])
            merged = [sorted_periods[0]]
            
            for current in sorted_periods[1:]:
                last = merged[-1]
                
                # Check if periods overlap
                if current['start_date'] <= last['end_date']:
                    # Merge periods
                    merged[-1] = {
                        'start_date': last['start_date'],
                        'end_date': max(last['end_date'], current['end_date']),
                        'start_year': last['start_year'],
                        'end_year': max(last['end_year'], current['end_year']),
                        'pattern_type': 'merged'
                    }
                else:
                    merged.append(current)
            
            return merged
            
        except Exception as e:
            logger.error(f"❌ Error merging periods: {e}")
            return periods
    
    def _deduplicate_periods(self, periods: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Remove duplicate experience periods"""
        try:
            seen = set()
            unique_periods = []
            
            for period in periods:
                key = (period['start_year'], period['end_year'])
                if key not in seen:
                    seen.add(key)
                    unique_periods.append(period)
            
            return unique_periods
            
        except Exception as e:
            logger.error(f"❌ Error deduplicating periods: {e}")
            return periods

# Initialize global improved experience extractor
improved_experience_extractor = ImprovedExperienceExtractor()
