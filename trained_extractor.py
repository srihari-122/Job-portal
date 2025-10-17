"""
Trained Extractor for Experience and Skills
Extracts explicit values from resume text without calculation
"""

import re
import logging
from typing import Dict, List, Any, Tuple
import json

logger = logging.getLogger(__name__)

class TrainedExtractor:
    """Trained extractor for experience and skills"""
    
    def __init__(self):
        # Experience patterns - extract explicit statements
        self.experience_patterns = [
            # Direct experience statements
            r'(?:total|overall|total\s+work)\s*(?:experience|exp)[:\s]*(\d+(?:\.\d+)?)\s*(?:to|-)?\s*(\d+(?:\.\d+)?)?\s*(?:years?|yrs?)',
            r'(?:experience|exp)[:\s]*(\d+(?:\.\d+)?)\s*(?:to|-)?\s*(\d+(?:\.\d+)?)?\s*(?:years?|yrs?)',
            r'(\d+(?:\.\d+)?)\s*(?:to|-)?\s*(\d+(?:\.\d+)?)?\s*(?:years?|yrs?)\s*(?:of\s*)?(?:experience|exp)',
            r'(?:over|more\s+than|above)\s+(\d+(?:\.\d+)?)\s*(?:years?|yrs?)',
            r'(\d+(?:\.\d+)?)\+?\s*(?:years?|yrs?)\s*(?:plus|and\s+above)',
            r'(?:around|approximately|about)\s+(\d+(?:\.\d+)?)\s*(?:years?|yrs?)',
            r'(?:minimum|at\s+least)\s+(\d+(?:\.\d+)?)\s*(?:years?|yrs?)',
            r'(?:maximum|up\s+to)\s+(\d+(?:\.\d+)?)\s*(?:years?|yrs?)',
            r'(?:exactly|precisely)\s+(\d+(?:\.\d+)?)\s*(?:years?|yrs?)',
            r'(?:close\s+to|nearly)\s+(\d+(?:\.\d+)?)\s*(?:years?|yrs?)'
        ]
        
        # Skills database with categories
        self.skills_database = {
            'programming': [
                'java', 'python', 'javascript', 'typescript', 'c++', 'c#', 'go', 'rust',
                'kotlin', 'swift', 'php', 'ruby', 'scala', 'r', 'matlab', 'perl',
                'shell', 'bash', 'powershell', 'sql', 'pl/sql', 't-sql'
            ],
            'web_frontend': [
                'html', 'css', 'react', 'angular', 'vue', 'ember', 'backbone', 'jquery',
                'bootstrap', 'sass', 'less', 'stylus', 'webpack', 'babel', 'eslint',
                'prettier', 'gulp', 'grunt', 'npm', 'yarn', 'pnpm'
            ],
            'web_backend': [
                'node.js', 'express', 'django', 'flask', 'fastapi', 'spring', 'spring boot',
                'hibernate', 'jpa', 'laravel', 'symfony', 'rails', 'asp.net', 'dotnet',
                'rest api', 'graphql', 'microservices', 'serverless'
            ],
            'database': [
                'mysql', 'postgresql', 'mongodb', 'redis', 'elasticsearch', 'cassandra',
                'dynamodb', 'oracle', 'sqlite', 'firebase', 'neo4j', 'couchdb',
                'mariadb', 'sql server', 'db2', 'teradata'
            ],
            'cloud': [
                'aws', 'azure', 'gcp', 'google cloud', 'docker', 'kubernetes', 'terraform',
                'ansible', 'chef', 'puppet', 'jenkins', 'gitlab ci', 'github actions',
                'cloudformation', 'serverless', 'lambda', 'ec2', 's3', 'rds'
            ],
            'mobile': [
                'android', 'ios', 'react native', 'flutter', 'xamarin', 'ionic', 'cordova',
                'swift', 'kotlin', 'objective-c', 'java android', 'swift ios'
            ],
            'ai_ml': [
                'tensorflow', 'pytorch', 'keras', 'scikit-learn', 'pandas', 'numpy',
                'opencv', 'nltk', 'spacy', 'transformers', 'hugging face', 'mlflow',
                'jupyter', 'matplotlib', 'seaborn', 'plotly'
            ],
            'devops': [
                'git', 'github', 'gitlab', 'bitbucket', 'jenkins', 'travis ci', 'circleci',
                'docker', 'kubernetes', 'helm', 'prometheus', 'grafana', 'kibana',
                'splunk', 'new relic', 'datadog', 'sentry'
            ],
            'testing': [
                'selenium', 'cypress', 'jest', 'mocha', 'pytest', 'junit', 'testng',
                'jasmine', 'karma', 'protractor', 'playwright', 'appium', 'cucumber',
                'bdd', 'tdd', 'unit testing', 'integration testing'
            ],
            'tools': [
                'maven', 'gradle', 'ant', 'npm', 'yarn', 'pip', 'conda', 'composer',
                'intellij', 'eclipse', 'vscode', 'vim', 'emacs', 'postman', 'insomnia',
                'fiddler', 'wireshark', 'jira', 'confluence', 'slack', 'teams'
            ]
        }
        
        # Experience keywords for fresher detection
        self.fresher_keywords = [
            'fresher', 'fresh graduate', 'recent graduate', 'new graduate', 'entry level',
            'junior', 'trainee', 'intern', 'internship', 'no experience', 'zero experience',
            'beginner', 'starter', 'newbie', 'rookie', 'novice', 'apprentice'
        ]
    
    def extract_experience(self, text: str) -> Dict[str, Any]:
        """Extract experience from resume text"""
        try:
            logger.info("⏰ Starting trained experience extraction...")
            
            text_lower = text.lower()
            
            # Check for fresher indicators first
            for keyword in self.fresher_keywords:
                if keyword in text_lower:
                    logger.info("✅ Fresher detected")
                    return {
                        'total_years': 0,
                        'total_months': 0,
                        'display': 'Fresher',
                        'extraction_method': 'fresher_detection'
                    }
            
            # Extract explicit experience statements
            for pattern in self.experience_patterns:
                matches = re.findall(pattern, text_lower)
                for match in matches:
                    if isinstance(match, tuple):
                        years = float(match[0]) if match[0] else 0
                        if match[1] and match[1] != '':
                            # Range found, take the higher value
                            years = max(years, float(match[1]))
                    else:
                        years = float(match)
                    
                    if 0 < years <= 30:
                        logger.info(f"✅ Experience extracted: {years} years")
                        return {
                            'total_years': int(years),
                            'total_months': int(years * 12),
                            'display': f"{int(years)} years",
                            'extraction_method': 'explicit_extraction'
                        }
            
            # If no explicit experience found, return not found
            logger.info("⚠️ No explicit experience found")
            return {
                'total_years': 0,
                'total_months': 0,
                'display': 'Experience not found',
                'extraction_method': 'not_found'
            }
            
        except Exception as e:
            logger.error(f"❌ Experience extraction error: {e}")
            return {
                'total_years': 0,
                'total_months': 0,
                'display': 'Extraction error',
                'extraction_method': 'error'
            }
    
    def extract_skills(self, text: str) -> List[str]:
        """Extract skills from resume text using comprehensive approach"""
        try:
            logger.info("🛠️ Starting comprehensive skills extraction...")
            
            text_lower = text.lower()
            found_skills = []
            
            # First, extract from predefined database
            for category, skills in self.skills_database.items():
                for skill in skills:
                    pattern = r'\b' + re.escape(skill.lower()) + r'\b'
                    if re.search(pattern, text_lower):
                        skill_title = skill.title()
                        if not any(s.lower() == skill.lower() for s in found_skills):
                            found_skills.append(skill_title)
                            logger.info(f"✅ Found predefined skill: {skill_title}")
            
            # Then, extract additional technical terms from the text
            technical_patterns = [
                # Programming languages
                r'\b(java|python|javascript|typescript|c\+\+|c#|go|rust|kotlin|swift|php|ruby|scala|r|matlab|perl|shell|bash|powershell)\b',
                # Frameworks and libraries
                r'\b(react|angular|vue|ember|backbone|jquery|bootstrap|sass|less|stylus|webpack|babel|eslint|prettier|gulp|grunt|npm|yarn|pnpm)\b',
                # Backend technologies
                r'\b(node\.js|nodejs|express|django|flask|fastapi|spring|spring boot|hibernate|jpa|laravel|symfony|rails|asp\.net|dotnet|rest api|graphql|microservices|serverless)\b',
                # Databases
                r'\b(mysql|postgresql|mongodb|redis|elasticsearch|cassandra|oracle|sqlite|sql server|dynamodb|firebase|supabase)\b',
                # Cloud and DevOps
                r'\b(docker|kubernetes|aws|azure|gcp|jenkins|git|github|gitlab|bitbucket|linux|ubuntu|centos|debian|terraform|ansible|prometheus|grafana)\b',
                # Tools and platforms
                r'\b(maven|gradle|intellij|vscode|postman|swagger|jira|confluence|slack|trello|figma|sketch|photoshop|illustrator)\b',
                # Testing frameworks
                r'\b(jest|mocha|chai|jasmine|karma|cypress|selenium|pytest|junit|testng|rspec|cucumber|protractor)\b',
                # Mobile technologies
                r'\b(react native|flutter|android|ios|xcode|android studio|expo|ionic|cordova|phonegap)\b',
                # Other technical terms
                r'\b(html|css|xml|json|yaml|toml|markdown|git|svn|mercurial|perforce|tfs|vsts|azure devops)\b'
            ]
            
            for pattern in technical_patterns:
                matches = re.findall(pattern, text_lower)
                for match in matches:
                    if isinstance(match, tuple):
                        match = match[0]  # Extract from tuple
                    skill_title = match.title()
                    if not any(s.lower() == match.lower() for s in found_skills):
                        found_skills.append(skill_title)
                        logger.info(f"✅ Found technical skill: {skill_title}")
            
            # Remove duplicates and sort
            unique_skills = list(set(found_skills))
            unique_skills.sort()
            
            logger.info(f"✅ Skills extracted: {len(unique_skills)} skills")
            logger.info(f"🔍 Extracted skills: {unique_skills}")
            return unique_skills
            
        except Exception as e:
            logger.error(f"❌ Skills extraction error: {e}")
            return []
    
    def extract_experience_and_skills(self, text: str) -> Tuple[Dict[str, Any], List[str]]:
        """Extract both experience and skills"""
        try:
            logger.info("🎯 Starting combined experience and skills extraction...")
            
            experience = self.extract_experience(text)
            skills = self.extract_skills(text)
            
            logger.info("✅ Combined extraction completed")
            return experience, skills
            
        except Exception as e:
            logger.error(f"❌ Combined extraction error: {e}")
            return self._get_empty_experience(), []
    
    def _get_empty_experience(self) -> Dict[str, Any]:
        """Return empty experience"""
        return {
            'total_years': 0,
            'total_months': 0,
            'display': 'Not found',
            'extraction_method': 'empty'
        }

# Initialize global trained extractor
trained_extractor = TrainedExtractor()
