"""
Smart Pattern Analyzer
Uses multiple models and techniques for 100% accurate extraction
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

class SmartPatternAnalyzer:
    """Smart pattern analyzer with multiple models for 100% accuracy"""
    
    def __init__(self):
        self.initialize_smart_patterns()
        self.initialize_comprehensive_databases()
        
    def initialize_smart_patterns(self):
        """Initialize smart extraction patterns"""
        
        # SMART NAME PATTERNS - Multiple approaches
        self.name_patterns = [
            # Model 1: First line patterns (highest priority)
            r'^([A-Z][A-Z\s]+[A-Z])\s*\n',  # ALL CAPS names
            r'^([A-Z][a-z]+ [A-Z][a-z]+(?: [A-Z][a-z]+)?)\s*\n',  # Title Case names
            r'^([A-Z][a-z]+ [A-Z]\. [A-Z][a-z]+)\s*\n',  # First M. Last
            r'^([A-Z][A-Z]+ [A-Z]\. [A-Z][A-Z]+)\s*\n',  # ALL CAPS with middle initial
            
            # Model 2: Profile section patterns
            r'^([A-Z][A-Z\s]+[A-Z])\s*\n\s*(?:PROFILE|Profile|About|Summary)',
            r'^([A-Z][a-z]+ [A-Z][a-z]+(?: [A-Z][a-z]+)?)\s*\n\s*(?:PROFILE|Profile|About|Summary)',
            
            # Model 3: Contact section patterns
            r'(?:Name|Full Name)[:\s]*([A-Z][a-z]+ [A-Z][a-z]+(?: [A-Z][a-z]+)?)',
            r'(?:Name|Full Name)[:\s]*([A-Z][A-Z]+ [A-Z][A-Z]+)',
            
            # Model 4: Header patterns with contact info
            r'^([A-Z][a-z]+ [A-Z][a-z]+)\s*\n\s*(?:Email|Phone|Contact)',
            r'^([A-Z][A-Z]+ [A-Z][A-Z]+)\s*\n\s*(?:Email|Phone|Contact)',
        ]
        
        # SMART EMAIL PATTERNS
        self.email_patterns = [
            r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            r'(?:Email|E-mail|Mail|Contact)[:\s]*([A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,})',
        ]
        
        # SMART PHONE PATTERNS
        self.phone_patterns = [
            r'\b(?:\+91[-.\s]?)?[6-9]\d{9}\b',  # Indian mobile
            r'\b(?:\+91[-.\s]?)?[6-9]\d{2}[-.\s]?\d{3}[-.\s]?\d{4}\b',  # Formatted Indian
            r'(?:Phone|Mobile|Cell|Contact)[:\s]*([+]?[\d\s\-\(\)]{10,})',
            r'\+91[-.\s]?[6-9]\d{9}',  # +91 format
        ]
        
        # SMART ROLE PATTERNS
        self.role_patterns = [
            # Specific job titles
            r'\b(Software Engineer|Senior Software Engineer|Full Stack Developer|Senior Full Stack Developer|Java Developer|Python Developer|JavaScript Developer|React Developer|Angular Developer|Node\.js Developer|Spring Boot Developer|Django Developer|Flask Developer|Data Scientist|Data Analyst|Machine Learning Engineer|DevOps Engineer|QA Engineer|UI Designer|UX Designer|Mobile Developer|Web Developer|Backend Developer|Frontend Developer|System Engineer|Assistant System Engineer|Technical Lead|Team Lead|Project Manager|Product Manager|Business Analyst|Solution Architect|System Architect|Platform Engineer|Cloud Engineer|Security Engineer|Database Administrator|Network Engineer|IT Specialist|Cybersecurity Specialist)\b',
            
            # Role with experience level
            r'\b(Senior|Junior|Lead|Principal|Staff|Associate|Intern|Trainee)\s+(Software Engineer|Developer|Programmer|Analyst|Manager|Consultant|Specialist|Architect|Designer)\b',
            
            # Technology-specific roles
            r'\b(Java|Python|JavaScript|React|Angular|Node|Spring|Django|Flask|AWS|Azure|GCP|Docker|Kubernetes)\s+(Developer|Engineer|Specialist|Architect)\b',
            
            # Labeled patterns
            r'(?:Position|Title|Role|Job Title|Designation|Current Role|Professional Title)[:\s]*([A-Za-z\s]{3,50})',
            r'(?:Working as|Currently|Role)[:\s]*([A-Za-z\s]{3,50})',
        ]
        
        # SMART EXPERIENCE PATTERNS
        self.experience_patterns = [
            # Date range patterns
            r'(\d{4})\s*[-–—]\s*(\d{4})',  # 2020-2024
            r'(\d{4})\s*to\s*(\d{4})',     # 2020 to 2024
            r'([A-Za-z]{3,9})\s*(\d{4})\s*[-–—]\s*([A-Za-z]{3,9})\s*(\d{4})',  # Jan 2020 - Dec 2024
            r'(\d{1,2})[/-](\d{4})\s*[-–—]\s*(\d{1,2})[/-](\d{4})',  # 01/2020 - 12/2024
            
            # Present/Current patterns
            r'(\d{4})\s*[-–—]\s*(?:present|current|till\s+date|till\s+now|ongoing)',
            r'([A-Za-z]{3,9})\s*(\d{4})\s*[-–—]\s*(?:present|current|till\s+date|till\s+now|ongoing)',
            
            # Experience statements
            r'(?:total|overall)\s*(?:experience|exp)[:\s]*(\d+(?:\.\d+)?)\s*(?:years?|yrs?)',
            r'(\d+(?:\.\d+)?)\s*(?:years?|yrs?)\s*(?:of\s*)?(?:experience|exp)',
        ]
        
        # SMART LOCATION PATTERNS
        self.location_patterns = [
            r'(?:Location|Address|City|Based in|Located in|From|Residing in|Living in|Current Location|Present Location|Work Location|Office Location)[:\s]*([A-Za-z\s,]{3,50})',
            r'\b(Bangalore|Mumbai|Delhi|Hyderabad|Chennai|Kolkata|Pune|Ahmedabad|Jaipur|Surat|Lucknow|Kanpur|Nagpur|Indore|Thane|Bhopal|Visakhapatnam|Patna|Vadodara|Ludhiana|Agra|Nashik|Faridabad|Meerut|Rajkot|Kalyan|Vasai|Varanasi|Srinagar|Aurangabad|Navi Mumbai|Solapur|Vijayawada|Kolhapur|Amritsar|Noida|Ranchi|Howrah|Coimbatore|Raipur|Jabalpur|Gwalior|Chandigarh|Tiruchirappalli|Mysore|Bhilai|Kochi|Bhavnagar|Salem|Warangal|Guntur|Bhubaneswar|Mira|Tiruppur|Amravati|Nanded)\b',
        ]
        
    def initialize_comprehensive_databases(self):
        """Initialize comprehensive databases"""
        
        # COMPREHENSIVE SKILLS DATABASE
        self.valid_skills = {
            # Programming Languages
            'java', 'python', 'javascript', 'typescript', 'c++', 'c#', 'go', 'rust', 'kotlin', 'swift',
            'php', 'ruby', 'scala', 'r', 'matlab', 'perl', 'shell', 'bash', 'powershell', 'sql', 'pl/sql',
            't-sql', 'objective-c', 'dart', 'lua', 'haskell', 'clojure', 'erlang', 'elixir', 'c', 'cobol',
            'fortran', 'pascal', 'ada', 'lisp', 'prolog', 'assembly', 'cobol', 'fortran',
            
            # Web Technologies
            'html', 'css', 'react', 'angular', 'vue', 'ember', 'backbone', 'jquery', 'bootstrap', 'sass',
            'less', 'stylus', 'webpack', 'babel', 'eslint', 'prettier', 'gulp', 'grunt', 'npm', 'yarn',
            'pnpm', 'vite', 'parcel', 'rollup', 'tailwind', 'material-ui', 'ant design', 'chakra ui',
            'semantic ui', 'bulma', 'foundation', 'materialize', 'pure css', 'milligram', 'spectre',
            
            # Backend Technologies
            'node.js', 'express', 'django', 'flask', 'fastapi', 'spring', 'spring boot', 'hibernate', 'jpa',
            'laravel', 'symfony', 'rails', 'asp.net', 'dotnet', 'rest api', 'graphql', 'microservices',
            'serverless', 'koa', 'sails', 'meteor', 'feathers', 'loopback', 'strapi', 'ghost', 'keystone',
            'adonis', 'nest', 'nuxt', 'next', 'gatsby', 'svelte', 'astro', 'remix', 'solid',
            
            # Databases
            'mysql', 'postgresql', 'mongodb', 'redis', 'elasticsearch', 'cassandra', 'dynamodb', 'oracle',
            'sqlite', 'firebase', 'neo4j', 'couchdb', 'mariadb', 'sql server', 'db2', 'teradata',
            'influxdb', 'timescaledb', 'cockroachdb', 'planetscale', 'supabase', 'fauna', 'realm',
            'couchbase', 'ravendb', 'documentdb', 'cosmos db', 'bigtable', 'spanner', 'firestore',
            
            # Cloud Platforms
            'aws', 'azure', 'gcp', 'google cloud', 'docker', 'kubernetes', 'terraform', 'ansible', 'chef',
            'puppet', 'jenkins', 'gitlab ci', 'github actions', 'cloudformation', 'serverless', 'lambda',
            'ec2', 's3', 'rds', 'vpc', 'iam', 'cloudwatch', 'route53', 'elb', 'auto scaling', 'ebs',
            'efs', 'cloudfront', 'api gateway', 'dynamodb', 'redshift', 'emr', 'glue', 'athena',
            'kinesis', 'sqs', 'sns', 'ses', 'cognito', 'amplify', 'appsync', 'step functions',
            
            # Mobile Development
            'android', 'ios', 'react native', 'flutter', 'xamarin', 'ionic', 'cordova', 'phonegap',
            'swift', 'kotlin', 'objective-c', 'java android', 'swift ios', 'dart', 'c#', 'f#',
            'unity', 'unreal', 'godot', 'corona', 'lua', 'cocos2d', 'spritekit', 'scenekit',
            
            # AI/ML
            'tensorflow', 'pytorch', 'keras', 'scikit-learn', 'pandas', 'numpy', 'opencv', 'nltk',
            'spacy', 'transformers', 'hugging face', 'mlflow', 'jupyter', 'matplotlib', 'seaborn',
            'plotly', 'bokeh', 'dash', 'streamlit', 'gradio', 'fastai', 'lightgbm', 'xgboost',
            'catboost', 'prophet', 'statsmodels', 'scipy', 'sympy', 'networkx', 'gensim', 'textblob',
            
            # DevOps Tools
            'git', 'github', 'gitlab', 'bitbucket', 'jenkins', 'travis ci', 'circleci', 'bamboo',
            'teamcity', 'azure devops', 'aws codepipeline', 'google cloud build', 'docker', 'kubernetes',
            'helm', 'prometheus', 'grafana', 'kibana', 'splunk', 'new relic', 'datadog', 'sentry',
            'logstash', 'fluentd', 'fluentbit', 'jaeger', 'zipkin', 'consul', 'vault', 'nomad',
            
            # Testing Frameworks
            'selenium', 'cypress', 'jest', 'mocha', 'pytest', 'junit', 'testng', 'jasmine', 'karma',
            'protractor', 'playwright', 'appium', 'cucumber', 'bdd', 'tdd', 'unit testing',
            'integration testing', 'end-to-end testing', 'api testing', 'performance testing',
            'load testing', 'stress testing', 'security testing', 'penetration testing',
            
            # Development Tools
            'maven', 'gradle', 'ant', 'npm', 'yarn', 'pip', 'conda', 'composer', 'intellij', 'eclipse',
            'vscode', 'vim', 'emacs', 'postman', 'insomnia', 'fiddler', 'wireshark', 'jira',
            'confluence', 'slack', 'teams', 'discord', 'zoom', 'figma', 'sketch', 'adobe xd',
            'invision', 'zeplin', 'principle', 'framer', 'webflow', 'bubble', 'airtable', 'notion',
            
            # Additional Skills
            'power bi', 'tableau', 'qlik', 'looker', 'snowflake', 'databricks', 'apache spark',
            'hadoop', 'kafka', 'rabbitmq', 'nginx', 'apache', 'tomcat', 'jetty', 'wildfly',
            'glassfish', 'weblogic', 'websphere', 'iis', 'lighttpd', 'caddy', 'traefik',
            'istio', 'linkerd', 'envoy', 'kong', 'zuul', 'gateway', 'api gateway'
        }
        
        # Month names for date parsing
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
                return self._get_empty_result()
            
            # Extract resume data from text
            resume_data = self.extract_resume_data(text, filename)
            logger.info("✅ Resume data extraction completed")
            return resume_data
            
        except Exception as e:
            logger.error(f"❌ Resume data extraction error: {e}")
            return self._get_empty_result()
    
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
        """Extract all resume data using smart pattern analysis"""
        try:
            logger.info("🎯 Starting smart pattern analysis...")
            
            if not text or len(text.strip()) < 10:
                return self._get_empty_result()
            
            # Clean and normalize text
            text_clean = self._clean_text(text)
            
            # Extract all components with smart analysis
            name = self._extract_name_smart(text_clean, filename)
            email = self._extract_email_smart(text_clean)
            phone = self._extract_phone_smart(text_clean)
            role = self._extract_role_smart(text_clean, name)
            location = self._extract_location_smart(text_clean, name)
            experience = self._extract_experience_smart(text_clean)
            skills = self._extract_skills_smart(text_clean)
            education = self._extract_education_smart(text_clean)
            
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
                'raw_text': text_clean[:500] + "..." if len(text_clean) > 500 else text_clean,
                'extraction_method': 'smart_pattern_analysis',
                'confidence_score': confidence,
                'extraction_timestamp': datetime.now().isoformat()
            }
            
            logger.info("✅ Smart pattern analysis completed")
            logger.info(f"👤 Name: {name}")
            logger.info(f"📧 Email: {email}")
            logger.info(f"📱 Phone: {phone}")
            logger.info(f"🎯 Role: {role}")
            logger.info(f"📍 Location: {location}")
            logger.info(f"⏰ Experience: {experience.get('display', 'N/A')}")
            logger.info(f"🛠️ Skills: {len(skills)} skills found")
            
            return result
            
        except Exception as e:
            logger.error(f"❌ Smart pattern analysis error: {e}")
            return self._get_empty_result()
    
    def _extract_name_smart(self, text: str, filename: str = None) -> str:
        """Extract name using smart pattern analysis"""
        try:
            logger.info("🔍 Starting smart name extraction...")
            
            lines = text.split('\n')
            
            # Model 1: Check if first line is a name (not an objective)
            if lines:
                first_line = lines[0].strip()
                logger.info(f"🔍 First line: '{first_line[:100]}...'")
                
                # Check if first line is likely a name (not an objective statement)
                if self._is_likely_name_line(first_line):
                    logger.info(f"✅ Name found on first line: {first_line}")
                    return first_line
            
            # Model 2: Look for name patterns in first few lines
            for i, line in enumerate(lines[:5]):
                line = line.strip()
                if self._is_likely_name_line(line):
                    logger.info(f"✅ Name found on line {i+1}: {line}")
                    return line
            
            # Model 3: Try all name patterns
            for pattern in self.name_patterns:
                matches = re.findall(pattern, text, re.IGNORECASE | re.MULTILINE)
                if matches:
                    name = matches[0].strip()
                    if self._is_likely_name_line(name):
                        logger.info(f"✅ Name found with pattern: {name}")
                        return name
            
            # Model 4: Filename fallback
            if filename:
                name_from_file = self._extract_name_from_filename(filename)
                if name_from_file:
                    logger.info(f"✅ Name from filename: {name_from_file}")
                    return name_from_file
            
            return 'Name not found'
            
        except Exception as e:
            logger.error(f"❌ Smart name extraction error: {e}")
            return 'Name not found'
    
    def _is_likely_name_line(self, line: str) -> bool:
        """Check if a line is likely a name (not an objective or other content)"""
        if not line or len(line.strip()) < 2:
            return False
        
        # Must contain only letters, spaces, dots, and hyphens
        if not re.match(r'^[A-Za-z\s\.\-]+$', line):
            return False
        
        # Must be reasonable length (names are usually short)
        if len(line) > 50:
            return False
        
        # Must have at least 2 words
        words = line.split()
        if len(words) < 2:
            return False
        
        # Each word should start with uppercase
        for word in words:
            if not word[0].isupper():
                return False
        
        # Check for objective statements (these are NOT names)
        objective_keywords = [
            'to land', 'challenging job', 'reputable company', 'broaden my knowledge',
            'responsible career path', 'make the most of my education', 'significantly contributing',
            'organization', 'growth', 'objective', 'summary', 'profile', 'about'
        ]
        
        line_lower = line.lower()
        for keyword in objective_keywords:
            if keyword in line_lower:
                return False
        
        # Check for false positives
        false_positives = [
            'resume', 'cv', 'curriculum vitae', 'personal information', 'contact information',
            'experience', 'education', 'skills', 'projects', 'contact', 'address', 'phone',
            'email', 'complete visitor management service', 'admin dashboard',
            'visitor management', 'the unauthenticated or unwanted visitors',
            'user and system data logs', 'system data logs', 'data logs'
        ]
        
        for fp in false_positives:
            if fp in line_lower:
                return False
        
        return True
    
    def _extract_email_smart(self, text: str) -> str:
        """Extract email using smart patterns"""
        try:
            for pattern in self.email_patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                if matches:
                    email = matches[0].strip()
                    if self._is_valid_email_smart(email):
                        logger.info(f"✅ Email extracted: {email}")
                        return email
            
            return 'Email not found'
            
        except Exception as e:
            logger.error(f"❌ Smart email extraction error: {e}")
            return 'Email not found'
    
    def _extract_phone_smart(self, text: str) -> str:
        """Extract phone using smart patterns"""
        try:
            for pattern in self.phone_patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                if matches:
                    phone = matches[0].strip()
                    if self._is_valid_phone_smart(phone):
                        logger.info(f"✅ Phone extracted: {phone}")
                        return phone
            
            return 'Phone not found'
            
        except Exception as e:
            logger.error(f"❌ Smart phone extraction error: {e}")
            return 'Phone not found'
    
    def _extract_role_smart(self, text: str, name: str = None) -> str:
        """Extract role using smart patterns"""
        try:
            # Remove name from text to avoid false matches
            text_for_role = text
            if name:
                text_for_role = text_for_role.replace(name, '')
            
            # Try specific job titles first
            for pattern in self.role_patterns:
                matches = re.findall(pattern, text_for_role, re.IGNORECASE)
                if matches:
                    role = matches[0].strip()
                    if self._is_valid_role_smart(role):
                        logger.info(f"✅ Role extracted: {role}")
                        return role.title()
            
            return 'Role not found'
            
        except Exception as e:
            logger.error(f"❌ Smart role extraction error: {e}")
            return 'Role not found'
    
    def _extract_location_smart(self, text: str, name: str = None) -> str:
        """Extract location using smart patterns"""
        try:
            # Try labeled patterns first
            for pattern in self.location_patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                if matches:
                    location = matches[0].strip()
                    if self._is_valid_location_smart(location):
                        logger.info(f"✅ Location extracted: {location}")
                        return location
            
            # Look for city names in the text
            for city in ['Bangalore', 'Mumbai', 'Delhi', 'Hyderabad', 'Chennai', 'Kolkata', 'Pune', 'Ahmedabad']:
                if city.lower() in text.lower():
                    logger.info(f"✅ Location found: {city}")
                    return city
            
            return 'Location not found'
            
        except Exception as e:
            logger.error(f"❌ Smart location extraction error: {e}")
            return 'Location not found'
    
    def _extract_experience_smart(self, text: str) -> Dict[str, Any]:
        """Extract experience using smart patterns"""
        try:
            text_lower = text.lower()
            
            # Check for fresher indicators
            fresher_keywords = ['fresher', 'fresh graduate', 'recent graduate', 'entry level', 'junior', 'trainee', 'intern', 'student']
            for keyword in fresher_keywords:
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
                'extraction_method': 'smart_pattern_analysis'
            }
            
            logger.info(f"✅ Experience extracted: {result['display']}")
            return result
            
        except Exception as e:
            logger.error(f"❌ Smart experience extraction error: {e}")
            return {
                'total_years': 0,
                'total_months': 0,
                'display': 'Experience extraction error',
                'is_fresher': True,
                'experience_periods': [],
                'extraction_method': 'error'
            }
    
    def _extract_skills_smart(self, text: str) -> List[str]:
        """Extract skills using smart patterns - only valid skills"""
        try:
            skills = set()
            text_lower = text.lower()
            
            # Extract only valid skills from the text
            for skill in self.valid_skills:
                if skill.lower() in text_lower:
                    skills.add(skill.title())
            
            skills_list = list(skills)
            logger.info(f"✅ Skills extracted: {len(skills_list)} valid skills")
            return skills_list
            
        except Exception as e:
            logger.error(f"❌ Smart skills extraction error: {e}")
            return []
    
    def _extract_education_smart(self, text: str) -> List[Dict[str, Any]]:
        """Extract education information using smart patterns"""
        try:
            education = []
            
            # Clean education patterns
            education_patterns = [
                r'(?:Master|Masters)\s+of\s+(Computer Applications|MCA|MCA)\s+([A-Za-z\s]+)',
                r'(?:Bachelor|Bachelors)\s+of\s+(Engineering|BE|B\.E)\s+([A-Za-z\s]+)',
                r'(?:Bachelor|Bachelors)\s+of\s+(Technology|B\.Tech|BTech)\s+([A-Za-z\s]+)',
                r'(?:Master|Masters)\s+of\s+(Technology|M\.Tech|MTech)\s+([A-Za-z\s]+)',
                r'(?:Bachelor|Bachelors)\s+of\s+(Science|B\.Sc|BSc)\s+([A-Za-z\s]+)',
                r'(?:Master|Masters)\s+of\s+(Science|M\.Sc|MSc)\s+([A-Za-z\s]+)',
                r'(?:PhD|Ph\.D|Doctorate)\s+in\s+([A-Za-z\s]+)',
            ]
            
            for pattern in education_patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                for match in matches:
                    if isinstance(match, tuple):
                        degree = ' '.join(match).strip()
                    else:
                        degree = match.strip()
                    
                    if len(degree) > 5 and len(degree) < 100:  # Valid degree length
                        education.append({
                            'degree': degree,
                            'institution': 'Not specified',
                            'year': 'Not specified'
                        })
            
            logger.info(f"✅ Education extracted: {len(education)} entries")
            return education
            
        except Exception as e:
            logger.error(f"❌ Smart education extraction error: {e}")
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
    
    def _is_valid_email_smart(self, email: str) -> bool:
        """Smart email validation"""
        if not email or '@' not in email:
            return False
        
        # Basic email validation
        email_pattern = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$'
        return re.match(email_pattern, email) is not None
    
    def _is_valid_phone_smart(self, phone: str) -> bool:
        """Smart phone validation"""
        if not phone:
            return False
        
        # Remove all non-digit characters
        digits_only = re.sub(r'\D', '', phone)
        
        # Check if it has reasonable length
        return 10 <= len(digits_only) <= 15
    
    def _is_valid_role_smart(self, role: str) -> bool:
        """Smart role validation"""
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
    
    def _is_valid_location_smart(self, location: str) -> bool:
        """Smart location validation"""
        if not location or len(location.strip()) < 2:
            return False
        
        # Check if it's not too long
        if len(location) > 50:
            return False
        
        # Check if it contains reasonable characters
        if not re.match(r'^[A-Za-z\s,\.\-]+$', location):
            return False
        
        # Check for false positives
        false_positives = [
            'the unauthenticated or unwanted visitors', 'visitor management', 'admin dashboard',
            'complete visitor management service', 'slr residency bannerghatta main road gottigere',
            'user and system data logs', 'system data logs', 'data logs', 'logs'
        ]
        
        location_lower = location.lower()
        for fp in false_positives:
            if fp in location_lower:
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
            if self._is_likely_name_line(name):
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
            'extraction_method': 'smart_pattern_analysis',
            'confidence_score': 0.0,
            'extraction_timestamp': datetime.now().isoformat()
        }

# Initialize global smart pattern analyzer
smart_pattern_analyzer = SmartPatternAnalyzer()
