"""
Precise Name and Role Extractor
Highly accurate extraction focusing on actual names and job titles
"""

import re
import logging
import os
from typing import Dict, List, Any, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

class PreciseNameRoleExtractor:
    """Highly precise extractor for names and roles from resumes"""
    
    def __init__(self):
        self.initialize_patterns()
        self.initialize_validation_rules()
        
    def initialize_patterns(self):
        """Initialize highly precise extraction patterns"""
        
        # PRECISE NAME PATTERNS - Focus on actual person names
        self.name_patterns = [
            # 1. Filename-based extraction (highest priority)
            r'^([A-Z][a-z]+ [A-Z][a-z]+(?: [A-Z][a-z]+)?)',  # Title Case names from filename
            
            # 2. Header patterns - first line of resume
            r'^([A-Z][a-z]+ [A-Z][a-z]+(?: [A-Z][a-z]+)?)\s*\n',  # Title Case at start
            
            # 3. Before contact information
            r'^([A-Z][a-z]+ [A-Z][a-z]+(?: [A-Z][a-z]+)?)\s*\n\s*(?:Email|Phone|Address|Contact)',
            
            # 4. Before professional sections
            r'^([A-Z][a-z]+ [A-Z][a-z]+(?: [A-Z][a-z]+)?)\s*\n\s*(?:PROFILE|Profile|About|Summary|OBJECTIVE|Objective)',
            
            # 5. Contact section patterns
            r'(?:Name|Full Name|Contact Name)[:\s]*([A-Z][a-z]+ [A-Z][a-z]+(?: [A-Z][a-z]+)?)',
            
            # 6. After email/phone patterns
            r'(?:Email|Phone|Address)[:\s]*[^\n]*\n\s*([A-Z][a-z]+ [A-Z][a-z]+(?: [A-Z][a-z]+)?)',
        ]
        
        # EXCLUSION PATTERNS - Words that should NOT be considered as names
        self.name_exclusions = [
            r'\b(TCS|IBM|Microsoft|Google|Amazon|Apple|Facebook|LinkedIn|Twitter|Instagram|YouTube|Netflix|Uber|Airbnb|Tesla|SpaceX|Oracle|SAP|Salesforce|Adobe|Intel|NVIDIA|AMD|Cisco|VMware|Red Hat|MongoDB|Elastic|Databricks|Snowflake|Palantir|ServiceNow|Workday|Atlassian|Slack|Zoom|Dropbox|Box|GitHub|GitLab|Bitbucket|Jenkins|Docker|Kubernetes|Terraform|Ansible|Chef|Puppet|Nagios|Splunk|New Relic|DataDog|PagerDuty|Twilio|Stripe|Square|PayPal|Venmo|Coinbase|Binance|Kraken|Robinhood|E\*TRADE|Fidelity|Charles Schwab|Vanguard|BlackRock|Goldman Sachs|JPMorgan|Morgan Stanley|Bank of America|Wells Fargo|Citigroup|American Express|Visa|Mastercard|Discover|Capital One|Chase|USAA|Navy Federal|Pentagon Federal|Alliant|Ally Bank|Marcus|SoFi|Betterment|Wealthfront|Acorns|Stash|M1 Finance|TD Ameritrade|Interactive Brokers)\b',
            r'\b(Recognition|Award|Certificate|Certification|Achievement|Honor|Distinction|Excellence|Outstanding|Merit|Commendation|Appreciation|Gratitude|Thanks|Acknowledgement|Tribute|Praise|Accolade|Laurel|Crown|Medal|Trophy|Plaque|Diploma|Degree|Bachelor|Master|PhD|Doctorate|Associate|License|Credential|Qualification|Competency|Proficiency|Expertise|Mastery|Skill|Ability|Talent|Gift|Capability|Capacity|Potential|Aptitude|Intelligence|Wisdom|Knowledge|Understanding|Comprehension|Grasp|Insight|Perception|Awareness|Consciousness|Realization|Acknowledgment|Admission|Confession|Declaration|Statement|Announcement|Proclamation|Revelation|Disclosure|Exposure|Unveiling|Presentation|Introduction|Launch|Release|Publication|Distribution|Circulation|Dissemination|Propagation|Spread|Transmission|Broadcast|Telecast|Webcast|Stream|Live|Real-time|Instant|Immediate|Prompt|Quick|Fast|Rapid|Swift|Speedy|Hasty|Hurried|Rushed|Urgent|Pressing|Critical|Important|Significant|Notable|Remarkable|Extraordinary|Exceptional|Superior|Excellent|Superb|Magnificent|Wonderful|Fantastic|Amazing|Incredible|Unbelievable|Vital|Crucial|Essential|Necessary|Required|Mandatory|Compulsory|Obligatory|Indispensable|Fundamental|Basic|Primary|Principal|Main|Chief|Leading|Foremost|Top|Best|Finest|Greatest|Highest|Maximum|Peak|Summit|Climax|Culmination|Pinnacle|Apex|Zenith|Acme)\b',
            r'\b(Passionate|Dedicated|Committed|Devoted|Loyal|Faithful|True|Genuine|Authentic|Real|Actual|Honest|Sincere|Candid|Frank|Open|Transparent|Clear|Obvious|Evident|Apparent|Visible|Noticeable|Observable|Perceptible|Detectable|Recognizable|Identifiable|Distinguishable|Discernible|Distinct|Sharp|Focused|Concentrated|Intense|Strong|Powerful|Mighty|Forceful|Robust|Sturdy|Solid|Firm|Steady|Stable|Reliable|Dependable|Trustworthy|Credible|Believable|Convincing|Persuasive|Compelling|Attractive|Appealing|Charming|Engaging|Captivating|Fascinating|Interesting|Intriguing|Exciting|Thrilling|Stimulating|Inspiring|Motivating|Encouraging|Uplifting|Energizing|Invigorating|Refreshing|Revitalizing|Rejuvenating|Renewing|Restoring|Healing|Therapeutic|Beneficial|Advantageous|Profitable|Rewarding|Fruitful|Productive|Effective|Efficient|Successful|Victorious|Triumphant|Winning|Achieving|Accomplishing|Completing|Finishing|Concluding|Ending|Terminating|Stopping|Ceasing|Halting|Pausing|Resting|Relaxing|Unwinding|Decompressing|Releasing|Letting go|Surrendering|Yielding|Giving up|Quitting|Abandoning|Deserting|Forsaking|Leaving|Departing|Going|Moving|Traveling|Journeying|Voyaging|Exploring|Discovering|Finding|Locating|Identifying|Recognizing|Acknowledging|Accepting|Embracing|Welcoming|Greeting|Saluting|Honoring|Respecting|Valuing|Appreciating|Cherishing|Treasing|Loving|Adoring|Worshipping|Revering|Esteeming|Prizing|Regarding|Considering|Thinking|Believing|Feeling|Sensing|Perceiving|Noticing|Observing|Watching|Monitoring|Tracking|Following|Pursuing|Chasing|Hunting|Seeking|Searching|Looking|Uncovering|Revealing|Exposing|Showing|Displaying|Presenting|Demonstrating|Illustrating|Explaining|Clarifying|Elucidating|Illuminating|Enlightening|Educating|Teaching|Instructing|Guiding|Directing|Leading|Managing|Controlling|Handling|Dealing|Processing|Working|Operating|Functioning|Performing|Executing|Implementing|Carrying out|Doing|Making|Creating|Building|Constructing|Developing|Designing|Planning|Organizing|Arranging|Structuring|Forming|Shaping|Molding|Crafting|Fashioning|Manufacturing|Producing|Generating)\b'
        ]
        
        # PRECISE ROLE PATTERNS - Focus on actual job titles
        self.role_patterns = [
            # 1. Exact job title matches (highest priority)
            r'\b(Software Engineer|Software Developer|Full Stack Developer|Frontend Developer|Backend Developer|Web Developer|Mobile Developer|DevOps Engineer|Data Scientist|Data Analyst|Machine Learning Engineer|AI Engineer|Cloud Engineer|Security Engineer|QA Engineer|Test Engineer|UI/UX Designer|Product Manager|Project Manager|Technical Lead|Team Lead|Solution Architect|System Architect|Database Administrator|Network Administrator|System Administrator|Business Analyst|System Analyst|Technical Writer|Scrum Master|Agile Coach|Engineering Manager|Development Manager|IT Manager|CTO|VP of Engineering|Director of Engineering)\b',
            
            # 2. Seniority + Technology combinations
            r'\b(Senior|Lead|Principal|Staff|Senior Staff|Principal Staff|Distinguished|Fellow)\s+(Software Engineer|Software Developer|Full Stack Developer|Frontend Developer|Backend Developer|Web Developer|Mobile Developer|DevOps Engineer|Data Scientist|Data Analyst|Machine Learning Engineer|AI Engineer|Cloud Engineer|Security Engineer|QA Engineer|Test Engineer|UI/UX Designer|Product Manager|Project Manager|Technical Lead|Team Lead|Solution Architect|System Architect|Database Administrator|Network Administrator|System Administrator|Business Analyst|System Analyst|Technical Writer|Scrum Master|Agile Coach|Engineering Manager|Development Manager|IT Manager)\b',
            
            # 3. Technology-specific roles
            r'\b(Java Developer|Python Developer|JavaScript Developer|React Developer|Angular Developer|Vue Developer|Node\.js Developer|Spring Boot Developer|Django Developer|Flask Developer|Laravel Developer|Ruby on Rails Developer|PHP Developer|C# Developer|C\+\+ Developer|Go Developer|Rust Developer|Swift Developer|Kotlin Developer|Flutter Developer|React Native Developer|Android Developer|iOS Developer)\b',
            
            # 4. Experience-based roles
            r'\b(Junior|Entry Level|Associate|Mid Level|Senior|Lead|Principal|Staff|Senior Staff|Principal Staff|Distinguished|Fellow)\s+(Developer|Engineer|Programmer|Analyst|Consultant|Specialist|Architect|Manager|Director)\b',
            
            # 5. Industry-specific roles
            r'\b(FinTech|HealthTech|EdTech|PropTech|RetailTech|TravelTech|FoodTech|AgriTech|CleanTech|BioTech|MedTech|AutoTech|AeroTech|SpaceTech|DefenseTech|GovTech|LegalTech|HRTech|MarTech|AdTech|GameTech|SportsTech|FashionTech|BeautyTech|WellnessTech|FitnessTech|PetTech|HomeTech|Smart Home|IoT|Blockchain|Cryptocurrency|NFT|Web3|Metaverse|AR|VR|XR|AI|ML|DL|NLP|Computer Vision|Robotics|Automation|RPA|Process Automation|Business Process Automation|Workflow Automation|Test Automation|DevOps|SRE|Platform Engineering|Cloud Engineering|Infrastructure Engineering|Site Reliability Engineering|Performance Engineering|Security Engineering|Compliance Engineering|Quality Engineering|Release Engineering|Build Engineering|Deployment Engineering|Configuration Management|Infrastructure as Code|Container Orchestration|Microservices|API Development|Integration|ETL|Data Engineering|Data Pipeline|Data Warehouse|Data Lake|Data Mesh|Data Fabric|Data Governance|Data Quality|Data Privacy|Data Security|Data Analytics|Business Intelligence|Data Visualization|Reporting|Dashboard|KPI|Metrics|Analytics|Insights|Intelligence|Optimization|Personalization|Recommendation|Search|Discovery|Content Management|Document Management|Knowledge Management|Learning Management|Customer Relationship Management|Enterprise Resource Planning|Supply Chain Management|Human Resource Management|Financial Management|Project Management|Portfolio Management|Risk Management|Compliance Management|Vendor Management|Contract Management|Asset Management|Inventory Management|Order Management|Payment Processing|Billing|Invoicing|Accounting|Finance|Treasury|Audit|Tax|Legal|Regulatory|Compliance|Governance|Security|Privacy|Risk|Fraud|Anti-Money Laundering|Know Your Customer|Customer Due Diligence|Enhanced Due Diligence|Sanctions|Embargo|Export Control|Trade Compliance|Environmental|Health and Safety|Quality|ISO|Six Sigma|Lean|Agile|Scrum|Kanban|SAFe|LeSS|Nexus|Disciplined Agile|Scaled Agile|Enterprise Agile|Business Agility|Digital Transformation|Digital Innovation|Digital Strategy|Digital Marketing|Digital Sales|Digital Commerce|E-commerce|Online Retail|Marketplace|Platform|SaaS|PaaS|IaaS|FaaS|Serverless|Cloud Native|Cloud First|Multi-Cloud|Hybrid Cloud|Edge Computing|Fog Computing|Quantum Computing|High Performance Computing|Distributed Computing|Parallel Computing|Grid Computing|Cluster Computing|Supercomputing|Mainframe|Legacy Systems|Modernization|Migration|Transformation|Integration|API|Microservices|Service Mesh|Event Driven|Message Queue|Stream Processing|Batch Processing|Real-time Processing|Near Real-time Processing|Lambda Architecture|Kappa Architecture|Data Streaming|Event Streaming|Change Data Capture|Database Replication|Data Synchronization|Data Consistency|ACID|BASE|CAP Theorem|Eventual Consistency|Strong Consistency|Weak Consistency|Read Consistency|Write Consistency|Transaction|Distributed Transaction|Two-Phase Commit|Saga Pattern|CQRS|Event Sourcing|Domain Driven Design|Hexagonal Architecture|Clean Architecture|Onion Architecture|Layered Architecture|MVC|MVP|MVVM|MVI|Flux|Redux|Vuex|NgRx|Akka|Actor Model|Reactive Programming|Functional Programming|Object-Oriented Programming|Procedural Programming|Imperative Programming|Declarative Programming|Logic Programming|Constraint Programming|Concurrent Programming|Parallel Programming|Asynchronous Programming|Synchronous Programming|Blocking|Non-blocking|Callback|Promise|Future|Async/Await|Coroutine|Generator|Iterator|Stream|Pipeline|Chain|Composition|Monad|Functor|Applicative|Semigroup|Monoid|Group|Ring|Field|Vector|Matrix|Tensor|Graph|Tree|Heap|Stack|Queue|Deque|List|Array|Set|Map|Dictionary|Hash Table|Bloom Filter|Trie|Suffix Tree|Suffix Array|B-Tree|B+ Tree|Red-Black Tree|AVL Tree|Splay Tree|Skip List|Linked List|Doubly Linked List|Circular Linked List|Static Array|Dynamic Array|Resizable Array|Gap Buffer|Rope|String|Text|Document|File|Directory|Folder|Path|URL|URI|URN|HTTP|HTTPS|FTP|SFTP|SSH|Telnet|SMTP|POP3|IMAP|DNS|DHCP|NTP|SNMP|LDAP|Kerberos|OAuth|SAML|JWT|OpenID|OpenID Connect|SAML|WS-Federation|WS-Trust|WS-Security|XML|JSON|YAML|TOML|INI|CSV|TSV|XML|HTML|XHTML|SVG|CSS|SCSS|SASS|Less|Stylus|PostCSS|Autoprefixer|Babel|Webpack|Rollup|Parcel|Vite|Snowpack|Esbuild|SWC|Terser|UglifyJS|Closure Compiler|TypeScript|Flow|ReasonML|Elm|PureScript|Haskell|Clojure|ClojureScript|Scala|F#|OCaml|Standard ML|Racket|Scheme|Common Lisp|Emacs Lisp|AutoLisp|Visual Lisp|Maxima|Axiom|Magma|GAP|SageMath|Mathematica|Maple|MATLAB|Octave|Scilab|R|Julia|Python|NumPy|SciPy|Pandas|Matplotlib|Seaborn|Plotly|Bokeh|Altair|Vega|D3.js|Observable|Jupyter|IPython|Colab|Kaggle|Paperspace|Gradient|Floyd|Crestle|Deepnote|CoCalc|SageMathCloud|Wolfram Cloud|Mathematica Online|Maple Cloud|MATLAB Online|Octave Online|RStudio Cloud|Posit Cloud|Anaconda Cloud|Conda|Pip|Poetry|Pipenv|Virtualenv|Conda|Mamba|Spack|Homebrew|Chocolatey|Scoop|Nix|Guix|Flatpak|Snap|AppImage|Docker|Podman|LXC|LXD|Kubernetes|Docker Swarm|Nomad|Mesos|Marathon|DC/OS|OpenShift|Rancher|K3s|K0s|MicroK8s|Kind|Minikube|Docker Desktop|Colima|Lima|OrbStack|Podman Desktop|Rancher Desktop|Kitematic|Portainer|Docker Compose|Docker Swarm|Kubernetes|Helm|Kustomize|Skaffold|Tilt|Garden|DevSpace|Okteto|Telepresence|Squash|Bridge|Kubefwd|Kubectl|Kubectx|Kubens|Kube-ps1|Kube-prompt|Kube-shell|Kubie|Kubectl-aliases|Kubectl-plugins|Krew|Kubectl-tree|Kubectl-grep|Kubectl-neat|Kubectl-iexec|Kubectl-debug|Kubectl-trace|Kubectl-top|Kubectl-logs|Kubectl-describe|Kubectl-get|Kubectl-create|Kubectl-apply|Kubectl-delete|Kubectl-patch|Kubectl-replace|Kubectl-edit|Kubectl-scale|Kubectl-rollout|Kubectl-expose|Kubectl-port-forward|Kubectl-proxy|Kubectl-cp|Kubectl-exec|Kubectl-attach|Kubectl-run|Kubectl-wait|Kubectl-diff|Kubectl-convert|Kubectl-version|Kubectl-cluster-info|Kubectl-config|Kubectl-auth|Kubectl-certificate|Kubectl-drain|Kubectl-uncordon|Kubectl-taint|Kubectl-untaint|Kubectl-label|Kubectl-annotate|Kubectl-completion|Kubectl-plugin|Kubectl-api-resources|Kubectl-api-versions|Kubectl-explain|Kubectl-options|Kubectl-help|Kubectl-version|Kubectl-cluster-info|Kubectl-config|Kubectl-auth|Kubectl-certificate|Kubectl-drain|Kubectl-uncordon|Kubectl-taint|Kubectl-untaint|Kubectl-label|Kubectl-annotate|Kubectl-completion|Kubectl-plugin|Kubectl-api-resources|Kubectl-api-versions|Kubectl-explain|Kubectl-options|Kubectl-help)\s+(Developer|Engineer|Programmer|Analyst|Consultant|Specialist|Architect|Manager|Director)\b',
            
            # 6. Work experience context
            r'(?:worked as|position of|role of|designation of|currently working as|presently working as|employed as|served as|acted as|functioned as|operated as|performed as|executed as|carried out as|fulfilled as|discharged as|exercised as|practiced as|engaged as|involved as|participated as|contributed as|assisted as|supported as|helped as|aided as|facilitated as|enabled as|empowered as|authorized as|delegated as|assigned as|appointed as|designated as|nominated as|selected as|chosen as|picked as|elected as|voted as|approved as|endorsed as|recommended as|suggested as|proposed as|offered as|presented as|introduced as|launched as|released as|published as|distributed as|circulated as|disseminated as|propagated as|spread as|transmitted as|broadcast as|telecast as|webcast as|streamed as|live as|real-time as|instant as|immediate as|prompt as|quick as|fast as|rapid as|swift as|speedy as|hasty as|hurried as|rushed as|urgent as|pressing as|critical as|important as|significant as|notable as|remarkable as|extraordinary as|exceptional as|outstanding as|superior as|excellent as|superb as|magnificent as|wonderful as|fantastic as|amazing as|incredible as|unbelievable as|remarkable as|notable as|significant as|important as|vital as|crucial as|essential as|necessary as|required as|mandatory as|compulsory as|obligatory as|indispensable as|fundamental as|basic as|primary as|principal as|main as|chief as|leading as|foremost as|top as|best as|finest as|greatest as|highest as|maximum as|peak as|summit as|climax as|culmination as|pinnacle as|apex as|zenith as|acme as)\s+([A-Za-z\s]{3,50})',
            
            # 7. Job title context
            r'(?:job title|position|role|title|designation|post|office|appointment|assignment|commission|mandate|charge|responsibility|duty|function|task|work|employment|occupation|profession|career|vocation|calling|trade|craft|skill|art|science|discipline|field|domain|area|sector|industry|business|enterprise|organization|company|corporation|firm|establishment|institution|agency|bureau|department|division|section|unit|team|group|crew|squad|gang|band|party|faction|clique|circle|set|class|category|type|kind|sort|variety|species|genus|family|order|phylum|kingdom|domain|realm|sphere|world|universe|cosmos|creation|nature|reality|existence|being|life|living|alive|animate|organic|biological|physical|material|tangible|concrete|solid|firm|hard|soft|smooth|rough|coarse|fine|delicate|fragile|brittle|strong|weak|powerful|mighty|forceful|robust|sturdy|durable|lasting|permanent|temporary|transient|fleeting|brief|short|long|extended|prolonged|protracted|drawn out|stretched|expanded|enlarged|increased|decreased|reduced|diminished|lessened|lowered|raised|elevated|lifted|hoisted|boosted|enhanced|improved|better|worse|superior|inferior|higher|lower|upper|lower|top|bottom|first|last|beginning|end|start|finish|commence|conclude|initiate|terminate|launch|land|take off|touch down|depart|arrive|leave|stay|remain|continue|persist|endure|survive|thrive|flourish|prosper|succeed|fail|win|lose|victory|defeat|triumph|disaster|success|failure|achievement|accomplishment|completion|finish|end|conclusion|result|outcome|consequence|effect|impact|influence|power|force|strength|energy|vigor|vitality|spirit|soul|heart|mind|brain|intellect|intelligence|wisdom|knowledge|understanding|comprehension|grasp|insight|perception|awareness|consciousness|realization|recognition|acknowledgment|admission|confession|declaration|statement|announcement|proclamation|revelation|disclosure|exposure|unveiling|presentation|introduction|launch|release|publication|distribution|circulation|dissemination|propagation|spread|transmission|broadcast|telecast|webcast|stream|live|real-time|instant|immediate|prompt|quick|fast|rapid|swift|speedy|hasty|hurried|rushed|urgent|pressing|critical|important|significant|notable|remarkable|extraordinary|exceptional|outstanding|superior|excellent|superb|magnificent|wonderful|fantastic|amazing|incredible|unbelievable|remarkable|notable|significant|important|vital|crucial|essential|necessary|required|mandatory|compulsory|obligatory|indispensable|fundamental|basic|primary|principal|main|chief|leading|foremost|top|best|finest|greatest|highest|maximum|peak|summit|climax|culmination|pinnacle|apex|zenith|acme)[:\s]*([A-Za-z\s]{3,50})',
        ]
        
        # ROLE EXCLUSION PATTERNS - Phrases that should NOT be considered as roles
        self.role_exclusions = [
            r'\b(Passionate about|Dedicated to|Committed to|Devoted to|Loyal to|Faithful to|True to|leveraging|utilizing|using|employing|applying|implementing|executing|performing|carrying out|conducting|undertaking|pursuing|following|adopting|embracing|accepting|taking|receiving|getting|obtaining|acquiring|gaining|earning|winning|achieving|accomplishing|completing|finishing|concluding|ending|terminating|stopping|ceasing|halting|pausing|resting|relaxing|unwinding|decompressing|releasing|letting go|surrendering|yielding|giving up|quitting|abandoning|deserting|forsaking|leaving|departing|going|moving|traveling|journeying|voyaging|exploring|discovering|finding|locating|identifying|recognizing|acknowledging|accepting|embracing|welcoming|greeting|saluting|honoring|respecting|valuing|appreciating|cherishing|treasing|loving|adoring|worshipping|revering|esteeming|prizing|regarding|considering|thinking|believing|feeling|sensing|perceiving|noticing|observing|watching|monitoring|tracking|following|pursuing|chasing|hunting|seeking|searching|looking|uncovering|revealing|exposing|showing|displaying|presenting|demonstrating|illustrating|explaining|clarifying|elucidating|illuminating|enlightening|educating|teaching|instructing|guiding|directing|leading|managing|controlling|handling|dealing|processing|working|operating|functioning|performing|executing|implementing|carrying out|doing|making|creating|building|constructing|developing|designing|planning|organizing|arranging|structuring|forming|shaping|molding|crafting|fashioning|manufacturing|producing|generating)\b',
            r'\b(leveraging|utilizing|using|employing|applying|implementing|executing|performing|carrying out|conducting|undertaking|pursuing|following|adopting|embracing|accepting|taking|receiving|getting|obtaining|acquiring|gaining|earning|winning|achieving|accomplishing|completing|finishing|concluding|ending|terminating|stopping|ceasing|halting|pausing|resting|relaxing|unwinding|decompressing|releasing|letting go|surrendering|yielding|giving up|quitting|abandoning|deserting|forsaking|leaving|departing|going|moving|traveling|journeying|voyaging|exploring|discovering|finding|locating|identifying|recognizing|acknowledging|accepting|embracing|welcoming|greeting|saluting|honoring|respecting|valuing|appreciating|cherishing|treasing|loving|adoring|worshipping|revering|esteeming|prizing|regarding|considering|thinking|believing|feeling|sensing|perceiving|noticing|observing|watching|monitoring|tracking|following|pursuing|chasing|hunting|seeking|searching|looking|uncovering|revealing|exposing|showing|displaying|presenting|demonstrating|illustrating|explaining|clarifying|elucidating|illuminating|enlightening|educating|teaching|instructing|guiding|directing|leading|managing|controlling|handling|dealing|processing|working|operating|functioning|performing|executing|implementing|carrying out|doing|making|creating|building|constructing|developing|designing|planning|organizing|arranging|structuring|forming|shaping|molding|crafting|fashioning|manufacturing|producing|generating)\s+(data|information|knowledge|wisdom|insight|intelligence|facts|figures|statistics|metrics|measurements|observations|findings|results|outcomes|consequences|effects|impacts|influences|powers|forces|strengths|energies|vigors|vitalities|spirits|souls|hearts|minds|brains|intellects|intelligences|wisdoms|knowledges|understandings|comprehensions|grasps|insights|perceptions|awarenesses|consciousnesses|realizations|recognitions|acknowledgments|admissions|confessions|declarations|statements|announcements|proclamations|revelations|disclosures|exposures|unveilings|presentations|introductions|launches|releases|publications|distributions|circulations|disseminations|propagations|spreads|transmissions|broadcasts|telecasts|webcasts|streams|lives|real-times|instants|immediates|prompts|quicks|fasts|rapids|swifts|speedies|hasties|hurrieds|rusheds|urgents|pressings|criticals|importants|significants|notables|remarkables|extraordinaries|exceptionals|outstandings|superiors|excellents|superbs|magnificents|wonderfuls|fantastics|amazings|incredibles|unbelievables|remarkables|notables|significants|importants|vitals|crucials|essentials|necessaries|requireds|mandatories|compulsories|obligatories|indispensables|fundamentals|basics|primaries|principals|mains|chiefs|leadings|foremosts|tops|bests|finests|greatests|highests|maximums|peaks|summits|climaxes|culminations|pinnacles|apexes|zeniths|acmes)\b',
        ]
        
    def initialize_validation_rules(self):
        """Initialize validation rules for names and roles"""
        
        # Name validation rules
        self.name_validation = {
            'min_length': 3,
            'max_length': 50,
            'min_words': 2,
            'max_words': 4,
            'must_have_capital': True,
            'exclude_numbers': True,
            'exclude_special_chars': True
        }
        
        # Role validation rules
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
        """Extract resume data with high precision"""
        try:
            logger.info("🎯 Starting precise resume extraction...")
            
            if not text or len(text.strip()) < 10:
                return self._get_empty_result()
            
            # Clean text
            text_clean = self._clean_text(text)
            
            # Extract with high precision
            name = self._extract_name_precise(text_clean, filename)
            role = self._extract_role_precise(text_clean, name)
            
            # Use other extractors for remaining fields
            from accurate_name_role_extractor import accurate_name_role_extractor
            other_data = accurate_name_role_extractor.extract_resume_data(text, filename)
            
            # Override with precise results
            result = {
                'name': name,
                'role': role,
                'email': other_data.get('email', 'Email not found'),
                'phone': other_data.get('phone', 'Phone not found'),
                'skills': other_data.get('skills', []),
                'experience': other_data.get('experience', {}),
                'location': other_data.get('location', 'Location not found'),
                'education': other_data.get('education', []),
                'raw_text': text_clean[:500] if text_clean else '',
                'extraction_method': 'precise_extraction',
                'confidence_score': self._calculate_confidence(name, role),
                'extraction_timestamp': datetime.now().isoformat()
            }
            
            logger.info("✅ Precise extraction completed")
            logger.info(f"👤 Name: {name}")
            logger.info(f"🎯 Role: {role}")
            return result
            
        except Exception as e:
            logger.error(f"❌ Precise extraction error: {e}")
            return self._get_empty_result()
    
    def _extract_name_precise(self, text: str, filename: str = None) -> str:
        """Extract name with high precision"""
        try:
            logger.info("🔍 Starting precise name extraction...")
            
            # Strategy 1: Filename-based extraction (highest priority)
            if filename:
                filename_name = self._extract_name_from_filename(filename)
                if filename_name and self._is_valid_name(filename_name):
                    logger.info(f"✅ Name found in filename: {filename_name}")
                    return filename_name
            
            # Strategy 2: Header-based extraction
            header_name = self._extract_name_from_header(text)
            if header_name and self._is_valid_name(header_name):
                logger.info(f"✅ Name found in header: {header_name}")
                return header_name
            
            # Strategy 3: Contact section extraction
            contact_name = self._extract_name_from_contact_section(text)
            if contact_name and self._is_valid_name(contact_name):
                logger.info(f"✅ Name found in contact section: {contact_name}")
                return contact_name
            
            logger.warning("⚠️ No valid name found")
            return 'Name not found'
            
        except Exception as e:
            logger.error(f"❌ Name extraction error: {e}")
            return 'Name not found'
    
    def _extract_role_precise(self, text: str, name: str = None) -> str:
        """Extract role with high precision"""
        try:
            logger.info("🔍 Starting precise role extraction...")
            
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
            
            # Strategy 2: Work experience context
            work_role = self._extract_role_from_work_experience(text_for_role)
            if work_role and self._is_valid_role(work_role):
                logger.info(f"✅ Role found in work experience: {work_role}")
                return work_role.title()
            
            # Strategy 3: Skills-based inference
            inferred_role = self._infer_role_from_skills(text_for_role)
            if inferred_role:
                logger.info(f"✅ Role inferred from skills: {inferred_role}")
                return inferred_role
            
            logger.warning("⚠️ No valid role found")
            return 'Role not found'
            
        except Exception as e:
            logger.error(f"❌ Role extraction error: {e}")
            return 'Role not found'
    
    def _extract_name_from_filename(self, filename: str) -> str:
        """Extract name from filename"""
        try:
            # Remove file extension
            name_part = os.path.splitext(filename)[0]
            logger.info(f"🔍 Extracting name from filename: {name_part}")
            
            # Try different patterns in order of priority
            patterns = [
                # Pattern 1: Names with underscores (e.g., "Pratik_Tarale")
                r'([A-Z][a-z]+_[A-Z][a-z]+(?:_[A-Z][a-z]+)?)',
                # Pattern 2: Names with hyphens (e.g., "Pratik-Tarale")
                r'([A-Z][a-z]+-[A-Z][a-z]+(?:-[A-Z][a-z]+)?)',
                # Pattern 3: Title Case names (e.g., "John Doe", "Mary Jane Smith")
                r'([A-Z][a-z]+ [A-Z][a-z]+(?: [A-Z][a-z]+)?)',
                # Pattern 4: ALL CAPS names (e.g., "JOHN DOE", "MARY JANE SMITH")
                r'([A-Z][A-Z]+ [A-Z][A-Z]+(?: [A-Z][A-Z]+)?)',
                # Pattern 5: Mixed case names (e.g., "John DOE", "MARY Jane")
                r'([A-Z][a-z]+ [A-Z][a-z]+(?: [A-Z][a-z]+)?)',
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
            
            # If no pattern matches, try to extract from common filename formats
            # Remove common prefixes/suffixes
            cleaned_name = re.sub(r'^(resume|cv|curriculum|vitae)[_\-\s]*', '', name_part, flags=re.IGNORECASE)
            cleaned_name = re.sub(r'[_\-\s]*(resume|cv|curriculum|vitae)$', '', cleaned_name, flags=re.IGNORECASE)
            cleaned_name = re.sub(r'[_\-\s]*\d+[_\-\s]*$', '', cleaned_name)  # Remove trailing numbers
            
            # Try to extract name from cleaned string
            if cleaned_name != name_part:
                for pattern in patterns[:3]:  # Try first 3 patterns on cleaned name
                    match = re.search(pattern, cleaned_name)
                    if match:
                        extracted_name = match.group(1).strip()
                        extracted_name = extracted_name.replace('_', ' ').replace('-', ' ')
                        extracted_name = ' '.join(word.capitalize() for word in extracted_name.split())
                        logger.info(f"✅ Name extracted from cleaned filename: {extracted_name}")
                        return extracted_name
            
            logger.warning(f"⚠️ No name pattern matched in filename: {name_part}")
            return None
            
        except Exception as e:
            logger.error(f"❌ Filename name extraction error: {e}")
            return None
    
    def _extract_name_from_header(self, text: str) -> str:
        """Extract name from document header"""
        try:
            # Get first few lines
            lines = text.split('\n')[:5]
            
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                
                # Check for name patterns
                for pattern in self.name_patterns[1:4]:  # Skip filename patterns
                    match = re.search(pattern, line, re.IGNORECASE)
                    if match:
                        name = match.group(1).strip()
                        if self._is_valid_name(name):
                            return name
            
            return None
            
        except Exception as e:
            logger.error(f"❌ Header name extraction error: {e}")
            return None
    
    def _extract_name_from_contact_section(self, text: str) -> str:
        """Extract name from contact section"""
        try:
            # Look for contact section patterns
            contact_patterns = [
                r'(?:Name|Full Name|Contact Name)[:\s]*([A-Z][a-z]+ [A-Z][a-z]+(?: [A-Z][a-z]+)?)',
                r'([A-Z][a-z]+ [A-Z][a-z]+(?: [A-Z][a-z]+)?)\s*\n\s*(?:Email|Phone|Address)',
            ]
            
            for pattern in contact_patterns:
                match = re.search(pattern, text, re.IGNORECASE)
                if match:
                    name = match.group(1).strip()
                    if self._is_valid_name(name):
                        return name
            
            return None
            
        except Exception as e:
            logger.error(f"❌ Contact name extraction error: {e}")
            return None
    
    def _extract_role_from_work_experience(self, text: str) -> str:
        """Extract role from work experience section"""
        try:
            # Look for work experience patterns with more specific context
            work_patterns = [
                # Pattern 1: Specific job titles in work context
                r'(?:worked as|position of|role of|designation of|currently working as|presently working as|employed as|served as)\s+(Software Engineer|Software Developer|Full Stack Developer|Frontend Developer|Backend Developer|Web Developer|Mobile Developer|DevOps Engineer|Data Scientist|Data Analyst|Machine Learning Engineer|AI Engineer|Cloud Engineer|Security Engineer|QA Engineer|Test Engineer|UI/UX Designer|Product Manager|Project Manager|Technical Lead|Team Lead|Solution Architect|System Architect|Database Administrator|Network Administrator|System Administrator|Business Analyst|System Analyst|Technical Writer|Scrum Master|Agile Coach|Engineering Manager|Development Manager|IT Manager|Java Developer|Python Developer|JavaScript Developer|React Developer|Angular Developer|Node\.js Developer|Spring Boot Developer|Django Developer|Flask Developer)',
                
                # Pattern 2: Seniority + role combinations
                r'(?:worked as|position of|role of|designation of|currently working as|presently working as|employed as|served as)\s+(Senior|Lead|Principal|Staff|Junior|Entry Level|Associate|Mid Level)\s+(Developer|Engineer|Programmer|Analyst|Consultant|Specialist|Architect|Manager|Director)',
                
                # Pattern 3: Technology-specific roles
                r'(?:worked as|position of|role of|designation of|currently working as|presently working as|employed as|served as)\s+(Java|Python|JavaScript|React|Angular|Vue|Node\.js|Spring|Django|Flask|Laravel|Ruby on Rails|PHP|C#|C\+\+|Go|Rust|Swift|Kotlin|Flutter|React Native|Android|iOS)\s+(Developer|Engineer|Programmer|Specialist)',
                
                # Pattern 4: Generic but valid roles
                r'(?:worked as|position of|role of|designation of|currently working as|presently working as|employed as|served as)\s+([A-Za-z\s]{3,50})',
                
                # Pattern 5: Role followed by technology
                r'([A-Za-z\s]{3,50})\s+(?:developer|engineer|manager|analyst|consultant|specialist|architect|programmer)',
            ]
            
            for i, pattern in enumerate(work_patterns):
                matches = re.findall(pattern, text, re.IGNORECASE)
                for match in matches:
                    role = match.strip()
                    if self._is_valid_role(role):
                        logger.info(f"✅ Role found in work experience with pattern {i+1}: {role}")
                        return role
            
            return None
            
        except Exception as e:
            logger.error(f"❌ Work experience role extraction error: {e}")
            return None
    
    def _infer_role_from_skills(self, text: str) -> str:
        """Infer role from skills mentioned"""
        try:
            # Common skill-to-role mappings
            skill_role_mapping = {
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
            }
            
            text_lower = text.lower()
            for skill, role in skill_role_mapping.items():
                if skill in text_lower:
                    return role
            
            return None
            
        except Exception as e:
            logger.error(f"❌ Skill-based role inference error: {e}")
            return None
    
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
    
    def _calculate_confidence(self, name: str, role: str) -> float:
        """Calculate confidence score"""
        try:
            confidence = 0.0
            
            # Name confidence
            if name and name != 'Name not found':
                confidence += 0.5
            
            # Role confidence
            if role and role != 'Role not found':
                confidence += 0.5
            
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
            'extraction_method': 'precise_extraction_error',
            'confidence_score': 0.0,
            'extraction_timestamp': datetime.now().isoformat()
        }

# Initialize the extractor
precise_name_role_extractor = PreciseNameRoleExtractor()
