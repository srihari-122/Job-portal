"""
Trained Location Extractor
Accurate location extraction from resume text
"""

import re
import logging
from typing import Dict, List, Any

logger = logging.getLogger(__name__)

class LocationExtractor:
    """Trained extractor for location extraction"""
    
    def __init__(self):
        # Location patterns - Enhanced for better extraction
        self.location_patterns = [
            r'Location[:\s]*([A-Za-z\s,]{3,50})',
            r'Address[:\s]*([A-Za-z\s,]{3,50})',
            r'City[:\s]*([A-Za-z\s,]{3,50})',
            r'Based in[:\s]*([A-Za-z\s,]{3,50})',
            r'Located in[:\s]*([A-Za-z\s,]{3,50})',
            r'From[:\s]*([A-Za-z\s,]{3,50})',
            r'Residing in[:\s]*([A-Za-z\s,]{3,50})',
            r'Living in[:\s]*([A-Za-z\s,]{3,50})',
            r'Current Location[:\s]*([A-Za-z\s,]{3,50})',
            r'Present Location[:\s]*([A-Za-z\s,]{3,50})',
            r'Work Location[:\s]*([A-Za-z\s,]{3,50})',
            r'Office Location[:\s]*([A-Za-z\s,]{3,50})',
            r'Bangalore',
            r'Mumbai',
            r'Delhi',
            r'Hyderabad',
            r'Chennai',
            r'Pune',
            r'Kolkata',
            r'Ahmedabad',
            r'Jaipur',
            r'Surat',
            r'Lucknow',
            r'Kanpur',
            r'Nagpur',
            r'Indore',
            r'Thane',
            r'Bhopal',
            r'Visakhapatnam',
            r'Patna',
            r'Vadodara',
            r'Ludhiana',
            r'Agra',
            r'Nashik',
            r'Faridabad',
            r'Meerut',
            r'Rajkot',
            r'Kalyan',
            r'Vasai',
            r'Varanasi',
            r'Srinagar',
            r'Aurangabad',
            r'Navi Mumbai',
            r'Solapur',
            r'Vijayawada',
            r'Kolhapur',
            r'Amritsar',
            r'Noida',
            r'Ranchi',
            r'Howrah',
            r'Coimbatore',
            r'Raipur',
            r'Jabalpur',
            r'Gwalior',
            r'Chandigarh',
            r'Tiruchirappalli',
            r'Mysore',
            r'Bhilai',
            r'Kochi',
            r'Bhavnagar',
            r'Salem',
            r'Warangal',
            r'Guntur',
            r'Bhubaneswar',
            r'Mira',
            r'Tiruppur',
            r'Amravati',
            r'Nanded'
        ]
        
        # Indian cities database
        self.indian_cities = [
            'mumbai', 'delhi', 'bangalore', 'hyderabad', 'chennai', 'kolkata', 'pune',
            'ahmedabad', 'jaipur', 'surat', 'lucknow', 'kanpur', 'nagpur', 'indore',
            'thane', 'bhopal', 'visakhapatnam', 'pimpri', 'patna', 'vadodara', 'ludhiana',
            'agra', 'nashik', 'faridabad', 'meerut', 'rajkot', 'kalyan', 'vasai',
            'varanasi', 'srinagar', 'aurangabad', 'navi mumbai', 'solapur', 'vijayawada',
            'kolhapur', 'amritsar', 'noida', 'ranchi', 'howrah', 'coimbatore', 'raipur',
            'jabalpur', 'gwalior', 'chandigarh', 'tiruchirappalli', 'mysore', 'bhilai',
            'kochi', 'bhavnagar', 'salem', 'warangal', 'guntur', 'bhubaneswar', 'mira',
            'tiruppur', 'amravati', 'nanded', 'kolhapur', 'sangli', 'malegaon', 'ulhasnagar',
            'jalgaon', 'akola', 'latur', 'ahmednagar', 'chandrapur', 'parbhani', 'ichalkaranji',
            'jalna', 'ambajogai', 'bhusawal', 'ratnagiri', 'beed', 'yavatmal', 'kamptee',
            'gondia', 'barsi', 'achalpur', 'osmanabad', 'nandurbar', 'wardha', 'udgir',
            'hinganghat', 'washim', 'pulgaon', 'malkapur', 'wani', 'lonavla', 'tahsil',
            'umarga', 'warora', 'talegaon', 'manmad', 'sangamner', 'shirpur', 'shirur',
            'pachora', 'jalgaon jamod', 'sakri', 'muktainagar', 'malkapur', 'sonpeth',
            'shahada', 'kalmeshwar', 'chopda', 'rahimapur', 'jintur', 'selu', 'surgana',
            'mohol', 'miraj', 'sangamner', 'partur', 'ghansawangi', 'chandur', 'purna',
            'rahata', 'rahuri', 'kopargaon', 'yeola', 'sangamner', 'akole', 'sangamner',
            'rahuri', 'kopargaon', 'yeola', 'sangamner', 'akole', 'sangamner', 'rahuri'
        ]
        
        # International cities database
        self.international_cities = [
            'new york', 'london', 'tokyo', 'paris', 'sydney', 'toronto', 'singapore',
            'dubai', 'hong kong', 'amsterdam', 'berlin', 'madrid', 'rome', 'vienna',
            'zurich', 'stockholm', 'copenhagen', 'oslo', 'helsinki', 'brussels',
            'warsaw', 'prague', 'budapest', 'bucharest', 'sofia', 'athens', 'lisbon',
            'dublin', 'glasgow', 'manchester', 'birmingham', 'leeds', 'liverpool',
            'bristol', 'sheffield', 'leicester', 'coventry', 'bradford', 'cardiff',
            'belfast', 'newcastle', 'nottingham', 'southampton', 'portsmouth', 'plymouth',
            'swansea', 'sunderland', 'wolverhampton', 'derby', 'southampton', 'portsmouth',
            'plymouth', 'swansea', 'sunderland', 'wolverhampton', 'derby', 'southampton'
        ]
        
        # States database
        self.indian_states = [
            'maharashtra', 'karnataka', 'tamil nadu', 'west bengal', 'gujarat', 'rajasthan',
            'uttar pradesh', 'bihar', 'andhra pradesh', 'telangana', 'odisha', 'kerala',
            'madhya pradesh', 'punjab', 'haryana', 'assam', 'chhattisgarh', 'jharkhand',
            'uttarakhand', 'himachal pradesh', 'tripura', 'meghalaya', 'manipur', 'nagaland',
            'goa', 'arunachal pradesh', 'mizoram', 'sikkim', 'delhi', 'chandigarh',
            'puducherry', 'dadra and nagar haveli', 'daman and diu', 'lakshadweep',
            'andaman and nicobar islands', 'jammu and kashmir', 'ladakh'
        ]
    
    def extract_location(self, text: str, name: str = None) -> str:
        """Extract location from resume text"""
        try:
            logger.info("📍 Starting trained location extraction...")
            
            # Clean text
            text_clean = self._clean_text(text)
            
            # Extract using patterns
            location = self._extract_with_patterns(text_clean)
            
            # Validate location
            validated_location = self._validate_location(location)
            
            # Filter out name if it appears in location
            if name and validated_location:
                validated_location = self._filter_name_from_location(validated_location, name)
            
            logger.info(f"✅ Location extracted: {validated_location}")
            return validated_location
            
        except Exception as e:
            logger.error(f"❌ Location extraction error: {e}")
            return 'Location not found'
    
    def _extract_with_patterns(self, text: str) -> str:
        """Extract location using patterns"""
        text_lower = text.lower()
        
        # First try structured patterns
        for pattern in self.location_patterns[:12]:  # First 12 are structured patterns
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                location = match.group(1).strip()
                if len(location) > 2 and len(location) < 50:
                    return location
        
        # Then try direct city name matches
        for city in self.location_patterns[12:]:  # Cities from index 12 onwards
            if city.lower() in text_lower:
                return city
        
        # Check against cities database
        for city in self.indian_cities + self.international_cities:
            if city in text_lower:
                return city.title()
        
        # Check against states database
        for state in self.indian_states:
            if state in text_lower:
                return state.title()
        
        # Fallback: Look for any capitalized words that might be locations
        # Split text into lines and look for location-like patterns
        lines = text.split('\n')
        for line in lines:
            line = line.strip()
            # Look for lines that might contain location info
            if any(keyword in line.lower() for keyword in ['location', 'address', 'city', 'based', 'located', 'from', 'residing', 'living']):
                # Extract potential location from the line
                words = line.split()
                for word in words:
                    word_clean = re.sub(r'[^\w]', '', word)
                    if len(word_clean) > 3 and word_clean[0].isupper():
                        # Check if it's a known city
                        if word_clean.lower() in [city.lower() for city in self.indian_cities + self.international_cities]:
                            return word_clean
        
        # Ultimate fallback: Look for any known city name anywhere in the text
        for city in self.indian_cities + self.international_cities:
            if city in text_lower:
                return city.title()
        
        # If still no location found, try to extract from common resume sections
        # Look for contact information section
        contact_keywords = ['contact', 'personal', 'details', 'information', 'profile']
        for keyword in contact_keywords:
            if keyword in text_lower:
                # Find the section and look for location
                lines = text.split('\n')
                for i, line in enumerate(lines):
                    if keyword in line.lower():
                        # Check next few lines for location
                        for j in range(i+1, min(i+5, len(lines))):
                            next_line = lines[j].strip()
                            for city in self.indian_cities + self.international_cities:
                                if city in next_line.lower():
                                    return city.title()
        
        return ''
    
    def _validate_location(self, location: str) -> str:
        """Validate extracted location"""
        if not location:
            return ''
        
        location_lower = location.lower()
        
        # Check if it's a known city
        for city in self.indian_cities + self.international_cities:
            if city in location_lower:
                return city.title()
        
        # Check if it's a known state
        for state in self.indian_states:
            if state in location_lower:
                return state.title()
        
        # If not found in database, return as is (might be a valid location)
        return location.title()
    
    def _filter_name_from_location(self, location: str, name: str) -> str:
        """Filter out name from location"""
        if not name or not location:
            return location
        
        name_parts = name.lower().split()
        location_lower = location.lower()
        
        # Remove name parts from location
        for part in name_parts:
            if len(part) > 2 and part in location_lower:
                location_lower = location_lower.replace(part, '').strip()
        
        # Clean up extra spaces
        location_clean = re.sub(r'\s+', ' ', location_lower).strip()
        
        return location_clean.title() if location_clean else location
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text.strip())
        
        # Remove special characters but keep basic punctuation
        text = re.sub(r'[^\w\s@\.\-\+\(\)]', ' ', text)
        
        return text

# Initialize global location extractor
location_extractor = LocationExtractor()
