"""
AI-Powered Resume Extractor
Using advanced AI models for accurate extraction
"""

import re
import logging
from datetime import datetime
from typing import Dict, List, Any, Tuple
import PyPDF2
import docx
import io
import os

# Try to import advanced AI libraries
try:
    import spacy
    SPACY_AVAILABLE = True
except ImportError:
    SPACY_AVAILABLE = False

try:
    from transformers import pipeline
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False

try:
    import nltk
    from nltk.tokenize import word_tokenize, sent_tokenize
    from nltk.tag import pos_tag
    from nltk.chunk import ne_chunk
    NLTK_AVAILABLE = True
except ImportError:
    NLTK_AVAILABLE = False

logger = logging.getLogger(__name__)

class AIResumeExtractor:
    """AI-powered resume extractor using advanced models"""
    
    def __init__(self):
        self.nlp = None
        self.ner_pipeline = None
        self._initialize_models()
        
        # Comprehensive skill database
        self.skill_database = [
            # Programming Languages
            'Python', 'Java', 'JavaScript', 'TypeScript', 'C++', 'C#', 'Go', 'Rust',
            'Swift', 'Kotlin', 'PHP', 'Ruby', 'Perl', 'Scala', 'R', 'MATLAB', 'C',
            'Objective-C', 'Assembly', 'Shell', 'Bash', 'PowerShell', 'VBA', 'Delphi',
            'Dart', 'Julia', 'Lua', 'Haskell', 'Clojure', 'Erlang', 'Elixir',
            
            # Web Technologies
            'HTML', 'CSS', 'React', 'Angular', 'Vue', 'Svelte', 'Bootstrap', 'Tailwind',
            'jQuery', 'SASS', 'SCSS', 'Less', 'Webpack', 'Vite', 'Next.js', 'Nuxt.js',
            'Ember.js', 'Backbone.js', 'Dart', 'Chart.js', 'Three.js', 'GSAP',
            'Redux', 'MobX', 'Vuex', 'Pinia', 'Storybook', 'Jest', 'Cypress',
            
            # Backend Technologies
            'Node.js', 'Express', 'Django', 'Flask', 'Spring', 'Laravel', 'Rails',
            'ASP.NET', 'FastAPI', 'Koa', 'Hapi', 'Sails.js', 'Meteor', 'NestJS',
            'Phoenix', 'Gin', 'Echo', 'Fiber', 'Gorilla', 'Chi',
            
            # Databases
            'SQL', 'MySQL', 'PostgreSQL', 'MongoDB', 'Redis', 'Oracle', 'SQLite',
            'Cassandra', 'DynamoDB', 'CouchDB', 'Neo4j', 'Elasticsearch', 'Firebase',
            'MariaDB', 'Couchbase', 'InfluxDB', 'TimescaleDB', 'ClickHouse',
            'ArangoDB', 'RethinkDB', 'CockroachDB', 'PlanetScale',
            
            # Cloud & DevOps
            'AWS', 'Azure', 'GCP', 'Docker', 'Kubernetes', 'Jenkins', 'GitLab',
            'GitHub Actions', 'Terraform', 'Ansible', 'Chef', 'Puppet', 'Vagrant',
            'CircleCI', 'Travis CI', 'GitHub', 'Bitbucket', 'Heroku', 'DigitalOcean',
            'Vercel', 'Netlify', 'Railway', 'Render', 'Fly.io',
            
            # Data Science
            'Pandas', 'NumPy', 'Scikit-learn', 'TensorFlow', 'PyTorch', 'Keras',
            'Spark', 'Hadoop', 'Jupyter', 'Matplotlib', 'Seaborn', 'Plotly',
            'Apache Airflow', 'Apache Kafka', 'Apache Storm', 'Apache Flink',
            'MLflow', 'Kubeflow', 'Weights & Biases', 'Comet', 'Neptune',
            
            # Mobile
            'React Native', 'Flutter', 'iOS', 'Android', 'Swift', 'Kotlin',
            'Xamarin', 'Ionic', 'Cordova', 'PhoneGap', 'Unity', 'Unreal Engine',
            'Expo', 'NativeScript', 'Appcelerator', 'Sencha Touch',
            
            # Testing
            'Selenium', 'Jest', 'Cypress', 'JUnit', 'Pytest', 'Mocha', 'Chai',
            'Jasmine', 'Karma', 'Protractor', 'TestNG', 'Cucumber', 'Playwright',
            'Detox', 'Appium', 'Espresso', 'XCUITest', 'Robot Framework',
            
            # Tools
            'Git', 'SVN', 'Mercurial', 'Jira', 'Confluence', 'Slack', 'Trello',
            'Asana', 'Figma', 'Sketch', 'Adobe XD', 'Postman', 'Insomnia', 'VS Code',
            'IntelliJ', 'Eclipse', 'PyCharm', 'WebStorm', 'Sublime Text', 'Vim',
            'Notion', 'Linear', 'Monday.com', 'ClickUp', 'Airtable',
            
            # Soft Skills
            'Communication', 'Leadership', 'Teamwork', 'Problem Solving', 'Analytical',
            'Project Management', 'Time Management', 'Critical Thinking', 'Creativity',
            'Adaptability', 'Collaboration', 'Presentation', 'Negotiation', 'Mentoring',
            'Strategic Thinking', 'Innovation', 'Agile', 'Scrum', 'Kanban',
            
            # Frameworks
            'Spring Boot', 'Django', 'Flask', 'Express', 'Laravel', 'Rails', 'Symfony',
            'CodeIgniter', 'CakePHP', 'Zend', 'Hibernate', 'MyBatis', 'JPA',
            'FastAPI', 'Sanic', 'Quart', 'Starlette', 'Uvicorn', 'Gunicorn',
            
            # AI/ML
            'Machine Learning', 'Deep Learning', 'Neural Networks', 'Computer Vision',
            'Natural Language Processing', 'Reinforcement Learning', 'Transfer Learning',
            'OpenAI', 'Hugging Face', 'LangChain', 'LlamaIndex', 'Pinecone', 'Weaviate'
        ]
        
        # Location database
        self.location_database = [
            'bangalore', 'bengaluru', 'mumbai', 'delhi', 'hyderabad', 'pune', 'chennai', 'kolkata',
            'ahmedabad', 'gurgaon', 'noida', 'jaipur', 'lucknow', 'indore', 'bhopal',
            'chandigarh', 'coimbatore', 'kochi', 'thiruvananthapuram', 'mysore', 'mangalore',
            'vadodara', 'surat', 'rajkot', 'bhubaneswar', 'bhubaneshwar', 'cuttack',
            'guwahati', 'shillong', 'imphal', 'aizawl', 'kohima', 'itanagar', 'gangtok',
            'kalaburgi', 'gulbarga', 'hubli', 'dharwad', 'belgaum', 'bellary', 'tumkur',
            'raichur', 'bidar', 'hospet', 'gadag', 'bagalkot', 'bijapur', 'kolar',
            'mandya', 'hassan', 'udupi', 'dakshina kannada', 'chikmagalur',
            'chitradurga', 'davangere', 'shimoga', 'chamrajanagar', 'kodagu', 'mysuru',
            'new york', 'san francisco', 'los angeles', 'chicago', 'boston', 'seattle',
            'austin', 'denver', 'miami', 'atlanta', 'dallas', 'houston', 'phoenix',
            'london', 'paris', 'berlin', 'madrid', 'rome', 'amsterdam', 'zurich',
            'singapore', 'hong kong', 'tokyo', 'seoul', 'sydney', 'melbourne', 'toronto',
            'vancouver', 'montreal', 'dubai', 'abu dhabi', 'riyadh', 'doha', 'kuwait'
        ]
    
    def _initialize_models(self):
        """Initialize AI models"""
        try:
            # Initialize spaCy
            if SPACY_AVAILABLE:
                try:
                    self.nlp = spacy.load("en_core_web_sm")
                    logger.info("✅ spaCy model loaded successfully")
                except OSError:
                    logger.warning("⚠️ spaCy model not found, using basic text processing")
                    self.nlp = None
            
            # Initialize Transformers NER pipeline
            if TRANSFORMERS_AVAILABLE:
                try:
                    self.ner_pipeline = pipeline("ner", 
                                               model="dbmdz/bert-large-cased-finetuned-conll03-english",
                                               aggregation_strategy="simple")
                    logger.info("✅ Transformers NER model loaded successfully")
                except Exception as e:
                    logger.warning(f"⚠️ Transformers NER model failed to load: {e}")
                    self.ner_pipeline = None
            
            # Download NLTK data
            if NLTK_AVAILABLE:
                try:
                    nltk.download('punkt', quiet=True)
                    nltk.download('averaged_perceptron_tagger', quiet=True)
                    nltk.download('maxent_ne_chunker', quiet=True)
                    nltk.download('words', quiet=True)
                    logger.info("✅ NLTK models downloaded successfully")
                except Exception as e:
                    logger.warning(f"⚠️ NLTK models failed to download: {e}")
            
        except Exception as e:
            logger.error(f"❌ Error initializing AI models: {e}")
    
    def extract_resume_content(self, text: str, filename: str = None) -> Dict[str, Any]:
        """Extract resume content using AI models"""
        try:
            logger.info("🤖 Starting AI-powered resume extraction...")
            
            if not text or len(text.strip()) < 10:
                return self._get_empty_extraction()
            
            # Clean text
            text_clean = self._clean_text(text)
            
            # Extract components using AI
            name = self._extract_name_ai(text_clean, filename)
            email = self._extract_email_ai(text_clean)
            phone = self._extract_phone_ai(text_clean)
            role = self._extract_role_ai(text_clean, name)
            location = self._extract_location_ai(text_clean, name)
            skills = self._extract_skills_ai(text_clean)
            experience = self._extract_experience_ai(text_clean)
            
            # Calculate confidence
            confidence = self._calculate_confidence(name, email, phone, skills, experience, role)
            
            extracted_data = {
                'name': name,
                'email': email,
                'phone': phone,
                'skills': skills,
                'experience': experience,
                'role': role,
                'location': location,
                'education': [],  # Removed as requested
                'raw_text': text_clean[:1000] + "..." if len(text_clean) > 1000 else text_clean,
                'extraction_method': 'ai_powered',
                'confidence_score': confidence,
                'extraction_timestamp': datetime.now().isoformat()
            }
            
            logger.info(f"✅ AI extraction completed:")
            logger.info(f"👤 Name: {name}")
            logger.info(f"📧 Email: {email}")
            logger.info(f"📱 Phone: {phone}")
            logger.info(f"🎯 Role: {role}")
            logger.info(f"📍 Location: {location}")
            logger.info(f"📊 Skills: {len(skills)} found")
            logger.info(f"⏰ Experience: {experience['display']}")
            logger.info(f"🎯 Confidence: {confidence:.2f}")
            
            return extracted_data
            
        except Exception as e:
            logger.error(f"❌ Error in AI resume extraction: {e}")
            return self._get_empty_extraction()
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text.strip())
        
        # Remove special characters but keep basic punctuation
        text = re.sub(r'[^\w\s@\.\-\+\(\)]', ' ', text)
        
        # Normalize line breaks
        text = re.sub(r'\n+', '\n', text)
        
        return text
    
    def _extract_name_ai(self, text: str, filename: str = None) -> str:
        """Extract name using AI models"""
        try:
            # Strategy 1: Extract from filename
            if filename and filename != 'undefined':
                name_from_file = filename.replace('.pdf', '').replace('.docx', '').replace('.doc', '')
                name_from_file = re.sub(r'^(resume|cv|curriculum|vitae)[_\-\s]*', '', name_from_file, flags=re.IGNORECASE)
                name_parts = re.split(r'[_\-\s]+', name_from_file)
                name_parts = [part.strip().title() for part in name_parts if part.strip() and len(part.strip()) > 1]
                if len(name_parts) >= 2:
                    return ' '.join(name_parts)
            
            # Strategy 2: Use spaCy NER
            if self.nlp:
                doc = self.nlp(text[:2000])
                for ent in doc.ents:
                    if ent.label_ == "PERSON" and len(ent.text.split()) >= 2:
                        # Validate name format
                        words = ent.text.split()
                        if all(word[0].isupper() for word in words if word):
                            return ent.text.title()
            
            # Strategy 3: Use Transformers NER
            if self.ner_pipeline:
                try:
                    entities = self.ner_pipeline(text[:1000])
                    for entity in entities:
                        if entity['entity_group'] == 'PER' and len(entity['word'].split()) >= 2:
                            return entity['word'].title()
                except Exception as e:
                    logger.warning(f"⚠️ Transformers NER failed: {e}")
            
            # Strategy 4: Use NLTK NER
            if NLTK_AVAILABLE:
                try:
                    sentences = sent_tokenize(text[:1000])
                    for sentence in sentences:
                        words = word_tokenize(sentence)
                        pos_tags = pos_tag(words)
                        chunks = ne_chunk(pos_tags)
                        
                        for chunk in chunks:
                            if hasattr(chunk, 'label') and chunk.label() == 'PERSON':
                                name = ' '.join([token for token, pos in chunk.leaves()])
                                if len(name.split()) >= 2:
                                    return name.title()
                except Exception as e:
                    logger.warning(f"⚠️ NLTK NER failed: {e}")
            
            # Strategy 5: Pattern matching in headers
            lines = text.split('\n')
            for i, line in enumerate(lines[:15]):
                line = line.strip()
                if len(line) < 3 or len(line) > 60:
                    continue
                
                # Look for name patterns (2-4 words, proper case)
                words = line.split()
                if 2 <= len(words) <= 4:
                    # Check if all words are proper nouns
                    if all(word[0].isupper() for word in words if word):
                        # Skip common non-name words
                        skip_words = {
                            'resume', 'cv', 'curriculum', 'vitae', 'email', 'phone', 'address',
                            'linkedin', 'github', 'objective', 'summary', 'profile', 'experience',
                            'education', 'skills', 'projects', 'certifications', 'contact',
                            'software', 'engineer', 'developer', 'manager', 'analyst'
                        }
                        if not any(word.lower() in skip_words for word in words):
                            return ' '.join(words)
            
            return 'Name not found'
            
        except Exception as e:
            logger.error(f"❌ Name extraction error: {e}")
            return 'Name extraction error'
    
    def _extract_email_ai(self, text: str) -> str:
        """Extract email using AI patterns"""
        try:
            email_patterns = [
                r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
                r'email[:\s]*([A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,})',
                r'e-mail[:\s]*([A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,})',
                r'contact[:\s]*([A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,})'
            ]
            
            emails_found = []
            for pattern in email_patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                for match in matches:
                    email = match.strip() if isinstance(match, str) else match
                    if '@' in email and '.' in email.split('@')[1]:
                        emails_found.append(email)
            
            if emails_found:
                return emails_found[0]
            
            return 'Email not found'
            
        except Exception as e:
            logger.error(f"❌ Email extraction error: {e}")
            return 'Email extraction error'
    
    def _extract_phone_ai(self, text: str) -> str:
        """Extract phone using AI patterns"""
        try:
            phone_patterns = [
                r'(\+91|91)?[-.\s]?\d{5}[-.\s]?\d{5}',  # Indian format
                r'(\+1|1)?[-.\s]?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',  # US format
                r'(\+44|44)?[-.\s]?\d{4}[-.\s]?\d{6}',  # UK format
                r'(\+?\d{1,3}[-.\s]?)?(\(?\d{3}\)?[-.\s]?)?\d{3}[-.\s]?\d{4}',  # Generic
                r'phone[:\s]*(\+?\d{1,3}[-.\s]?)?(\(?\d{3}\)?[-.\s]?)?\d{3}[-.\s]?\d{4}',
                r'mobile[:\s]*(\+?\d{1,3}[-.\s]?)?(\(?\d{3}\)?[-.\s]?)?\d{3}[-.\s]?\d{4}',
                r'contact[:\s]*(\+?\d{1,3}[-.\s]?)?(\(?\d{3}\)?[-.\s]?)?\d{3}[-.\s]?\d{4}',
                r'cell[:\s]*(\+?\d{1,3}[-.\s]?)?(\(?\d{3}\)?[-.\s]?)?\d{3}[-.\s]?\d{4}',
                r'tel[:\s]*(\+?\d{1,3}[-.\s]?)?(\(?\d{3}\)?[-.\s]?)?\d{3}[-.\s]?\d{4}',
                r'(\+91|91)?\s?\d{5}\s?\d{5}',  # Indian format without separators
                r'(\+91|91)?\s?\d{10}',  # Indian format 10 digits
                r'\d{10}',  # Simple 10 digits
                r'\d{5}\s?\d{5}',  # 5-5 format
                r'\d{3}\s?\d{3}\s?\d{4}',  # 3-3-4 format
                r'\d{4}\s?\d{3}\s?\d{3}'  # 4-3-3 format
            ]
            
            phones_found = []
            for pattern in phone_patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                for match in matches:
                    phone = ''.join(match) if isinstance(match, tuple) else match
                    phone_clean = re.sub(r'[^\d+]', '', phone)
                    
                    # Validate phone length and format
                    if len(phone_clean) >= 10 and len(phone_clean) <= 15:
                        phones_found.append(phone_clean)
            
            if phones_found:
                return phones_found[0]
            
            return 'Phone not found'
            
        except Exception as e:
            logger.error(f"❌ Phone extraction error: {e}")
            return 'Phone extraction error'
    
    def _extract_role_ai(self, text: str, name: str) -> str:
        """Extract role using AI models"""
        try:
            # Get name words to exclude
            name_words = set()
            if name and name != 'Name not found':
                name_words = set(name.lower().split())
            
            # Use spaCy NER for organizations and roles
            if self.nlp:
                doc = self.nlp(text[:2000])
                for ent in doc.ents:
                    if ent.label_ == "ORG" and any(role_word in ent.text.lower() for role_word in ['developer', 'engineer', 'manager', 'analyst']):
                        if ent.text.lower() not in name_words:
                            return ent.text.title()
            
            # Look for role in work experience section
            work_section_patterns = [
                r'(?:worked\s+as|position\s+of|role\s+of|designation\s+of|currently\s+working\s+as|presently\s+working\s+as|job\s+title|position|role|title)[:\s]*([A-Za-z\s]{3,60})',
                r'([A-Za-z\s]{3,60})\s+(?:developer|engineer|manager|analyst|consultant|specialist|architect|programmer)',
                r'(?:as\s+a\s+|as\s+an\s+|as\s+)\s*([A-Za-z\s]{3,60})'
            ]
            
            for pattern in work_section_patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                for match in matches:
                    role = match.strip()
                    if len(role.split()) >= 2:
                        # Check if role contains name words
                        if name.lower() not in role.lower():
                            return role.title()
            
            # Common role patterns
            role_patterns = [
                r'(?:Software|Web|Frontend|Backend|Full.?Stack|Mobile|DevOps|Data|Machine Learning|AI)\s+(?:Developer|Engineer|Programmer|Architect|Consultant|Manager|Analyst|Scientist)',
                r'(?:Senior|Junior|Lead|Principal|Staff)\s+(?:Developer|Engineer|Programmer|Architect|Consultant|Manager|Analyst|Scientist)',
                r'(?:Project|Product|Business|System|Data|QA|Test)\s+(?:Manager|Analyst|Engineer|Consultant)',
                r'(?:UI|UX|Graphic|Web|Product)\s+(?:Designer|Developer|Engineer)',
                r'(?:Database|System|Network|IT)\s+(?:Administrator|Engineer|Specialist)',
                r'(?:Cloud|AWS|Azure|GCP)\s+(?:Engineer|Architect|Consultant|Specialist)',
                r'(?:Security|Cybersecurity)\s+(?:Engineer|Analyst|Consultant|Specialist)',
                r'(?:Data|Analytics|Business)\s+(?:Analyst|Scientist|Engineer|Consultant)'
            ]
            
            for pattern in role_patterns:
                match = re.search(pattern, text, re.IGNORECASE)
                if match:
                    role = match.group(0)
                    if name.lower() not in role.lower():
                        return role.title()
            
            # Default role based on skills
            text_lower = text.lower()
            if 'java' in text_lower and 'spring' in text_lower:
                return 'Full Stack Java Developer'
            elif 'java' in text_lower:
                return 'Java Developer'
            elif 'developer' in text_lower:
                return 'Software Developer'
            
            return 'Developer'
            
        except Exception as e:
            logger.error(f"❌ Role extraction error: {e}")
            return 'Developer'
    
    def _extract_location_ai(self, text: str, name: str) -> str:
        """Extract location using AI models"""
        try:
            # Use spaCy NER for locations
            if self.nlp:
                doc = self.nlp(text[:2000])
                for ent in doc.ents:
                    if ent.label_ == "GPE":  # Geopolitical entity
                        if name.lower() not in ent.text.lower():
                            return ent.text.title()
            
            # Use Transformers NER for locations
            if self.ner_pipeline:
                try:
                    entities = self.ner_pipeline(text[:1000])
                    for entity in entities:
                        if entity['entity_group'] == 'LOC' and name.lower() not in entity['word'].lower():
                            return entity['word'].title()
                except Exception as e:
                    logger.warning(f"⚠️ Transformers location extraction failed: {e}")
            
            # Look for known locations in text
            text_lower = text.lower()
            for location in self.location_database:
                if location in text_lower and location not in name.lower():
                    return location.title()
            
            # Pattern-based extraction
            location_patterns = [
                r'location[:\s]*([A-Za-z\s]{3,40})',
                r'address[:\s]*([A-Za-z\s]{3,40})',
                r'city[:\s]*([A-Za-z\s]{3,40})',
                r'based\s+in[:\s]*([A-Za-z\s]{3,40})',
                r'located\s+in[:\s]*([A-Za-z\s]{3,40})',
                r'residing\s+in[:\s]*([A-Za-z\s]{3,40})',
                r'from[:\s]*([A-Za-z\s]{3,40})',
                r'lives\s+in[:\s]*([A-Za-z\s]{3,40})',
                r'stays\s+in[:\s]*([A-Za-z\s]{3,40})'
            ]
            
            for pattern in location_patterns:
                match = re.search(pattern, text, re.IGNORECASE)
                if match:
                    location = match.group(1).strip()
                    if len(location.split()) >= 1 and name.lower() not in location.lower():
                        return location.title()
            
            return 'Location not found'
            
        except Exception as e:
            logger.error(f"❌ Location extraction error: {e}")
            return 'Location not found'
    
    def _extract_skills_ai(self, text: str) -> List[str]:
        """Extract skills using AI models"""
        try:
            skills = []
            text_lower = text.lower()
            
            # Extract from specific skills sections
            skill_sections = [
                r'skills?[:\s]*(.*?)(?:\n\n|\n[A-Z]|$)',
                r'technical\s+skills?[:\s]*(.*?)(?:\n\n|\n[A-Z]|$)',
                r'technologies?[:\s]*(.*?)(?:\n\n|\n[A-Z]|$)',
                r'tools?\s+and\s+technologies?[:\s]*(.*?)(?:\n\n|\n[A-Z]|$)',
                r'programming\s+languages?[:\s]*(.*?)(?:\n\n|\n[A-Z]|$)',
                r'frameworks?[:\s]*(.*?)(?:\n\n|\n[A-Z]|$)',
                r'libraries?[:\s]*(.*?)(?:\n\n|\n[A-Z]|$)',
                r'software\s+skills?[:\s]*(.*?)(?:\n\n|\n[A-Z]|$)',
                r'core\s+competencies?[:\s]*(.*?)(?:\n\n|\n[A-Z]|$)',
                r'expertise[:\s]*(.*?)(?:\n\n|\n[A-Z]|$)',
                r'competencies?[:\s]*(.*?)(?:\n\n|\n[A-Z]|$)',
                r'proficiencies?[:\s]*(.*?)(?:\n\n|\n[A-Z]|$)'
            ]
            
            for pattern in skill_sections:
                matches = re.findall(pattern, text, re.IGNORECASE | re.DOTALL)
                for match in matches:
                    section_text = match.lower()
                    for skill in self.skill_database:
                        if skill.lower() in section_text and skill not in skills:
                            skills.append(skill)
            
            # Look for skills in bullet points or lists
            bullet_patterns = [
                r'[•\-\*]\s*([A-Za-z0-9\s\.]+)',
                r'\d+\.\s*([A-Za-z0-9\s\.]+)',
                r'[•\-\*]\s*([A-Za-z0-9\s\.]+)'
            ]
            
            for pattern in bullet_patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                for match in matches:
                    potential_skill = match.strip()
                    if len(potential_skill) > 2 and len(potential_skill) < 30:
                        for skill in self.skill_database:
                            if skill.lower() == potential_skill.lower() and skill not in skills:
                                skills.append(skill)
            
            # Extract skills from work experience sections
            work_sections = [
                r'work\s+experience[:\s]*(.*?)(?:\n\n|\n[A-Z]|$)',
                r'professional\s+experience[:\s]*(.*?)(?:\n\n|\n[A-Z]|$)',
                r'employment\s+history[:\s]*(.*?)(?:\n\n|\n[A-Z]|$)',
                r'career\s+history[:\s]*(.*?)(?:\n\n|\n[A-Z]|$)',
                r'job\s+history[:\s]*(.*?)(?:\n\n|\n[A-Z]|$)'
            ]
            
            for pattern in work_sections:
                matches = re.findall(pattern, text, re.IGNORECASE | re.DOTALL)
                for match in matches:
                    section_text = match.lower()
                    for skill in self.skill_database:
                        if skill.lower() in section_text and skill not in skills:
                            skills.append(skill)
            
            # Extract skills from projects section
            project_sections = [
                r'projects?[:\s]*(.*?)(?:\n\n|\n[A-Z]|$)',
                r'personal\s+projects?[:\s]*(.*?)(?:\n\n|\n[A-Z]|$)',
                r'academic\s+projects?[:\s]*(.*?)(?:\n\n|\n[A-Z]|$)',
                r'professional\s+projects?[:\s]*(.*?)(?:\n\n|\n[A-Z]|$)'
            ]
            
            for pattern in project_sections:
                matches = re.findall(pattern, text, re.IGNORECASE | re.DOTALL)
                for match in matches:
                    section_text = match.lower()
                    for skill in self.skill_database:
                        if skill.lower() in section_text and skill not in skills:
                            skills.append(skill)
            
            # Remove duplicates and limit results
            skills = list(set(skills))
            skills = skills[:25]  # Limit to top 25 skills
            
            return skills
            
        except Exception as e:
            logger.error(f"❌ Skills extraction error: {e}")
            return []
    
    def _extract_experience_ai(self, text: str) -> Dict[str, Any]:
        """Extract experience using AI models"""
        try:
            text_lower = text.lower()
            experience_years = 0
            
            # Enhanced pattern-based extraction
            enhanced_patterns = [
                r'(\d+)\s*(?:to|-)?\s*(\d+)?\s*(?:years?|yrs?)\s*(?:of\s*)?(?:experience|exp)',
                r'(?:experience|exp)[:\s]*(\d+)\s*(?:to|-)?\s*(\d+)?\s*(?:years?|yrs?)',
                r'(\d+)\+?\s*(?:years?|yrs?)\s*(?:of\s*)?(?:experience|exp)',
                r'(?:total|overall)\s*(?:experience|exp)[:\s]*(\d+)\s*(?:years?|yrs?)',
                r'(\d+)\s*(?:to|-)?\s*(\d+)?\s*(?:years?|yrs?)\s*(?:of\s*)?(?:work|professional)',
                r'(?:work|professional)\s*(?:experience|exp)[:\s]*(\d+)\s*(?:to|-)?\s*(\d+)?\s*(?:years?|yrs?)',
                r'(\d+)\s*(?:to|-)?\s*(\d+)?\s*(?:years?|yrs?)\s*(?:in\s*)?(?:software|development|engineering)',
                r'(?:software|development|engineering)\s*(?:experience|exp)[:\s]*(\d+)\s*(?:to|-)?\s*(\d+)?\s*(?:years?|yrs?)',
                r'(?:since|from)\s+\d{4}.*?(?:years?|yrs?)',
                r'(?:over|more\s+than)\s+(\d+)\s*(?:years?|yrs?)',
                r'(\d+)\s*(?:years?|yrs?)\s*(?:plus|and\s+above)'
            ]
            
            for pattern in enhanced_patterns:
                matches = re.findall(pattern, text_lower)
                for match in matches:
                    if isinstance(match, tuple):
                        years = int(match[0]) if match[0] else 0
                        if match[1]:
                            years = max(years, int(match[1]))
                    else:
                        years = int(match)
                    
                    if 0 < years <= 30:
                        experience_years = years
                        break
                if experience_years > 0:
                    break
            
            # Date-based calculation
            if experience_years == 0:
                experience_years = self._calculate_experience_from_dates(text)
            
            # Job title indicators
            if experience_years == 0:
                experience_indicators = {
                    'senior': 5, 'lead': 6, 'principal': 8, 'staff': 7, 'architect': 8,
                    'manager': 5, 'director': 8, 'vp': 10, 'cto': 12, 'head': 6,
                    'junior': 1, 'associate': 2, 'entry': 0, 'fresher': 0, 'intern': 0,
                    'trainee': 0, 'graduate': 0, 'new grad': 0, 'student': 0
                }
                
                for indicator, years in experience_indicators.items():
                    if indicator in text_lower:
                        experience_years = years
                        break
            
            return {
                'total_years': experience_years,
                'total_months': experience_years * 12,
                'display': f"{experience_years} years" if experience_years > 0 else "Experience not found"
            }
            
        except Exception as e:
            logger.error(f"❌ Experience extraction error: {e}")
            return {'total_years': 0, 'total_months': 0, 'display': 'Experience extraction error'}
    
    def _calculate_experience_from_dates(self, text: str) -> int:
        """Calculate experience from work history dates"""
        try:
            date_patterns = [
                r'(\d{4})\s*(?:to|-)?\s*(?:present|current|now|\d{4})',
                r'(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)\s+\d{4}\s*(?:to|-)?\s*(?:present|current|now|(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)\s+\d{4})',
                r'\d{1,2}/\d{4}\s*(?:to|-)?\s*(?:present|current|now|\d{1,2}/\d{4})',
                r'\d{1,2}-\d{4}\s*(?:to|-)?\s*(?:present|current|now|\d{1,2}-\d{4})',
                r'(?:since|from)\s+(\d{4})',
                r'(?:started|began)\s+(?:in\s+)?(\d{4})',
                r'(?:joined|employed)\s+(?:in\s+)?(\d{4})'
            ]
            
            dates = []
            for pattern in date_patterns:
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
                        # If no end date, assume current year
                        if len(years) == 1:
                            years.append(current_year)
                        return max(years) - min(years)
                except:
                    pass
            
            return 0
            
        except Exception as e:
            logger.error(f"❌ Date calculation error: {e}")
            return 0
    
    def _calculate_confidence(self, name: str, email: str, phone: str, skills: List[str], experience: Dict, role: str) -> float:
        """Calculate extraction confidence score"""
        try:
            confidence = 0.0
            
            # Name confidence
            if name and name not in ['Name not found', 'Name extraction error']:
                confidence += 0.2
            
            # Email confidence
            if email and email not in ['Email not found', 'Email extraction error']:
                confidence += 0.2
            
            # Phone confidence
            if phone and phone not in ['Phone not found', 'Phone extraction error']:
                confidence += 0.2
            
            # Skills confidence
            if skills and len(skills) > 0:
                confidence += min(0.3, len(skills) * 0.01)
            
            # Experience confidence
            if experience and experience.get('total_years', 0) > 0:
                confidence += 0.1
            
            # Role confidence
            if role and role not in ['Role not found', 'Role extraction error']:
                confidence += 0.1
            
            return min(1.0, confidence)
            
        except Exception as e:
            logger.error(f"❌ Confidence calculation error: {e}")
            return 0.5
    
    def _get_empty_extraction(self) -> Dict[str, Any]:
        """Return empty extraction result"""
        return {
            'name': 'No text found',
            'email': 'No text found',
            'phone': 'No text found',
            'skills': [],
            'experience': {'total_years': 0, 'total_months': 0, 'display': 'No text found'},
            'role': 'No text found',
            'location': 'No text found',
            'education': [],
            'raw_text': '',
            'extraction_method': 'no_text',
            'confidence_score': 0.0,
            'extraction_timestamp': datetime.now().isoformat()
        }

# Initialize global AI extractor instance
ai_extractor = AIResumeExtractor()
