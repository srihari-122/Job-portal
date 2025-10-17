"""
Comprehensive Accurate Extractor
Complete resume extraction with accurate name, role, skills, and experience
"""

import re
import logging
import os
from typing import Dict, List, Any, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

class ComprehensiveAccurateExtractor:
    """Comprehensive extractor for all resume components with high accuracy"""
    
    def __init__(self):
        self.initialize_patterns()
        self.initialize_validation_rules()
        self.initialize_skills_database()
        
    def initialize_patterns(self):
        """Initialize precise extraction patterns"""
        
        # PRECISE NAME PATTERNS - Priority order matters
        self.name_patterns = [
            # 1. Filename-based extraction (highest priority)
            r'^([A-Z][A-Z]+ [A-Z][A-Z]+)',  # ALL CAPS names from filename
            r'^([A-Z][a-z]+ [A-Z][a-z]+(?: [A-Z][a-z]+)?)',  # Title Case names from filename
            
            # 2. Header patterns (second priority)
            r'^([A-Z][A-Z]+ [A-Z][A-Z]+)\s*\n',  # ALL CAPS at start of text
            r'^([A-Z][a-z]+ [A-Z][a-z]+(?: [A-Z][a-z]+)?)\s*\n',  # Title Case at start
            
            # 3. Before common sections
            r'([A-Z][A-Z]+ [A-Z][A-Z]+)\s+(?:PROFILE|Profile|About|Summary|SKILLS|Skills|EDUCATION|Education|EXPERIENCE|Experience)',
            r'([A-Z][a-z]+ [A-Z][a-z]+(?: [A-Z][a-z]+)?)\s+(?:PROFILE|Profile|About|Summary|SKILLS|Skills|EDUCATION|Education|EXPERIENCE|Experience)',
            
            # 4. Contact section patterns
            r'(?:Name|Full Name|Contact Name)[:\s]*([A-Z][A-Z]+ [A-Z][A-Z]+)',
            r'(?:Name|Full Name|Contact Name)[:\s]*([A-Z][a-z]+ [A-Z][a-z]+(?: [A-Z][a-z]+)?)',
            
            # 5. General patterns in text
            r'\b([A-Z][A-Z]+ [A-Z][A-Z]+)\b',  # ALL CAPS anywhere
            r'\b([A-Z][a-z]+ [A-Z][a-z]+(?: [A-Z][a-z]+)?)\b',  # Title Case anywhere
        ]
        
        # PRECISE ROLE PATTERNS - Specific and comprehensive
        self.role_patterns = [
            # 1. Exact role matches (highest priority)
            r'\b(Full\s*Stack\s*Java\s*Developer)\b',
            r'\b(Full\s*Stack\s*Python\s*Developer)\b',
            r'\b(Full\s*Stack\s*JavaScript\s*Developer)\b',
            r'\b(Full\s*Stack\s*Developer)\b',
            
            # 2. Technology-specific roles
            r'\b(Java\s*Developer)\b',
            r'\b(Python\s*Developer)\b',
            r'\b(JavaScript\s*Developer)\b',
            r'\b(React\s*Developer)\b',
            r'\b(Angular\s*Developer)\b',
            r'\b(Node\.js\s*Developer)\b',
            r'\b(Spring\s*Boot\s*Developer)\b',
            r'\b(Django\s*Developer)\b',
            r'\b(Flask\s*Developer)\b',
            
            # 3. Seniority + Technology
            r'\b(Senior\s*Full\s*Stack\s*Developer)\b',
            r'\b(Senior\s*Java\s*Developer)\b',
            r'\b(Senior\s*Python\s*Developer)\b',
            r'\b(Senior\s*JavaScript\s*Developer)\b',
            r'\b(Lead\s*Full\s*Stack\s*Developer)\b',
            r'\b(Lead\s*Java\s*Developer)\b',
            r'\b(Principal\s*Full\s*Stack\s*Developer)\b',
            
            # 4. General developer roles
            r'\b(Software\s*Engineer)\b',
            r'\b(Web\s*Developer)\b',
            r'\b(Frontend\s*Developer)\b',
            r'\b(Backend\s*Developer)\b',
            r'\b(Mobile\s*Developer)\b',
            
            # 5. Other technical roles
            r'\b(Data\s*Scientist)\b',
            r'\b(Data\s*Analyst)\b',
            r'\b(Machine\s*Learning\s*Engineer)\b',
            r'\b(DevOps\s*Engineer)\b',
            r'\b(QA\s*Engineer)\b',
            r'\b(UI\/UX\s*Designer)\b',
            r'\b(Cloud\s*Engineer)\b',
            r'\b(Security\s*Engineer)\b',
            
            # 6. Management roles
            r'\b(Technical\s*Lead)\b',
            r'\b(Team\s*Lead)\b',
            r'\b(Project\s*Manager)\b',
            r'\b(Product\s*Manager)\b',
            r'\b(Solution\s*Architect)\b',
            r'\b(System\s*Architect)\b',
            
            # 7. Context-based patterns
            r'(?:Position|Title|Role|Job Title|Designation|Current Role|Professional Title)[:\s]*([A-Za-z\s]{3,50})',
            r'(?:Working as|Currently|Role)[:\s]*([A-Za-z\s]{3,50})',
            r'(?:I am|I\'m)[:\s]*([A-Za-z\s]{3,50})',
            r'(?:As a|Being a)[:\s]*([A-Za-z\s]{3,50})',
        ]
        
        # EMAIL PATTERNS
        self.email_patterns = [
            r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            r'(?:Email|E-mail|Mail|Contact)[:\s]*([A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,})',
        ]
        
        # PHONE PATTERNS
        self.phone_patterns = [
            r'\b(?:\+91[-.\s]?)?[6-9]\d{9}\b',
            r'\b(?:\+91[-.\s]?)?[6-9]\d{2}[-.\s]?\d{3}[-.\s]?\d{4}\b',
            r'(?:Phone|Mobile|Cell|Contact)[:\s]*([+]?[\d\s\-\(\)]{10,})',
            r'\+91[-.\s]?[6-9]\d{9}',
        ]
        
        # LOCATION PATTERNS
        self.location_patterns = [
            r'(?:Location|Address|City|Based in|Located in|From|Residing in|Living in|Current Location|Present Location|Work Location|Office Location)[:\s]*([A-Za-z\s,]{3,50})',
            r'\b(Bangalore|Mumbai|Delhi|Hyderabad|Chennai|Kolkata|Pune|Ahmedabad|Jaipur|Surat|Lucknow|Kanpur|Nagpur|Indore|Thane|Bhopal|Visakhapatnam|Patna|Vadodara|Ludhiana|Agra|Nashik|Faridabad|Meerut|Rajkot|Kalyan|Vasai|Varanasi|Srinagar|Aurangabad|Navi Mumbai|Solapur|Vijayawada|Kolhapur|Amritsar|Noida|Ranchi|Howrah|Coimbatore|Raipur|Jabalpur|Gwalior|Chandigarh|Tiruchirappalli|Mysore|Bhilai|Kochi|Bhavnagar|Salem|Warangal|Guntur|Bhubaneswar|Mira|Tiruppur|Amravati|Nanded)\b',
        ]
        
        # EXPERIENCE PATTERNS
        self.experience_patterns = [
            r'(\d{4})\s*[-–—]\s*(\d{4})',
            r'(\d{4})\s*to\s*(\d{4})',
            r'([A-Za-z]{3,9})\s*(\d{4})\s*[-–—]\s*([A-Za-z]{3,9})\s*(\d{4})',
            r'(\d{1,2})[/-](\d{4})\s*[-–—]\s*(\d{1,2})[/-](\d{4})',
            r'(\d{4})\s*[-–—]\s*(?:present|current|till\s+date|till\s+now|ongoing)',
            r'([A-Za-z]{3,9})\s*(\d{4})\s*[-–—]\s*(?:present|current|till\s+date|till\s+now|ongoing)',
            r'(?:total|overall)\s*(?:experience|exp)[:\s]*(\d+(?:\.\d+)?)\s*(?:years?|yrs?)',
            r'(\d+(?:\.\d+)?)\s*(?:years?|yrs?)\s*(?:of\s*)?(?:experience|exp)',
            r'(\d+(?:\.\d+)?)\s*(?:to|-)?\s*(\d+(?:\.\d+)?)?\s*(?:years?|yrs?)\s*(?:of\s*)?(?:experience|exp)',
            r'(?:experience|exp)[:\s]*(\d+(?:\.\d+)?)\s*(?:to|-)?\s*(\d+(?:\.\d+)?)?\s*(?:years?|yrs?)',
        ]
        
    def initialize_validation_rules(self):
        """Initialize validation rules for names and roles"""
        
        # FALSE POSITIVES for names (things that look like names but aren't)
        self.name_false_positives = [
            'resume', 'cv', 'curriculum vitae', 'personal information', 'contact information',
            'objective', 'summary', 'profile', 'about', 'contact', 'address', 'phone', 'email',
            'experience', 'education', 'skills', 'projects', 'certifications', 'achievements',
            'complete visitor management service', 'admin dashboard', 'visitor management',
            'the unauthenticated or unwanted visitors', 'user and system data logs',
            'system data logs', 'data logs', 'logs', 'to land', 'challenging job',
            'reputable company', 'broaden my knowledge', 'responsible career path',
            'make the most of my education', 'significantly contributing', 'organization',
            'growth', 'former assistant', 'assistant', 'former', 'current', 'present',
            'working', 'employed', 'job', 'position', 'role', 'title', 'designation'
        ]
        
        # VALID ROLE KEYWORDS
        self.valid_role_keywords = [
            'developer', 'engineer', 'analyst', 'manager', 'designer', 'architect',
            'specialist', 'consultant', 'lead', 'senior', 'junior', 'associate',
            'intern', 'trainee', 'coordinator', 'supervisor', 'director', 'executive',
            'programmer', 'coder', 'technician', 'administrator', 'officer', 'scientist'
        ]
        
        # VALID TECHNOLOGY KEYWORDS for roles
        self.valid_tech_keywords = [
            'java', 'python', 'javascript', 'react', 'angular', 'node', 'spring',
            'sql', 'mongodb', 'aws', 'azure', 'docker', 'kubernetes', 'git',
            'html', 'css', 'bootstrap', 'jquery', 'express', 'django', 'flask',
            'full stack', 'frontend', 'backend', 'mobile', 'web', 'data', 'cloud',
            'security', 'devops', 'qa', 'ui', 'ux', 'software', 'machine learning',
            'artificial intelligence', 'network', 'database', 'game', 'embedded',
            'system', 'platform', 'product', 'technical'
        ]
        
    def initialize_skills_database(self):
        """Initialize comprehensive skills database"""
        
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
    
    def extract_resume_data(self, text: str, filename: str = None) -> Dict[str, Any]:
        """Extract complete resume data with high accuracy"""
        try:
            logger.info("🎯 Starting comprehensive accurate extraction...")
            
            if not text or len(text.strip()) < 10:
                return self._get_empty_result()
            
            # Clean text
            text_clean = self._clean_text(text)
            
            # Extract all components with high precision
            name = self._extract_name_accurate(text_clean, filename)
            role = self._extract_role_accurate(text_clean, name)
            email = self._extract_email_accurate(text_clean)
            phone = self._extract_phone_accurate(text_clean)
            location = self._extract_location_accurate(text_clean, name)
            experience = self._extract_experience_accurate(text_clean)
            skills = self._extract_skills_accurate(text_clean)
            education = self._extract_education_accurate(text_clean)
            
            # Calculate confidence
            confidence = self._calculate_confidence(name, email, phone, role, skills, experience)
            
            result = {
                'name': name,
                'email': email,
                'phone': phone,
                'role': role,
                'location': location,
                'experience': experience,
                'skills': skills,
                'education': education,
                'raw_text': text_clean[:500] + "..." if len(text_clean) > 500 else text_clean,
                'extraction_method': 'comprehensive_accurate_extraction',
                'confidence_score': confidence,
                'extraction_timestamp': datetime.now().isoformat()
            }
            
            logger.info("✅ Comprehensive accurate extraction completed:")
            logger.info(f"👤 Name: {name}")
            logger.info(f"🎯 Role: {role}")
            logger.info(f"📧 Email: {email}")
            logger.info(f"📱 Phone: {phone}")
            logger.info(f"📍 Location: {location}")
            logger.info(f"⏰ Experience: {experience.get('display', 'N/A')}")
            logger.info(f"🛠️ Skills: {len(skills)} skills found")
            logger.info(f"🎓 Education: {len(education)} entries found")
            logger.info(f"🎯 Confidence: {confidence:.2f}")
            
            return result
            
        except Exception as e:
            logger.error(f"❌ Comprehensive extraction error: {e}")
            return self._get_empty_result()
    
    def _extract_name_accurate(self, text: str, filename: str = None) -> str:
        """Extract name with high accuracy"""
        try:
            logger.info("🔍 Starting accurate name extraction...")
            
            # Strategy 1: Extract from filename (highest priority)
            if filename:
                name_from_file = self._extract_name_from_filename(filename)
                if name_from_file and self._is_valid_name(name_from_file):
                    logger.info(f"✅ Name from filename: {name_from_file}")
                    return name_from_file
            
            # Strategy 2: Try all name patterns in priority order
            for i, pattern in enumerate(self.name_patterns):
                matches = re.findall(pattern, text, re.IGNORECASE)
                if matches:
                    for match in matches:
                        name = match.strip()
                        if self._is_valid_name(name):
                            logger.info(f"✅ Name found with pattern {i+1}: {name}")
                            return name
            
            # Strategy 3: Look in first few lines
            lines = text.split('\n')
            for i, line in enumerate(lines[:10]):  # Check first 10 lines
                line = line.strip()
                if self._is_valid_name(line):
                    logger.info(f"✅ Name found on line {i+1}: {line}")
                    return line
            
            logger.warning("⚠️ No valid name found")
            return 'Name not found'
            
        except Exception as e:
            logger.error(f"❌ Name extraction error: {e}")
            return 'Name not found'
    
    def _extract_role_accurate(self, text: str, name: str = None) -> str:
        """Extract role with high accuracy"""
        try:
            logger.info("🔍 Starting accurate role extraction...")
            
            # Remove name from text to avoid false matches
            text_for_role = text
            if name and name != 'Name not found':
                text_for_role = text_for_role.replace(name, '')
            
            # Strategy 1: Try exact role patterns first
            for i, pattern in enumerate(self.role_patterns):
                matches = re.findall(pattern, text_for_role, re.IGNORECASE)
                if matches:
                    for match in matches:
                        role = match.strip()
                        if self._is_valid_role(role):
                            logger.info(f"✅ Role found with pattern {i+1}: {role}")
                            return role.title()
            
            # Strategy 2: Look for role keywords in context
            role_context = self._find_role_in_context(text_for_role)
            if role_context and self._is_valid_role(role_context):
                logger.info(f"✅ Role found in context: {role_context}")
                return role_context.title()
            
            # Strategy 3: Default based on skills/technologies mentioned
            default_role = self._infer_role_from_content(text_for_role)
            if default_role:
                logger.info(f"✅ Role inferred from content: {default_role}")
                return default_role
            
            logger.warning("⚠️ No valid role found")
            return 'Role not found'
            
        except Exception as e:
            logger.error(f"❌ Role extraction error: {e}")
            return 'Role not found'
    
    def _extract_email_accurate(self, text: str) -> str:
        """Extract email with high accuracy"""
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
    
    def _extract_phone_accurate(self, text: str) -> str:
        """Extract phone with high accuracy"""
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
    
    def _extract_location_accurate(self, text: str, name: str = None) -> str:
        """Extract location with high accuracy"""
        try:
            logger.info("🔍 Starting accurate location extraction...")
            
            # Remove name from text to avoid false matches
            text_for_location = text
            if name and name != 'Name not found':
                text_for_location = text_for_location.replace(name, '')
            
            # Strategy 1: Try labeled patterns first
            for pattern in self.location_patterns:
                matches = re.findall(pattern, text_for_location, re.IGNORECASE)
                if matches:
                    for match in matches:
                        location = match.strip()
                        if self._is_valid_location(location):
                            logger.info(f"✅ Location extracted: {location}")
                            return location.title()
            
            # Strategy 2: Look for known cities
            known_cities = [
                'bangalore', 'mumbai', 'delhi', 'hyderabad', 'chennai', 'kolkata', 'pune', 'ahmedabad',
                'jaipur', 'surat', 'lucknow', 'kanpur', 'nagpur', 'indore', 'thane', 'bhopal',
                'visakhapatnam', 'patna', 'vadodara', 'ludhiana', 'agra', 'nashik', 'faridabad',
                'meerut', 'rajkot', 'kalyan', 'vasai', 'varanasi', 'srinagar', 'aurangabad',
                'noida', 'ranchi', 'howrah', 'coimbatore', 'raipur', 'jabalpur', 'gwalior',
                'chandigarh', 'tiruchirappalli', 'mysore', 'bhilai', 'kochi', 'bhavnagar',
                'salem', 'warangal', 'guntur', 'bhubaneswar', 'mira', 'tiruppur', 'amravati', 'nanded'
            ]
            
            text_lower = text_for_location.lower()
            for city in known_cities:
                if city in text_lower:
                    logger.info(f"✅ Location found: {city}")
                    return city.title()
            
            logger.warning("⚠️ No valid location found")
            return 'Location not found'
            
        except Exception as e:
            logger.error(f"❌ Location extraction error: {e}")
            return 'Location not found'
    
    def _extract_experience_accurate(self, text: str) -> Dict[str, Any]:
        """Extract experience with high accuracy"""
        try:
            logger.info("🔍 Starting accurate experience extraction...")
            
            text_lower = text.lower()
            
            # Check for fresher indicators first
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
                'extraction_method': 'comprehensive_accurate_extraction'
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
    
    def _extract_skills_accurate(self, text: str) -> List[str]:
        """Extract skills with high accuracy"""
        try:
            logger.info("🔍 Starting accurate skills extraction...")
            
            skills = set()
            text_lower = text.lower()
            
            # Extract only valid skills from the text
            for skill in self.valid_skills:
                if skill.lower() in text_lower:
                    skills.add(skill.title())
            
            skills_list = list(skills)
            skills_list.sort()  # Sort alphabetically
            
            logger.info(f"✅ Skills extracted: {len(skills_list)} valid skills")
            return skills_list
            
        except Exception as e:
            logger.error(f"❌ Skills extraction error: {e}")
            return []
    
    def _extract_education_accurate(self, text: str) -> List[Dict[str, Any]]:
        """Extract education with high accuracy"""
        try:
            logger.info("🔍 Starting accurate education extraction...")
            
            education = []
            
            # Education patterns
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
                from dateutil.relativedelta import relativedelta
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
    
    def _extract_name_from_filename(self, filename: str) -> Optional[str]:
        """Extract name from filename"""
        try:
            # Remove file extension
            name = filename.replace('.pdf', '').replace('.docx', '').replace('.txt', '')
            
            # Remove common prefixes/suffixes
            name = re.sub(r'^(resume|cv|curriculum_vitae)_?', '', name, flags=re.IGNORECASE)
            name = re.sub(r'_\d+$', '', name)  # Remove timestamps
            name = re.sub(r'_\d+_', '_', name)  # Remove middle timestamps
            
            # Convert underscores and hyphens to spaces
            name = re.sub(r'[_-]', ' ', name)
            
            # Check if it looks like a name
            if self._is_valid_name(name):
                return name
            
            return None
            
        except Exception as e:
            logger.error(f"❌ Error extracting name from filename: {e}")
            return None
    
    def _is_valid_name(self, name: str) -> bool:
        """Validate if text is likely a real name"""
        if not name or len(name.strip()) < 2:
            return False
        
        # Must contain only letters, spaces, dots, and hyphens
        if not re.match(r'^[A-Za-z\s\.\-]+$', name):
            return False
        
        # Must be reasonable length
        if len(name) > 50:
            return False
        
        # Must have at least 2 words
        words = name.split()
        if len(words) < 2:
            return False
        
        # Each word should start with uppercase
        for word in words:
            if not word[0].isupper():
                return False
        
        # Check for false positives
        name_lower = name.lower()
        for fp in self.name_false_positives:
            if fp in name_lower:
                return False
        
        # Additional validation: names shouldn't contain common job terms
        job_terms = ['developer', 'engineer', 'manager', 'analyst', 'assistant', 'former', 'current']
        for term in job_terms:
            if term in name_lower:
                return False
        
        return True
    
    def _is_valid_role(self, role: str) -> bool:
        """Validate if text is likely a real role"""
        if not role or len(role.strip()) < 3:
            return False
        
        role_lower = role.lower()
        
        # Check if role contains job-related keywords
        has_job_keyword = any(keyword in role_lower for keyword in self.valid_role_keywords)
        
        # Check if role contains technology keywords
        has_tech_keyword = any(keyword in role_lower for keyword in self.valid_tech_keywords)
        
        # Role is valid if it has job keywords or tech keywords
        return has_job_keyword or has_tech_keyword
    
    def _is_valid_email(self, email: str) -> bool:
        """Validate email format"""
        if not email or '@' not in email:
            return False
        
        email_pattern = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$'
        return re.match(email_pattern, email) is not None
    
    def _is_valid_phone(self, phone: str) -> bool:
        """Validate phone format"""
        if not phone:
            return False
        
        # Remove all non-digit characters
        digits_only = re.sub(r'\D', '', phone)
        
        # Check if it has reasonable length
        return 10 <= len(digits_only) <= 15
    
    def _is_valid_location(self, location: str) -> bool:
        """Validate location format"""
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
    
    def _find_role_in_context(self, text: str) -> Optional[str]:
        """Find role by looking for context around role keywords"""
        try:
            # Look for role keywords and extract surrounding context
            for keyword in self.valid_role_keywords:
                pattern = rf'\b([A-Za-z\s]*(?:senior|junior|lead|principal|staff)?\s*[A-Za-z\s]*{keyword}[A-Za-z\s]*)\b'
                matches = re.findall(pattern, text, re.IGNORECASE)
                if matches:
                    for match in matches:
                        role = match.strip()
                        if len(role) > 3 and len(role) < 50:
                            return role
            
            return None
            
        except Exception as e:
            logger.error(f"❌ Error finding role in context: {e}")
            return None
    
    def _infer_role_from_content(self, text: str) -> Optional[str]:
        """Infer role from content analysis"""
        try:
            text_lower = text.lower()
            
            # Check for specific technology combinations
            if 'java' in text_lower and 'spring' in text_lower:
                return 'Full Stack Java Developer'
            elif 'java' in text_lower:
                return 'Java Developer'
            elif 'python' in text_lower and ('django' in text_lower or 'flask' in text_lower):
                return 'Full Stack Python Developer'
            elif 'python' in text_lower:
                return 'Python Developer'
            elif 'javascript' in text_lower and ('react' in text_lower or 'angular' in text_lower):
                return 'Full Stack JavaScript Developer'
            elif 'javascript' in text_lower:
                return 'JavaScript Developer'
            elif 'react' in text_lower:
                return 'React Developer'
            elif 'angular' in text_lower:
                return 'Angular Developer'
            elif 'developer' in text_lower:
                return 'Software Developer'
            elif 'engineer' in text_lower:
                return 'Software Engineer'
            
            return None
            
        except Exception as e:
            logger.error(f"❌ Error inferring role from content: {e}")
            return None
    
    def _calculate_confidence(self, name: str, email: str, phone: str, role: str, skills: List[str], experience: Dict[str, Any]) -> float:
        """Calculate extraction confidence score"""
        try:
            confidence = 0.0
            
            # Name confidence (30%)
            if name != 'Name not found':
                confidence += 0.3
            
            # Role confidence (25%)
            if role != 'Role not found':
                confidence += 0.25
            
            # Email confidence (15%)
            if email != 'Email not found':
                confidence += 0.15
            
            # Phone confidence (10%)
            if phone != 'Phone not found':
                confidence += 0.1
            
            # Skills confidence (10%)
            if len(skills) > 0:
                confidence += min(0.1, len(skills) * 0.01)
            
            # Experience confidence (10%)
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
            'role': 'Role not found',
            'location': 'Location not found',
            'experience': {
                'total_years': 0,
                'total_months': 0,
                'display': 'Experience not found',
                'is_fresher': True,
                'experience_periods': [],
                'extraction_method': 'empty_result'
            },
            'skills': [],
            'education': [],
            'raw_text': '',
            'extraction_method': 'comprehensive_accurate_extraction',
            'confidence_score': 0.0,
            'extraction_timestamp': datetime.now().isoformat()
        }

# Initialize global comprehensive accurate extractor
comprehensive_accurate_extractor = ComprehensiveAccurateExtractor()

