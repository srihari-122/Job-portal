"""
Advanced Text Extraction System
Supports multiple file formats with robust text extraction
"""

import os
import logging
from typing import Optional, Tuple
import PyPDF2
import docx
import io

# Try to import advanced text extraction libraries
try:
    import fitz  # PyMuPDF
    PYMUPDF_AVAILABLE = True
except ImportError:
    PYMUPDF_AVAILABLE = False

try:
    import textract
    TEXTRACT_AVAILABLE = True
except ImportError:
    TEXTRACT_AVAILABLE = False

try:
    import pdfplumber
    PDFPLUMBER_AVAILABLE = True
except ImportError:
    PDFPLUMBER_AVAILABLE = False

logger = logging.getLogger(__name__)

class AdvancedTextExtractor:
    """Advanced text extractor supporting multiple file formats"""
    
    def __init__(self):
        self.supported_formats = {
            '.pdf': self._extract_pdf,
            '.docx': self._extract_docx,
            '.doc': self._extract_doc,
            '.txt': self._extract_txt
        }
    
    def extract_text(self, file_path: str) -> Tuple[str, bool]:
        """Extract text from file with multiple fallback methods"""
        try:
            if not os.path.exists(file_path):
                return "", False
            
            file_ext = os.path.splitext(file_path)[1].lower()
            
            if file_ext not in self.supported_formats:
                logger.warning(f"Unsupported file format: {file_ext}")
                return "", False
            
            # Try multiple extraction methods
            text = ""
            success = False
            
            # Method 1: Use the primary extractor for the file type
            try:
                text = self.supported_formats[file_ext](file_path)
                if text and len(text.strip()) > 10:
                    success = True
                    logger.info(f"✅ Text extracted using primary method for {file_ext}")
            except Exception as e:
                logger.warning(f"⚠️ Primary extraction failed for {file_ext}: {e}")
            
            # Method 2: For PDFs, try alternative methods
            if not success and file_ext == '.pdf':
                text, success = self._extract_pdf_fallback(file_path)
            
            # Method 3: For DOCX, try alternative methods
            if not success and file_ext == '.docx':
                text, success = self._extract_docx_fallback(file_path)
            
            if success:
                logger.info(f"✅ Successfully extracted {len(text)} characters from {file_path}")
            else:
                logger.error(f"❌ Failed to extract text from {file_path}")
            
            return text, success
            
        except Exception as e:
            logger.error(f"❌ Text extraction error: {e}")
            return "", False
    
    def _extract_pdf(self, file_path: str) -> str:
        """Extract text from PDF using PyPDF2"""
        try:
            text = ""
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
            return text.strip()
        except Exception as e:
            logger.error(f"❌ PyPDF2 extraction error: {e}")
            return ""
    
    def _extract_docx(self, file_path: str) -> str:
        """Extract text from DOCX file"""
        try:
            doc = docx.Document(file_path)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text.strip()
        except Exception as e:
            logger.error(f"❌ DOCX extraction error: {e}")
            return ""
    
    def _extract_doc(self, file_path: str) -> str:
        """Extract text from DOC file (basic implementation)"""
        try:
            # For DOC files, we'll try to use python-docx if possible
            # This is a basic implementation - DOC support is limited
            logger.warning("⚠️ DOC file support is limited. Consider converting to DOCX.")
            return ""
        except Exception as e:
            logger.error(f"❌ DOC extraction error: {e}")
            return ""
    
    def _extract_txt(self, file_path: str) -> str:
        """Extract text from TXT file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read().strip()
        except UnicodeDecodeError:
            try:
                with open(file_path, 'r', encoding='latin-1') as file:
                    return file.read().strip()
            except Exception as e:
                logger.error(f"❌ TXT extraction error: {e}")
                return ""
        except Exception as e:
            logger.error(f"❌ TXT extraction error: {e}")
            return ""
    
    def _extract_pdf_fallback(self, file_path: str) -> Tuple[str, bool]:
        """Fallback PDF extraction methods"""
        text = ""
        success = False
        
        # Try PyMuPDF (fitz)
        if PYMUPDF_AVAILABLE:
            try:
                doc = fitz.open(file_path)
                for page in doc:
                    text += page.get_text()
                doc.close()
                if text and len(text.strip()) > 10:
                    success = True
                    logger.info("✅ PDF text extracted using PyMuPDF")
            except Exception as e:
                logger.warning(f"⚠️ PyMuPDF extraction failed: {e}")
        
        # Try pdfplumber
        if not success and PDFPLUMBER_AVAILABLE:
            try:
                with pdfplumber.open(file_path) as pdf:
                    for page in pdf.pages:
                        page_text = page.extract_text()
                        if page_text:
                            text += page_text + "\n"
                if text and len(text.strip()) > 10:
                    success = True
                    logger.info("✅ PDF text extracted using pdfplumber")
            except Exception as e:
                logger.warning(f"⚠️ pdfplumber extraction failed: {e}")
        
        # Try textract
        if not success and TEXTRACT_AVAILABLE:
            try:
                text = textract.process(file_path).decode('utf-8')
                if text and len(text.strip()) > 10:
                    success = True
                    logger.info("✅ PDF text extracted using textract")
            except Exception as e:
                logger.warning(f"⚠️ textract extraction failed: {e}")
        
        return text.strip(), success
    
    def _extract_docx_fallback(self, file_path: str) -> Tuple[str, bool]:
        """Fallback DOCX extraction methods"""
        text = ""
        success = False
        
        # Try textract for DOCX
        if TEXTRACT_AVAILABLE:
            try:
                text = textract.process(file_path).decode('utf-8')
                if text and len(text.strip()) > 10:
                    success = True
                    logger.info("✅ DOCX text extracted using textract")
            except Exception as e:
                logger.warning(f"⚠️ textract DOCX extraction failed: {e}")
        
        return text.strip(), success

# Initialize global text extractor
text_extractor = AdvancedTextExtractor()
