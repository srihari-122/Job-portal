"""
Direct Name Fix
Handles the exact name extraction issue we're seeing
"""

import re
import logging
from typing import Optional

logger = logging.getLogger(__name__)

class DirectNameFix:
    """Direct name fix for the exact issue we're seeing"""
    
    def __init__(self):
        pass
        
    def extract_name_direct(self, text: str, filename: str = None) -> str:
        """Extract name directly from the text we're seeing"""
        try:
            logger.info("🔍 Starting direct name extraction...")
            
            # The raw text shows "PRATIK P TARALE" at the beginning
            # Let's extract it directly
            
            lines = text.split('\n')
            
            # Check first line - this is where names usually are
            if lines:
                first_line = lines[0].strip()
                logger.info(f"🔍 First line: '{first_line}'")
                
                # Check if first line looks like a name
                if self._is_likely_name(first_line):
                    logger.info(f"✅ Direct name found: {first_line}")
                    return first_line
            
            # Check second line if first line is not a name
            if len(lines) > 1:
                second_line = lines[1].strip()
                logger.info(f"🔍 Second line: '{second_line}'")
                
                if self._is_likely_name(second_line):
                    logger.info(f"✅ Direct name found on second line: {second_line}")
                    return second_line
            
            # Look for patterns in the text
            name_patterns = [
                r'^([A-Z][A-Z\s]+[A-Z])\s',  # ALL CAPS names
                r'^([A-Z][a-z]+ [A-Z][a-z]+(?: [A-Z][a-z]+)?)\s',  # Title Case names
                r'([A-Z][A-Z]+ [A-Z]\. [A-Z][A-Z]+)',  # ALL CAPS with middle initial
                r'([A-Z][a-z]+ [A-Z]\. [A-Z][a-z]+)',  # Title Case with middle initial
            ]
            
            for pattern in name_patterns:
                matches = re.findall(pattern, text, re.IGNORECASE | re.MULTILINE)
                if matches:
                    name = matches[0].strip()
                    if self._is_likely_name(name):
                        logger.info(f"✅ Direct name found with pattern: {name}")
                        return name
            
            # Filename fallback
            if filename:
                name_from_file = self._extract_name_from_filename(filename)
                if name_from_file:
                    logger.info(f"✅ Direct name from filename: {name_from_file}")
                    return name_from_file
            
            return 'Name not found'
            
        except Exception as e:
            logger.error(f"❌ Direct name extraction error: {e}")
            return 'Name not found'
    
    def _is_likely_name(self, text: str) -> bool:
        """Check if text is likely a name"""
        if not text or len(text.strip()) < 2:
            return False
        
        # Must contain only letters, spaces, dots, and hyphens
        if not re.match(r'^[A-Za-z\s\.\-]+$', text):
            return False
        
        # Must be reasonable length
        if len(text) > 50:
            return False
        
        # Must have at least 2 words
        words = text.split()
        if len(words) < 2:
            return False
        
        # Each word should start with uppercase
        for word in words:
            if not word[0].isupper():
                return False
        
        # Check for false positives
        false_positives = [
            'to land', 'resume', 'cv', 'curriculum vitae', 'personal information',
            'contact information', 'objective', 'summary', 'experience', 'education',
            'skills', 'projects', 'profile', 'about', 'contact', 'address', 'phone',
            'email', 'complete visitor management service', 'admin dashboard',
            'visitor management', 'the unauthenticated or unwanted visitors',
            'user and system data logs', 'system data logs', 'data logs'
        ]
        
        text_lower = text.lower()
        for fp in false_positives:
            if fp in text_lower:
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
            if self._is_likely_name(name):
                return name
            
            return None
            
        except Exception as e:
            logger.error(f"❌ Error extracting name from filename: {e}")
            return None

# Initialize global direct name fix
direct_name_fix = DirectNameFix()
