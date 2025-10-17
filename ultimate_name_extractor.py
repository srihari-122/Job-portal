"""
Ultimate Name Extractor
Handles the most difficult name extraction cases
"""

import re
import logging
from typing import Optional

logger = logging.getLogger(__name__)

class UltimateNameExtractor:
    """Ultimate name extractor for the most difficult cases"""
    
    def __init__(self):
        self.initialize_ultimate_patterns()
        
    def initialize_ultimate_patterns(self):
        """Initialize ultimate name patterns"""
        
        # Ultimate name patterns for difficult cases
        self.ultimate_patterns = [
            # ALL CAPS names at the beginning
            r'^([A-Z][A-Z\s]+[A-Z])\s*\n',
            r'^([A-Z][A-Z]+ [A-Z][A-Z]+)\s*\n',
            r'^([A-Z][A-Z]+ [A-Z]\. [A-Z][A-Z]+)\s*\n',
            
            # Mixed case names
            r'^([A-Z][a-z]+ [A-Z][a-z]+(?: [A-Z][a-z]+)?)\s*\n',
            r'^([A-Z][a-z]+ [A-Z]\. [A-Z][a-z]+)\s*\n',
            
            # Names with middle initials
            r'^([A-Z][A-Z]+ [A-Z]\. [A-Z][A-Z]+)\s*\n',
            r'^([A-Z][a-z]+ [A-Z]\. [A-Z][a-z]+)\s*\n',
            
            # Profile section names
            r'^([A-Z][A-Z\s]+[A-Z])\s*\n\s*(?:PROFILE|Profile|About|Summary)',
            r'^([A-Z][a-z]+ [A-Z][a-z]+(?: [A-Z][a-z]+)?)\s*\n\s*(?:PROFILE|Profile|About|Summary)',
        ]
        
        # Common false positives to avoid
        self.false_positives = [
            'resume', 'cv', 'curriculum vitae', 'personal information', 'contact information',
            'objective', 'summary', 'experience', 'education', 'skills', 'projects', 'to land',
            'and phone number', 'profile', 'about', 'contact', 'address', 'phone', 'email',
            'complete visitor management service', 'admin dashboard', 'visitor management',
            'slr residency bannerghatta main road gottigere', 'the unauthenticated or unwanted visitors',
            'user and system data logs', 'system data logs', 'data logs', 'logs'
        ]
        
    def extract_name_ultimate(self, text: str, filename: str = None) -> str:
        """Extract name using ultimate patterns"""
        try:
            logger.info("🔍 Starting ultimate name extraction...")
            
            lines = text.split('\n')
            
            # Priority 1: First line (most common for names)
            if lines:
                first_line = lines[0].strip()
                if self._is_valid_name_ultimate(first_line):
                    logger.info(f"✅ Name extracted from first line: {first_line}")
                    return first_line
            
            # Priority 2: Try all ultimate patterns
            for pattern in self.ultimate_patterns:
                matches = re.findall(pattern, text, re.IGNORECASE | re.MULTILINE)
                if matches:
                    name = matches[0].strip()
                    if self._is_valid_name_ultimate(name):
                        logger.info(f"✅ Name extracted with ultimate pattern: {name}")
                        return name
            
            # Priority 3: Look for name in first few lines
            for i, line in enumerate(lines[:5]):
                line = line.strip()
                if self._is_valid_name_ultimate(line):
                    logger.info(f"✅ Name extracted from line {i+1}: {line}")
                    return line
            
            # Priority 4: Filename fallback
            if filename:
                name_from_file = self._extract_name_from_filename(filename)
                if name_from_file:
                    logger.info(f"✅ Name extracted from filename: {name_from_file}")
                    return name_from_file
            
            return 'Name not found'
            
        except Exception as e:
            logger.error(f"❌ Ultimate name extraction error: {e}")
            return 'Name not found'
    
    def _is_valid_name_ultimate(self, name: str) -> bool:
        """Ultimate name validation"""
        if not name or len(name.strip()) < 2:
            return False
        
        # Check if it contains only letters, spaces, dots, and hyphens
        if not re.match(r'^[A-Za-z\s\.\-]+$', name):
            return False
        
        # Check if it's not too long
        if len(name) > 50:
            return False
        
        # Check if it's not a false positive
        name_lower = name.lower()
        for fp in self.false_positives:
            if fp in name_lower:
                return False
        
        # Check if it looks like a real name (has at least 2 words)
        words = name.split()
        if len(words) < 2:
            return False
        
        # Check if each word starts with a capital letter
        for word in words:
            if not word[0].isupper():
                return False
        
        return True
    
    def _extract_name_from_filename(self, filename: str) -> Optional[str]:
        """Extract name from filename"""
        try:
            # Remove file extension
            name = filename.replace('.pdf', '').replace('.docx', '').replace('.txt', '')
            
            # Remove common prefixes/suffixes
            name = re.sub(r'^(resume|cv|curriculum_vitae)_?', '', name, flags=re.IGNORECASE)
            name = re.sub(r'_\d+$', '', name)  # Remove timestamps
            name = re.sub(r'_\d+_', '_', name)  # Remove middle timestamps
            
            # Check if it looks like a name
            if self._is_valid_name_ultimate(name):
                return name
            
            return None
            
        except Exception as e:
            logger.error(f"❌ Error extracting name from filename: {e}")
            return None

# Initialize global ultimate name extractor
ultimate_name_extractor = UltimateNameExtractor()
