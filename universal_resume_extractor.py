"""
Universal Resume Extractor
Handles ALL possible resume formats with advanced pattern recognition
"""

import re
import logging
import os
import io
from datetime import datetime
from typing import Dict, List, Any, Tuple, Optional
import json
from dateutil.relativedelta import relativedelta
import PyPDF2
import docx

logger = logging.getLogger(__name__)

class UniversalResumeExtractor:
    """Universal resume extractor that handles all possible formats"""
    
    def __init__(self):
        self.initialize_patterns()
        self.initialize_databases()
        
    def initialize_patterns(self):
        """Initialize all extraction patterns"""
        
        # NAME PATTERNS - Handle all possible name formats
        self.name_patterns = [
            # Direct name patterns
            r'^([A-Z][a-z]+ [A-Z][a-z]+(?: [A-Z][a-z]+)?)',  # First Last (Middle)
            r'^([A-Z][A-Z]+ [A-Z][A-Z]+)',  # FIRST LAST
            r'^([A-Z][a-z]+ [A-Z]\. [A-Z][a-z]+)',  # First M. Last
            
            # Labeled patterns
            r'(?:Name|Full Name|Candidate Name|Applicant Name)[:\s]*([A-Z][a-z]+ [A-Z][a-z]+(?: [A-Z][a-z]+)?)',
            r'(?:Name|Full Name|Candidate Name|Applicant Name)[:\s]*([A-Z][A-Z]+ [A-Z][A-Z]+)',
            
            # Header patterns
            r'^([A-Z][a-z]+ [A-Z][a-z]+)\s*\n\s*(?:Email|Phone|Contact|Address)',
            r'^([A-Z][A-Z]+ [A-Z][A-Z]+)\s*\n\s*(?:Email|Phone|Contact|Address)',
            
            # Contact section patterns
            r'(?:Contact Information|Personal Information|About)[:\s]*\n\s*([A-Z][a-z]+ [A-Z][a-z]+)',
            
            # Resume header patterns
            r'^([A-Z][a-z]+ [A-Z][a-z]+)\s*\n\s*(?:Software Engineer|Developer|Analyst|Manager)',
            r'^([A-Z][A-Z]+ [A-Z][A-Z]+)\s*\n\s*(?:SOFTWARE ENGINEER|DEVELOPER|ANALYST|MANAGER)',
        ]
        
        # EMAIL PATTERNS - Comprehensive email detection
        self.email_patterns = [
            r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',  # Standard email
            r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}',  # Without word boundaries
            r'(?:Email|E-mail|Mail|Contact)[:\s]*([A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,})',
            r'(?:Email|E-mail|Mail|Contact)[:\s]*([A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,})',
        ]
        
        # PHONE PATTERNS - All possible phone formats
        self.phone_patterns = [
            # Indian formats
            r'\b(?:\+91[-.\s]?)?[6-9]\d{9}\b',  # +91-9876543210, 9876543210
            r'\b(?:\+91[-.\s]?)?[6-9]\d{2}[-.\s]?\d{3}[-.\s]?\d{4}\b',  # +91-987-654-3210
            
            # International formats
            r'\b(?:\+1[-.\s]?)?\(?[0-9]{3}\)?[-.\s]?[0-9]{3}[-.\s]?[0-9]{4}\b',  # US format
            r'\b(?:\+44[-.\s]?)?[0-9]{2,4}[-.\s]?[0-9]{3,4}[-.\s]?[0-9]{3,4}\b',  # UK format
            
            # Generic formats
            r'\b\d{10,15}\b',  # 10-15 digits
            r'\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b',  # XXX-XXX-XXXX
            r'\b\d{4}[-.\s]?\d{3}[-.\s]?\d{3}\b',  # XXXX-XXX-XXX
            
            # Labeled patterns
            r'(?:Phone|Mobile|Cell|Tel|Telephone)[:\s]*([+]?[\d\s\-\(\)]{10,})',
            r'(?:Phone|Mobile|Cell|Tel|Telephone)[:\s]*([+]?[\d\s\-\(\)\.]{10,})',
        ]
        
        # ROLE PATTERNS - Comprehensive role detection
        self.role_patterns = [
            # Direct role statements
            r'(?:Position|Title|Role|Job Title|Designation|Current Role|Professional Title)[:\s]*([A-Za-z\s]{3,50})',
            r'(?:Working as|Currently|Role)[:\s]*([A-Za-z\s]{3,50})',
            r'(?:I am|I\'m)[:\s]*([A-Za-z\s]{3,50})',
            r'(?:As a|Being a)[:\s]*([A-Za-z\s]{3,50})',
            
            # Job title patterns
            r'(?:Software Engineer|Developer|Analyst|Manager|Consultant|Specialist|Architect|Lead|Senior|Junior|Principal|Staff)',
            r'(?:Full Stack|Frontend|Backend|Mobile|Web|Data|Cloud|Security|DevOps|QA|UI|UX|Machine Learning|AI)',
            
            # Experience section patterns
            r'(?:Experience|Work Experience|Professional Experience|Employment)[:\s]*\n\s*([A-Za-z\s]{3,50})',
            r'(?:Current Position|Present Role|Current Job)[:\s]*([A-Za-z\s]{3,50})',
            
            # Objective/Summary patterns
            r'(?:Objective|Summary|Profile|About)[:\s]*\n\s*([A-Za-z\s]{3,100})',
        ]
        
        # EXPERIENCE PATTERNS - All possible date formats
        self.experience_patterns = [
            # YYYY-YYYY formats
            r'(\d{4})\s*[-–—]\s*(\d{4})',  # 2020-2024, 2020 – 2024, 2020—2024
            r'(\d{4})\s*to\s*(\d{4})',     # 2020 to 2024
            r'(\d{4})\s*-\s*(\d{4})',      # 2020 - 2024
            
            # Month-Year formats
            r'([A-Za-z]{3,9})\s*(\d{4})\s*[-–—]\s*([A-Za-z]{3,9})\s*(\d{4})',  # Jan 2020 - Dec 2024
            r'([A-Za-z]{3,9})\s*(\d{4})\s*to\s*([A-Za-z]{3,9})\s*(\d{4})',     # Jan 2020 to Dec 2024
            r'(\d{1,2})[/-](\d{4})\s*[-–—]\s*(\d{1,2})[/-](\d{4})',            # 01/2020 - 12/2024
            
            # Present/Current patterns
            r'(\d{4})\s*[-–—]\s*(?:present|current|till\s+date|till\s+now|ongoing)',    # 2020 - Present
            r'([A-Za-z]{3,9})\s*(\d{4})\s*[-–—]\s*(?:present|current|till\s+date|till\s+now|ongoing)',  # Jan 2020 - Present
            r'(\d{1,2})[/-](\d{4})\s*[-–—]\s*(?:present|current|till\s+date|till\s+now|ongoing)',       # 01/2020 - Present
            
            # Direct experience statements
            r'(?:total|overall|total\s+work)\s*(?:experience|exp)[:\s]*(\d+(?:\.\d+)?)\s*(?:to|-)?\s*(\d+(?:\.\d+)?)?\s*(?:years?|yrs?)',
            r'(?:experience|exp)[:\s]*(\d+(?:\.\d+)?)\s*(?:to|-)?\s*(\d+(?:\.\d+)?)?\s*(?:years?|yrs?)',
            r'(\d+(?:\.\d+)?)\s*(?:to|-)?\s*(\d+(?:\.\d+)?)?\s*(?:years?|yrs?)\s*(?:of\s*)?(?:experience|exp)',
            
            # Fresher patterns
            r'(?:fresher|fresh graduate|recent graduate|new graduate|entry level|junior|trainee|intern|no experience|zero experience)',
        ]
        
        # SKILL PATTERNS - Comprehensive skill detection
        self.skill_patterns = [
            # Technical skills section
            r'(?:Technical Skills|Skills|Technologies|Programming Languages|Tools|Frameworks)[:\s]*\n\s*([A-Za-z\s,\.\-\+\(\)\/]+)',
            r'(?:Technical Skills|Skills|Technologies|Programming Languages|Tools|Frameworks)[:\s]*([A-Za-z\s,\.\-\+\(\)\/]+)',
            
            # Categorized skills
            r'(?:Languages|Programming)[:\s]*([A-Za-z\s,\.\-\+\(\)\/]+)',
            r'(?:Frameworks|Libraries)[:\s]*([A-Za-z\s,\.\-\+\(\)\/]+)',
            r'(?:Databases|Database)[:\s]*([A-Za-z\s,\.\-\+\(\)\/]+)',
            r'(?:Tools|Software)[:\s]*([A-Za-z\s,\.\-\+\(\)\/]+)',
            r'(?:Cloud|Platforms)[:\s]*([A-Za-z\s,\.\-\+\(\)\/]+)',
            
            # Inline skills
            r'(?:Proficient in|Experienced with|Knowledge of|Familiar with)[:\s]*([A-Za-z\s,\.\-\+\(\)\/]+)',
            r'(?:Expertise in|Specialized in|Skilled in)[:\s]*([A-Za-z\s,\.\-\+\(\)\/]+)',
            
            # Bullet point skills
            r'[•\-\*]\s*([A-Za-z\s,\.\-\+\(\)\/]+(?:Java|Python|JavaScript|React|Angular|Node|Spring|Django|Flask|MySQL|MongoDB|AWS|Azure|Docker|Kubernetes)[A-Za-z\s,\.\-\+\(\)\/]*)',
        ]
        
        # LOCATION PATTERNS - Comprehensive location detection
        self.location_patterns = [
            # Labeled patterns
            r'(?:Location|Address|City|Based in|Located in|From|Residing in|Living in|Current Location|Present Location|Work Location|Office Location)[:\s]*([A-Za-z\s,]{3,50})',
            
            # Indian cities
            r'\b(?:Mumbai|Delhi|Bangalore|Hyderabad|Chennai|Kolkata|Pune|Ahmedabad|Jaipur|Surat|Lucknow|Kanpur|Nagpur|Indore|Thane|Bhopal|Visakhapatnam|Patna|Vadodara|Ludhiana|Agra|Nashik|Faridabad|Meerut|Rajkot|Kalyan|Vasai|Varanasi|Srinagar|Aurangabad|Navi Mumbai|Solapur|Vijayawada|Kolhapur|Amritsar|Noida|Ranchi|Howrah|Coimbatore|Raipur|Jabalpur|Gwalior|Chandigarh|Tiruchirappalli|Mysore|Bhilai|Kochi|Bhavnagar|Salem|Warangal|Guntur|Bhubaneswar|Mira|Tiruppur|Amravati|Nanded)\b',
            
            # International cities
            r'\b(?:New York|Los Angeles|Chicago|Houston|Phoenix|Philadelphia|San Antonio|San Diego|Dallas|San Jose|Austin|Jacksonville|Fort Worth|Columbus|Charlotte|San Francisco|Indianapolis|Seattle|Denver|Washington|Boston|El Paso|Nashville|Detroit|Oklahoma City|Portland|Las Vegas|Memphis|Louisville|Baltimore|Milwaukee|Albuquerque|Tucson|Fresno|Sacramento|Kansas City|Mesa|Atlanta|Colorado Springs|Raleigh|Omaha|Miami|Oakland|Minneapolis|Tulsa|Cleveland|Wichita|Arlington|New Orleans|Honolulu|Anaheim|Santa Ana|Corpus Christi|Riverside|Lexington|Henderson|Stockton|Saint Paul|Cincinnati|St. Louis|Pittsburgh|Anchorage|Plano|Orlando|Irvine|Newark|Durham|Chula Vista|Fort Wayne|Jersey City|St. Petersburg|Laredo|Madison|Chandler|Buffalo|Lubbock|Scottsdale|Reno|Glendale|Gilbert|Winston-Salem|North Las Vegas|Norfolk|Chesapeake|Garland|Irving|Hialeah|Fremont|Boise|Richmond|Baton Rouge|Spokane|Des Moines|Modesto|Fayetteville|Tacoma|Oxnard|Fontana|Columbus|Montgomery|Moreno Valley|Shreveport|Aurora|Yonkers|Akron|Huntington Beach|Little Rock|Augusta|Amarillo|Glendale|Mobile|Grand Rapids|Salt Lake City|Tallahassee|Huntsville|Grand Prairie|Knoxville|Worcester|Newport News|Brownsville|Overland Park|Santa Clarita|Providence|Garden Grove|Chattanooga|Oceanside|Jackson|Fort Lauderdale|Santa Rosa|Rancho Cucamonga|Port St. Lucie|Tempe|Ontario|Vancouver|Cape Coral|Sioux Falls|Springfield|Peoria|Pembroke Pines|Elk Grove|Salem|Lancaster|Corona|Eugene|Palmdale|Salinas|Springfield|Pasadena|Fort Collins|Hayward|Pomona|Cary|Rockford|Alexandria|Escondido|McKinney|Kansas City|Joliet|Sunnyvale|Torrance|Bridgeport|Lakewood|Hollywood|Paterson|Naperville|Syracuse|Mesquite|Dayton|Savannah|Clarksville|Orange|Pasadena|Fullerton|Killeen|Frisco|Hampton|McAllen|Warren|Bellevue|West Valley City|Columbia|Olathe|Sterling Heights|New Haven|Miramar|Waco|Thousand Oaks|Cedar Rapids|Charleston|Sioux City|Round Rock|Fargo|Carrollton|Roseville|Gainesville|Coral Springs|Columbia|Sterling Heights|New Haven|Miramar|Waco|Thousand Oaks|Cedar Rapids|Charleston|Sioux City|Round Rock|Fargo|Carrollton|Roseville|Gainesville|Coral Springs)\b',
        ]
        
    def initialize_databases(self):
        """Initialize comprehensive databases"""
        
        # Comprehensive skills database
        self.skills_database = {
            'programming_languages': [
                'java', 'python', 'javascript', 'typescript', 'c++', 'c#', 'go', 'rust', 'kotlin', 'swift',
                'php', 'ruby', 'scala', 'r', 'matlab', 'perl', 'shell', 'bash', 'powershell', 'sql', 'pl/sql',
                't-sql', 'objective-c', 'dart', 'lua', 'haskell', 'clojure', 'erlang', 'elixir', 'crystal',
                'nim', 'zig', 'odin', 'v', 'julia', 'fortran', 'cobol', 'pascal', 'ada', 'lisp', 'prolog'
            ],
            'web_frontend': [
                'html', 'css', 'react', 'angular', 'vue', 'ember', 'backbone', 'jquery', 'bootstrap', 'sass',
                'less', 'stylus', 'webpack', 'babel', 'eslint', 'prettier', 'gulp', 'grunt', 'npm', 'yarn',
                'pnpm', 'vite', 'parcel', 'rollup', 'tailwind', 'material-ui', 'ant design', 'chakra ui',
                'semantic ui', 'bulma', 'foundation', 'materialize', 'pure css', 'milligram', 'spectre'
            ],
            'web_backend': [
                'node.js', 'express', 'django', 'flask', 'fastapi', 'spring', 'spring boot', 'hibernate', 'jpa',
                'laravel', 'symfony', 'rails', 'asp.net', 'dotnet', 'rest api', 'graphql', 'microservices',
                'serverless', 'koa', 'sails', 'meteor', 'feathers', 'loopback', 'strapi', 'ghost', 'keystone',
                'adonis', 'nest', 'nuxt', 'next', 'gatsby', 'svelte', 'astro', 'remix', 'solid'
            ],
            'databases': [
                'mysql', 'postgresql', 'mongodb', 'redis', 'elasticsearch', 'cassandra', 'dynamodb', 'oracle',
                'sqlite', 'firebase', 'neo4j', 'couchdb', 'mariadb', 'sql server', 'db2', 'teradata',
                'influxdb', 'timescaledb', 'cockroachdb', 'planetscale', 'supabase', 'fauna', 'realm',
                'couchbase', 'ravendb', 'documentdb', 'cosmos db', 'bigtable', 'spanner', 'firestore'
            ],
            'cloud_platforms': [
                'aws', 'azure', 'gcp', 'google cloud', 'docker', 'kubernetes', 'terraform', 'ansible', 'chef',
                'puppet', 'jenkins', 'gitlab ci', 'github actions', 'cloudformation', 'serverless', 'lambda',
                'ec2', 's3', 'rds', 'vpc', 'iam', 'cloudwatch', 'route53', 'elb', 'auto scaling', 'ebs',
                'efs', 'cloudfront', 'api gateway', 'dynamodb', 'redshift', 'emr', 'glue', 'athena',
                'kinesis', 'sqs', 'sns', 'ses', 'cognito', 'amplify', 'appsync', 'step functions'
            ],
            'mobile_development': [
                'android', 'ios', 'react native', 'flutter', 'xamarin', 'ionic', 'cordova', 'phonegap',
                'swift', 'kotlin', 'objective-c', 'java android', 'swift ios', 'dart', 'c#', 'f#',
                'unity', 'unreal', 'godot', 'corona', 'lua', 'cocos2d', 'spritekit', 'scenekit'
            ],
            'ai_ml': [
                'tensorflow', 'pytorch', 'keras', 'scikit-learn', 'pandas', 'numpy', 'opencv', 'nltk',
                'spacy', 'transformers', 'hugging face', 'mlflow', 'jupyter', 'matplotlib', 'seaborn',
                'plotly', 'bokeh', 'dash', 'streamlit', 'gradio', 'fastai', 'lightgbm', 'xgboost',
                'catboost', 'prophet', 'statsmodels', 'scipy', 'sympy', 'networkx', 'gensim', 'textblob'
            ],
            'devops_tools': [
                'git', 'github', 'gitlab', 'bitbucket', 'jenkins', 'travis ci', 'circleci', 'bamboo',
                'teamcity', 'azure devops', 'aws codepipeline', 'google cloud build', 'docker', 'kubernetes',
                'helm', 'prometheus', 'grafana', 'kibana', 'splunk', 'new relic', 'datadog', 'sentry',
                'logstash', 'fluentd', 'fluentbit', 'jaeger', 'zipkin', 'consul', 'vault', 'nomad'
            ],
            'testing_frameworks': [
                'selenium', 'cypress', 'jest', 'mocha', 'pytest', 'junit', 'testng', 'jasmine', 'karma',
                'protractor', 'playwright', 'appium', 'cucumber', 'bdd', 'tdd', 'unit testing',
                'integration testing', 'end-to-end testing', 'api testing', 'performance testing',
                'load testing', 'stress testing', 'security testing', 'penetration testing'
            ],
            'development_tools': [
                'maven', 'gradle', 'ant', 'npm', 'yarn', 'pip', 'conda', 'composer', 'intellij', 'eclipse',
                'vscode', 'vim', 'emacs', 'postman', 'insomnia', 'fiddler', 'wireshark', 'jira',
                'confluence', 'slack', 'teams', 'discord', 'zoom', 'figma', 'sketch', 'adobe xd',
                'invision', 'zeplin', 'principle', 'framer', 'webflow', 'bubble', 'airtable', 'notion'
            ]
        }
        
        # Month name mappings
        self.month_names = {
            'january': 1, 'jan': 1, '01': 1, '1': 1,
            'february': 2, 'feb': 2, '02': 2, '2': 2,
            'march': 3, 'mar': 3, '03': 3, '3': 3,
            'april': 4, 'apr': 4, '04': 4, '4': 4,
            'may': 5, '05': 5, '5': 5,
            'june': 6, 'jun': 6, '06': 6, '6': 6,
            'july': 7, 'jul': 7, '07': 7, '7': 7,
            'august': 8, 'aug': 8, '08': 8, '8': 8,
            'september': 9, 'sep': 9, 'sept': 9, '09': 9, '9': 9,
            'october': 10, 'oct': 10, '10': 10,
            'november': 11, 'nov': 11, '11': 11,
            'december': 12, 'dec': 12, '12': 12
        }
        
        # Fresher keywords
        self.fresher_keywords = [
            'fresher', 'fresh graduate', 'recent graduate', 'new graduate', 'entry level',
            'junior', 'trainee', 'intern', 'internship', 'no experience', 'zero experience',
            'beginner', 'starter', 'newbie', 'rookie', 'novice', 'apprentice', 'student',
            'undergraduate', 'graduate', 'postgraduate', 'phd', 'masters', 'bachelors'
        ]
        
    def extract_resume_data_from_file(self, file_path: str) -> Dict[str, Any]:
        """Extract resume data from file path"""
        try:
            logger.info(f"📄 Extracting resume data from file: {file_path}")
            
            # Read file content
            with open(file_path, 'rb') as file:
                file_content = file.read()
            
            # Extract text
            filename = os.path.basename(file_path)
            text = self.extract_text_from_file(file_content, filename)
            
            if not text:
                logger.error(f"❌ No text extracted from file: {file_path}")
                return {}
            
            # Extract resume data from text
            resume_data = self.extract_resume_data(text, filename)
            logger.info("✅ Resume data extraction completed")
            return resume_data
            
        except Exception as e:
            logger.error(f"❌ Resume data extraction error: {e}")
            return {}
    
    def extract_text_from_file(self, file_content: bytes, filename: str) -> str:
        """Extract text from uploaded file"""
        try:
            logger.info(f"📄 Extracting text from file: {filename}")
            
            if filename.lower().endswith('.pdf'):
                return self._extract_from_pdf(file_content)
            elif filename.lower().endswith('.docx'):
                return self._extract_from_docx(file_content)
            elif filename.lower().endswith('.txt'):
                return self._extract_from_txt(file_content)
            else:
                logger.error(f"❌ Unsupported file format: {filename}")
                return ""
                
        except Exception as e:
            logger.error(f"❌ Text extraction error: {e}")
            return ""
    
    def _extract_from_pdf(self, file_content: bytes) -> str:
        """Extract text from PDF"""
        try:
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(file_content))
            text = ""
            
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            
            return text.strip()
        except Exception as e:
            logger.error(f"❌ PDF extraction error: {e}")
            return ""
    
    def _extract_from_docx(self, file_content: bytes) -> str:
        """Extract text from DOCX"""
        try:
            doc = docx.Document(io.BytesIO(file_content))
            text = ""
            
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            
            return text.strip()
        except Exception as e:
            logger.error(f"❌ DOCX extraction error: {e}")
            return ""
    
    def _extract_from_txt(self, file_content: bytes) -> str:
        """Extract text from TXT"""
        try:
            return file_content.decode('utf-8').strip()
        except Exception as e:
            logger.error(f"❌ TXT extraction error: {e}")
            return ""

    def extract_resume_data(self, text: str, filename: str = None) -> Dict[str, Any]:
        """Extract all resume data using universal patterns"""
        try:
            logger.info("🚀 Starting universal resume extraction...")
            
            if not text or len(text.strip()) < 10:
                return self._get_empty_result()
            
            # Clean and normalize text
            text_clean = self._clean_text(text)
            
            # Extract all components
            name = self._extract_name_universal(text_clean, filename)
            email = self._extract_email_universal(text_clean)
            phone = self._extract_phone_universal(text_clean)
            role = self._extract_role_universal(text_clean, name)
            location = self._extract_location_universal(text_clean, name)
            experience = self._extract_experience_universal(text_clean)
            skills = self._extract_skills_universal(text_clean)
            education = self._extract_education_universal(text_clean)
            
            # Calculate confidence score
            confidence = self._calculate_confidence(name, email, phone, skills, experience, role)
            
            result = {
                'name': name,
                'email': email,
                'phone': phone,
                'location': location,
                'experience': experience,
                'role': role,
                'skills': skills,
                'education': education,
                'raw_text': text_clean[:1000] + "..." if len(text_clean) > 1000 else text_clean,
                'extraction_method': 'universal_extraction',
                'confidence_score': confidence,
                'extraction_timestamp': datetime.now().isoformat()
            }
            
            logger.info("✅ Universal resume extraction completed")
            logger.info(f"👤 Name: {name}")
            logger.info(f"📧 Email: {email}")
            logger.info(f"📱 Phone: {phone}")
            logger.info(f"🎯 Role: {role}")
            logger.info(f"📍 Location: {location}")
            logger.info(f"⏰ Experience: {experience.get('display', 'N/A')}")
            logger.info(f"🛠️ Skills: {len(skills)} skills found")
            
            return result
            
        except Exception as e:
            logger.error(f"❌ Universal resume extraction error: {e}")
            return self._get_empty_result()
    
    def _extract_name_universal(self, text: str, filename: str = None) -> str:
        """Extract name using all possible patterns"""
        try:
            lines = text.split('\n')
            
            # Try all name patterns
            for pattern in self.name_patterns:
                matches = re.findall(pattern, text, re.IGNORECASE | re.MULTILINE)
                if matches:
                    name = matches[0].strip()
                    if self._is_valid_name(name):
                        logger.info(f"✅ Name extracted with pattern: {name}")
                        return name
            
            # Fallback: first line if it looks like a name
            if lines:
                first_line = lines[0].strip()
                if self._is_valid_name(first_line):
                    logger.info(f"✅ Name extracted from first line: {first_line}")
                    return first_line
            
            # Fallback: filename if it contains a name
            if filename:
                name_from_file = self._extract_name_from_filename(filename)
                if name_from_file:
                    logger.info(f"✅ Name extracted from filename: {name_from_file}")
                    return name_from_file
            
            return 'Name not found'
            
        except Exception as e:
            logger.error(f"❌ Name extraction error: {e}")
            return 'Name not found'
    
    def _extract_email_universal(self, text: str) -> str:
        """Extract email using all possible patterns"""
        try:
            for pattern in self.email_patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                if matches:
                    email = matches[0].strip()
                    if self._is_valid_email(email):
                        logger.info(f"✅ Email extracted: {email}")
                        return email
            
            return 'Email not found'
            
        except Exception as e:
            logger.error(f"❌ Email extraction error: {e}")
            return 'Email not found'
    
    def _extract_phone_universal(self, text: str) -> str:
        """Extract phone using all possible patterns"""
        try:
            for pattern in self.phone_patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                if matches:
                    phone = matches[0].strip()
                    if self._is_valid_phone(phone):
                        logger.info(f"✅ Phone extracted: {phone}")
                        return phone
            
            return 'Phone not found'
            
        except Exception as e:
            logger.error(f"❌ Phone extraction error: {e}")
            return 'Phone not found'
    
    def _extract_role_universal(self, text: str, name: str = None) -> str:
        """Extract role using all possible patterns"""
        try:
            # Remove name from text to avoid false matches
            text_for_role = text
            if name:
                text_for_role = text_for_role.replace(name, '')
            
            # Try all role patterns
            for pattern in self.role_patterns:
                matches = re.findall(pattern, text_for_role, re.IGNORECASE)
                if matches:
                    role = matches[0].strip()
                    if self._is_valid_role(role):
                        logger.info(f"✅ Role extracted: {role}")
                        return role.title()
            
            # Fallback: look for common job titles
            common_roles = [
                'software engineer', 'developer', 'programmer', 'analyst', 'manager',
                'consultant', 'specialist', 'architect', 'lead', 'senior', 'junior',
                'full stack developer', 'frontend developer', 'backend developer',
                'web developer', 'mobile developer', 'data scientist', 'data analyst'
            ]
            
            text_lower = text_for_role.lower()
            for role in common_roles:
                if role in text_lower:
                    logger.info(f"✅ Role found in text: {role}")
                    return role.title()
            
            return 'Role not found'
            
        except Exception as e:
            logger.error(f"❌ Role extraction error: {e}")
            return 'Role not found'
    
    def _extract_location_universal(self, text: str, name: str = None) -> str:
        """Extract location using all possible patterns"""
        try:
            # Try all location patterns
            for pattern in self.location_patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                if matches:
                    location = matches[0].strip()
                    if self._is_valid_location(location):
                        logger.info(f"✅ Location extracted: {location}")
                        return location
            
            return 'Location not found'
            
        except Exception as e:
            logger.error(f"❌ Location extraction error: {e}")
            return 'Location not found'
    
    def _extract_experience_universal(self, text: str) -> Dict[str, Any]:
        """Extract experience using all possible patterns"""
        try:
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
                'extraction_method': 'universal_extraction'
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
    
    def _extract_skills_universal(self, text: str) -> List[str]:
        """Extract skills using all possible patterns"""
        try:
            skills = set()
            
            # Try all skill patterns
            for pattern in self.skill_patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                for match in matches:
                    if isinstance(match, tuple):
                        match = ' '.join(match)
                    extracted_skills = self._parse_skills_from_text(match)
                    skills.update(extracted_skills)
            
            # Also search for skills directly in text
            text_lower = text.lower()
            for category, category_skills in self.skills_database.items():
                for skill in category_skills:
                    if skill.lower() in text_lower:
                        skills.add(skill.title())
            
            skills_list = list(skills)
            logger.info(f"✅ Skills extracted: {len(skills_list)} skills")
            return skills_list
            
        except Exception as e:
            logger.error(f"❌ Skills extraction error: {e}")
            return []
    
    def _extract_education_universal(self, text: str) -> List[Dict[str, Any]]:
        """Extract education information"""
        try:
            education = []
            
            # Education patterns
            education_patterns = [
                r'(?:Education|Academic|Qualifications|Degree)[:\s]*\n\s*([A-Za-z\s,\.\-\+\(\)\/]+)',
                r'(?:Bachelor|Master|PhD|Doctorate|Diploma|Certificate)[:\s]*([A-Za-z\s,\.\-\+\(\)\/]+)',
                r'(?:B\.?Tech|M\.?Tech|B\.?E|M\.?E|B\.?Sc|M\.?Sc|B\.?A|M\.?A)[:\s]*([A-Za-z\s,\.\-\+\(\)\/]+)',
            ]
            
            for pattern in education_patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                for match in matches:
                    education.append({
                        'degree': match.strip(),
                        'institution': 'Not specified',
                        'year': 'Not specified'
                    })
            
            logger.info(f"✅ Education extracted: {len(education)} entries")
            return education
            
        except Exception as e:
            logger.error(f"❌ Education extraction error: {e}")
            return []
    
    def _extract_experience_periods(self, text: str) -> List[Dict[str, Any]]:
        """Extract all experience periods from text"""
        periods = []
        
        try:
            # Try all experience patterns
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
                    'end_date': datetime(end_year, end_month, 28),
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
                total_months += max(0, months)
            
            return total_months
            
        except Exception as e:
            logger.error(f"❌ Error calculating total experience: {e}")
            return 0
    
    def _merge_overlapping_periods(self, periods: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Merge overlapping experience periods"""
        try:
            if not periods:
                return []
            
            sorted_periods = sorted(periods, key=lambda x: x['start_date'])
            merged = [sorted_periods[0]]
            
            for current in sorted_periods[1:]:
                last = merged[-1]
                
                if current['start_date'] <= last['end_date']:
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
    
    def _parse_skills_from_text(self, text: str) -> List[str]:
        """Parse skills from text string"""
        try:
            skills = []
            
            # Split by common separators
            separators = [',', ';', '|', '\n', '•', '-', '*']
            for sep in separators:
                if sep in text:
                    parts = text.split(sep)
                    for part in parts:
                        skill = part.strip()
                        if skill and len(skill) > 1:
                            skills.append(skill.title())
                    break
            
            # If no separators found, treat as single skill
            if not skills:
                skill = text.strip()
                if skill and len(skill) > 1:
                    skills.append(skill.title())
            
            return skills
            
        except Exception as e:
            logger.error(f"❌ Error parsing skills from text: {e}")
            return []
    
    def _is_valid_name(self, name: str) -> bool:
        """Check if extracted name is valid"""
        if not name or len(name.strip()) < 2:
            return False
        
        # Check if it contains only letters and spaces
        if not re.match(r'^[A-Za-z\s\.\-]+$', name):
            return False
        
        # Check if it's not too long
        if len(name) > 50:
            return False
        
        # Check if it's not a common false positive
        false_positives = [
            'resume', 'cv', 'curriculum vitae', 'personal information', 'contact information',
            'objective', 'summary', 'experience', 'education', 'skills', 'projects'
        ]
        
        name_lower = name.lower()
        for fp in false_positives:
            if fp in name_lower:
                return False
        
        return True
    
    def _is_valid_email(self, email: str) -> bool:
        """Check if extracted email is valid"""
        if not email or '@' not in email:
            return False
        
        # Basic email validation
        email_pattern = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$'
        return re.match(email_pattern, email) is not None
    
    def _is_valid_phone(self, phone: str) -> bool:
        """Check if extracted phone is valid"""
        if not phone:
            return False
        
        # Remove all non-digit characters
        digits_only = re.sub(r'\D', '', phone)
        
        # Check if it has reasonable length
        return 10 <= len(digits_only) <= 15
    
    def _is_valid_role(self, role: str) -> bool:
        """Check if extracted role is valid"""
        if not role or len(role.strip()) < 3:
            return False
        
        # Check if role contains job-related keywords
        job_keywords = [
            'developer', 'engineer', 'analyst', 'manager', 'designer', 'architect',
            'specialist', 'consultant', 'lead', 'senior', 'junior', 'associate',
            'intern', 'trainee', 'coordinator', 'supervisor', 'director', 'executive',
            'programmer', 'coder', 'technician', 'administrator', 'officer'
        ]
        
        role_lower = role.lower()
        return any(keyword in role_lower for keyword in job_keywords)
    
    def _is_valid_location(self, location: str) -> bool:
        """Check if extracted location is valid"""
        if not location or len(location.strip()) < 2:
            return False
        
        # Check if it's not too long
        if len(location) > 50:
            return False
        
        # Check if it contains reasonable characters
        if not re.match(r'^[A-Za-z\s,\.\-]+$', location):
            return False
        
        return True
    
    def _extract_name_from_filename(self, filename: str) -> str:
        """Extract name from filename"""
        try:
            # Remove file extension
            name = filename.replace('.pdf', '').replace('.docx', '').replace('.txt', '')
            
            # Remove common prefixes/suffixes
            name = re.sub(r'^(resume|cv|curriculum_vitae)_?', '', name, flags=re.IGNORECASE)
            name = re.sub(r'_\d+$', '', name)  # Remove timestamps
            
            # Check if it looks like a name
            if self._is_valid_name(name):
                return name
            
            return None
            
        except Exception as e:
            logger.error(f"❌ Error extracting name from filename: {e}")
            return None
    
    def _calculate_confidence(self, name: str, email: str, phone: str, skills: List[str], experience: Dict[str, Any], role: str) -> float:
        """Calculate extraction confidence score"""
        try:
            confidence = 0.0
            
            # Name confidence
            if name != 'Name not found':
                confidence += 0.2
            
            # Email confidence
            if email != 'Email not found':
                confidence += 0.2
            
            # Phone confidence
            if phone != 'Phone not found':
                confidence += 0.1
            
            # Role confidence
            if role != 'Role not found':
                confidence += 0.2
            
            # Skills confidence
            if len(skills) > 0:
                confidence += min(0.2, len(skills) * 0.02)
            
            # Experience confidence
            if experience.get('total_years', 0) > 0 or experience.get('is_fresher', False):
                confidence += 0.1
            
            return min(confidence, 1.0)
            
        except Exception as e:
            logger.error(f"❌ Error calculating confidence: {e}")
            return 0.5
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        try:
            # Remove extra whitespace
            text = re.sub(r'\s+', ' ', text.strip())
            
            # Remove special characters but keep basic punctuation
            text = re.sub(r'[^\w\s@\.\-\+\(\)\/]', ' ', text)
            
            # Normalize line breaks
            text = re.sub(r'\n+', '\n', text)
            
            return text
            
        except Exception as e:
            logger.error(f"❌ Error cleaning text: {e}")
            return text
    
    def _get_empty_result(self) -> Dict[str, Any]:
        """Return empty result"""
        return {
            'name': 'Name not found',
            'email': 'Email not found',
            'phone': 'Phone not found',
            'location': 'Location not found',
            'experience': {
                'total_years': 0,
                'total_months': 0,
                'display': 'Experience not found',
                'is_fresher': True,
                'experience_periods': [],
                'extraction_method': 'empty_result'
            },
            'role': 'Role not found',
            'skills': [],
            'education': [],
            'raw_text': '',
            'extraction_method': 'universal_extraction',
            'confidence_score': 0.0,
            'extraction_timestamp': datetime.now().isoformat()
        }

# Initialize global universal resume extractor
universal_resume_extractor = UniversalResumeExtractor()
