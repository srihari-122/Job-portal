"""
Advanced Accurate Resume Extractor
Uses multiple AI techniques and validation methods for maximum accuracy
"""

import re
import logging
import os
from typing import Dict, List, Any, Optional
from datetime import datetime
import spacy
from nltk import sent_tokenize, word_tokenize, pos_tag, ne_chunk
from nltk.corpus import stopwords
import nltk

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('taggers/averaged_perceptron_tagger')
except LookupError:
    nltk.download('averaged_perceptron_tagger')

try:
    nltk.data.find('chunkers/maxent_ne_chunker')
except LookupError:
    nltk.download('maxent_ne_chunker')

try:
    nltk.data.find('corpora/words')
except LookupError:
    nltk.download('words')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

logger = logging.getLogger(__name__)

class AdvancedAccurateExtractor:
    """Advanced extractor with multiple AI techniques for maximum accuracy"""
    
    def __init__(self):
        self.initialize_nlp()
        self.initialize_patterns()
        self.initialize_validation_rules()
        
    def initialize_nlp(self):
        """Initialize NLP models"""
        try:
            # Try to load spaCy model
            self.nlp = spacy.load("en_core_web_sm")
            logger.info("✅ spaCy model loaded successfully")
        except OSError:
            logger.warning("⚠️ spaCy model not found, using NLTK only")
            self.nlp = None
        
        # Initialize stopwords
        try:
            self.stop_words = set(stopwords.words('english'))
        except:
            self.stop_words = set()
        
    def initialize_patterns(self):
        """Initialize advanced extraction patterns"""
        
        # ADVANCED NAME PATTERNS
        self.name_patterns = [
            # Filename patterns (highest priority)
            r'([A-Z][a-z]+_[A-Z][a-z]+(?:_[A-Z][a-z]+)?)',  # Underscore names
            r'([A-Z][a-z]+-[A-Z][a-z]+(?:-[A-Z][a-z]+)?)',  # Hyphen names
            r'([A-Z][a-z]+ [A-Z][a-z]+(?: [A-Z][a-z]+)?)',  # Space names
            
            # Document header patterns
            r'^([A-Z][A-Z\s]+[A-Z])\s*\n',  # ALL CAPS names at start
            r'^([A-Z][a-z]+ [A-Z][a-z]+(?: [A-Z][a-z]+)?)\s*\n',  # Title case at start
            
            # Contact section patterns
            r'(?:Name|Full Name|Contact Name)[:\s]*([A-Z][a-z]+ [A-Z][a-z]+(?: [A-Z][a-z]+)?)',
            r'([A-Z][a-z]+ [A-Z][a-z]+(?: [A-Z][a-z]+)?)\s*\n\s*(?:Email|Phone|Address|Contact)',
            
            # Profile section patterns
            r'([A-Z][a-z]+ [A-Z][a-z]+(?: [A-Z][a-z]+)?)\s*\n\s*(?:PROFILE|Profile|About|Summary|OBJECTIVE|Objective)',
        ]
        
        # ADVANCED ROLE PATTERNS
        self.role_patterns = [
            # Specific job titles (highest priority)
            r'\b(Software Engineer|Software Developer|Full Stack Developer|Frontend Developer|Backend Developer|Web Developer|Mobile Developer|DevOps Engineer|Data Scientist|Data Analyst|Machine Learning Engineer|AI Engineer|Cloud Engineer|Security Engineer|QA Engineer|Test Engineer|UI/UX Designer|Product Manager|Project Manager|Technical Lead|Team Lead|Solution Architect|System Architect|Database Administrator|Network Administrator|System Administrator|Business Analyst|System Analyst|Technical Writer|Scrum Master|Agile Coach|Engineering Manager|Development Manager|IT Manager|CTO|VP of Engineering|Director of Engineering)\b',
            
            # Seniority + role combinations
            r'\b(Senior|Lead|Principal|Staff|Senior Staff|Principal Staff|Distinguished|Fellow)\s+(Software Engineer|Software Developer|Full Stack Developer|Frontend Developer|Backend Developer|Web Developer|Mobile Developer|DevOps Engineer|Data Scientist|Data Analyst|Machine Learning Engineer|AI Engineer|Cloud Engineer|Security Engineer|QA Engineer|Test Engineer|UI/UX Designer|Product Manager|Project Manager|Technical Lead|Team Lead|Solution Architect|System Architect|Database Administrator|Network Administrator|System Administrator|Business Analyst|System Analyst|Technical Writer|Scrum Master|Agile Coach|Engineering Manager|Development Manager|IT Manager)\b',
            
            # Technology-specific roles
            r'\b(Full Stack Java Developer|Java Developer|Python Developer|JavaScript Developer|React Developer|Angular Developer|Vue Developer|Node\.js Developer|Spring Boot Developer|Django Developer|Flask Developer|Laravel Developer|Ruby on Rails Developer|PHP Developer|C# Developer|C\+\+ Developer|Go Developer|Rust Developer|Swift Developer|Kotlin Developer|Flutter Developer|React Native Developer|Android Developer|iOS Developer)\b',
            
            # Experience-based roles
            r'\b(Junior|Entry Level|Associate|Mid Level|Senior|Lead|Principal|Staff|Senior Staff|Principal Staff|Distinguished|Fellow)\s+(Developer|Engineer|Programmer|Analyst|Consultant|Specialist|Architect|Manager|Director)\b',
            
            # Work experience context
            r'(?:worked as|position of|role of|designation of|currently working as|presently working as|employed as|served as|acting as|functioning as|operating as|performing as|executing as|carrying out as|fulfilling as|discharging as|exercising as|practicing as|engaged as|involved as|participated as|contributed as|assisted as|supported as|helped as|aided as|facilitated as|enabled as|empowered as|authorized as|delegated as|assigned as|appointed as|designated as|nominated as|selected as|chosen as|picked as|elected as|voted as|approved as|endorsed as|recommended as|suggested as|proposed as|offered as|presented as|introduced as|launched as|released as|published as|distributed as|circulated as|disseminated as|propagated as|spread as|transmitted as|broadcast as|telecast as|webcast as|streamed as|live as|real-time as|instant as|immediate as|prompt as|quick as|fast as|rapid as|swift as|speedy as|hasty as|hurried as|rushed as|urgent as|pressing as|critical as|important as|significant as|notable as|remarkable as|extraordinary as|exceptional as|outstanding as|superior as|excellent as|superb as|magnificent as|wonderful as|fantastic as|amazing as|incredible as|unbelievable as|remarkable as|notable as|significant as|important as|vital as|crucial as|essential as|necessary as|required as|mandatory as|compulsory as|obligatory as|indispensable as|fundamental as|basic as|primary as|principal as|main as|chief as|leading as|foremost as|top as|best as|finest as|greatest as|highest as|maximum as|peak as|summit as|climax as|culmination as|pinnacle as|apex as|zenith as|acme as)\s+(Software Engineer|Software Developer|Full Stack Developer|Frontend Developer|Backend Developer|Web Developer|Mobile Developer|DevOps Engineer|Data Scientist|Data Analyst|Machine Learning Engineer|AI Engineer|Cloud Engineer|Security Engineer|QA Engineer|Test Engineer|UI/UX Designer|Product Manager|Project Manager|Technical Lead|Team Lead|Solution Architect|System Architect|Database Administrator|Network Administrator|System Administrator|Business Analyst|System Analyst|Technical Writer|Scrum Master|Agile Coach|Engineering Manager|Development Manager|IT Manager|Java Developer|Python Developer|JavaScript Developer|React Developer|Angular Developer|Node\.js Developer|Spring Boot Developer|Django Developer|Flask Developer)',
            
            # Job title context
            r'(?:job title|position|role|title|designation|post|office|appointment|assignment|commission|mandate|charge|responsibility|duty|function|task|work|employment|occupation|profession|career|vocation|calling|trade|craft|skill|art|science|discipline|field|domain|area|sector|industry|business|enterprise|organization|company|corporation|firm|establishment|institution|agency|bureau|department|division|section|unit|team|group|crew|squad|gang|band|party|faction|clique|circle|set|class|category|type|kind|sort|variety|species|genus|family|order|phylum|kingdom|domain|realm|sphere|world|universe|cosmos|creation|nature|reality|existence|being|life|living|alive|animate|organic|biological|physical|material|tangible|concrete|solid|firm|hard|soft|smooth|rough|coarse|fine|delicate|fragile|brittle|strong|weak|powerful|mighty|forceful|robust|sturdy|durable|lasting|permanent|temporary|transient|fleeting|brief|short|long|extended|prolonged|protracted|drawn out|stretched|expanded|enlarged|increased|decreased|reduced|diminished|lessened|lowered|raised|elevated|lifted|hoisted|boosted|enhanced|improved|better|worse|superior|inferior|higher|lower|upper|lower|top|bottom|first|last|beginning|end|start|finish|commence|conclude|initiate|terminate|launch|land|take off|touch down|depart|arrive|leave|stay|remain|continue|persist|endure|survive|thrive|flourish|prosper|succeed|fail|win|lose|victory|defeat|triumph|disaster|success|failure|achievement|accomplishment|completion|finish|end|conclusion|result|outcome|consequence|effect|impact|influence|power|force|strength|energy|vigor|vitality|spirit|soul|heart|mind|brain|intellect|intelligence|wisdom|knowledge|understanding|comprehension|grasp|insight|perception|awareness|consciousness|realization|recognition|acknowledgment|admission|confession|declaration|statement|announcement|proclamation|revelation|disclosure|exposure|unveiling|presentation|introduction|launch|release|publication|distribution|circulation|dissemination|propagation|spread|transmission|broadcast|telecast|webcast|stream|live|real-time|instant|immediate|prompt|quick|fast|rapid|swift|speedy|hasty|hurried|rushed|urgent|pressing|critical|important|significant|notable|remarkable|extraordinary|exceptional|outstanding|superior|excellent|superb|magnificent|wonderful|fantastic|amazing|incredible|unbelievable|remarkable|notable|significant|important|vital|crucial|essential|necessary|required|mandatory|compulsory|obligatory|indispensable|fundamental|basic|primary|principal|main|chief|leading|foremost|top|best|finest|greatest|highest|maximum|peak|summit|climax|culmination|pinnacle|apex|zenith|acme)[:\s]*([A-Za-z\s]{3,50})',
        ]
        
        # EXCLUSION PATTERNS
        self.name_exclusions = [
            r'\b(TCS|IBM|Microsoft|Google|Amazon|Apple|Facebook|LinkedIn|Twitter|Instagram|YouTube|Netflix|Uber|Airbnb|Tesla|SpaceX|Oracle|SAP|Salesforce|Adobe|Intel|NVIDIA|AMD|Cisco|VMware|Red Hat|MongoDB|Elastic|Databricks|Snowflake|Palantir|ServiceNow|Workday|Atlassian|Slack|Zoom|Dropbox|Box|GitHub|GitLab|Bitbucket|Jenkins|Docker|Kubernetes|Terraform|Ansible|Chef|Puppet|Nagios|Splunk|New Relic|DataDog|PagerDuty|Twilio|Stripe|Square|PayPal|Venmo|Coinbase|Binance|Kraken|Robinhood|E\*TRADE|Fidelity|Charles Schwab|Vanguard|BlackRock|Goldman Sachs|JPMorgan|Morgan Stanley|Bank of America|Wells Fargo|Citigroup|American Express|Visa|Mastercard|Discover|Capital One|Chase|USAA|Navy Federal|Pentagon Federal|Alliant|Ally Bank|Marcus|SoFi|Betterment|Wealthfront|Acorns|Stash|M1 Finance|TD Ameritrade|Interactive Brokers)\b',
            r'\b(Recognition|Award|Certificate|Certification|Achievement|Honor|Distinction|Excellence|Outstanding|Merit|Commendation|Appreciation|Gratitude|Thanks|Acknowledgement|Tribute|Praise|Accolade|Laurel|Crown|Medal|Trophy|Plaque|Diploma|Degree|Bachelor|Master|PhD|Doctorate|Associate|License|Credential|Qualification|Competency|Proficiency|Expertise|Mastery|Skill|Ability|Talent|Gift|Capability|Capacity|Potential|Aptitude|Intelligence|Wisdom|Knowledge|Understanding|Comprehension|Grasp|Insight|Perception|Awareness|Consciousness|Realization|Acknowledgment|Admission|Confession|Declaration|Statement|Announcement|Proclamation|Revelation|Disclosure|Exposure|Unveiling|Presentation|Introduction|Launch|Release|Publication|Distribution|Circulation|Dissemination|Propagation|Spread|Transmission|Broadcast|Telecast|Webcast|Stream|Live|Real-time|Instant|Immediate|Prompt|Quick|Fast|Rapid|Swift|Speedy|Hasty|Hurried|Rushed|Urgent|Pressing|Critical|Important|Significant|Notable|Remarkable|Extraordinary|Exceptional|Superior|Excellent|Superb|Magnificent|Wonderful|Fantastic|Amazing|Incredible|Unbelievable|Vital|Crucial|Essential|Necessary|Required|Mandatory|Compulsory|Obligatory|Indispensable|Fundamental|Basic|Primary|Principal|Main|Chief|Leading|Foremost|Top|Best|Finest|Greatest|Highest|Maximum|Peak|Summit|Climax|Culmination|Pinnacle|Apex|Zenith|Acme)\b',
        ]
        
        self.role_exclusions = [
            r'\b(Passionate about|Dedicated to|Committed to|Devoted to|Loyal to|Faithful to|True to|leveraging|utilizing|using|employing|applying|implementing|executing|performing|carrying out|conducting|undertaking|pursuing|following|adopting|embracing|accepting|taking|receiving|getting|obtaining|acquiring|gaining|earning|winning|achieving|accomplishing|completing|finishing|concluding|ending|terminating|stopping|ceasing|halting|pausing|resting|relaxing|unwinding|decompressing|releasing|letting go|surrendering|yielding|giving up|quitting|abandoning|deserting|forsaking|leaving|departing|going|moving|traveling|journeying|voyaging|exploring|discovering|finding|locating|identifying|recognizing|acknowledging|accepting|embracing|welcoming|greeting|saluting|honoring|respecting|valuing|appreciating|cherishing|treasing|loving|adoring|worshipping|revering|esteeming|prizing|regarding|considering|thinking|believing|feeling|sensing|perceiving|noticing|observing|watching|monitoring|tracking|following|pursuing|chasing|hunting|seeking|searching|looking|uncovering|revealing|exposing|showing|displaying|presenting|demonstrating|illustrating|explaining|clarifying|elucidating|illuminating|enlightening|educating|teaching|instructing|guiding|directing|leading|managing|controlling|handling|dealing|processing|working|operating|functioning|performing|executing|implementing|carrying out|doing|making|creating|building|constructing|developing|designing|planning|organizing|arranging|structuring|forming|shaping|molding|crafting|fashioning|manufacturing|producing|generating)\b',
            r'\b(leveraging|utilizing|using|employing|applying|implementing|executing|performing|carrying out|conducting|undertaking|pursuing|following|adopting|embracing|accepting|taking|receiving|getting|obtaining|acquiring|gaining|earning|winning|achieving|accomplishing|completing|finishing|concluding|ending|terminating|stopping|ceasing|halting|pausing|resting|relaxing|unwinding|decompressing|releasing|letting go|surrendering|yielding|giving up|quitting|abandoning|deserting|forsaking|leaving|departing|going|moving|traveling|journeying|voyaging|exploring|discovering|finding|locating|identifying|recognizing|acknowledging|accepting|embracing|welcoming|greeting|saluting|honoring|respecting|valuing|appreciating|cherishing|treasing|loving|adoring|worshipping|revering|esteeming|prizing|regarding|considering|thinking|believing|feeling|sensing|perceiving|noticing|observing|watching|monitoring|tracking|following|pursuing|chasing|hunting|seeking|searching|looking|uncovering|revealing|exposing|showing|displaying|presenting|demonstrating|illustrating|explaining|clarifying|elucidating|illuminating|enlightening|educating|teaching|instructing|guiding|directing|leading|managing|controlling|handling|dealing|processing|working|operating|functioning|performing|executing|implementing|carrying out|doing|making|creating|building|constructing|developing|designing|planning|organizing|arranging|structuring|forming|shaping|molding|crafting|fashioning|manufacturing|producing|generating)\s+(data|information|knowledge|wisdom|insight|intelligence|facts|figures|statistics|metrics|measurements|observations|findings|results|outcomes|consequences|effects|impacts|influences|powers|forces|strengths|energies|vigors|vitalities|spirits|souls|hearts|minds|brains|intellects|intelligences|wisdoms|knowledges|understandings|comprehensions|grasps|insights|perceptions|awarenesses|consciousnesses|realizations|recognitions|acknowledgments|admissions|confessions|declarations|statements|announcements|proclamations|revelations|disclosures|exposures|unveilings|presentations|introductions|launches|releases|publications|distributions|circulations|disseminations|propagations|spreads|transmissions|broadcasts|telecasts|webcasts|streams|lives|real-times|instants|immediates|prompts|quicks|fasts|rapids|swifts|speedies|hasties|hurrieds|rusheds|urgents|pressings|criticals|importants|significants|notables|remarkables|extraordinaries|exceptionals|outstandings|superiors|excellents|superbs|magnificents|wonderfuls|fantastics|amazings|incredibles|unbelievables|remarkables|notables|significants|importants|vitals|crucials|essentials|necessaries|requireds|mandatories|compulsories|obligatories|indispensables|fundamentals|basics|primaries|principals|mains|chiefs|leadings|foremosts|tops|bests|finests|greatests|highests|maximums|peaks|summits|climaxes|culminations|pinnacles|apexes|zeniths|acmes)\b',
        ]
        
    def initialize_validation_rules(self):
        """Initialize validation rules"""
        self.name_validation = {
            'min_length': 3,
            'max_length': 50,
            'min_words': 2,
            'max_words': 4,
            'must_have_capital': True,
            'exclude_numbers': True,
            'exclude_special_chars': True
        }
        
        self.role_validation = {
            'min_length': 3,
            'max_length': 100,
            'min_words': 1,
            'max_words': 8,
            'must_have_capital': True,
            'exclude_numbers': False,
            'exclude_special_chars': False
        }
    
    def extract_resume_data(self, text: str, filename: str = None) -> Dict[str, Any]:
        """Extract resume data with advanced AI techniques"""
        try:
            logger.info("🚀 Starting advanced accurate resume extraction...")
            
            if not text or len(text.strip()) < 10:
                return self._get_empty_result()
            
            # Clean text
            text_clean = self._clean_text(text)
            
            # Extract with multiple techniques
            name = self._extract_name_advanced(text_clean, filename)
            role = self._extract_role_advanced(text_clean, name)
            email = self._extract_email_advanced(text_clean)
            phone = self._extract_phone_advanced(text_clean)
            skills = self._extract_skills_advanced(text_clean)
            experience = self._extract_experience_advanced(text_clean)
            location = self._extract_location_advanced(text_clean)
            education = self._extract_education_advanced(text_clean)
            
            result = {
                'name': name,
                'role': role,
                'email': email,
                'phone': phone,
                'skills': skills,
                'experience': experience,
                'location': location,
                'education': education,
                'raw_text': text_clean[:500] if text_clean else '',
                'extraction_method': 'advanced_accurate_extraction',
                'confidence_score': self._calculate_confidence(name, role, email, phone),
                'extraction_timestamp': datetime.now().isoformat()
            }
            
            logger.info("✅ Advanced extraction completed")
            logger.info(f"👤 Name: {name}")
            logger.info(f"🎯 Role: {role}")
            logger.info(f"📧 Email: {email}")
            logger.info(f"📱 Phone: {phone}")
            logger.info(f"🛠️ Skills: {len(skills)} skills found")
            
            return result
            
        except Exception as e:
            logger.error(f"❌ Advanced extraction error: {e}")
            return self._get_empty_result()
    
    def _extract_name_advanced(self, text: str, filename: str = None) -> str:
        """Extract name using advanced AI techniques"""
        try:
            logger.info("🔍 Starting advanced name extraction...")
            
            # Strategy 1: Filename extraction (highest priority)
            if filename:
                filename_name = self._extract_name_from_filename(filename)
                if filename_name and self._is_valid_name(filename_name):
                    logger.info(f"✅ Name found in filename: {filename_name}")
                    return filename_name
            
            # Strategy 2: spaCy NER
            if self.nlp:
                doc = self.nlp(text[:2000])
                for ent in doc.ents:
                    if ent.label_ == "PERSON" and len(ent.text.split()) >= 2:
                        name = ent.text.strip()
                        if self._is_valid_name(name):
                            logger.info(f"✅ Name found with spaCy NER: {name}")
                            return name.title()
            
            # Strategy 3: NLTK NER
            try:
                sentences = sent_tokenize(text[:1000])
                for sentence in sentences:
                    words = word_tokenize(sentence)
                    pos_tags = pos_tag(words)
                    chunks = ne_chunk(pos_tags)
                    
                    for chunk in chunks:
                        if hasattr(chunk, 'label') and chunk.label() == 'PERSON':
                            name = ' '.join([token for token, pos in chunk.leaves()])
                            if self._is_valid_name(name):
                                logger.info(f"✅ Name found with NLTK NER: {name}")
                                return name.title()
            except Exception as e:
                logger.warning(f"⚠️ NLTK NER failed: {e}")
            
            # Strategy 4: Pattern matching
            for i, pattern in enumerate(self.name_patterns[3:], 1):  # Skip filename patterns
                matches = re.findall(pattern, text, re.IGNORECASE | re.MULTILINE)
                if matches:
                    for match in matches:
                        name = match.strip()
                        if self._is_valid_name(name):
                            logger.info(f"✅ Name found with pattern {i}: {name}")
                            return name.title()
            
            logger.warning("⚠️ No valid name found")
            return 'Name not found'
            
        except Exception as e:
            logger.error(f"❌ Advanced name extraction error: {e}")
            return 'Name not found'
    
    def _extract_role_advanced(self, text: str, name: str = None) -> str:
        """Extract role using advanced AI techniques"""
        try:
            logger.info("🔍 Starting advanced role extraction...")
            
            # Remove name from text to avoid false matches
            text_for_role = text
            if name and name != 'Name not found':
                text_for_role = text_for_role.replace(name, '')
            
            # Strategy 1: Exact job title matches
            for i, pattern in enumerate(self.role_patterns):
                matches = re.findall(pattern, text_for_role, re.IGNORECASE)
                if matches:
                    for match in matches:
                        role = match.strip()
                        if self._is_valid_role(role):
                            logger.info(f"✅ Role found with pattern {i+1}: {role}")
                            return role.title()
            
            # Strategy 2: Skills-based inference
            inferred_role = self._infer_role_from_skills(text_for_role)
            if inferred_role:
                logger.info(f"✅ Role inferred from skills: {inferred_role}")
                return inferred_role
            
            logger.warning("⚠️ No valid role found")
            return 'Role not found'
            
        except Exception as e:
            logger.error(f"❌ Advanced role extraction error: {e}")
            return 'Role not found'
    
    def _extract_name_from_filename(self, filename: str) -> str:
        """Extract name from filename with advanced patterns"""
        try:
            name_part = os.path.splitext(filename)[0]
            logger.info(f"🔍 Extracting name from filename: {name_part}")
            
            # Try different patterns in order of priority
            patterns = [
                r'([A-Z][a-z]+_[A-Z][a-z]+(?:_[A-Z][a-z]+)?)',  # Underscore names
                r'([A-Z][a-z]+-[A-Z][a-z]+(?:-[A-Z][a-z]+)?)',  # Hyphen names
                r'([A-Z][a-z]+ [A-Z][a-z]+(?: [A-Z][a-z]+)?)',  # Space names
            ]
            
            for i, pattern in enumerate(patterns):
                match = re.search(pattern, name_part)
                if match:
                    extracted_name = match.group(1).strip()
                    # Clean up the name
                    extracted_name = extracted_name.replace('_', ' ').replace('-', ' ')
                    extracted_name = ' '.join(word.capitalize() for word in extracted_name.split())
                    logger.info(f"✅ Name extracted with pattern {i+1}: {extracted_name}")
                    return extracted_name
            
            return None
            
        except Exception as e:
            logger.error(f"❌ Filename name extraction error: {e}")
            return None
    
    def _infer_role_from_skills(self, text: str) -> str:
        """Infer role from skills mentioned"""
        try:
            # Enhanced skill-to-role mappings
            skill_role_mapping = {
                'full stack java': 'Full Stack Java Developer',
                'java': 'Java Developer',
                'python': 'Python Developer',
                'javascript': 'JavaScript Developer',
                'react': 'React Developer',
                'angular': 'Angular Developer',
                'node': 'Node.js Developer',
                'spring': 'Spring Developer',
                'django': 'Django Developer',
                'flask': 'Flask Developer',
                'sql': 'Database Developer',
                'mysql': 'Database Developer',
                'mongodb': 'Database Developer',
                'aws': 'Cloud Engineer',
                'azure': 'Cloud Engineer',
                'docker': 'DevOps Engineer',
                'kubernetes': 'DevOps Engineer',
                'machine learning': 'Machine Learning Engineer',
                'data science': 'Data Scientist',
                'artificial intelligence': 'AI Engineer',
                'full stack': 'Full Stack Developer',
                'frontend': 'Frontend Developer',
                'backend': 'Backend Developer',
                'web': 'Web Developer',
                'mobile': 'Mobile Developer',
                'devops': 'DevOps Engineer',
                'data analyst': 'Data Analyst',
                'business analyst': 'Business Analyst',
                'product manager': 'Product Manager',
                'project manager': 'Project Manager',
                'ui/ux': 'UI/UX Designer',
                'qa': 'QA Engineer',
                'test': 'Test Engineer',
            }
            
            text_lower = text.lower()
            for skill, role in skill_role_mapping.items():
                if skill in text_lower:
                    return role
            
            return None
            
        except Exception as e:
            logger.error(f"❌ Skill-based role inference error: {e}")
            return None
    
    def _extract_email_advanced(self, text: str) -> str:
        """Extract email using advanced patterns"""
        try:
            email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            matches = re.findall(email_pattern, text)
            if matches:
                return matches[0]
            return 'Email not found'
        except Exception as e:
            logger.error(f"❌ Email extraction error: {e}")
            return 'Email not found'
    
    def _extract_phone_advanced(self, text: str) -> str:
        """Extract phone using advanced patterns"""
        try:
            phone_patterns = [
                r'\b\d{10}\b',  # 10 digits
                r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',  # US format
                r'\b\+\d{1,3}[-.\s]?\d{1,4}[-.\s]?\d{1,4}[-.\s]?\d{1,9}\b',  # International
            ]
            
            for pattern in phone_patterns:
                matches = re.findall(pattern, text)
                if matches:
                    return matches[0]
            return 'Phone not found'
        except Exception as e:
            logger.error(f"❌ Phone extraction error: {e}")
            return 'Phone not found'
    
    def _extract_skills_advanced(self, text: str) -> List[str]:
        """Extract skills using advanced techniques"""
        try:
            # Common technical skills
            common_skills = [
                'Java', 'Python', 'JavaScript', 'React', 'Angular', 'Vue', 'Node.js',
                'Spring', 'Django', 'Flask', 'Laravel', 'Ruby on Rails', 'PHP',
                'C#', 'C++', 'Go', 'Rust', 'Swift', 'Kotlin', 'Flutter',
                'React Native', 'Android', 'iOS', 'HTML', 'CSS', 'Bootstrap',
                'SQL', 'MySQL', 'PostgreSQL', 'MongoDB', 'Redis', 'Elasticsearch',
                'AWS', 'Azure', 'GCP', 'Docker', 'Kubernetes', 'Jenkins',
                'Git', 'GitHub', 'GitLab', 'Jira', 'Confluence', 'Agile',
                'Scrum', 'DevOps', 'CI/CD', 'REST API', 'GraphQL', 'Microservices',
                'Machine Learning', 'Data Science', 'TensorFlow', 'PyTorch',
                'Power BI', 'Tableau', 'Excel', 'R', 'SAS', 'SPSS'
            ]
            
            text_lower = text.lower()
            found_skills = []
            
            for skill in common_skills:
                if skill.lower() in text_lower:
                    found_skills.append(skill)
            
            return found_skills
            
        except Exception as e:
            logger.error(f"❌ Skills extraction error: {e}")
            return []
    
    def _extract_experience_advanced(self, text: str) -> Dict[str, Any]:
        """Extract experience using advanced techniques"""
        try:
            # Look for experience patterns with decimal support
            experience_patterns = [
                r'(\d+\.?\d*)\s*years?\s*(?:of\s*)?experience',
                r'experience\s*(?:of\s*)?(\d+\.?\d*)\s*years?',
                r'(\d+\.?\d*)\s*years?\s*(?:in|with)',
                r'(\d+\.?\d*)\s*years?\s*(?:of\s*)?(?:professional|work|industry)',
                r'(\d+\.?\d*)\s*years?\s*(?:of\s*)?(?:software|development|engineering)',
            ]
            
            for pattern in experience_patterns:
                match = re.search(pattern, text, re.IGNORECASE)
                if match:
                    years_str = match.group(1)
                    years = float(years_str)
                    months = int(years * 12)
                    
                    # Format display based on decimal or whole number
                    if years == int(years):
                        display = f'{int(years)} years'
                    else:
                        display = f'{years} years'
                    
                    return {
                        'total_years': years,
                        'total_months': months,
                        'display': display if years > 0 else 'Fresher (0 years)',
                        'is_fresher': years == 0,
                        'experience_periods': [],
                        'extraction_method': 'pattern_matching'
                    }
            
            # Look for specific experience mentions in context
            context_patterns = [
                r'(?:with|having|over)\s+(\d+\.?\d*)\s*years?\s*(?:of\s*)?(?:experience|experience in)',
                r'(\d+\.?\d*)\s*years?\s*(?:of\s*)?(?:relevant|total|overall)',
            ]
            
            for pattern in context_patterns:
                match = re.search(pattern, text, re.IGNORECASE)
                if match:
                    years_str = match.group(1)
                    years = float(years_str)
                    months = int(years * 12)
                    
                    if years == int(years):
                        display = f'{int(years)} years'
                    else:
                        display = f'{years} years'
                    
                    return {
                        'total_years': years,
                        'total_months': months,
                        'display': display if years > 0 else 'Fresher (0 years)',
                        'is_fresher': years == 0,
                        'experience_periods': [],
                        'extraction_method': 'context_matching'
                    }
            
            # Default to fresher if no experience found
            return {
                'total_years': 0,
                'total_months': 0,
                'display': 'Fresher (0 years)',
                'is_fresher': True,
                'experience_periods': [],
                'extraction_method': 'fresher_detection'
            }
            
        except Exception as e:
            logger.error(f"❌ Experience extraction error: {e}")
            return {
                'total_years': 0,
                'total_months': 0,
                'display': 'Experience not found',
                'is_fresher': True,
                'experience_periods': [],
                'extraction_method': 'error'
            }
    
    def _extract_location_advanced(self, text: str) -> str:
        """Extract location using advanced techniques"""
        try:
            # Common location patterns
            location_patterns = [
                r'\b(?:located in|based in|from|lives in|resides in)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)',
                r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s*,\s*[A-Z]{2}\b',  # City, State
                r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s*,\s*[A-Z][a-z]+\b',  # City, Country
            ]
            
            for pattern in location_patterns:
                match = re.search(pattern, text, re.IGNORECASE)
                if match:
                    return match.group(1).strip()
            
            return 'Location not found'
            
        except Exception as e:
            logger.error(f"❌ Location extraction error: {e}")
            return 'Location not found'
    
    def _extract_education_advanced(self, text: str) -> List[Dict[str, str]]:
        """Extract education using advanced techniques"""
        try:
            education = []
            
            # Look for degree patterns
            degree_patterns = [
                r'\b(Bachelor|Master|PhD|Doctorate|Associate|Diploma|Certificate)\s+(?:of|in)\s+([A-Za-z\s]+)',
                r'\b([A-Za-z\s]+)\s+(?:Bachelor|Master|PhD|Doctorate|Associate|Diploma|Certificate)',
            ]
            
            for pattern in degree_patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                for match in matches:
                    education.append({
                        'degree': match[0] if len(match) > 1 else match,
                        'institution': 'Not specified',
                        'year': 'Not specified'
                    })
            
            return education if education else [{
                'degree': 'Not specified',
                'institution': 'Not specified',
                'year': 'Not specified'
            }]
            
        except Exception as e:
            logger.error(f"❌ Education extraction error: {e}")
            return [{
                'degree': 'Not specified',
                'institution': 'Not specified',
                'year': 'Not specified'
            }]
    
    def _is_valid_name(self, name: str) -> bool:
        """Validate if extracted text is a valid name"""
        try:
            if not name or len(name.strip()) < self.name_validation['min_length']:
                return False
            
            name = name.strip()
            
            # Check length
            if len(name) > self.name_validation['max_length']:
                return False
            
            # Check word count
            words = name.split()
            if len(words) < self.name_validation['min_words'] or len(words) > self.name_validation['max_words']:
                return False
            
            # Check for capital letters
            if self.name_validation['must_have_capital'] and not any(c.isupper() for c in name):
                return False
            
            # Check for numbers
            if self.name_validation['exclude_numbers'] and any(c.isdigit() for c in name):
                return False
            
            # Check for special characters
            if self.name_validation['exclude_special_chars'] and not name.replace(' ', '').replace('-', '').replace("'", '').isalpha():
                return False
            
            # Check exclusions
            for exclusion in self.name_exclusions:
                if re.search(exclusion, name, re.IGNORECASE):
                    return False
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Name validation error: {e}")
            return False
    
    def _is_valid_role(self, role: str) -> bool:
        """Validate if extracted text is a valid role"""
        try:
            if not role or len(role.strip()) < self.role_validation['min_length']:
                return False
            
            role = role.strip()
            
            # Check length
            if len(role) > self.role_validation['max_length']:
                return False
            
            # Check word count
            words = role.split()
            if len(words) < self.role_validation['min_words'] or len(words) > self.role_validation['max_words']:
                return False
            
            # Check for capital letters
            if self.role_validation['must_have_capital'] and not any(c.isupper() for c in role):
                return False
            
            # Check exclusions
            for exclusion in self.role_exclusions:
                if re.search(exclusion, role, re.IGNORECASE):
                    return False
            
            # Check if it contains actual job title keywords
            job_keywords = [
                'developer', 'engineer', 'programmer', 'analyst', 'consultant', 'specialist',
                'architect', 'manager', 'director', 'lead', 'coordinator', 'administrator',
                'designer', 'writer', 'editor', 'researcher', 'scientist', 'technician',
                'operator', 'supervisor', 'executive', 'officer', 'assistant', 'associate',
                'intern', 'trainee', 'apprentice', 'junior', 'senior', 'principal', 'staff'
            ]
            
            role_lower = role.lower()
            has_job_keyword = any(keyword in role_lower for keyword in job_keywords)
            
            if not has_job_keyword:
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Role validation error: {e}")
            return False
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        try:
            # Remove extra whitespace
            text = re.sub(r'\s+', ' ', text.strip())
            
            # Remove special characters that might interfere
            text = re.sub(r'[^\w\s@.-]', ' ', text)
            
            return text
            
        except Exception as e:
            logger.error(f"❌ Text cleaning error: {e}")
            return text
    
    def _calculate_confidence(self, name: str, role: str, email: str, phone: str) -> float:
        """Calculate confidence score"""
        try:
            confidence = 0.0
            
            # Name confidence
            if name and name != 'Name not found':
                confidence += 0.3
            
            # Role confidence
            if role and role != 'Role not found':
                confidence += 0.3
            
            # Email confidence
            if email and email != 'Email not found':
                confidence += 0.2
            
            # Phone confidence
            if phone and phone != 'Phone not found':
                confidence += 0.2
            
            return confidence
            
        except Exception as e:
            logger.error(f"❌ Confidence calculation error: {e}")
            return 0.0
    
    def _get_empty_result(self) -> Dict[str, Any]:
        """Return empty result structure"""
        return {
            'name': 'Name not found',
            'email': 'Email not found',
            'phone': 'Phone not found',
            'skills': [],
            'experience': {'total_years': 0, 'total_months': 0, 'display': 'Experience not found'},
            'role': 'Role not found',
            'location': 'Location not found',
            'education': [],
            'raw_text': '',
            'extraction_method': 'advanced_accurate_extraction_error',
            'confidence_score': 0.0,
            'extraction_timestamp': datetime.now().isoformat()
        }

# Initialize the extractor
advanced_accurate_extractor = AdvancedAccurateExtractor()
