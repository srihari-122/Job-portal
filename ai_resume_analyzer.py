"""
AI Resume Analyzer
Advanced AI analysis based on specific resume content
"""

import logging
from typing import Dict, List, Any
from datetime import datetime

logger = logging.getLogger(__name__)

class AIResumeAnalyzer:
    """AI-powered resume analysis"""
    
    def __init__(self):
        # Industry standards database
        self.industry_standards = {
            'software_developer': {
                'required_skills': ['programming', 'database', 'version control', 'testing'],
                'salary_range': {'junior': (300000, 600000), 'mid': (600000, 1200000), 'senior': (1200000, 2500000)},
                'growth_path': ['Senior Developer', 'Tech Lead', 'Solution Architect', 'Principal Engineer', 'Engineering Manager'],
                'future_roles': ['Cloud Architect', 'DevOps Engineer', 'Platform Engineer', 'Technical Product Manager', 'Engineering Manager'],
                'industry_trends': ['Cloud-native development', 'Microservices architecture', 'AI/ML integration', 'DevOps practices', 'Remote work expertise']
            },
            'data_scientist': {
                'required_skills': ['python', 'machine learning', 'statistics', 'data analysis'],
                'salary_range': {'junior': (400000, 800000), 'mid': (800000, 1500000), 'senior': (1500000, 3000000)},
                'growth_path': ['Senior Data Scientist', 'Principal Data Scientist', 'Head of Data Science', 'Chief Data Officer', 'VP of Data'],
                'future_roles': ['ML Engineer', 'AI Research Scientist', 'Data Engineering Lead', 'Chief Data Officer', 'Product Manager (AI)'],
                'industry_trends': ['Generative AI', 'Large Language Models', 'MLOps', 'Real-time analytics', 'Ethical AI']
            },
            'full_stack': {
                'required_skills': ['frontend', 'backend', 'database', 'deployment'],
                'salary_range': {'junior': (400000, 800000), 'mid': (800000, 1500000), 'senior': (1500000, 3000000)},
                'growth_path': ['Senior Full Stack Developer', 'Tech Lead', 'Engineering Manager', 'VP Engineering', 'CTO'],
                'future_roles': ['Product Manager', 'Technical Consultant', 'Startup Founder', 'Solution Architect', 'VP Engineering'],
                'industry_trends': ['Serverless architecture', 'Edge computing', 'Progressive Web Apps', 'API-first development', 'Low-code platforms']
            },
            'frontend': {
                'required_skills': ['html', 'css', 'javascript', 'react', 'responsive design'],
                'salary_range': {'junior': (300000, 600000), 'mid': (600000, 1200000), 'senior': (1200000, 2400000)},
                'growth_path': ['Senior Frontend Developer', 'Frontend Lead', 'UI/UX Engineer', 'Frontend Architect', 'Head of Frontend'],
                'future_roles': ['Product Designer', 'Technical Writer', 'Developer Advocate', 'Mobile Developer', 'Web3 Developer'],
                'industry_trends': ['Web3/Blockchain', 'AR/VR interfaces', 'Voice interfaces', 'Accessibility-first design', 'Performance optimization']
            },
            'backend': {
                'required_skills': ['server-side programming', 'database design', 'api development', 'cloud services'],
                'salary_range': {'junior': (350000, 700000), 'mid': (700000, 1400000), 'senior': (1400000, 2800000)},
                'growth_path': ['Senior Backend Developer', 'Backend Lead', 'System Architect', 'Principal Engineer', 'VP Engineering'],
                'future_roles': ['Cloud Solutions Architect', 'Platform Engineer', 'Security Engineer', 'Technical Consultant', 'VP Engineering'],
                'industry_trends': ['Serverless computing', 'GraphQL adoption', 'Event-driven architecture', 'Zero-trust security', 'Edge computing']
            },
            'devops': {
                'required_skills': ['cloud platforms', 'containerization', 'ci/cd', 'infrastructure as code'],
                'salary_range': {'junior': (400000, 800000), 'mid': (800000, 1600000), 'senior': (1600000, 3200000)},
                'growth_path': ['Senior DevOps Engineer', 'DevOps Lead', 'Platform Engineer', 'Site Reliability Engineer', 'CTO'],
                'future_roles': ['Cloud Architect', 'Security Engineer', 'Technical Product Manager', 'Engineering Manager', 'CTO'],
                'industry_trends': ['GitOps', 'Cloud-native security', 'Observability', 'FinOps', 'Platform engineering']
            },
            'mobile': {
                'required_skills': ['mobile development', 'cross-platform frameworks', 'app store optimization'],
                'salary_range': {'junior': (350000, 700000), 'mid': (700000, 1400000), 'senior': (1400000, 2800000)},
                'growth_path': ['Senior Mobile Developer', 'Mobile Lead', 'Mobile Architect', 'Principal Mobile Engineer', 'Head of Mobile'],
                'future_roles': ['Product Manager', 'Technical Writer', 'Developer Advocate', 'AR/VR Developer', 'IoT Developer'],
                'industry_trends': ['Cross-platform development', 'AR/VR integration', 'IoT connectivity', 'Performance optimization', 'Privacy-first design']
            },
            'qa': {
                'required_skills': ['testing methodologies', 'automation tools', 'bug tracking', 'test planning'],
                'salary_range': {'junior': (250000, 500000), 'mid': (500000, 1000000), 'senior': (1000000, 2000000)},
                'growth_path': ['Senior QA Engineer', 'QA Lead', 'Test Architect', 'Quality Manager', 'Head of Quality'],
                'future_roles': ['DevOps Engineer', 'Product Manager', 'Technical Writer', 'Automation Engineer', 'Engineering Manager'],
                'industry_trends': ['Test automation', 'AI-powered testing', 'Performance testing', 'Security testing', 'Continuous testing']
            },
            'ui_ux': {
                'required_skills': ['user research', 'wireframing', 'prototyping', 'design systems'],
                'salary_range': {'junior': (300000, 600000), 'mid': (600000, 1200000), 'senior': (1200000, 2400000)},
                'growth_path': ['Senior UI/UX Designer', 'Design Lead', 'Design Manager', 'Head of Design', 'VP of Design'],
                'future_roles': ['Product Manager', 'Design Consultant', 'Creative Director', 'User Researcher', 'Design Systems Lead'],
                'industry_trends': ['Design systems', 'Voice interfaces', 'AR/VR design', 'Accessibility design', 'Data-driven design']
            }
        }
        
        # Skill categories
        self.skill_categories = {
            'programming': ['java', 'python', 'javascript', 'c++', 'c#', 'go', 'rust', 'kotlin', 'swift'],
            'frontend': ['html', 'css', 'react', 'angular', 'vue', 'bootstrap', 'jquery'],
            'backend': ['node.js', 'django', 'flask', 'spring', 'express', 'laravel'],
            'database': ['mysql', 'postgresql', 'mongodb', 'redis', 'oracle', 'sqlite'],
            'cloud': ['aws', 'azure', 'gcp', 'docker', 'kubernetes', 'terraform'],
            'mobile': ['android', 'ios', 'react native', 'flutter', 'xamarin'],
            'ai_ml': ['tensorflow', 'pytorch', 'pandas', 'numpy', 'scikit-learn'],
            'devops': ['git', 'jenkins', 'prometheus', 'grafana', 'ansible'],
            'testing': ['selenium', 'jest', 'cypress', 'pytest', 'junit'],
            'tools': ['maven', 'gradle', 'intellij', 'vscode', 'postman']
        }
    
    def analyze_resume(self, resume_data: Dict[str, Any]) -> Dict[str, Any]:
        """Comprehensive AI analysis of resume"""
        try:
            logger.info("🤖 Starting comprehensive AI resume analysis...")
            
            # Extract key information with error handling
            name = resume_data.get('name', 'Unknown')
            role = resume_data.get('role', 'Developer')
            
            # Handle experience data properly
            experience_data = resume_data.get('experience', {})
            if isinstance(experience_data, dict):
                experience = experience_data.get('total_years', 0)
                if not isinstance(experience, (int, float)):
                    experience = 0
            elif isinstance(experience_data, (int, float)):
                experience = experience_data
            else:
                experience = 0
            
            # Handle skills data properly
            skills_data = resume_data.get('skills', [])
            if isinstance(skills_data, list):
                skills = [str(skill).strip() for skill in skills_data if skill and str(skill).strip()]
            else:
                skills = []
            
            location = resume_data.get('location', 'Unknown')
            email = resume_data.get('email', 'Unknown')
            
            logger.info(f"📊 Extracted data - Name: {name}, Role: {role}, Experience: {experience}, Skills: {len(skills)}, Location: {location}")
            logger.info(f"🔍 Debug - Raw resume_data keys: {list(resume_data.keys())}")
            logger.info(f"🔍 Debug - Skills data type: {type(skills_data)}, Skills content: {skills_data}")
            logger.info(f"🔍 Debug - Skills list: {skills}")
            logger.info(f"🔍 Debug - Experience data: {experience_data}")
            logger.info(f"🔍 Debug - Role data: {role}")
            logger.info(f"🔍 Debug - Location data: {location}")
            
            # Perform comprehensive analysis
            logger.info("🔍 Starting candidate profile analysis...")
            candidate_profile = self._analyze_candidate_profile(name, role, experience, skills, location)
            
            logger.info("🔍 Starting skills analysis...")
            skill_analysis = self._analyze_skills(skills, role)
            
            logger.info("🔍 Starting career progression analysis...")
            career_progression = self._analyze_career_progression(role, experience, skills)
            
            # Market positioning removed as requested
            market_positioning = {}
            
            logger.info("🔍 Starting recommendations generation...")
            recommendations = self._generate_recommendations(role, experience, skills)
            
            # Strengths & Weaknesses removed as requested
            strengths_weaknesses = {}
            
            logger.info("🔍 Starting AI insights generation...")
            ai_insights = self._generate_ai_insights(resume_data)
            
            logger.info("🔍 Starting skill gap analysis...")
            skill_gap_analysis = self._analyze_skill_gaps(resume_data)
            
            logger.info("🔍 Starting salary projection analysis...")
            salary_projection = self._analyze_salary_projection(resume_data)
            
            logger.info("🔍 Starting location growth analysis...")
            location_growth_analysis = self._analyze_location_growth(resume_data)
            
            logger.info("🔍 Starting career growth analysis...")
            career_growth_analysis = self._analyze_career_growth(resume_data)
            
            analysis_result = {
                'candidate_profile': candidate_profile,
                'skill_analysis': skill_analysis,
                'career_progression': career_progression,
                'market_positioning': market_positioning,
                'recommendations': recommendations,
                'strengths_weaknesses': strengths_weaknesses,
                'ai_insights': ai_insights,
                'skill_gap_analysis': skill_gap_analysis,
                'salary_projection': salary_projection,
                'location_growth_analysis': location_growth_analysis,
                'career_growth_analysis': career_growth_analysis,
                'analysis_timestamp': datetime.now().isoformat()
            }
            
            logger.info("✅ AI resume analysis completed successfully")
            return analysis_result
            
        except Exception as e:
            logger.error(f"❌ AI resume analysis error: {e}")
            logger.error(f"❌ Error type: {type(e).__name__}")
            logger.error(f"❌ Error details: {str(e)}")
            import traceback
            logger.error(f"❌ Traceback: {traceback.format_exc()}")
            return {'error': f'Analysis error: {str(e)}'}
    
    def _analyze_candidate_profile(self, name: str, role: str, experience: int, skills: List[str], location: str) -> Dict[str, Any]:
        """Analyze candidate profile"""
        return {
            'name': name,
            'role': role,
            'experience_level': self._get_experience_level(experience),
            'skill_count': len(skills),
            'location': location,
            'profile_summary': f"{name} is a {role} with {experience} years of experience, located in {location}. "
                              f"Has expertise in {len(skills)} technical skills.",
            'career_stage': self._determine_career_stage(experience)
        }
    
    def _analyze_skills(self, skills: List[str], role: str) -> Dict[str, Any]:
        """Analyze skills comprehensively"""
        try:
            logger.info(f"🔍 Skills analysis input - Skills: {skills}, Role: {role}")
            logger.info(f"🔍 Skills analysis input - Skills count: {len(skills)}, Skills type: {type(skills)}")
            
            skill_analysis = {
                'total_skills': len(skills),
                'skill_categories': {},
                'missing_skills': [],
                'strength_areas': [],
                'skill_gaps': []
            }
            
            # Categorize skills
            categorized_count = 0
            for skill in skills:
                if isinstance(skill, str):
                    skill_lower = skill.lower()
                    logger.info(f"🔍 Processing skill: '{skill}' (lowercase: '{skill_lower}')")
                    skill_categorized = False
                    for category, category_skills in self.skill_categories.items():
                        if any(cat_skill in skill_lower for cat_skill in category_skills):
                            if category not in skill_analysis['skill_categories']:
                                skill_analysis['skill_categories'][category] = []
                            skill_analysis['skill_categories'][category].append(skill)
                            skill_categorized = True
                            categorized_count += 1
                            logger.info(f"🔍 Skill '{skill}' categorized as '{category}'")
                            break
                    if not skill_categorized:
                        logger.info(f"🔍 Skill '{skill}' not categorized - no matching category found")
            
            logger.info(f"🔍 Total skills: {len(skills)}, Categorized: {categorized_count}")
            
            # Determine strength areas
            skill_analysis['strength_areas'] = []
            for category, category_skills in skill_analysis['skill_categories'].items():
                if len(category_skills) >= 2:  # Strong if 2+ skills in category
                    skill_analysis['strength_areas'].append(category.title())
            
            # Remove skill gaps section as requested
            skill_analysis['skill_gaps'] = []
            skill_analysis['missing_skills'] = []
            
            return skill_analysis
            
        except Exception as e:
            logger.error(f"❌ Skills analysis error: {e}")
            return {
                'total_skills': 0,
                'skill_categories': {},
                'missing_skills': [],
                'strength_areas': [],
                'skill_gaps': []
            }
    
    def _analyze_career_progression(self, role: str, experience: int, skills: List[str]) -> Dict[str, Any]:
        """Analyze career progression opportunities"""
        progression = {
            'current_level': self._get_experience_level(experience),
            'next_steps': [],
            'career_path': [],
            'timeline': {}
        }
        
        # Determine career path based on role with enhanced matching
        logger.info(f"🔍 Career progression - Role: '{role}', Role lower: '{role.lower()}'")
        logger.info(f"🔍 Available industry standards keys: {list(self.industry_standards.keys())}")
        
        matched_role = None
        if role.lower() in self.industry_standards:
            matched_role = role.lower()
            progression['career_path'] = self.industry_standards[matched_role]['growth_path']
            progression['future_roles'] = self.industry_standards[matched_role]['future_roles']
            progression['industry_trends'] = self.industry_standards[matched_role]['industry_trends']
            logger.info(f"✅ Career path found: {progression['career_path']}")
        else:
            # Try fuzzy matching for common variations
            role_lower = role.lower()
            
            # Check for specific role combinations first
            if 'frontend' in role_lower and 'developer' in role_lower:
                matched_role = 'frontend'
            elif 'backend' in role_lower and 'developer' in role_lower:
                matched_role = 'backend'
            elif 'full stack' in role_lower or ('full' in role_lower and 'stack' in role_lower):
                matched_role = 'full_stack'
            elif 'data scientist' in role_lower or ('data' in role_lower and 'scientist' in role_lower):
                matched_role = 'data_scientist'
            elif 'data analyst' in role_lower or ('data' in role_lower and 'analyst' in role_lower):
                matched_role = 'data_scientist'
            elif 'machine learning' in role_lower or 'ml engineer' in role_lower:
                matched_role = 'data_scientist'
            elif 'devops' in role_lower or 'dev ops' in role_lower or 'sre' in role_lower:
                matched_role = 'devops'
            elif 'mobile developer' in role_lower or 'ios' in role_lower or 'android' in role_lower:
                matched_role = 'mobile'
            elif 'qa engineer' in role_lower or 'quality' in role_lower or 'test' in role_lower:
                matched_role = 'qa'
            elif 'ui designer' in role_lower or 'ux designer' in role_lower or ('ui' in role_lower and 'design' in role_lower):
                matched_role = 'ui_ux'
            elif 'software developer' in role_lower or 'software engineer' in role_lower:
                matched_role = 'software_developer'
            elif 'web developer' in role_lower:
                matched_role = 'frontend'
            elif 'cloud engineer' in role_lower or 'platform engineer' in role_lower:
                matched_role = 'devops'
            elif 'developer' in role_lower or 'engineer' in role_lower:
                matched_role = 'software_developer'
            
            if matched_role:
                progression['career_path'] = self.industry_standards[matched_role]['growth_path']
                progression['future_roles'] = self.industry_standards[matched_role]['future_roles']
                progression['industry_trends'] = self.industry_standards[matched_role]['industry_trends']
                logger.info(f"✅ Career path matched to {matched_role}: {progression['career_path']}")
            else:
                # Default career path for unknown roles
                progression['career_path'] = ['Senior Developer', 'Tech Lead', 'Solution Architect', 'Principal Engineer', 'Engineering Manager']
                progression['future_roles'] = ['Technical Consultant', 'Product Manager', 'Engineering Manager', 'Startup Founder', 'CTO']
                progression['industry_trends'] = ['Digital transformation', 'Cloud migration', 'AI integration', 'Remote work', 'Agile methodologies']
                logger.info(f"⚠️ Using default career path: {progression['career_path']}")
        
        # AI-powered timeline and next steps based on actual experience and skills
        timeline_info = self._calculate_ai_timeline(experience, skills, matched_role, progression)
        progression['timeline'] = timeline_info['timeline']
        progression['next_steps'] = timeline_info['next_steps']
        
        return progression
    
    def _calculate_ai_timeline(self, experience: int, skills: List[str], matched_role: str, progression: Dict[str, Any]) -> Dict[str, Any]:
        """AI-powered timeline calculation based on actual resume data"""
        logger.info(f"⏰ Calculating AI timeline - Experience: {experience}, Skills: {len(skills)}, Role: {matched_role}")
        logger.info(f"🔍 Timeline Debug - Skills: {skills}")
        logger.info(f"🔍 Timeline Debug - Experience type: {type(experience)}, Value: {experience}")
        logger.info(f"🔍 Timeline Debug - Matched role: {matched_role}")
        
        # Analyze skill maturity and complexity
        skill_maturity = self._assess_skill_maturity(skills)
        skill_count = len(skills) if skills else 0
        
        logger.info(f"🔍 Timeline Debug - Skill maturity: {skill_maturity}, Skill count: {skill_count}")
        
        # Determine timeline based on experience, skills, and role
        if experience < 1:
            timeline_years = "1-2 years"
            target_role = progression['career_path'][0] if progression['career_path'] else 'Junior Developer'
            next_steps = self._get_entry_level_steps(skills, matched_role, progression)
        elif experience < 3:
            timeline_years = "2-3 years"
            target_role = progression['career_path'][0] if progression['career_path'] else 'Mid-Level Developer'
            next_steps = self._get_junior_level_steps(skills, matched_role, progression)
        elif experience < 5:
            timeline_years = "2-4 years"
            target_role = progression['career_path'][0] if progression['career_path'] else 'Senior Developer'
            next_steps = self._get_mid_level_steps(skills, matched_role, progression)
        elif experience < 8:
            timeline_years = "3-5 years"
            target_role = progression['career_path'][1] if len(progression['career_path']) > 1 else 'Tech Lead'
            next_steps = self._get_senior_level_steps(skills, matched_role, progression)
        else:
            timeline_years = "4-6 years"
            target_role = progression['career_path'][2] if len(progression['career_path']) > 2 else 'Principal Engineer'
            next_steps = self._get_lead_level_steps(skills, matched_role, progression)
        
        # Adjust timeline based on skill maturity
        if skill_maturity == 'Advanced' and experience < 3:
            timeline_years = "1-2 years"  # Accelerated progression
        elif skill_maturity == 'Beginner' and experience >= 3:
            timeline_years = "3-5 years"  # Slower progression
        
        timeline = {
            'next_level': timeline_years,
            'target_role': target_role,
            'skill_maturity': skill_maturity,
            'acceleration_factor': self._calculate_acceleration_factor(skills, experience)
        }
        
        logger.info(f"✅ AI timeline calculated - Years: {timeline_years}, Target: {target_role}, Maturity: {skill_maturity}")
        
        return {
            'timeline': timeline,
            'next_steps': next_steps
        }
    
    def _assess_skill_maturity(self, skills: List[str]) -> str:
        """Assess skill maturity based on actual skills"""
        if not skills:
            return 'Beginner'
        
        skill_lower = [skill.lower() for skill in skills if isinstance(skill, str)]
        
        # Advanced skills that indicate maturity
        advanced_skills = [
            'kubernetes', 'docker', 'microservices', 'architecture', 'system design',
            'machine learning', 'ai', 'tensorflow', 'pytorch', 'aws', 'azure', 'gcp',
            'terraform', 'ansible', 'ci/cd', 'monitoring', 'observability', 'security'
        ]
        
        # Intermediate skills
        intermediate_skills = [
            'react', 'angular', 'vue', 'node.js', 'python', 'java', 'spring',
            'sql', 'mongodb', 'redis', 'git', 'jenkins', 'testing', 'api'
        ]
        
        advanced_count = sum(1 for skill in skill_lower if any(adv in skill for adv in advanced_skills))
        intermediate_count = sum(1 for skill in skill_lower if any(int_skill in skill for int_skill in intermediate_skills))
        
        if advanced_count >= 3:
            return 'Advanced'
        elif intermediate_count >= 5 or advanced_count >= 1:
            return 'Intermediate'
        else:
            return 'Beginner'
    
    def _calculate_acceleration_factor(self, skills: List[str], experience: int) -> str:
        """Calculate career acceleration factor"""
        skill_count = len(skills) if skills else 0
        skill_maturity = self._assess_skill_maturity(skills)
        
        if skill_maturity == 'Advanced' and skill_count >= 15:
            return 'High Acceleration'
        elif skill_maturity == 'Intermediate' and skill_count >= 10:
            return 'Moderate Acceleration'
        else:
            return 'Standard Progression'
    
    def _get_entry_level_steps(self, skills: List[str], role: str, progression: Dict[str, Any]) -> List[str]:
        """Get next steps for entry level"""
        steps = [
            "Build strong foundation in core programming concepts",
            "Complete 2-3 hands-on projects to showcase skills",
            "Learn version control and basic development practices"
        ]
        
        if role and 'industry_trends' in progression:
            steps.append(f"Focus on trending technology: {progression['industry_trends'][0]}")
        
        return steps
    
    def _get_junior_level_steps(self, skills: List[str], role: str, progression: Dict[str, Any]) -> List[str]:
        """Get next steps for junior level"""
        steps = [
            "Take on more complex projects and responsibilities",
            "Learn advanced frameworks and tools in your domain",
            "Start contributing to open-source projects"
        ]
        
        if role and 'industry_trends' in progression:
            steps.append(f"Develop expertise in: {', '.join(progression['industry_trends'][:2])}")
        
        return steps
    
    def _get_mid_level_steps(self, skills: List[str], role: str, progression: Dict[str, Any]) -> List[str]:
        """Get next steps for mid level"""
        steps = [
            "Learn system design and architecture patterns",
            "Take on technical leadership roles in projects",
            "Mentor junior developers and share knowledge"
        ]
        
        if role and 'industry_trends' in progression:
            steps.append(f"Master advanced technologies: {', '.join(progression['industry_trends'][:2])}")
        
        return steps
    
    def _get_senior_level_steps(self, skills: List[str], role: str, progression: Dict[str, Any]) -> List[str]:
        """Get next steps for senior level"""
        steps = [
            "Lead architectural decisions and technical initiatives",
            "Mentor multiple team members and drive technical excellence",
            "Develop expertise in emerging technologies"
        ]
        
        if role and 'future_roles' in progression:
            steps.append(f"Explore advanced roles: {', '.join(progression['future_roles'][:2])}")
        
        return steps
    
    def _get_lead_level_steps(self, skills: List[str], role: str, progression: Dict[str, Any]) -> List[str]:
        """Get next steps for lead level"""
        steps = [
            "Focus on strategic technical leadership and innovation",
            "Drive organizational technical standards and best practices",
            "Consider transitioning to management or specialized consulting"
        ]
        
        if role and 'future_roles' in progression:
            steps.append(f"Pursue executive roles: {', '.join(progression['future_roles'][:2])}")
        
        return steps
    
    def _analyze_market_positioning(self, role: str, experience: int, location: str, skills: List[str]) -> Dict[str, Any]:
        """Analyze market positioning based on user's specific resume data"""
        logger.info(f"🔍 Market positioning analysis - Role: '{role}', Experience: {experience}, Location: '{location}', Skills: {len(skills)}")
        
        # Determine market demand based on role and experience
        market_demand = self._assess_market_demand(role, experience)
        
        # Calculate role-specific salary expectation
        salary_expectation = self._calculate_salary_expectation(role, experience)
        
        # Analyze location advantage based on actual location
        location_advantage = self._analyze_location_advantage(location)
        
        # Assess competitiveness based on actual skills and experience
        competitiveness = self._assess_competitiveness(skills, experience)
        
        # Get role-specific market trends
        market_trends = self._get_market_trends(role)
        
        positioning = {
            'market_demand': market_demand,
            'salary_expectation': salary_expectation,
            'location_advantage': location_advantage,
            'competitiveness': competitiveness,
            'market_trends': market_trends,
            'role_specificity': self._get_role_specificity(role, skills),
            'skill_market_value': self._assess_skill_market_value(skills, role)
        }
        
        logger.info(f"✅ Market positioning completed - Demand: {market_demand}, Competitiveness: {competitiveness}")
        return positioning
    
    def _generate_recommendations(self, role: str, experience: int, skills: List[str]) -> List[str]:
        """Generate AI-powered personalized recommendations based on user's resume"""
        logger.info(f"💡 Generating recommendations - Role: '{role}', Experience: {experience}, Skills: {len(skills)}")
        
        recommendations = []
        role_lower = role.lower()
        
        # Analyze skill gaps and missing technologies
        skill_lower = [skill.lower() for skill in skills if isinstance(skill, str)]
        
        # Role-specific recommendations based on actual skills
        if 'data scientist' in role_lower or 'machine learning' in role_lower:
            recommendations.extend(self._get_data_science_recommendations(skill_lower, experience))
        elif 'full stack' in role_lower:
            recommendations.extend(self._get_fullstack_recommendations(skill_lower, experience))
        elif 'frontend' in role_lower:
            recommendations.extend(self._get_frontend_recommendations(skill_lower, experience))
        elif 'backend' in role_lower:
            recommendations.extend(self._get_backend_recommendations(skill_lower, experience))
        elif 'devops' in role_lower:
            recommendations.extend(self._get_devops_recommendations(skill_lower, experience))
        elif 'mobile' in role_lower:
            recommendations.extend(self._get_mobile_recommendations(skill_lower, experience))
        else:
            recommendations.extend(self._get_general_recommendations(skill_lower, experience, role))
        
        # Experience-based career progression recommendations
        if experience < 2:
            recommendations.extend([
                "Build a strong portfolio with 3-5 diverse projects",
                "Contribute to open-source projects to gain visibility",
                "Attend tech meetups and conferences in your area"
            ])
        elif experience < 5:
            recommendations.extend([
                "Take on technical leadership roles in projects",
                "Mentor junior developers to develop leadership skills",
                "Consider pursuing relevant certifications"
            ])
        else:
            recommendations.extend([
                "Focus on architectural decision-making and system design",
                "Develop expertise in emerging technologies relevant to your domain",
                "Consider transitioning to technical management or consulting"
            ])
        
        # Skill-specific recommendations based on what's missing
        missing_skills = self._identify_missing_skills(skill_lower, role_lower)
        if missing_skills:
            recommendations.append(f"Learn missing technologies: {', '.join(missing_skills[:3])}")
        
        # Limit to 6 most relevant recommendations
        recommendations = recommendations[:6]
        
        logger.info(f"✅ Generated {len(recommendations)} personalized recommendations")
        return recommendations
    
    def _get_data_science_recommendations(self, skills: List[str], experience: int) -> List[str]:
        """Data science specific recommendations"""
        recommendations = []
        
        if not any('python' in skill for skill in skills):
            recommendations.append("Learn Python programming fundamentals")
        if not any('sql' in skill for skill in skills):
            recommendations.append("Master SQL for data manipulation and analysis")
        if not any('machine learning' in skill or 'ml' in skill for skill in skills):
            recommendations.append("Study machine learning algorithms and frameworks")
        if not any('tensorflow' in skill or 'pytorch' in skill for skill in skills):
            recommendations.append("Learn deep learning frameworks (TensorFlow/PyTorch)")
        if not any('aws' in skill or 'azure' in skill or 'gcp' in skill for skill in skills):
            recommendations.append("Get familiar with cloud platforms for ML deployment")
        
        return recommendations
    
    def _get_fullstack_recommendations(self, skills: List[str], experience: int) -> List[str]:
        """Full stack specific recommendations"""
        recommendations = []
        
        if not any('react' in skill or 'angular' in skill or 'vue' in skill for skill in skills):
            recommendations.append("Master a modern frontend framework (React/Angular/Vue)")
        if not any('node.js' in skill or 'express' in skill for skill in skills):
            recommendations.append("Learn backend development with Node.js and Express")
        if not any('sql' in skill or 'mongodb' in skill for skill in skills):
            recommendations.append("Develop database design and querying skills")
        if not any('aws' in skill or 'docker' in skill for skill in skills):
            recommendations.append("Learn cloud deployment and containerization")
        if not any('git' in skill for skill in skills):
            recommendations.append("Master version control with Git and GitHub")
        
        return recommendations
    
    def _get_frontend_recommendations(self, skills: List[str], experience: int) -> List[str]:
        """Frontend specific recommendations"""
        recommendations = []
        
        if not any('react' in skill for skill in skills):
            recommendations.append("Learn React.js for modern web development")
        if not any('typescript' in skill for skill in skills):
            recommendations.append("Master TypeScript for type-safe JavaScript")
        if not any('css' in skill or 'sass' in skill for skill in skills):
            recommendations.append("Advanced CSS and styling techniques")
        if not any('webpack' in skill or 'vite' in skill for skill in skills):
            recommendations.append("Learn modern build tools and bundlers")
        if not any('testing' in skill or 'jest' in skill for skill in skills):
            recommendations.append("Implement frontend testing strategies")
        
        return recommendations
    
    def _get_backend_recommendations(self, skills: List[str], experience: int) -> List[str]:
        """Backend specific recommendations"""
        recommendations = []
        
        if not any('api' in skill or 'rest' in skill for skill in skills):
            recommendations.append("Master RESTful API design and development")
        if not any('database' in skill or 'sql' in skill for skill in skills):
            recommendations.append("Advanced database design and optimization")
        if not any('microservices' in skill for skill in skills):
            recommendations.append("Learn microservices architecture patterns")
        if not any('security' in skill or 'auth' in skill for skill in skills):
            recommendations.append("Implement security best practices and authentication")
        if not any('docker' in skill or 'kubernetes' in skill for skill in skills):
            recommendations.append("Containerization and orchestration technologies")
        
        return recommendations
    
    def _get_devops_recommendations(self, skills: List[str], experience: int) -> List[str]:
        """DevOps specific recommendations"""
        recommendations = []
        
        if not any('kubernetes' in skill for skill in skills):
            recommendations.append("Master Kubernetes for container orchestration")
        if not any('terraform' in skill or 'ansible' in skill for skill in skills):
            recommendations.append("Learn Infrastructure as Code (Terraform/Ansible)")
        if not any('monitoring' in skill or 'prometheus' in skill for skill in skills):
            recommendations.append("Implement monitoring and observability solutions")
        if not any('ci/cd' in skill or 'jenkins' in skill for skill in skills):
            recommendations.append("Master CI/CD pipeline design and implementation")
        if not any('security' in skill for skill in skills):
            recommendations.append("Learn DevSecOps and security automation")
        
        return recommendations
    
    def _get_mobile_recommendations(self, skills: List[str], experience: int) -> List[str]:
        """Mobile development specific recommendations"""
        recommendations = []
        
        if not any('react native' in skill or 'flutter' in skill for skill in skills):
            recommendations.append("Learn cross-platform mobile development")
        if not any('ios' in skill or 'android' in skill for skill in skills):
            recommendations.append("Master native mobile development")
        if not any('testing' in skill for skill in skills):
            recommendations.append("Implement mobile app testing strategies")
        if not any('performance' in skill for skill in skills):
            recommendations.append("Learn mobile app performance optimization")
        if not any('app store' in skill for skill in skills):
            recommendations.append("Understand app store optimization and deployment")
        
        return recommendations
    
    def _get_general_recommendations(self, skills: List[str], experience: int, role: str) -> List[str]:
        """General recommendations for unknown roles"""
        recommendations = []
        
        if len(skills) < 10:
            recommendations.append("Expand your technical skill set")
        if not any('git' in skill for skill in skills):
            recommendations.append("Master version control with Git")
        if not any('testing' in skill for skill in skills):
            recommendations.append("Learn software testing methodologies")
        if not any('documentation' in skill for skill in skills):
            recommendations.append("Improve technical documentation skills")
        
        return recommendations
    
    def _identify_missing_skills(self, skills: List[str], role: str) -> List[str]:
        """Identify missing skills based on role"""
        essential_skills = {
            'data scientist': ['python', 'sql', 'machine learning', 'statistics', 'pandas'],
            'full stack': ['javascript', 'html', 'css', 'sql', 'git'],
            'frontend': ['html', 'css', 'javascript', 'react', 'git'],
            'backend': ['python', 'sql', 'api', 'database', 'git'],
            'devops': ['docker', 'kubernetes', 'aws', 'git', 'ci/cd'],
            'mobile': ['react native', 'ios', 'android', 'git', 'testing']
        }
        
        missing = []
        for role_key, required_skills in essential_skills.items():
            if role_key in role:
                for skill in required_skills:
                    if not any(skill in existing_skill for existing_skill in skills):
                        missing.append(skill)
                break
        
        return missing[:5]  # Return top 5 missing skills
    
    def _analyze_strengths_weaknesses(self, skills: List[str], role: str, experience: int) -> Dict[str, Any]:
        """Analyze strengths and weaknesses"""
        return {
            'strengths': [
                f"Strong technical foundation with {len(skills)} skills",
                f"Relevant experience in {role} domain",
                "Good skill diversity across multiple technologies"
            ],
            'weaknesses': [
                "Limited experience in advanced system design" if experience < 3 else "May need leadership development",
                "Could benefit from more specialized domain knowledge",
                "Consider expanding into emerging technologies"
            ],
            'improvement_areas': [
                "System design and architecture",
                "Leadership and mentoring",
                "Domain-specific expertise"
            ]
        }
    
    def _generate_ai_insights(self, resume_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate AI-powered insights based on actual resume data"""
        try:
            logger.info("🤖 Generating AI insights based on resume data...")
            
            # Extract key information
            name = resume_data.get('name', 'Unknown')
            role = resume_data.get('role', 'Developer')
            experience_data = resume_data.get('experience', {})
            skills_data = resume_data.get('skills', [])
            location = resume_data.get('location', 'Unknown')
            
            # Handle experience data
            if isinstance(experience_data, dict):
                experience_years = experience_data.get('total_years', 0)
            else:
                experience_years = 0
            
            # Handle skills data
            if isinstance(skills_data, list):
                skills = [str(skill).strip() for skill in skills_data if skill and str(skill).strip()]
            else:
                skills = []
            
            logger.info(f"🔍 AI Insights - Name: {name}, Role: {role}, Experience: {experience_years}, Skills: {len(skills)}")
            logger.info(f"🔍 AI Insights - Skills list: {skills}")
            
            # Calculate AI score based on actual data
            ai_score = self._calculate_ai_score(resume_data)
            
            # Determine market readiness based on role and experience
            market_readiness = self._assess_market_readiness(role, experience_years, skills)
            
            # Assess growth potential based on skills and experience
            growth_potential = self._assess_growth_potential(skills, experience_years, role)
            
            # Generate role-specific recommended actions
            recommended_actions = self._generate_role_specific_actions(role, skills, experience_years)
            
            # Calculate AI confidence based on data completeness
            ai_confidence = self._calculate_ai_confidence(resume_data)
            
            insights = {
                'ai_score': ai_score,
                'market_readiness': market_readiness,
                'growth_potential': growth_potential,
                'recommended_actions': recommended_actions,
                'ai_confidence': ai_confidence
            }
            
            logger.info(f"✅ AI insights generated - Score: {ai_score}, Readiness: {market_readiness}, Growth: {growth_potential}")
            return insights
            
        except Exception as e:
            logger.error(f"❌ AI insights generation error: {e}")
            return {
                'ai_score': 0.0,
                'market_readiness': 'Unknown',
                'growth_potential': 'Unknown',
                'recommended_actions': [],
                'ai_confidence': 0.0
            }
    
    def _assess_market_readiness(self, role: str, experience: int, skills: List[str]) -> str:
        """Assess market readiness based on role, experience, and skills"""
        logger.info(f"🎯 Assessing market readiness - Role: {role}, Experience: {experience}, Skills: {len(skills)}")
        
        role_lower = role.lower()
        skill_count = len(skills) if skills else 0
        
        # Role-specific readiness criteria
        if 'data scientist' in role_lower or 'machine learning' in role_lower:
            if experience >= 3 and skill_count >= 10:
                return 'Ready for senior data science positions'
            elif experience >= 1 and skill_count >= 5:
                return 'Ready for mid-level data science positions'
            else:
                return 'Entry-level data science ready'
        elif 'full stack' in role_lower:
            if experience >= 4 and skill_count >= 15:
                return 'Ready for senior full-stack positions'
            elif experience >= 2 and skill_count >= 10:
                return 'Ready for mid-level full-stack positions'
            else:
                return 'Entry-level full-stack ready'
        elif 'frontend' in role_lower:
            if experience >= 3 and skill_count >= 8:
                return 'Ready for senior frontend positions'
            elif experience >= 1 and skill_count >= 5:
                return 'Ready for mid-level frontend positions'
            else:
                return 'Entry-level frontend ready'
        elif 'backend' in role_lower:
            if experience >= 3 and skill_count >= 8:
                return 'Ready for senior backend positions'
            elif experience >= 1 and skill_count >= 5:
                return 'Ready for mid-level backend positions'
            else:
                return 'Entry-level backend ready'
        else:
            # Generic assessment
            if experience >= 5 and skill_count >= 15:
                return 'Ready for senior positions'
            elif experience >= 2 and skill_count >= 8:
                return 'Ready for mid-level positions'
            else:
                return 'Entry-level ready'
    
    def _assess_growth_potential(self, skills: List[str], experience: int, role: str) -> str:
        """Assess growth potential based on skills and experience"""
        logger.info(f"📈 Assessing growth potential - Skills: {len(skills)}, Experience: {experience}")
        
        if not skills:
            return 'Limited - No skills identified'
        
        skill_count = len(skills)
        role_lower = role.lower()
        
        # High-value skills that indicate growth potential
        high_value_skills = [
            'python', 'javascript', 'react', 'node.js', 'aws', 'docker', 'kubernetes',
            'machine learning', 'ai', 'tensorflow', 'pytorch', 'sql', 'mongodb',
            'git', 'jenkins', 'terraform', 'ansible', 'elasticsearch', 'redis'
        ]
        
        skill_lower = [skill.lower() for skill in skills if isinstance(skill, str)]
        high_value_count = sum(1 for skill in skill_lower if any(hv_skill in skill for hv_skill in high_value_skills))
        
        # Role-specific growth potential
        if 'data scientist' in role_lower or 'machine learning' in role_lower:
            if high_value_count >= 5 and skill_count >= 12:
                return 'Very High - Strong AI/ML foundation'
            elif high_value_count >= 3 and skill_count >= 8:
                return 'High - Good technical foundation'
            else:
                return 'Moderate - Needs skill development'
        elif 'full stack' in role_lower:
            if high_value_count >= 6 and skill_count >= 15:
                return 'Very High - Comprehensive skill set'
            elif high_value_count >= 4 and skill_count >= 10:
                return 'High - Good full-stack foundation'
            else:
                return 'Moderate - Needs skill development'
        else:
            # Generic assessment
            if high_value_count >= 5 and skill_count >= 15:
                return 'Very High - Strong technical foundation'
            elif high_value_count >= 3 and skill_count >= 10:
                return 'High - Good skill diversity'
            elif high_value_count >= 1 and skill_count >= 5:
                return 'Moderate - Developing skills'
            else:
                return 'Limited - Needs skill development'
    
    def _generate_role_specific_actions(self, role: str, skills: List[str], experience: int) -> List[str]:
        """Generate role-specific recommended actions"""
        logger.info(f"💡 Generating role-specific actions - Role: {role}, Skills: {len(skills)}, Experience: {experience}")
        
        actions = []
        role_lower = role.lower()
        skill_lower = [skill.lower() for skill in skills if isinstance(skill, str)]
        
        # Role-specific actions
        if 'data scientist' in role_lower or 'machine learning' in role_lower:
            if not any('python' in skill for skill in skill_lower):
                actions.append("Learn Python programming fundamentals")
            if not any('sql' in skill for skill in skill_lower):
                actions.append("Master SQL for data manipulation")
            if not any('machine learning' in skill or 'ml' in skill for skill in skill_lower):
                actions.append("Study machine learning algorithms and frameworks")
            if not any('tensorflow' in skill or 'pytorch' in skill for skill in skill_lower):
                actions.append("Learn deep learning frameworks")
            actions.append("Build a portfolio of data science projects")
            actions.append("Contribute to open-source ML projects")
        elif 'full stack' in role_lower:
            if not any('react' in skill or 'angular' in skill or 'vue' in skill for skill in skill_lower):
                actions.append("Master a modern frontend framework")
            if not any('node.js' in skill or 'express' in skill for skill in skill_lower):
                actions.append("Learn backend development with Node.js")
            if not any('sql' in skill or 'mongodb' in skill for skill in skill_lower):
                actions.append("Develop database design skills")
            if not any('aws' in skill or 'docker' in skill for skill in skill_lower):
                actions.append("Learn cloud deployment and containerization")
            actions.append("Build full-stack applications")
            actions.append("Learn DevOps practices")
        elif 'frontend' in role_lower:
            if not any('react' in skill for skill in skill_lower):
                actions.append("Learn React.js for modern web development")
            if not any('typescript' in skill for skill in skill_lower):
                actions.append("Master TypeScript for type-safe JavaScript")
            if not any('css' in skill or 'sass' in skill for skill in skill_lower):
                actions.append("Advanced CSS and styling techniques")
            actions.append("Build responsive web applications")
            actions.append("Learn modern build tools and bundlers")
        else:
            # Generic actions
            if len(skills) < 10:
                actions.append("Expand your technical skill set")
            if not any('git' in skill for skill in skill_lower):
                actions.append("Master version control with Git")
            if not any('testing' in skill for skill in skill_lower):
                actions.append("Learn software testing methodologies")
            actions.append("Build a strong portfolio of projects")
            actions.append("Contribute to open-source projects")
        
        # Experience-based actions
        if experience < 2:
            actions.append("Focus on building strong technical foundation")
            actions.append("Complete online courses in your domain")
        elif experience < 5:
            actions.append("Take on technical leadership roles")
            actions.append("Mentor junior developers")
        else:
            actions.append("Focus on architectural decision-making")
            actions.append("Develop expertise in emerging technologies")
        
        # Limit to 6 most relevant actions
        return actions[:6]
    
    def _calculate_ai_confidence(self, resume_data: Dict[str, Any]) -> float:
        """Calculate AI confidence based on data completeness"""
        try:
            confidence = 0.0
            
            # Check data completeness
            if resume_data.get('name') and resume_data['name'] != 'Unknown':
                confidence += 0.2
            if resume_data.get('role') and resume_data['role'] != 'Unknown':
                confidence += 0.2
            if resume_data.get('experience') and isinstance(resume_data['experience'], dict):
                experience = resume_data['experience'].get('total_years', 0)
                if experience > 0:
                    confidence += 0.2
            if resume_data.get('skills') and isinstance(resume_data['skills'], list) and len(resume_data['skills']) > 0:
                confidence += 0.2
            if resume_data.get('location') and resume_data['location'] != 'Unknown':
                confidence += 0.1
            if resume_data.get('email') and resume_data['email'] != 'Unknown':
                confidence += 0.1
            
            return min(confidence, 1.0)
        except Exception as e:
            logger.error(f"❌ AI confidence calculation error: {e}")
            return 0.0
    
    def _analyze_skill_gaps(self, role: str, skills: List[str]) -> Dict[str, Any]:
        """Analyze skill gaps based on role and actual skills"""
        try:
            logger.info(f"🔍 Analyzing skill gaps - Role: {role}, Skills: {len(skills)}")
            
            if not skills:
                return {
                    'gap_score': 0.0,
                    'role_category': 'Unknown',
                    'missing_skills': [],
                    'total_required': 0,
                    'total_present': 0,
                    'recommendations': ['Upload a resume to analyze skills']
                }
            
            role_lower = role.lower()
            skill_lower = [skill.lower() for skill in skills if isinstance(skill, str)]
            
            # Define required skills by role
            required_skills = {
                'data scientist': ['python', 'sql', 'machine learning', 'statistics', 'pandas', 'numpy', 'scikit-learn', 'tensorflow', 'pytorch'],
                'full stack': ['html', 'css', 'javascript', 'react', 'node.js', 'sql', 'git', 'api', 'mongodb'],
                'frontend': ['html', 'css', 'javascript', 'react', 'git', 'npm', 'webpack', 'responsive design'],
                'backend': ['python', 'sql', 'api', 'database', 'git', 'rest', 'microservices', 'docker'],
                'devops': ['docker', 'kubernetes', 'aws', 'git', 'ci/cd', 'terraform', 'ansible', 'monitoring'],
                'mobile': ['react native', 'ios', 'android', 'git', 'testing', 'app store', 'performance']
            }
            
            # Find matching role
            matched_role = None
            for role_key in required_skills.keys():
                if role_key in role_lower:
                    matched_role = role_key
                    break
            
            if not matched_role:
                matched_role = 'general'
                required_skills['general'] = ['git', 'testing', 'documentation', 'problem solving', 'communication']
            
            required = required_skills[matched_role]
            present_skills = []
            missing_skills = []
            
            # Check which required skills are present
            for req_skill in required:
                if any(req_skill in skill for skill in skill_lower):
                    present_skills.append(req_skill)
                else:
                    missing_skills.append(req_skill)
            
            # Calculate gap score
            total_required = len(required)
            total_present = len(present_skills)
            gap_score = (total_present / total_required) * 100 if total_required > 0 else 0
            
            # Generate recommendations
            recommendations = []
            if missing_skills:
                recommendations.append(f"Learn missing technologies: {', '.join(missing_skills[:3])}")
            if total_present < total_required * 0.5:
                recommendations.append("Focus on building core technical skills")
            if total_present >= total_required * 0.8:
                recommendations.append("Consider advanced specialization")
            recommendations.append("Build projects to demonstrate skills")
            
            skill_gap_analysis = {
                'gap_score': round(gap_score, 1),
                'role_category': matched_role.title(),
                'missing_skills': missing_skills,
                'total_required': total_required,
                'total_present': total_present,
                'recommendations': recommendations
            }
            
            logger.info(f"✅ Skill gap analysis completed - Gap Score: {gap_score}%, Missing: {len(missing_skills)}")
            return skill_gap_analysis
            
        except Exception as e:
            logger.error(f"❌ Skill gap analysis error: {e}")
            return {
                'gap_score': 0.0,
                'role_category': 'Unknown',
                'missing_skills': [],
                'total_required': 0,
                'total_present': 0,
                'recommendations': ['Analysis failed']
            }
    
    def _assess_market_readiness(self, role: str, experience_years: int, skills: List[str]) -> str:
        """Assess market readiness based on role, experience, and skills"""
        logger.info(f"🎯 Assessing market readiness - Role: {role}, Experience: {experience_years}, Skills: {len(skills)}")
        
        # Role-specific readiness assessment
        if 'data' in role.lower() or 'analyst' in role.lower():
            if experience_years >= 3 and len(skills) >= 8:
                return 'Ready for senior data roles'
            elif experience_years >= 1 and len(skills) >= 5:
                return 'Ready for mid-level data positions'
            else:
                return 'Entry-level data positions'
        
        elif 'frontend' in role.lower() or 'ui' in role.lower():
            if experience_years >= 3 and len(skills) >= 6:
                return 'Ready for senior frontend roles'
            elif experience_years >= 1 and len(skills) >= 4:
                return 'Ready for mid-level frontend positions'
            else:
                return 'Entry-level frontend positions'
        
        elif 'backend' in role.lower() or 'api' in role.lower():
            if experience_years >= 3 and len(skills) >= 7:
                return 'Ready for senior backend roles'
            elif experience_years >= 1 and len(skills) >= 5:
                return 'Ready for mid-level backend positions'
            else:
                return 'Entry-level backend positions'
        
        elif 'fullstack' in role.lower() or 'full stack' in role.lower():
            if experience_years >= 3 and len(skills) >= 10:
                return 'Ready for senior fullstack roles'
            elif experience_years >= 1 and len(skills) >= 7:
                return 'Ready for mid-level fullstack positions'
            else:
                return 'Entry-level fullstack positions'
        
        else:  # Generic developer roles
            if experience_years >= 3 and len(skills) >= 8:
                return 'Ready for senior developer roles'
            elif experience_years >= 1 and len(skills) >= 5:
                return 'Ready for mid-level developer positions'
            else:
                return 'Entry-level developer positions'
    
    def _assess_growth_potential(self, skills: List[str], experience_years: int, role: str) -> str:
        """Assess growth potential based on skills diversity and experience"""
        logger.info(f"📈 Assessing growth potential - Skills: {len(skills)}, Experience: {experience_years}, Role: {role}")
        
        # Count skill categories
        skill_categories = set()
        for skill in skills:
            skill_lower = skill.lower()
            if any(tech in skill_lower for tech in ['python', 'java', 'javascript', 'react', 'angular', 'vue']):
                skill_categories.add('Programming')
            if any(tech in skill_lower for tech in ['sql', 'database', 'mysql', 'postgresql', 'mongodb']):
                skill_categories.add('Database')
            if any(tech in skill_lower for tech in ['aws', 'azure', 'docker', 'kubernetes', 'devops']):
                skill_categories.add('Cloud/DevOps')
            if any(tech in skill_lower for tech in ['machine learning', 'ai', 'tensorflow', 'pytorch', 'data science']):
                skill_categories.add('AI/ML')
            if any(tech in skill_lower for tech in ['git', 'github', 'ci/cd', 'jenkins', 'testing']):
                skill_categories.add('Tools/Methodologies')
        
        category_count = len(skill_categories)
        
        # Assess growth potential
        if category_count >= 4 and experience_years >= 2:
            return 'Very High - Well-rounded skill set'
        elif category_count >= 3 and experience_years >= 1:
            return 'High - Good skill diversity'
        elif category_count >= 2:
            return 'Moderate - Focused skill set'
        else:
            return 'Developing - Early career stage'
    
    def _generate_role_specific_actions(self, role: str, skills: List[str], experience_years: int) -> List[str]:
        """Generate role-specific recommended actions based on actual role and skills"""
        logger.info(f"💡 Generating role-specific actions - Role: '{role}', Skills: {len(skills)}, Experience: {experience_years}")
        
        # Convert skills to lowercase for matching
        skills_lower = [skill.lower() for skill in skills]
        role_lower = role.lower()
        
        actions = []
        
        # Determine role category based on role and skills
        role_category = self._determine_role_category(role_lower, skills_lower)
        logger.info(f"🎯 Determined role category: {role_category}")
        
        # Generate actions based on role category and existing skills
        if role_category == 'data_science':
            actions = self._get_data_science_actions(skills_lower, experience_years)
        elif role_category == 'frontend':
            actions = self._get_frontend_actions(skills_lower, experience_years)
        elif role_category == 'backend':
            actions = self._get_backend_actions(skills_lower, experience_years)
        elif role_category == 'fullstack':
            actions = self._get_fullstack_actions(skills_lower, experience_years)
        elif role_category == 'devops':
            actions = self._get_devops_actions(skills_lower, experience_years)
        elif role_category == 'mobile':
            actions = self._get_mobile_actions(skills_lower, experience_years)
        elif role_category == 'qa':
            actions = self._get_qa_actions(skills_lower, experience_years)
        else:
            actions = self._get_generic_actions(skills_lower, experience_years)
        
        logger.info(f"✅ Generated {len(actions)} role-specific actions for {role_category}")
        return actions[:6]  # Limit to 6 most relevant actions
    
    def _determine_role_category(self, role_lower: str, skills_lower: List[str]) -> str:
        """Determine specific role category based on role and skills"""
        logger.info(f"🔍 Determining specific role category - Role: '{role_lower}', Skills count: {len(skills_lower)}")
        
        # PRIORITY 1: Determine specific role based on role title and skills
        # Java-specific roles
        if 'java' in role_lower and any(skill in skills_lower for skill in ['java', 'spring', 'spring boot', 'hibernate', 'jpa']):
            if 'full stack' in role_lower or ('frontend' in skills_lower and 'backend' in skills_lower):
                logger.info("✅ Role category determined: java_fullstack (from role title and skills)")
                return 'java_fullstack'
            elif any(skill in skills_lower for skill in ['html', 'css', 'javascript', 'bootstrap']):
                logger.info("✅ Role category determined: java_fullstack (from skills analysis)")
                return 'java_fullstack'
            else:
                logger.info("✅ Role category determined: java_backend (from role title)")
                return 'java_backend'
        
        # Python-specific roles
        elif 'python' in role_lower and any(skill in skills_lower for skill in ['python', 'django', 'flask', 'fastapi']):
            if 'full stack' in role_lower or ('frontend' in skills_lower and 'backend' in skills_lower):
                logger.info("✅ Role category determined: python_fullstack (from role title and skills)")
                return 'python_fullstack'
            else:
                logger.info("✅ Role category determined: python_backend (from role title)")
                return 'python_backend'
        
        # JavaScript/Node.js specific roles
        elif any(keyword in role_lower for keyword in ['javascript', 'node.js', 'nodejs']) and any(skill in skills_lower for skill in ['javascript', 'node.js', 'express', 'react', 'angular', 'vue']):
            if 'full stack' in role_lower or ('frontend' in skills_lower and 'backend' in skills_lower):
                logger.info("✅ Role category determined: javascript_fullstack (from role title and skills)")
                return 'javascript_fullstack'
            else:
                logger.info("✅ Role category determined: javascript_backend (from role title)")
                return 'javascript_backend'
        
        # Generic full stack roles
        elif any(keyword in role_lower for keyword in ['fullstack', 'full stack', 'full-stack', 'full stack developer']):
            # Analyze skills to determine specific stack
            if any(skill in skills_lower for skill in ['java', 'spring', 'spring boot']):
                logger.info("✅ Role category determined: java_fullstack (from skills analysis)")
                return 'java_fullstack'
            elif any(skill in skills_lower for skill in ['python', 'django', 'flask']):
                logger.info("✅ Role category determined: python_fullstack (from skills analysis)")
                return 'python_fullstack'
            elif any(skill in skills_lower for skill in ['javascript', 'node.js', 'react', 'angular', 'vue']):
                logger.info("✅ Role category determined: javascript_fullstack (from skills analysis)")
                return 'javascript_fullstack'
            else:
                logger.info("✅ Role category determined: generic_fullstack (from role title)")
                return 'generic_fullstack'
        elif any(keyword in role_lower for keyword in ['data', 'analyst', 'scientist', 'ml', 'machine learning', 'ai', 'data science']):
            logger.info("✅ Role category determined: data_science (from role title)")
            return 'data_science'
        elif any(keyword in role_lower for keyword in ['frontend', 'ui', 'ux', 'web', 'front-end']):
            logger.info("✅ Role category determined: frontend (from role title)")
            return 'frontend'
        elif any(keyword in role_lower for keyword in ['backend', 'api', 'server', 'microservices', 'back-end']):
            logger.info("✅ Role category determined: backend (from role title)")
            return 'backend'
        elif any(keyword in role_lower for keyword in ['devops', 'cloud', 'infrastructure', 'deployment', 'sre']):
            logger.info("✅ Role category determined: devops (from role title)")
            return 'devops'
        elif any(keyword in role_lower for keyword in ['mobile', 'android', 'ios', 'react native', 'flutter']):
            logger.info("✅ Role category determined: mobile (from role title)")
            return 'mobile'
        elif any(keyword in role_lower for keyword in ['qa', 'testing', 'quality', 'test', 'automation']):
            logger.info("✅ Role category determined: qa (from role title)")
            return 'qa'
        # Check for generic developer roles
        elif any(keyword in role_lower for keyword in ['java developer', 'python developer', 'javascript developer', 'software engineer', 'web developer']):
            logger.info("✅ Role category determined: software_developer (from role title)")
            return 'software_developer'
        
        # PRIORITY 2: If role title is unclear, analyze skills with stricter criteria
        # Count skills in each category
        data_science_skills = len([s for s in skills_lower if s in ['python', 'sql', 'machine learning', 'data science', 'pandas', 'numpy', 'tensorflow', 'pytorch', 'matplotlib', 'seaborn', 'jupyter', 'tableau', 'power bi', 'statistics', 'data analysis', 'data cleaning']])
        frontend_skills = len([s for s in skills_lower if s in ['html', 'css', 'javascript', 'react', 'angular', 'vue', 'bootstrap', 'tailwind', 'typescript', 'responsive', 'dom', 'webpack', 'vite']])
        backend_skills = len([s for s in skills_lower if s in ['python', 'java', 'node.js', 'spring', 'django', 'flask', 'express', 'sql', 'mongodb', 'rest', 'api', 'microservices', 'authentication', 'jwt']])
        devops_skills = len([s for s in skills_lower if s in ['docker', 'kubernetes', 'aws', 'azure', 'jenkins', 'terraform', 'ansible', 'ci/cd', 'monitoring', 'linux']])
        mobile_skills = len([s for s in skills_lower if s in ['android', 'ios', 'react native', 'flutter', 'kotlin', 'swift', 'mobile', 'app development']])
        qa_skills = len([s for s in skills_lower if s in ['selenium', 'testing', 'automation', 'junit', 'testng', 'cypress', 'postman', 'api testing', 'performance testing']])
        
        logger.info(f"🔍 Skill counts - Data Science: {data_science_skills}, Frontend: {frontend_skills}, Backend: {backend_skills}, DevOps: {devops_skills}, Mobile: {mobile_skills}, QA: {qa_skills}")
        
        # Determine category based on highest skill count (minimum 2 skills required)
        skill_counts = {
            'data_science': data_science_skills,
            'frontend': frontend_skills,
            'backend': backend_skills,
            'devops': devops_skills,
            'mobile': mobile_skills,
            'qa': qa_skills
        }
        
        # Find category with highest skill count
        max_category = max(skill_counts, key=skill_counts.get)
        max_count = skill_counts[max_category]
        
        # Only classify if there are at least 2 skills in that category
        if max_count >= 2:
            logger.info(f"✅ Role category determined: {max_category} (from skills analysis, count: {max_count})")
            return max_category
        
        # PRIORITY 3: Check for fullstack indicators (both frontend and backend skills)
        frontend_backend_skills = len([s for s in skills_lower if s in ['html', 'css', 'javascript', 'react', 'angular', 'vue', 'python', 'java', 'node.js', 'sql', 'api', 'rest']])
        if frontend_backend_skills >= 4:  # At least 4 combined frontend/backend skills
            logger.info("✅ Role category determined: fullstack (from combined frontend/backend skills)")
            return 'fullstack'
        
        # Default to generic if no clear category
        logger.info("✅ Role category determined: generic (no clear specialization)")
        return 'generic'
    
    def _get_data_science_actions(self, skills_lower: List[str], experience_years: int) -> List[str]:
        """Get data science specific actions based on actual skills"""
        actions = []
        
        # Check for specific missing Python skills
        if 'python' not in skills_lower:
            actions.append("Complete Python programming course and build data analysis projects")
        elif 'pandas' not in skills_lower:
            actions.append("Master Pandas for data manipulation and analysis")
        elif 'numpy' not in skills_lower:
            actions.append("Learn NumPy for numerical computing and array operations")
        
        # Check for SQL skills
        if 'sql' not in skills_lower:
            actions.append("Master SQL for database querying and data extraction")
        
        # Check for machine learning skills
        if 'machine learning' not in skills_lower and 'ml' not in skills_lower:
            actions.append("Learn machine learning algorithms with scikit-learn")
        elif 'scikit-learn' not in skills_lower:
            actions.append("Master scikit-learn for ML model implementation")
        
        # Check for data visualization
        if 'data visualization' not in skills_lower and 'matplotlib' not in skills_lower:
            actions.append("Learn data visualization with Matplotlib and Seaborn")
        elif 'seaborn' not in skills_lower:
            actions.append("Master Seaborn for statistical data visualization")
        
        # Check for statistical analysis
        if 'statistics' not in skills_lower:
            actions.append("Learn statistical analysis and hypothesis testing")
        
        # Check for cloud platforms
        if 'aws' not in skills_lower and 'azure' not in skills_lower:
            actions.append("Learn cloud platforms for data engineering (AWS/Azure)")
        
        # Experience-based specific actions
        if experience_years < 1:
            actions.extend([
                "Complete data science projects on Kaggle competitions",
                "Build portfolio with real-world datasets and analysis"
            ])
        elif experience_years < 3:
            actions.extend([
                "Focus on advanced ML techniques and model deployment",
                "Learn deep learning frameworks (TensorFlow/PyTorch)"
            ])
        else:
            actions.extend([
                "Master MLOps and production model deployment",
                "Lead data science teams and mentor junior data scientists"
            ])
        
        return actions
    
    def _get_frontend_actions(self, skills_lower: List[str], experience_years: int) -> List[str]:
        """Get frontend specific actions based on actual skills"""
        actions = []
        
        # Check for specific missing JavaScript framework
        if 'react' not in skills_lower and 'angular' not in skills_lower and 'vue' not in skills_lower:
            actions.append("Learn a modern JavaScript framework (React/Angular/Vue)")
        elif 'react' not in skills_lower:
            actions.append("Master React with hooks, state management, and component lifecycle")
        elif 'angular' not in skills_lower:
            actions.append("Learn Angular with TypeScript and component architecture")
        elif 'vue' not in skills_lower:
            actions.append("Master Vue.js with Vuex for state management")
        
        # Check for TypeScript
        if 'typescript' not in skills_lower:
            actions.append("Learn TypeScript for better code quality and type safety")
        
        # Check for CSS frameworks
        if 'bootstrap' not in skills_lower and 'tailwind' not in skills_lower:
            actions.append("Learn CSS frameworks (Bootstrap/Tailwind CSS)")
        elif 'tailwind' not in skills_lower:
            actions.append("Master Tailwind CSS for utility-first styling")
        
        # Check for responsive design
        if 'responsive' not in skills_lower and 'mobile' not in skills_lower:
            actions.append("Master responsive design and mobile-first development")
        
        # Check for accessibility
        if 'accessibility' not in skills_lower and 'a11y' not in skills_lower:
            actions.append("Learn web accessibility standards (WCAG) and ARIA")
        
        # Check for build tools
        if 'webpack' not in skills_lower and 'vite' not in skills_lower:
            actions.append("Learn modern build tools (Webpack/Vite) for project bundling")
        
        # Experience-based specific actions
        if experience_years < 1:
            actions.extend([
                "Build interactive portfolio projects with animations",
                "Practice CSS Grid and Flexbox layouts"
            ])
        elif experience_years < 3:
            actions.extend([
                "Learn advanced frontend architecture patterns",
                "Master performance optimization and code splitting"
            ])
        else:
            actions.extend([
                "Lead frontend development teams and architecture decisions",
                "Mentor junior developers and establish coding standards"
            ])
        
        return actions
    
    def _get_backend_actions(self, skills_lower: List[str], experience_years: int) -> List[str]:
        """Get backend specific actions based on actual skills"""
        actions = []
        
        # Check for specific missing programming language
        if 'python' not in skills_lower and 'java' not in skills_lower and 'node.js' not in skills_lower:
            actions.append("Learn a backend programming language (Python/Java/Node.js)")
        elif 'python' not in skills_lower:
            actions.append("Master Python with Django/Flask for web development")
        elif 'java' not in skills_lower:
            actions.append("Learn Java with Spring Boot for enterprise applications")
        elif 'node.js' not in skills_lower:
            actions.append("Master Node.js with Express.js for server-side development")
        
        # Check for API development
        if 'api' not in skills_lower and 'rest' not in skills_lower:
            actions.append("Learn RESTful API design and development best practices")
        elif 'rest' not in skills_lower:
            actions.append("Master REST API principles and HTTP methods")
        
        # Check for database skills
        if 'sql' not in skills_lower and 'mongodb' not in skills_lower:
            actions.append("Learn database technologies (SQL/NoSQL)")
        elif 'sql' not in skills_lower:
            actions.append("Master SQL for database design and query optimization")
        elif 'mongodb' not in skills_lower:
            actions.append("Learn MongoDB for NoSQL database management")
        
        # Check for authentication
        if 'authentication' not in skills_lower and 'jwt' not in skills_lower:
            actions.append("Learn authentication and authorization (JWT/OAuth)")
        
        # Check for microservices
        if 'microservices' not in skills_lower:
            actions.append("Learn microservices architecture and design patterns")
        
        # Check for containerization
        if 'docker' not in skills_lower:
            actions.append("Master Docker for application containerization")
        
        # Experience-based specific actions
        if experience_years < 1:
            actions.extend([
                "Build RESTful APIs with proper error handling",
                "Practice database design and normalization"
            ])
        elif experience_years < 3:
            actions.extend([
                "Learn system design and scalability patterns",
                "Master caching strategies and performance optimization"
            ])
        else:
            actions.extend([
                "Design and architect large-scale backend systems",
                "Lead backend development teams and establish best practices"
            ])
        
        return actions
    
    def _get_fullstack_actions(self, skills_lower: List[str], experience_years: int) -> List[str]:
        """Get fullstack specific actions based on actual skills"""
        actions = []
        
        # Check for specific missing frontend skills
        if 'react' not in skills_lower and 'angular' not in skills_lower and 'vue' not in skills_lower:
            actions.append("Learn a modern frontend framework (React/Angular/Vue)")
        elif 'react' not in skills_lower:
            actions.append("Master React with hooks, state management, and component architecture")
        
        # Check for specific missing backend skills
        if 'node.js' not in skills_lower and 'python' not in skills_lower and 'java' not in skills_lower:
            actions.append("Learn a backend programming language (Node.js/Python/Java)")
        elif 'node.js' not in skills_lower:
            actions.append("Learn Node.js for backend development and API creation")
        
        # Check for database skills
        if 'sql' not in skills_lower and 'mongodb' not in skills_lower:
            actions.append("Master database technologies (SQL/NoSQL)")
        elif 'sql' not in skills_lower:
            actions.append("Learn SQL for database design and query optimization")
        
        # Check for deployment skills
        if 'docker' not in skills_lower and 'aws' not in skills_lower:
            actions.append("Learn containerization and cloud deployment (Docker/AWS)")
        elif 'docker' not in skills_lower:
            actions.append("Master Docker for application containerization")
        
        # Check for API skills
        if 'api' not in skills_lower and 'rest' not in skills_lower:
            actions.append("Learn RESTful API design and development")
        
        # Check for version control
        if 'git' not in skills_lower:
            actions.append("Master Git version control and collaboration workflows")
        
        # Experience-based specific actions
        if experience_years < 1:
            actions.extend([
                "Build a complete full-stack project from scratch",
                "Practice with both frontend and backend technologies daily"
            ])
        elif experience_years < 3:
            actions.extend([
                "Create scalable full-stack applications",
                "Learn advanced frontend and backend integration patterns"
            ])
        else:
            actions.extend([
                "Design and architect large-scale full-stack systems",
                "Lead full-stack development teams and mentor junior developers"
            ])
        
        return actions
    
    def _get_devops_actions(self, skills_lower: List[str], experience_years: int) -> List[str]:
        """Get DevOps specific actions"""
        actions = []
        
        # Check missing skills and suggest
        if 'docker' not in skills_lower:
            actions.append("Master Docker containerization")
        if 'kubernetes' not in skills_lower:
            actions.append("Learn Kubernetes orchestration")
        if 'aws' not in skills_lower and 'azure' not in skills_lower:
            actions.append("Learn cloud platforms (AWS/Azure/GCP)")
        if 'ci/cd' not in skills_lower and 'jenkins' not in skills_lower:
            actions.append("Master CI/CD pipeline automation")
        
        # Experience-based actions
        if experience_years < 2:
            actions.extend([
                "Practice infrastructure as code (Terraform/Ansible)",
                "Learn monitoring and logging tools"
            ])
        else:
            actions.extend([
                "Focus on advanced cloud architecture",
                "Learn security and compliance practices"
            ])
        
        return actions
    
    def _get_mobile_actions(self, skills_lower: List[str], experience_years: int) -> List[str]:
        """Get mobile specific actions"""
        actions = []
        
        # Check missing skills and suggest
        if 'react native' not in skills_lower and 'flutter' not in skills_lower:
            actions.append("Learn cross-platform development (React Native/Flutter)")
        if 'android' not in skills_lower and 'ios' not in skills_lower:
            actions.append("Master native mobile development")
        if 'mobile ui' not in skills_lower and 'mobile design' not in skills_lower:
            actions.append("Learn mobile UI/UX design principles")
        
        # Experience-based actions
        if experience_years < 2:
            actions.extend([
                "Build mobile app portfolio",
                "Practice mobile performance optimization"
            ])
        else:
            actions.extend([
                "Focus on advanced mobile architecture",
                "Learn mobile security and best practices"
            ])
        
        return actions
    
    def _get_qa_actions(self, skills_lower: List[str], experience_years: int) -> List[str]:
        """Get QA specific actions"""
        actions = []
        
        # Check missing skills and suggest
        if 'automation' not in skills_lower and 'selenium' not in skills_lower:
            actions.append("Learn test automation frameworks (Selenium/Cypress)")
        if 'api testing' not in skills_lower and 'postman' not in skills_lower:
            actions.append("Master API testing tools and techniques")
        if 'performance testing' not in skills_lower:
            actions.append("Learn performance and load testing")
        
        # Experience-based actions
        if experience_years < 2:
            actions.extend([
                "Build comprehensive test suites",
                "Practice different testing methodologies"
            ])
        else:
            actions.extend([
                "Focus on test strategy and planning",
                "Learn advanced testing tools and frameworks"
            ])
        
        return actions
    
    def _get_generic_actions(self, skills_lower: List[str], experience_years: int) -> List[str]:
        """Get generic actions for unknown roles"""
        actions = []
        
        # Check for programming skills
        if not any(skill in skills_lower for skill in ['python', 'java', 'javascript', 'c++', 'c#']):
            actions.append("Learn a programming language (Python/Java/JavaScript)")
        
        # Check for version control
        if 'git' not in skills_lower:
            actions.append("Master version control with Git")
        
        # Check for database skills
        if 'sql' not in skills_lower and 'database' not in skills_lower:
            actions.append("Learn database fundamentals")
        
        # Experience-based actions
        if experience_years < 1:
            actions.extend([
                "Complete programming fundamentals",
                "Build basic projects to showcase skills"
            ])
        elif experience_years < 3:
            actions.extend([
                "Take on more complex projects",
                "Learn industry-specific tools and frameworks"
            ])
        else:
            actions.extend([
                "Consider specialization in a specific domain",
                "Focus on leadership and mentoring skills"
            ])
        
        return actions
    
    def _generate_skill_gap_recommendations(self, missing_skills: List[str], role_category: str, experience_years: int) -> List[str]:
        """Generate specific recommendations based on missing skills and user profile"""
        logger.info(f"💡 Generating skill gap recommendations - Missing: {len(missing_skills)}, Role: {role_category}, Experience: {experience_years}")
        logger.info(f"🔍 Missing skills: {missing_skills}")
        
        recommendations = []
        
        # Generate specific, actionable recommendations for each missing skill
        for skill in missing_skills:
            skill_lower = skill.lower()
            
            # Core programming skills
            if skill_lower == 'python':
                recommendations.append("Complete Python programming course and build 2-3 data analysis projects")
            elif skill_lower == 'sql':
                recommendations.append("Learn SQL fundamentals and practice with real databases (MySQL/PostgreSQL)")
            elif skill_lower == 'javascript':
                recommendations.append("Master JavaScript ES6+ features and DOM manipulation")
            elif skill_lower == 'java':
                recommendations.append("Learn Java programming and Spring Boot framework")
            
            # Frontend technologies
            elif skill_lower == 'react':
                recommendations.append("Build React applications with hooks, state management, and component architecture")
            elif skill_lower == 'angular':
                recommendations.append("Learn Angular with TypeScript and component-based architecture")
            elif skill_lower == 'vue':
                recommendations.append("Master Vue.js with Vuex for state management")
            elif skill_lower == 'html':
                recommendations.append("Master HTML5 semantic elements and accessibility")
            elif skill_lower == 'css':
                recommendations.append("Learn CSS3, Flexbox, Grid, and responsive design")
            elif skill_lower == 'typescript':
                recommendations.append("Learn TypeScript for better code quality and type safety")
            
            # Backend technologies
            elif skill_lower == 'node.js':
                recommendations.append("Learn Node.js backend development with Express.js framework")
            elif skill_lower == 'rest api':
                recommendations.append("Master RESTful API design, development, and documentation")
            elif skill_lower == 'microservices':
                recommendations.append("Study microservices architecture patterns and implementation")
            elif skill_lower == 'authentication':
                recommendations.append("Learn authentication and authorization (JWT, OAuth)")
            
            # Database skills
            elif skill_lower == 'database design':
                recommendations.append("Learn database design, normalization, and optimization")
            elif skill_lower == 'mongodb':
                recommendations.append("Master MongoDB for NoSQL database management")
            
            # Cloud and DevOps
            elif skill_lower == 'aws':
                recommendations.append("Complete AWS fundamentals certification and hands-on labs")
            elif skill_lower == 'docker':
                recommendations.append("Learn Docker containerization and container orchestration")
            elif skill_lower == 'kubernetes':
                recommendations.append("Master Kubernetes for container orchestration and deployment")
            elif skill_lower == 'ci/cd':
                recommendations.append("Learn CI/CD pipeline automation with Jenkins/GitHub Actions")
            
            # Data Science and ML
            elif skill_lower == 'machine learning':
                recommendations.append("Study ML algorithms and implement projects with scikit-learn")
            elif skill_lower == 'data visualization':
                recommendations.append("Learn data visualization with Matplotlib, Seaborn, and Plotly")
            elif skill_lower == 'pandas':
                recommendations.append("Master Pandas for data manipulation and analysis")
            elif skill_lower == 'numpy':
                recommendations.append("Learn NumPy for numerical computing and array operations")
            elif skill_lower == 'statistics':
                recommendations.append("Learn statistical analysis and hypothesis testing")
            
            # Development tools
            elif skill_lower == 'git':
                recommendations.append("Master Git version control and GitHub/GitLab workflows")
            elif skill_lower == 'testing':
                recommendations.append("Learn automated testing frameworks and test-driven development")
            elif skill_lower == 'system design':
                recommendations.append("Study system design patterns and scalability principles")
            
            # Generic fallback
            else:
                recommendations.append(f"Learn {skill} through online courses and practical projects")
        
        # Add role-specific recommendations based on experience level
        if role_category == 'data_science':
            if experience_years < 2:
                recommendations.extend([
                    "Complete data science projects on Kaggle competitions",
                    "Learn statistical analysis and hypothesis testing",
                    "Practice with real-world datasets and data cleaning"
                ])
            else:
                recommendations.extend([
                    "Focus on advanced ML techniques and model deployment",
                    "Learn MLOps and production model deployment",
                    "Master deep learning frameworks (TensorFlow/PyTorch)"
                ])
        
        elif role_category == 'frontend':
            if experience_years < 2:
                recommendations.extend([
                    "Build responsive web applications with modern frameworks",
                    "Learn CSS frameworks (Bootstrap/Tailwind) and preprocessors",
                    "Practice accessibility and performance optimization"
                ])
            else:
                recommendations.extend([
                    "Learn advanced frontend architecture patterns",
                    "Master performance optimization and code splitting",
                    "Consider frontend team leadership and mentoring"
                ])
        
        elif role_category == 'backend':
            if experience_years < 2:
                recommendations.extend([
                    "Learn database design and optimization techniques",
                    "Practice API security and authentication",
                    "Study system design and scalability patterns"
                ])
            else:
                recommendations.extend([
                    "Focus on advanced backend architecture and microservices",
                    "Learn distributed systems and caching strategies",
                    "Consider backend team leadership and system design"
                ])
        
        elif role_category == 'fullstack':
            if experience_years < 2:
                recommendations.extend([
                    "Build end-to-end web applications from scratch",
                    "Learn deployment and hosting strategies",
                    "Practice full-stack project architecture"
                ])
            else:
                recommendations.extend([
                    "Focus on scalable system architecture and design",
                    "Learn advanced deployment and monitoring",
                    "Consider full-stack team leadership and mentoring"
                ])
        
        elif role_category == 'devops':
            if experience_years < 2:
                recommendations.extend([
                    "Learn infrastructure as code (Terraform/Ansible)",
                    "Master monitoring and logging tools",
                    "Practice cloud security and compliance"
                ])
            else:
                recommendations.extend([
                    "Focus on advanced cloud architecture and automation",
                    "Learn security and compliance best practices",
                    "Consider DevOps team leadership and architecture"
                ])
        
        # Experience-based general recommendations
        if experience_years < 1:
            recommendations.extend([
                "Complete internship or entry-level projects",
                "Join coding communities and forums",
                "Practice coding challenges daily"
            ])
        elif experience_years < 3:
            recommendations.extend([
                "Take on more complex projects",
                "Mentor junior developers",
                "Contribute to open-source projects"
            ])
        else:
            recommendations.extend([
                "Consider leadership and architecture roles",
                "Share knowledge through blogs/talks",
                "Stay updated with latest industry trends"
            ])
        
        # Remove duplicates and limit to most relevant recommendations
        unique_recommendations = list(dict.fromkeys(recommendations))
        logger.info(f"✅ Generated {len(unique_recommendations)} unique recommendations")
        return unique_recommendations[:8]
    
    def _calculate_ai_confidence(self, resume_data: Dict[str, Any]) -> float:
        """Calculate AI confidence based on data completeness"""
        logger.info("🎯 Calculating AI confidence based on data completeness...")
        
        confidence_score = 0.0
        total_fields = 6
        
        # Check key fields completeness
        if resume_data.get('name') and resume_data.get('name') != 'Unknown':
            confidence_score += 0.2
        if resume_data.get('role') and resume_data.get('role') != 'Developer':
            confidence_score += 0.2
        if resume_data.get('experience'):
            confidence_score += 0.2
        if resume_data.get('skills') and len(resume_data.get('skills', [])) > 0:
            confidence_score += 0.2
        if resume_data.get('location') and resume_data.get('location') != 'Unknown':
            confidence_score += 0.1
        if resume_data.get('email') or resume_data.get('phone'):
            confidence_score += 0.1
        
        confidence = round(confidence_score, 2)
        logger.info(f"✅ AI confidence calculated: {confidence}")
        return confidence
    
    def _analyze_skill_gaps(self, resume_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze skill gaps based on role and extracted skills"""
        try:
            logger.info("🔍 Starting skill gap analysis...")
            
            # Extract data
            role = resume_data.get('role', 'Developer')
            skills_data = resume_data.get('skills', [])
            experience_data = resume_data.get('experience', {})
            
            # Handle skills data
            if isinstance(skills_data, list):
                skills = [str(skill).strip().lower() for skill in skills_data if skill and str(skill).strip()]
            else:
                skills = []
            
            # Handle experience data
            if isinstance(experience_data, dict):
                experience_years = experience_data.get('total_years', 0)
            else:
                experience_years = 0
            
            logger.info(f"🎯 Skill Gap Analysis - Role: '{role}', Skills: {len(skills)}")
            logger.info(f"🔍 Extracted skills: {skills[:10]}...")  # Show first 10 skills
            
            # Define role-specific required skills based on actual skills
            required_skills = self._get_role_required_skills(role, skills)
            logger.info(f"📋 Required skills for role '{role}': {required_skills}")
            
            # Find missing skills using improved matching
            missing_skills = []
            matched_skills = []
            
            for required_skill in required_skills:
                skill_found = False
                for skill in skills:
                    if self._skills_match(skill, required_skill):
                        skill_found = True
                        matched_skills.append(required_skill)
                        logger.info(f"✅ Skill match: '{skill}' matches '{required_skill}'")
                        break
                
                if not skill_found:
                    missing_skills.append(required_skill)
                    logger.info(f"❌ Missing skill: '{required_skill}'")
            
            logger.info(f"📊 Skill matching results - Matched: {len(matched_skills)}, Missing: {len(missing_skills)}")
            logger.info(f"✅ Matched skills: {matched_skills}")
            logger.info(f"❌ Missing skills: {missing_skills}")
            
            # Calculate gap score based on user's actual skills vs missing skills
            total_extracted_skills = len(skills)
            total_missing_skills = len(missing_skills)
            total_relevant_skills = total_extracted_skills + total_missing_skills
            gap_score = round((total_extracted_skills / total_relevant_skills) * 100, 1) if total_relevant_skills > 0 else 0
            
            # Calculate actual skills count (all extracted skills)
            actual_skills_count = len(skills)
            total_present = len(matched_skills)
            total_required = len(required_skills)  # Define total_required
            logger.info(f"📊 Skill count comparison - Total extracted: {actual_skills_count}, Role-specific present: {total_present}, Missing: {len(missing_skills)}")
            
            # Determine role category
            role_category = self._categorize_role(role)
            
            # Generate recommendations based on missing skills
            # Convert display role category to internal category for recommendations
            internal_role_category = self._convert_display_to_internal_category(role_category)
            recommendations = self._generate_skill_gap_recommendations(missing_skills, internal_role_category, experience_years)
            
            skill_gap_analysis = {
                'gap_score': gap_score,
                'missing_skills': missing_skills,
                'total_present': total_present,
                'total_extracted_skills': actual_skills_count,  # All extracted skills
                'role_category': role_category,
                'total_required': total_required,
                'recommendations': recommendations
            }
            
            logger.info(f"✅ Skill gap analysis completed - Gap Score: {gap_score}%, Missing: {len(missing_skills)}")
            return skill_gap_analysis
            
        except Exception as e:
            logger.error(f"❌ Skill gap analysis error: {e}")
            return {
                'gap_score': 0.0,
                'missing_skills': [],
                'total_present': 0,
                'role_category': 'Unknown',
                'total_required': 0
            }
    
    def _get_role_required_skills(self, role: str, skills: List[str]) -> List[str]:
        """Get required skills for specific role based on actual skills and role"""
        role_lower = role.lower()
        skills_lower = [skill.lower() for skill in skills]
        
        logger.info(f"🔍 Getting required skills for role: '{role}' with {len(skills)} existing skills")
        logger.info(f"🔍 User's actual skills: {skills}")
        
        # Determine role category
        role_category = self._determine_role_category(role_lower, skills_lower)
        logger.info(f"🎯 Role category determined: {role_category}")
        
        # Build required skills based on user's actual skills and role
        required_skills = self._build_personalized_required_skills(role, skills, role_category)
        
        logger.info(f"📋 Personalized required skills ({len(required_skills)}): {required_skills}")
        return required_skills
    
    def _build_personalized_required_skills(self, role: str, user_skills: List[str], role_category: str) -> List[str]:
        """Build personalized required skills based on user's actual skills and role"""
        logger.info(f"🔧 Building personalized skills for role: '{role}', category: {role_category}")
        logger.info(f"🔧 User skills received: {user_skills}")
        logger.info(f"🔧 User skills count: {len(user_skills)}")
        logger.info(f"🔧 User skills type: {type(user_skills)}")
        
        # Handle empty or invalid skills
        if not user_skills or not isinstance(user_skills, list):
            logger.warning(f"⚠️ Invalid skills data: {user_skills}")
            return ['Upload resume to analyze skills']
        
        required_skills = []
        user_skills_lower = [skill.lower() for skill in user_skills if skill and isinstance(skill, str)]
        
        # Start with user's existing skills (they're already covered)
        covered_skills = []
        for skill in user_skills:
            if skill.lower() not in covered_skills:
                covered_skills.append(skill.lower())
        
        # Add complementary skills based on user's existing skills
        complementary_skills = []
        
        # Analyze user's skill stack to determine missing components
        has_frontend = any(skill in user_skills_lower for skill in ['html', 'css', 'javascript', 'bootstrap', 'react', 'angular', 'vue'])
        has_backend = any(skill in user_skills_lower for skill in ['java', 'spring', 'spring boot', 'python', 'node.js', 'express'])
        has_database = any(skill in user_skills_lower for skill in ['mysql', 'oracle', 'sql', 'postgresql', 'mongodb'])
        has_devops = any(skill in user_skills_lower for skill in ['docker', 'kubernetes', 'aws', 'azure', 'jenkins'])
        has_testing = any(skill in user_skills_lower for skill in ['junit', 'testng', 'selenium', 'jest', 'cypress'])
        has_version_control = any(skill in user_skills_lower for skill in ['git', 'github', 'gitlab'])
        has_build_tools = any(skill in user_skills_lower for skill in ['maven', 'gradle', 'npm', 'yarn'])
        
        # Frontend skills analysis
        if has_frontend:
            if 'javascript' in user_skills_lower and 'react' not in user_skills_lower:
                complementary_skills.extend(['React', 'Modern JavaScript', 'ES6+'])
            if 'bootstrap' in user_skills_lower:
                complementary_skills.extend(['CSS Grid', 'Flexbox', 'Responsive Design'])
            if not any(skill in user_skills_lower for skill in ['typescript', 'ts']):
                complementary_skills.extend(['TypeScript', 'Type Safety'])
        
        # Backend skills analysis
        if has_backend:
            if 'java' in user_skills_lower and 'spring boot' not in user_skills_lower:
                complementary_skills.extend(['Spring Boot', 'REST API', 'Microservices'])
            if 'python' in user_skills_lower and not any(skill in user_skills_lower for skill in ['django', 'flask']):
                complementary_skills.extend(['Django/Flask', 'Python Web Framework'])
            if not has_database:
                complementary_skills.extend(['Database Integration', 'SQL', 'ORM'])
        
        # Database skills analysis
        if has_database:
            if 'sql' in user_skills_lower and 'mysql' not in user_skills_lower:
                complementary_skills.extend(['MySQL/PostgreSQL', 'Database Design'])
            if not any(skill in user_skills_lower for skill in ['redis', 'mongodb']):
                complementary_skills.extend(['NoSQL Database', 'Caching'])
        
        # DevOps and deployment
        if not has_devops:
            if has_backend:
                complementary_skills.extend(['Docker', 'Cloud Deployment', 'CI/CD'])
            if has_frontend:
                complementary_skills.extend(['Web Hosting', 'CDN', 'Performance Optimization'])
        
        # Testing
        if not has_testing:
            if has_backend:
                complementary_skills.extend(['Unit Testing', 'Integration Testing', 'Test Automation'])
            if has_frontend:
                complementary_skills.extend(['Frontend Testing', 'E2E Testing'])
        
        # Version control and collaboration
        if has_version_control:
            complementary_skills.extend(['Code Review', 'Branching Strategy', 'Collaborative Development'])
        
        # Build and deployment
        if has_build_tools:
            complementary_skills.extend(['Build Automation', 'Dependency Management', 'Package Management'])
        
        # Role-specific recommendations based on specific categories
        internal_category = self._convert_display_to_internal_category(role_category)
        
        if internal_category == 'java_fullstack':
            if has_frontend and not has_backend:
                complementary_skills.extend(['Spring Boot', 'JPA/Hibernate', 'Microservices'])
            elif has_backend and not has_frontend:
                complementary_skills.extend(['React/Angular', 'Bootstrap', 'Responsive Design'])
            else:
                complementary_skills.extend(['Spring Security', 'Docker', 'CI/CD'])
        
        elif internal_category == 'java_backend':
            complementary_skills.extend(['Spring Security', 'Microservices', 'Docker', 'Kubernetes'])
        
        elif internal_category == 'python_fullstack':
            if has_frontend and not has_backend:
                complementary_skills.extend(['Django/Flask', 'FastAPI', 'Celery'])
            elif has_backend and not has_frontend:
                complementary_skills.extend(['React/Vue', 'Bootstrap', 'Responsive Design'])
            else:
                complementary_skills.extend(['Redis', 'Docker', 'CI/CD'])
        
        elif internal_category == 'python_backend':
            complementary_skills.extend(['FastAPI', 'Celery', 'Redis', 'Docker'])
        
        elif internal_category == 'javascript_fullstack':
            if has_frontend and not has_backend:
                complementary_skills.extend(['Node.js', 'Express', 'MongoDB'])
            elif has_backend and not has_frontend:
                complementary_skills.extend(['React/Angular/Vue', 'Bootstrap', 'TypeScript'])
            else:
                complementary_skills.extend(['GraphQL', 'Socket.io', 'Docker'])
        
        elif internal_category == 'javascript_backend':
            complementary_skills.extend(['GraphQL', 'Socket.io', 'Redis', 'Docker'])
        
        elif internal_category == 'generic_fullstack':
            if has_frontend and not has_backend:
                complementary_skills.extend(['Backend Development', 'API Design', 'Server-side Logic'])
            elif has_backend and not has_frontend:
                complementary_skills.extend(['Frontend Development', 'User Interface', 'Client-side Logic'])
            elif not has_frontend and not has_backend:
                complementary_skills.extend(['Full Stack Framework', 'End-to-End Development'])
        
        # Security and best practices
        if has_backend or has_frontend:
            complementary_skills.extend(['Security Best Practices', 'Authentication', 'Authorization'])
        
        # Performance and optimization
        if has_frontend:
            complementary_skills.extend(['Performance Optimization', 'SEO', 'Accessibility'])
        if has_backend:
            complementary_skills.extend(['API Optimization', 'Caching Strategies', 'Load Balancing'])
        
        # Remove duplicates and filter out skills user already has
        complementary_skills = list(set(complementary_skills))
        final_skills = []
        
        for skill in complementary_skills:
            skill_lower = skill.lower()
            # Only add if user doesn't already have this skill or similar
            if not any(existing_skill.lower() == skill_lower or 
                      skill_lower in existing_skill.lower() or 
                      existing_skill.lower() in skill_lower 
                      for existing_skill in user_skills):
                final_skills.append(skill)
        
        # Limit to most relevant skills (8-12 skills)
        final_skills = final_skills[:10]
        
        logger.info(f"✅ Personalized skills built: {len(final_skills)} complementary skills")
        logger.info(f"🔍 Complementary skills: {final_skills}")
        
        return final_skills
    
    def _get_base_required_skills(self, role_category: str) -> List[str]:
        """Get base required skills for role category"""
        # Convert display category to internal category if needed
        internal_category = self._convert_display_to_internal_category(role_category)
        
        if internal_category == 'data_science':
            return [
                'Python', 'SQL', 'Machine Learning', 'Data Visualization',
                'Statistics', 'Pandas', 'NumPy', 'Jupyter', 'Tableau', 'Power BI',
                'Data Analysis', 'Data Cleaning', 'Feature Engineering'
            ]
        elif internal_category == 'frontend':
            return [
                'HTML', 'CSS', 'JavaScript', 'React', 'Angular', 'Vue',
                'Responsive Design', 'Git', 'Bootstrap', 'TypeScript',
                'DOM Manipulation', 'State Management', 'Webpack'
            ]
        elif internal_category == 'backend':
            return [
                'Python', 'Java', 'Node.js', 'SQL', 'REST API', 'Microservices',
                'Docker', 'AWS', 'Database Design', 'Spring Boot',
                'Authentication', 'Caching', 'Load Balancing'
            ]
        elif internal_category == 'java_fullstack':
            return [
                'Java', 'Spring Boot', 'HTML', 'CSS', 'JavaScript', 'MySQL', 'Git',
                'REST API', 'Maven', 'JPA/Hibernate', 'Bootstrap', 'jQuery'
            ]
        elif internal_category == 'java_backend':
            return [
                'Java', 'Spring Boot', 'MySQL', 'REST API', 'Maven', 'JPA/Hibernate',
                'Microservices', 'Security', 'Testing', 'Git'
            ]
        elif internal_category == 'python_fullstack':
            return [
                'Python', 'Django/Flask', 'HTML', 'CSS', 'JavaScript', 'PostgreSQL', 'Git',
                'REST API', 'Pip', 'SQLAlchemy', 'Bootstrap', 'React/Vue'
            ]
        elif internal_category == 'python_backend':
            return [
                'Python', 'Django/Flask', 'PostgreSQL', 'REST API', 'Pip', 'SQLAlchemy',
                'FastAPI', 'Celery', 'Redis', 'Git'
            ]
        elif internal_category == 'javascript_fullstack':
            return [
                'JavaScript', 'Node.js', 'React/Angular/Vue', 'HTML', 'CSS', 'MongoDB', 'Git',
                'Express', 'NPM', 'REST API', 'Bootstrap', 'TypeScript'
            ]
        elif internal_category == 'javascript_backend':
            return [
                'JavaScript', 'Node.js', 'Express', 'MongoDB', 'REST API', 'NPM',
                'GraphQL', 'Socket.io', 'JWT', 'Git'
            ]
        elif internal_category == 'generic_fullstack':
            return [
                'HTML', 'CSS', 'JavaScript', 'Git', 'Database', 'API Development',
                'Frontend Framework', 'Backend Framework', 'Version Control',
                'Responsive Design', 'Testing', 'Deployment'
            ]
        elif internal_category == 'devops':
            return [
                'Docker', 'Kubernetes', 'AWS', 'Azure', 'Jenkins', 'Git',
                'Linux', 'Python', 'Monitoring', 'CI/CD',
                'Infrastructure as Code', 'Terraform', 'Ansible'
            ]
        elif internal_category == 'mobile':
            return [
                'React Native', 'Flutter', 'Android', 'iOS', 'Mobile Development',
                'Mobile UI', 'Mobile Testing', 'App Store', 'Google Play'
            ]
        elif internal_category == 'qa':
            return [
                'Selenium', 'Testing', 'Automation', 'JUnit', 'TestNG', 'Cypress',
                'API Testing', 'Performance Testing', 'Test Planning', 'Quality Assurance'
            ]
        else:  # Generic developer
            return [
                'Programming', 'Data Structures', 'Algorithms', 'Git',
                'Database', 'API Development', 'Testing', 'Problem Solving',
                'Software Development', 'Code Review', 'Debugging'
            ]
    
    def _customize_required_skills(self, base_skills: List[str], user_skills: List[str], role_category: str) -> List[str]:
        """Customize required skills based on user's existing skills"""
        logger.info(f"🔧 Customizing required skills for {role_category} role")
        
        # Start with base skills
        required_skills = base_skills.copy()
        
        # Add skills that user already has (to show they're covered)
        user_skill_matches = []
        for user_skill in user_skills:
            for base_skill in base_skills:
                if self._skills_match(user_skill, base_skill):
                    user_skill_matches.append(base_skill)
                    break
        
        # Remove skills user already has from missing skills
        for matched_skill in user_skill_matches:
            if matched_skill in required_skills:
                required_skills.remove(matched_skill)
        
        # Add role-specific skills based on user's existing skills
        internal_category = self._convert_display_to_internal_category(role_category)
        if internal_category == 'fullstack':
            # If user has Java skills, focus on Java ecosystem
            if any(skill in user_skills for skill in ['java', 'spring', 'spring boot']):
                required_skills.extend(['Spring Boot', 'Java', 'SQL', 'REST API'])
            # If user has frontend skills, add backend requirements
            if any(skill in user_skills for skill in ['html', 'css', 'javascript', 'bootstrap']):
                required_skills.extend(['Backend Framework', 'API Development', 'Database'])
            # If user has database skills, add backend requirements
            if any(skill in user_skills for skill in ['mysql', 'oracle', 'sql']):
                required_skills.extend(['Backend Framework', 'API Development'])
        
        elif internal_category == 'data_science':
            # If user has basic Python, add advanced data science skills
            if 'python' in user_skills:
                required_skills.extend(['Scikit-learn', 'TensorFlow', 'PyTorch', 'Deep Learning'])
            if 'sql' in user_skills:
                required_skills.extend(['Database Optimization', 'ETL Processes', 'Data Warehousing'])
        
        elif internal_category == 'frontend':
            # If user has basic HTML/CSS, add modern framework requirements
            if any(skill in user_skills for skill in ['html', 'css']):
                required_skills.extend(['Frontend Framework', 'TypeScript', 'State Management'])
        
        elif internal_category == 'backend':
            # If user has basic programming, add advanced backend skills
            if any(skill in user_skills for skill in ['python', 'java', 'node.js']):
                required_skills.extend(['API Development', 'Database Design', 'Authentication'])
        
        # Remove duplicates and limit to reasonable number
        required_skills = list(dict.fromkeys(required_skills))  # Remove duplicates while preserving order
        required_skills = required_skills[:15]  # Limit to 15 most relevant skills
        
        logger.info(f"✅ Customized to {len(required_skills)} required skills")
        return required_skills
    
    def _skills_match(self, user_skill: str, required_skill: str) -> bool:
        """Check if user skill matches required skill"""
        user_lower = user_skill.lower().strip()
        required_lower = required_skill.lower().strip()
        
        # Skip very short matches to avoid false positives
        if len(user_lower) < 3 or len(required_lower) < 3:
            return False
        
        # Exact match
        if user_lower == required_lower:
            return True
        
        # Check for skill matches with flexible mapping
        skill_mapping = {
            # Frontend skills
            'html': ['html', 'html5', 'hypertext markup language'],
            'css': ['css', 'css3', 'cascading style sheets', 'bootstrap', 'tailwind'],
            'javascript': ['javascript', 'js', 'ecmascript', 'jquery', 'react', 'angular', 'vue'],
            'frontend framework': ['react', 'angular', 'vue', 'ember', 'svelte', 'next.js'],
            'responsive design': ['responsive', 'mobile-first', 'bootstrap', 'css grid', 'flexbox'],
            
            # Backend skills
            'java': ['java', 'spring', 'spring boot', 'hibernate', 'jpa'],
            'python': ['python', 'django', 'flask', 'fastapi'],
            'node.js': ['node.js', 'nodejs', 'express', 'npm'],
            'backend framework': ['spring', 'spring boot', 'django', 'flask', 'express', 'rails'],
            'api development': ['rest api', 'graphql', 'api', 'microservices', 'web services'],
            
            # Database skills
            'database': ['mysql', 'postgresql', 'mongodb', 'sqlite', 'oracle', 'sql server'],
            'sql': ['sql', 'mysql', 'postgresql', 'oracle', 'sqlite'],
            
            # DevOps/Deployment
            'version control': ['git', 'github', 'gitlab', 'bitbucket', 'svn'],
            'deployment': ['docker', 'kubernetes', 'aws', 'azure', 'heroku', 'vercel'],
            'testing': ['junit', 'testng', 'jest', 'mocha', 'selenium', 'cypress'],
            
            # General skills
            'git': ['git', 'github', 'gitlab', 'bitbucket'],
            'maven': ['maven', 'gradle', 'build tool'],
            'spring boot': ['spring boot', 'spring', 'spring framework']
        }
        
        # Check exact matches first
        for skill_key, variations in skill_mapping.items():
            if user_lower in variations and required_lower in variations:
                return True
            if user_lower == skill_key and required_lower in variations:
                return True
            if required_lower == skill_key and user_lower in variations:
                return True
        
        # Prevent false positives by checking if skills are too different
        # Only allow partial matches if they share significant overlap
        if len(user_lower) >= 4 and len(required_lower) >= 4:
            # Check if one skill is contained in the other (but not vice versa)
            if user_lower in required_lower and len(user_lower) >= len(required_lower) * 0.7:
                return True
            if required_lower in user_lower and len(required_lower) >= len(user_lower) * 0.7:
                return True
        
        return False
    
    def _convert_display_to_internal_category(self, display_category: str) -> str:
        """Convert display role category to internal category"""
        category_mapping = {
            'Java Full Stack Development': 'java_fullstack',
            'Java Backend Development': 'java_backend',
            'Python Full Stack Development': 'python_fullstack',
            'Python Backend Development': 'python_backend',
            'JavaScript Full Stack Development': 'javascript_fullstack',
            'JavaScript Backend Development': 'javascript_backend',
            'Data Science/Analytics': 'data_science',
            'Frontend Development': 'frontend',
            'Backend Development': 'backend',
            'Full Stack Development': 'generic_fullstack',
            'DevOps/Cloud': 'devops',
            'Mobile Development': 'mobile',
            'Quality Assurance': 'qa',
            'Software Development': 'generic'
        }
        return category_mapping.get(display_category, 'generic')
    
    def _categorize_role(self, role: str) -> str:
        """Categorize role into specific categories"""
        role_lower = role.lower()
        
        # Java-specific roles
        if 'java' in role_lower:
            if 'full stack' in role_lower:
                return 'Java Full Stack Development'
            else:
                return 'Java Backend Development'
        
        # Python-specific roles
        elif 'python' in role_lower:
            if 'full stack' in role_lower:
                return 'Python Full Stack Development'
            else:
                return 'Python Backend Development'
        
        # JavaScript/Node.js specific roles
        elif any(keyword in role_lower for keyword in ['javascript', 'node.js', 'nodejs']):
            if 'full stack' in role_lower:
                return 'JavaScript Full Stack Development'
            else:
                return 'JavaScript Backend Development'
        
        # Data Science roles
        elif any(keyword in role_lower for keyword in ['data', 'analyst', 'scientist', 'ml', 'machine learning', 'ai', 'data science']):
            return 'Data Science/Analytics'
        
        # Frontend roles
        elif any(keyword in role_lower for keyword in ['frontend', 'ui', 'ux', 'web', 'front-end']):
            return 'Frontend Development'
        
        # Backend roles
        elif any(keyword in role_lower for keyword in ['backend', 'api', 'server', 'microservices', 'back-end']):
            return 'Backend Development'
        
        # Generic full stack roles
        elif any(keyword in role_lower for keyword in ['fullstack', 'full stack', 'full-stack', 'full stack developer']):
            return 'Full Stack Development'
        
        # DevOps roles
        elif any(keyword in role_lower for keyword in ['devops', 'cloud', 'infrastructure', 'deployment', 'sre']):
            return 'DevOps/Cloud'
        
        # Mobile roles
        elif any(keyword in role_lower for keyword in ['mobile', 'android', 'ios', 'react native', 'flutter']):
            return 'Mobile Development'
        
        # QA roles
        elif any(keyword in role_lower for keyword in ['qa', 'testing', 'quality', 'test', 'automation']):
            return 'Quality Assurance'
        
        else:
            return 'Software Development'
    
    def _analyze_salary_projection(self, resume_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze salary projection based on skills and experience from resume"""
        try:
            logger.info("💰 Starting salary projection analysis...")
            
            # Extract data
            role = resume_data.get('role', 'Developer')
            experience_data = resume_data.get('experience', {})
            skills_data = resume_data.get('skills', [])
            
            # Handle experience data
            if isinstance(experience_data, dict):
                experience_years = experience_data.get('total_years', 0)
            else:
                experience_years = 0
            
            # Handle skills data
            if isinstance(skills_data, list):
                skills = [str(skill).strip() for skill in skills_data if skill and str(skill).strip()]
            else:
                skills = []
            
            logger.info(f"💰 Salary Projection - Role: {role}, Experience: {experience_years}, Skills: {len(skills)}")
            
            # Calculate salary based on skills and experience
            projected_salary = self._calculate_salary_from_skills_experience(role, experience_years, skills)
            
            # Calculate salary range (±15%)
            min_salary = int(projected_salary * 0.85)
            max_salary = int(projected_salary * 1.15)
            
            salary_projection = {
                'projected_salary': projected_salary,
                'min_salary': min_salary,
                'max_salary': max_salary,
                'level': self._get_experience_level(experience_years),
                'skill_count': len(skills),
                'experience_years': experience_years
            }
            
            logger.info(f"✅ Salary projection completed - Projected: ₹{projected_salary:,}, Range: ₹{min_salary:,} - ₹{max_salary:,}")
            return salary_projection
            
        except Exception as e:
            logger.error(f"❌ Salary projection analysis error: {e}")
            return {
                'projected_salary': 0,
                'min_salary': 0,
                'max_salary': 0,
                'level': 'Unknown',
                'skill_count': 0,
                'experience_years': 0
            }
    
    def _calculate_salary_from_skills_experience(self, role: str, experience_years: int, skills: List[str]) -> int:
        """Calculate realistic salary based on actual market data and resume analysis"""
        logger.info(f"💰 AI Salary Analysis - Role: '{role}', Experience: {experience_years} years, Skills: {len(skills)}")
        
        # Determine role category for market-based salary calculation
        role_category = self._determine_role_category(role.lower(), [s.lower() for s in skills])
        logger.info(f"🎯 Role category determined: {role_category}")
        
        # Realistic salary ranges based on actual Indian IT market (2024)
        market_salaries = {
            'data_science': {
                'fresher': (250000, 400000),      # 2.5-4 LPA
                'junior': (400000, 600000),       # 4-6 LPA
                'mid': (600000, 900000),          # 6-9 LPA
                'senior': (900000, 1300000),      # 9-13 LPA
                'lead': (1300000, 1800000)        # 13-18 LPA
            },
            'frontend': {
                'fresher': (200000, 350000),      # 2-3.5 LPA
                'junior': (350000, 550000),       # 3.5-5.5 LPA
                'mid': (550000, 800000),          # 5.5-8 LPA
                'senior': (800000, 1200000),      # 8-12 LPA
                'lead': (1200000, 1600000)        # 12-16 LPA
            },
            'backend': {
                'fresher': (250000, 400000),      # 2.5-4 LPA
                'junior': (400000, 600000),       # 4-6 LPA
                'mid': (600000, 900000),          # 6-9 LPA
                'senior': (900000, 1300000),      # 9-13 LPA
                'lead': (1300000, 1800000)        # 13-18 LPA
            },
            'fullstack': {
                'fresher': (300000, 450000),      # 3-4.5 LPA
                'junior': (450000, 700000),       # 4.5-7 LPA
                'mid': (700000, 1000000),         # 7-10 LPA
                'senior': (1000000, 1400000),     # 10-14 LPA
                'lead': (1400000, 1900000)        # 14-19 LPA
            },
            'devops': {
                'fresher': (300000, 500000),      # 3-5 LPA
                'junior': (500000, 750000),       # 5-7.5 LPA
                'mid': (750000, 1100000),         # 7.5-11 LPA
                'senior': (1100000, 1600000),     # 11-16 LPA
                'lead': (1600000, 2200000)        # 16-22 LPA
            },
            'mobile': {
                'fresher': (250000, 400000),      # 2.5-4 LPA
                'junior': (400000, 600000),       # 4-6 LPA
                'mid': (600000, 900000),          # 6-9 LPA
                'senior': (900000, 1300000),      # 9-13 LPA
                'lead': (1300000, 1800000)        # 13-18 LPA
            },
            'qa': {
                'fresher': (200000, 320000),      # 2-3.2 LPA
                'junior': (320000, 500000),       # 3.2-5 LPA
                'mid': (500000, 750000),          # 5-7.5 LPA
                'senior': (750000, 1100000),      # 7.5-11 LPA
                'lead': (1100000, 1500000)        # 11-15 LPA
            },
            'generic': {
                'fresher': (200000, 350000),      # 2-3.5 LPA
                'junior': (350000, 550000),       # 3.5-5.5 LPA
                'mid': (550000, 800000),          # 5.5-8 LPA
                'senior': (800000, 1200000),      # 8-12 LPA
                'lead': (1200000, 1600000)        # 12-16 LPA
            }
        }
        
        # Determine experience level
        if experience_years <= 0:
            exp_level = 'fresher'
        elif experience_years <= 2:
            exp_level = 'junior'
        elif experience_years <= 5:
            exp_level = 'mid'
        elif experience_years <= 8:
            exp_level = 'senior'
        else:
            exp_level = 'lead'
        
        logger.info(f"📊 Experience level: {exp_level} ({experience_years} years)")
        
        # Get base salary range for role and experience level
        salary_range = market_salaries.get(role_category, market_salaries['generic'])[exp_level]
        min_salary, max_salary = salary_range
        
        logger.info(f"💰 Base salary range: ₹{min_salary:,} - ₹{max_salary:,}")
        
        # Calculate skill-based adjustment
        skill_adjustment = self._calculate_skill_adjustment(skills, role_category)
        
        # Calculate final salary using lower end of range for more realistic projections
        base_salary = min_salary + (max_salary - min_salary) * 0.3  # 30% into the range
        adjusted_salary = int(base_salary * skill_adjustment)
        
        # Ensure salary stays within reasonable bounds
        final_salary = max(min_salary, min(max_salary, adjusted_salary))
        
        logger.info(f"💰 Skill adjustment: {skill_adjustment:.2f}")
        logger.info(f"💰 Final AI-calculated salary: ₹{final_salary:,}")
        
        return final_salary
    
    def _calculate_skill_adjustment(self, skills: List[str], role_category: str) -> float:
        """Calculate skill-based salary adjustment factor"""
        skill_count = len(skills)
        
        # Conservative base adjustment based on skill count
        if skill_count <= 3:
            base_adjustment = 0.8   # Below average
        elif skill_count <= 6:
            base_adjustment = 0.9   # Slightly below average
        elif skill_count <= 10:
            base_adjustment = 1.0   # Average
        elif skill_count <= 15:
            base_adjustment = 1.05  # Slightly above average
        elif skill_count <= 20:
            base_adjustment = 1.08  # Good
        else:
            base_adjustment = 1.1   # Excellent
        
        # High-demand skills bonus
        high_demand_skills = {
            'data_science': ['python', 'machine learning', 'data science', 'sql', 'pandas', 'numpy', 'tensorflow', 'pytorch', 'statistics', 'data visualization'],
            'frontend': ['react', 'angular', 'vue', 'javascript', 'typescript', 'html', 'css', 'responsive design', 'webpack', 'bootstrap'],
            'backend': ['python', 'java', 'node.js', 'sql', 'rest api', 'microservices', 'docker', 'aws', 'spring boot', 'django'],
            'fullstack': ['react', 'node.js', 'python', 'javascript', 'sql', 'html', 'css', 'rest api', 'docker', 'aws'],
            'devops': ['docker', 'kubernetes', 'aws', 'azure', 'jenkins', 'terraform', 'ansible', 'ci/cd', 'monitoring', 'linux'],
            'mobile': ['react native', 'flutter', 'android', 'ios', 'mobile development', 'kotlin', 'swift', 'mobile ui'],
            'qa': ['selenium', 'testing', 'automation', 'junit', 'testng', 'cypress', 'api testing', 'performance testing'],
            'generic': ['python', 'java', 'javascript', 'sql', 'git', 'docker', 'aws', 'testing', 'api', 'database']
        }
        
        relevant_skills = high_demand_skills.get(role_category, high_demand_skills['generic'])
        
        # Count matching high-demand skills
        matching_skills = 0
        for skill in skills:
            skill_lower = skill.lower()
            for demand_skill in relevant_skills:
                if demand_skill in skill_lower or skill_lower in demand_skill:
                    matching_skills += 1
                    break
        
        # Conservative bonus based on matching skills
        if matching_skills >= 8:
            skill_bonus = 1.08  # Excellent match
        elif matching_skills >= 6:
            skill_bonus = 1.05  # Good match
        elif matching_skills >= 4:
            skill_bonus = 1.03  # Above average match
        elif matching_skills >= 2:
            skill_bonus = 1.0   # Average match
        else:
            skill_bonus = 0.95  # Below average match
        
        final_adjustment = base_adjustment * skill_bonus
        
        logger.info(f"🔍 Skill analysis - Total: {skill_count}, High-demand matches: {matching_skills}")
        logger.info(f"🔍 Adjustment factors - Base: {base_adjustment:.2f}, Bonus: {skill_bonus:.2f}, Final: {final_adjustment:.2f}")
        
        return final_adjustment
    
    def _analyze_career_growth(self, resume_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze career growth based on resume data"""
        try:
            logger.info("📈 Starting career growth analysis...")
            
            # Extract data
            role = resume_data.get('role', 'Developer')
            experience_data = resume_data.get('experience', {})
            skills_data = resume_data.get('skills', [])
            
            # Handle experience data
            if isinstance(experience_data, dict):
                experience_years = experience_data.get('total_years', 0)
            else:
                experience_years = 0
            
            # Handle skills data
            if isinstance(skills_data, list):
                skills = [str(skill).strip() for skill in skills_data if skill and str(skill).strip()]
            else:
                skills = []
            
            logger.info(f"📈 Career Growth Analysis - Role: {role}, Experience: {experience_years}, Skills: {len(skills)}")
            
            # Determine career stage
            career_stage = self._determine_career_stage(experience_years)
            
            # Calculate growth metrics
            growth_metrics = self._calculate_growth_metrics(role, experience_years, skills)
            
            # Generate career path
            career_path = self._generate_career_path(role, experience_years, skills)
            
            # Generate growth recommendations
            growth_recommendations = self._generate_growth_recommendations(role, experience_years, skills)
            
            career_growth_analysis = {
                'career_stage': career_stage,
                'growth_metrics': growth_metrics,
                'career_path': career_path,
                'growth_recommendations': growth_recommendations
            }
            
            logger.info(f"✅ Career growth analysis completed - Stage: {career_stage}")
            return career_growth_analysis
            
        except Exception as e:
            logger.error(f"❌ Career growth analysis error: {e}")
            return {
                'career_stage': 'Unknown',
                'growth_metrics': {
                    'market_demand': 'N/A',
                    'growth_rate': 'N/A',
                    'experience_score': 0,
                    'skill_score': 0,
                    'promotion_probability': 0.0
                },
                'career_path': [],
                'growth_recommendations': []
            }
    
    def _determine_career_stage(self, experience_years: int) -> str:
        """Determine career stage based on experience"""
        if experience_years <= 0:
            return "Entry Level"
        elif experience_years <= 2:
            return "Junior Level"
        elif experience_years <= 5:
            return "Mid Level"
        elif experience_years <= 8:
            return "Senior Level"
        else:
            return "Lead/Principal Level"
    
    def _calculate_growth_metrics(self, role: str, experience_years: int, skills: List[str]) -> Dict[str, Any]:
        """Calculate growth metrics based on role, experience, and skills"""
        logger.info(f"📊 Calculating growth metrics for {role} with {experience_years} years experience")
        
        # Determine role category
        role_category = self._determine_role_category(role.lower(), [s.lower() for s in skills])
        
        # Market demand by role category
        market_demand_map = {
            'data_science': 'High',
            'frontend': 'High',
            'backend': 'High',
            'fullstack': 'Very High',
            'devops': 'Very High',
            'mobile': 'Medium',
            'qa': 'Medium',
            'generic': 'Medium'
        }
        
        market_demand = market_demand_map.get(role_category, 'Medium')
        
        # Growth rate based on experience and role
        if experience_years <= 2:
            growth_rate = 'Fast' if role_category in ['data_science', 'fullstack', 'devops'] else 'Moderate'
        elif experience_years <= 5:
            growth_rate = 'Moderate' if role_category in ['data_science', 'fullstack', 'devops'] else 'Steady'
        else:
            growth_rate = 'Steady'
        
        # Experience score (0-100)
        experience_score = min(100, int((experience_years / 10) * 100))
        
        # Skill score based on skill count and relevance
        skill_count = len(skills)
        if skill_count <= 5:
            skill_score = 30
        elif skill_count <= 10:
            skill_score = 50
        elif skill_count <= 15:
            skill_score = 70
        elif skill_count <= 20:
            skill_score = 85
        else:
            skill_score = 100
        
        # Promotion probability based on experience, skills, and role demand
        base_probability = 0.3  # Base 30%
        
        # Experience bonus
        if experience_years >= 3:
            base_probability += 0.2
        if experience_years >= 5:
            base_probability += 0.2
        
        # Skill bonus
        if skill_count >= 10:
            base_probability += 0.15
        if skill_count >= 15:
            base_probability += 0.1
        
        # Role demand bonus
        if market_demand == 'Very High':
            base_probability += 0.1
        elif market_demand == 'High':
            base_probability += 0.05
        
        promotion_probability = min(0.95, base_probability)
        
        logger.info(f"📊 Growth metrics - Market Demand: {market_demand}, Growth Rate: {growth_rate}")
        logger.info(f"📊 Scores - Experience: {experience_score}, Skills: {skill_score}, Promotion: {promotion_probability:.2f}")
        
        return {
            'market_demand': market_demand,
            'growth_rate': growth_rate,
            'experience_score': experience_score,
            'skill_score': skill_score,
            'promotion_probability': promotion_probability
        }
    
    def _generate_career_path(self, role: str, experience_years: int, skills: List[str]) -> List[str]:
        """Generate career path based on role and experience"""
        logger.info(f"🛤️ Generating career path for {role} with {experience_years} years experience")
        
        role_category = self._determine_role_category(role.lower(), [s.lower() for s in skills])
        
        # Define career paths by role category
        career_paths = {
            'data_science': [
                'Data Analyst',
                'Senior Data Analyst',
                'Data Scientist',
                'Senior Data Scientist',
                'Lead Data Scientist',
                'Principal Data Scientist'
            ],
            'frontend': [
                'Frontend Developer',
                'Senior Frontend Developer',
                'Frontend Lead',
                'Frontend Architect',
                'UI/UX Lead',
                'Frontend Manager'
            ],
            'backend': [
                'Backend Developer',
                'Senior Backend Developer',
                'Backend Lead',
                'Backend Architect',
                'API Lead',
                'Backend Manager'
            ],
            'fullstack': [
                'Full Stack Developer',
                'Senior Full Stack Developer',
                'Full Stack Lead',
                'Full Stack Architect',
                'Technical Lead',
                'Engineering Manager'
            ],
            'devops': [
                'DevOps Engineer',
                'Senior DevOps Engineer',
                'DevOps Lead',
                'DevOps Architect',
                'Platform Engineer',
                'DevOps Manager'
            ],
            'mobile': [
                'Mobile Developer',
                'Senior Mobile Developer',
                'Mobile Lead',
                'Mobile Architect',
                'Mobile Team Lead',
                'Mobile Manager'
            ],
            'qa': [
                'QA Engineer',
                'Senior QA Engineer',
                'QA Lead',
                'QA Architect',
                'Test Manager',
                'Quality Manager'
            ],
            'generic': [
                'Software Developer',
                'Senior Software Developer',
                'Technical Lead',
                'Software Architect',
                'Engineering Lead',
                'Engineering Manager'
            ]
        }
        
        path = career_paths.get(role_category, career_paths['generic'])
        
        # Determine current position in path
        if experience_years <= 0:
            current_index = 0
        elif experience_years <= 2:
            current_index = 1
        elif experience_years <= 5:
            current_index = 2
        elif experience_years <= 8:
            current_index = 3
        else:
            current_index = 4
        
        # Return next 3-4 steps from current position
        next_steps = path[current_index:current_index + 4]
        
        logger.info(f"🛤️ Career path generated: {next_steps}")
        return next_steps
    
    def _generate_growth_recommendations(self, role: str, experience_years: int, skills: List[str]) -> List[str]:
        """Generate growth recommendations based on role, experience, and skills"""
        logger.info(f"💡 Generating growth recommendations for {role} with {experience_years} years experience")
        
        recommendations = []
        role_category = self._determine_role_category(role.lower(), [s.lower() for s in skills])
        
        # Experience-based recommendations
        if experience_years <= 2:
            recommendations.extend([
                "Focus on mastering core technologies",
                "Build 2-3 portfolio projects",
                "Contribute to open-source projects",
                "Attend tech meetups and conferences"
            ])
        elif experience_years <= 5:
            recommendations.extend([
                "Take on more complex projects",
                "Mentor junior developers",
                "Learn system design principles",
                "Consider technical certifications"
            ])
        else:
            recommendations.extend([
                "Focus on leadership and architecture",
                "Share knowledge through blogs/talks",
                "Consider management track",
                "Stay updated with latest trends"
            ])
        
        # Role-specific recommendations
        if role_category == 'data_science':
            recommendations.extend([
                "Complete advanced ML courses",
                "Work on Kaggle competitions",
                "Learn cloud platforms (AWS/GCP)",
                "Master data visualization tools"
            ])
        elif role_category == 'frontend':
            recommendations.extend([
                "Learn modern frameworks (React/Vue/Angular)",
                "Master responsive design",
                "Learn performance optimization",
                "Understand accessibility standards"
            ])
        elif role_category == 'backend':
            recommendations.extend([
                "Learn microservices architecture",
                "Master database optimization",
                "Learn cloud platforms",
                "Understand security best practices"
            ])
        elif role_category == 'fullstack':
            recommendations.extend([
                "Master both frontend and backend",
                "Learn DevOps practices",
                "Understand system design",
                "Focus on full-stack architecture"
            ])
        elif role_category == 'devops':
            recommendations.extend([
                "Master containerization (Docker/K8s)",
                "Learn infrastructure as code",
                "Understand monitoring and logging",
                "Focus on automation and CI/CD"
            ])
        
        # Limit to most relevant recommendations
        unique_recommendations = list(dict.fromkeys(recommendations))
        logger.info(f"💡 Generated {len(unique_recommendations)} growth recommendations")
        return unique_recommendations[:6]
    
    def _get_role_base_salary(self, role: str) -> int:
        """Get base salary for specific role"""
        role_lower = role.lower()
        
        if 'data' in role_lower or 'analyst' in role_lower:
            return 800000  # ₹8 LPA
        elif 'frontend' in role_lower or 'ui' in role_lower:
            return 700000  # ₹7 LPA
        elif 'backend' in role_lower or 'api' in role_lower:
            return 750000  # ₹7.5 LPA
        elif 'fullstack' in role_lower or 'full stack' in role_lower:
            return 900000  # ₹9 LPA
        elif 'devops' in role_lower:
            return 850000  # ₹8.5 LPA
        elif 'mobile' in role_lower:
            return 750000  # ₹7.5 LPA
        elif 'qa' in role_lower or 'testing' in role_lower:
            return 600000  # ₹6 LPA
        else:  # Generic developer
            return 700000  # ₹7 LPA
    
    def _calculate_experience_multiplier(self, experience_years: int) -> float:
        """Calculate experience multiplier"""
        if experience_years == 0:
            return 0.6  # Fresher
        elif experience_years < 1:
            return 0.7  # Entry level
        elif experience_years < 2:
            return 0.8  # Junior
        elif experience_years < 3:
            return 0.9  # Mid-Junior
        elif experience_years < 5:
            return 1.0  # Mid level
        elif experience_years < 8:
            return 1.3  # Senior
        elif experience_years < 12:
            return 1.6  # Lead
        else:
            return 2.0  # Principal
    
    def _calculate_location_multiplier(self, location: str) -> float:
        """Calculate location multiplier"""
        location_lower = location.lower()
        
        # Tier 1 cities
        if any(city in location_lower for city in ['bangalore', 'mumbai', 'delhi', 'hyderabad', 'pune', 'chennai']):
            return 1.2
        # Tier 2 cities
        elif any(city in location_lower for city in ['kolkata', 'ahmedabad', 'jaipur', 'lucknow', 'kanpur', 'nagpur']):
            return 1.0
        # Tier 3 cities
        elif any(city in location_lower for city in ['indore', 'bhopal', 'coimbatore', 'kochi', 'visakhapatnam']):
            return 0.9
        # International
        elif any(country in location_lower for country in ['usa', 'uk', 'canada', 'australia', 'singapore']):
            return 2.0
        else:
            return 0.8  # Default
    
    def _calculate_skill_multiplier(self, skills: List[str], role: str) -> float:
        """Calculate skill multiplier based on skill count and relevance"""
        if not skills:
            return 0.8
        
        # Count relevant skills
        relevant_skills = 0
        role_lower = role.lower()
        
        for skill in skills:
            skill_lower = skill.lower()
            if 'data' in role_lower and any(tech in skill_lower for tech in ['python', 'sql', 'machine learning', 'data science']):
                relevant_skills += 1
            elif 'frontend' in role_lower and any(tech in skill_lower for tech in ['html', 'css', 'javascript', 'react', 'angular']):
                relevant_skills += 1
            elif 'backend' in role_lower and any(tech in skill_lower for tech in ['python', 'java', 'node.js', 'sql', 'api']):
                relevant_skills += 1
            elif 'fullstack' in role_lower and any(tech in skill_lower for tech in ['html', 'css', 'javascript', 'python', 'java', 'sql']):
                relevant_skills += 1
            elif 'devops' in role_lower and any(tech in skill_lower for tech in ['docker', 'kubernetes', 'aws', 'azure', 'jenkins']):
                relevant_skills += 1
            else:
                relevant_skills += 0.5  # Generic skills
        
        # Calculate multiplier based on relevant skills
        if relevant_skills >= 8:
            return 1.3
        elif relevant_skills >= 6:
            return 1.2
        elif relevant_skills >= 4:
            return 1.1
        elif relevant_skills >= 2:
            return 1.0
        else:
            return 0.9
    
    def _calculate_role_multiplier(self, role: str) -> float:
        """Calculate role multiplier based on role demand"""
        role_lower = role.lower()
        
        # High demand roles
        if any(keyword in role_lower for keyword in ['data scientist', 'machine learning', 'ai', 'devops', 'cloud']):
            return 1.2
        # Medium demand roles
        elif any(keyword in role_lower for keyword in ['fullstack', 'full stack', 'backend', 'frontend']):
            return 1.1
        # Standard roles
        else:
            return 1.0
    
    def _analyze_location_growth(self, resume_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze location growth opportunities"""
        try:
            logger.info("📍 Starting location growth analysis...")
            
            # Extract data
            location = resume_data.get('location', 'Unknown')
            role = resume_data.get('role', 'Developer')
            experience_data = resume_data.get('experience', {})
            
            # Handle experience data
            if isinstance(experience_data, dict):
                experience_years = experience_data.get('total_years', 0)
            else:
                experience_years = 0
            
            logger.info(f"📍 Location Growth Analysis - Location: {location}, Role: {role}, Experience: {experience_years}")
            
            # Analyze current location
            current_location = self._analyze_current_location(location, role)
            
            # Analyze relocation benefits
            relocation_benefits = self._analyze_relocation_benefits(location, role, experience_years)
            
            # Analyze growth opportunities
            growth_opportunities = self._analyze_growth_opportunities(location, role)
            
            # Generate alternative locations
            alternative_locations = self._generate_alternative_locations(location, role, experience_years)
            
            location_growth_analysis = {
                'current_location': current_location,
                'relocation_benefits': relocation_benefits,
                'growth_opportunities': growth_opportunities,
                'alternative_locations': alternative_locations
            }
            
            logger.info(f"✅ Location growth analysis completed - Current: {location}, Tech Hub: {current_location.get('tech_hub', False)}")
            return location_growth_analysis
            
        except Exception as e:
            logger.error(f"❌ Location growth analysis error: {e}")
            return {
                'current_location': {'name': 'Unknown', 'salary_multiplier': 1.0, 'growth_rate': 0.0, 'tech_hub': False},
                'relocation_benefits': {'relocation_score': 0, 'recommended_locations': [], 'benefits': []},
                'growth_opportunities': {'opportunities': [], 'challenges': []}
            }
    
    def _analyze_current_location(self, location: str, role: str) -> Dict[str, Any]:
        """Analyze current location characteristics"""
        location_lower = location.lower()
        
        # Tier 1 cities
        if any(city in location_lower for city in ['bangalore', 'mumbai', 'delhi', 'hyderabad', 'pune', 'chennai']):
            return {
                'name': location.title(),
                'salary_multiplier': 1.2,
                'growth_rate': 0.15,
                'tech_hub': True,
                'job_opportunities': 'High',
                'cost_of_living': 'High'
            }
        # Tier 2 cities
        elif any(city in location_lower for city in ['kolkata', 'ahmedabad', 'jaipur', 'lucknow', 'kanpur', 'nagpur']):
            return {
                'name': location.title(),
                'salary_multiplier': 1.0,
                'growth_rate': 0.10,
                'tech_hub': False,
                'job_opportunities': 'Medium',
                'cost_of_living': 'Medium'
            }
        # Tier 3 cities
        elif any(city in location_lower for city in ['indore', 'bhopal', 'coimbatore', 'kochi', 'visakhapatnam']):
            return {
                'name': location.title(),
                'salary_multiplier': 0.9,
                'growth_rate': 0.08,
                'tech_hub': False,
                'job_opportunities': 'Low',
                'cost_of_living': 'Low'
            }
        # International
        elif any(country in location_lower for country in ['usa', 'uk', 'canada', 'australia', 'singapore']):
            return {
                'name': location.title(),
                'salary_multiplier': 2.0,
                'growth_rate': 0.12,
                'tech_hub': True,
                'job_opportunities': 'Very High',
                'cost_of_living': 'Very High'
            }
        else:
            return {
                'name': location.title(),
                'salary_multiplier': 0.8,
                'growth_rate': 0.05,
                'tech_hub': False,
                'job_opportunities': 'Low',
                'cost_of_living': 'Low'
            }
    
    def _analyze_relocation_benefits(self, location: str, role: str, experience_years: int) -> Dict[str, Any]:
        """Analyze relocation benefits"""
        location_lower = location.lower()
        
        # Determine if relocation is beneficial
        if any(city in location_lower for city in ['bangalore', 'mumbai', 'delhi', 'hyderabad', 'pune', 'chennai']):
            # Already in tier 1 city
            relocation_score = 60
            recommended_locations = []
            benefits = ['Already in a major tech hub', 'Good job opportunities', 'High salary potential']
        elif any(country in location_lower for country in ['usa', 'uk', 'canada', 'australia', 'singapore']):
            # Already international
            relocation_score = 80
            recommended_locations = []
            benefits = ['International experience', 'High salary potential', 'Global opportunities']
        else:
            # In tier 2/3 city - relocation recommended
            relocation_score = 85
            recommended_locations = ['Bangalore', 'Mumbai', 'Delhi', 'Hyderabad', 'Pune', 'Chennai']
            benefits = [
                'Higher salary potential (20-40% increase)',
                'More job opportunities',
                'Better career growth',
                'Access to tech communities',
                'Exposure to latest technologies'
            ]
        
        # Calculate salary increase percentage
        current_multiplier = self._get_location_multiplier(location)
        best_multiplier = 1.2  # Tier 1 cities
        
        if current_multiplier < best_multiplier:
            salary_increase_percent = int(((best_multiplier - current_multiplier) / current_multiplier) * 100)
        else:
            salary_increase_percent = 0
        
        # Calculate growth increase percentage
        current_growth = self._get_location_growth_rate(location)
        best_growth = 0.15  # Tier 1 cities
        
        if current_growth < best_growth:
            growth_increase_percent = int(((best_growth - current_growth) / current_growth) * 100)
        else:
            growth_increase_percent = 0
        
        # Determine recommended location
        if relocation_score >= 80:
            recommended_location = "Stay in current location"
        elif recommended_locations:
            recommended_location = recommended_locations[0]  # Best option
        else:
            recommended_location = "Consider relocation"
        
        return {
            'relocation_score': relocation_score,
            'recommended_locations': recommended_locations,
            'benefits': benefits,
            'salary_increase_percent': salary_increase_percent,
            'growth_increase_percent': growth_increase_percent,
            'recommended_location': recommended_location
        }
    
    def _analyze_growth_opportunities(self, location: str, role: str) -> Dict[str, Any]:
        """Analyze growth opportunities in current location"""
        location_lower = location.lower()
        
        if any(city in location_lower for city in ['bangalore', 'mumbai', 'delhi', 'hyderabad', 'pune', 'chennai']):
            opportunities = [
                'Access to top tech companies',
                'Active tech meetups and communities',
                'Startup ecosystem',
                'Higher education opportunities',
                'Networking events'
            ]
            challenges = [
                'High competition',
                'Cost of living',
                'Traffic and commute'
            ]
        elif any(country in location_lower for country in ['usa', 'uk', 'canada', 'australia', 'singapore']):
            opportunities = [
                'Global career opportunities',
                'High salary potential',
                'Diverse work environment',
                'Advanced technology exposure',
                'International networking'
            ]
            challenges = [
                'Work visa requirements',
                'Cultural adaptation',
                'Higher cost of living'
            ]
        else:
            opportunities = [
                'Lower cost of living',
                'Less competition',
                'Work-life balance',
                'Local networking'
            ]
            challenges = [
                'Limited job opportunities',
                'Lower salary potential',
                'Limited tech exposure',
                'Fewer networking events'
            ]
        
            return {
                'opportunities': opportunities,
                'challenges': challenges
            }
    
    def _get_location_multiplier(self, location: str) -> float:
        """Get salary multiplier for location"""
        location_lower = location.lower()
        
        if any(city in location_lower for city in ['bangalore', 'mumbai', 'delhi', 'hyderabad', 'pune', 'chennai']):
            return 1.2
        elif any(country in location_lower for country in ['usa', 'uk', 'canada', 'australia', 'singapore']):
            return 2.0
        elif any(city in location_lower for city in ['kolkata', 'ahmedabad', 'jaipur', 'lucknow', 'kanpur', 'nagpur']):
            return 1.0
        elif any(city in location_lower for city in ['indore', 'bhopal', 'coimbatore', 'kochi', 'visakhapatnam']):
            return 0.9
        else:
            return 0.8
    
    def _get_location_growth_rate(self, location: str) -> float:
        """Get growth rate for location"""
        location_lower = location.lower()
        
        if any(city in location_lower for city in ['bangalore', 'mumbai', 'delhi', 'hyderabad', 'pune', 'chennai']):
            return 0.15
        elif any(country in location_lower for country in ['usa', 'uk', 'canada', 'australia', 'singapore']):
            return 0.12
        elif any(city in location_lower for city in ['kolkata', 'ahmedabad', 'jaipur', 'lucknow', 'kanpur', 'nagpur']):
            return 0.10
        elif any(city in location_lower for city in ['indore', 'bhopal', 'coimbatore', 'kochi', 'visakhapatnam']):
            return 0.08
        else:
            return 0.05
    
    def _generate_alternative_locations(self, current_location: str, role: str, experience_years: int) -> List[Dict[str, Any]]:
        """Generate alternative locations based on role and experience"""
        logger.info(f"🌍 Generating alternative locations for {role} with {experience_years} years experience")
        
        current_location_lower = current_location.lower()
        
        # Define alternative locations with their characteristics
        alternative_locations = [
            {
                'name': 'Bangalore',
                'salary_multiplier': 1.2,
                'growth_rate': 0.15,
                'tech_hub': True,
                'job_opportunities': 'Very High',
                'cost_of_living': 'High',
                'reason': 'Tech capital of India'
            },
            {
                'name': 'Mumbai',
                'salary_multiplier': 1.2,
                'growth_rate': 0.14,
                'tech_hub': True,
                'job_opportunities': 'Very High',
                'cost_of_living': 'Very High',
                'reason': 'Financial and tech hub'
            },
            {
                'name': 'Hyderabad',
                'salary_multiplier': 1.1,
                'growth_rate': 0.13,
                'tech_hub': True,
                'job_opportunities': 'High',
                'cost_of_living': 'Medium',
                'reason': 'Growing tech ecosystem'
            },
            {
                'name': 'Pune',
                'salary_multiplier': 1.1,
                'growth_rate': 0.12,
                'tech_hub': True,
                'job_opportunities': 'High',
                'cost_of_living': 'Medium',
                'reason': 'Automotive and IT hub'
            },
            {
                'name': 'Chennai',
                'salary_multiplier': 1.0,
                'growth_rate': 0.11,
                'tech_hub': True,
                'job_opportunities': 'High',
                'cost_of_living': 'Medium',
                'reason': 'Manufacturing and IT hub'
            },
            {
                'name': 'Delhi NCR',
                'salary_multiplier': 1.1,
                'growth_rate': 0.12,
                'tech_hub': True,
                'job_opportunities': 'High',
                'cost_of_living': 'High',
                'reason': 'Government and corporate hub'
            }
        ]
        
        # Filter out current location
        filtered_locations = [loc for loc in alternative_locations if loc['name'].lower() not in current_location_lower]
        
        # Sort by relevance based on role and experience
        if experience_years <= 2:
            # For freshers, prioritize cost of living and opportunities
            filtered_locations.sort(key=lambda x: (x['job_opportunities'] == 'Very High', x['cost_of_living'] != 'Very High', x['salary_multiplier']), reverse=True)
        elif experience_years <= 5:
            # For mid-level, balance salary and growth
            filtered_locations.sort(key=lambda x: (x['salary_multiplier'], x['growth_rate']), reverse=True)
        else:
            # For senior, prioritize salary and tech hub status
            filtered_locations.sort(key=lambda x: (x['tech_hub'], x['salary_multiplier'], x['growth_rate']), reverse=True)
        
        # Return top 3 alternatives
        top_alternatives = filtered_locations[:3]
        
        logger.info(f"🌍 Generated {len(top_alternatives)} alternative locations")
        return top_alternatives
    
    def _get_experience_level(self, experience: int) -> str:
        """Get AI-powered experience level based on actual experience"""
        logger.info(f"🎯 Analyzing experience level - Experience: {experience}")
        
        if experience == 0:
            return 'Entry Level'
        elif experience < 1:
            return 'Junior Level'
        elif experience < 3:
            return 'Mid-Junior Level'
        elif experience < 5:
            return 'Mid Level'
        elif experience < 8:
            return 'Senior Level'
        elif experience < 12:
            return 'Lead Level'
        else:
            return 'Principal Level'
    
    def _determine_career_stage(self, experience: int) -> str:
        """Determine career stage"""
        if experience == 0:
            return 'Entry Level'
        elif experience < 3:
            return 'Early Career'
        elif experience < 7:
            return 'Mid Career'
        else:
            return 'Senior Level'
    
    def _calculate_salary_expectation(self, role: str, experience: int) -> Dict[str, Any]:
        """Calculate salary expectation based on role and experience"""
        logger.info(f"💰 Calculating salary for role: '{role}', experience: {experience}")
        
        # Determine experience level
        if experience < 2:
            level = 'junior'
        elif experience < 5:
            level = 'mid'
        else:
            level = 'senior'
            
        # Role-specific base salaries (in INR)
        role_base_salaries = {
            'data scientist': {'junior': (500000, 800000), 'mid': (1000000, 1800000), 'senior': (1800000, 3500000)},
            'machine learning': {'junior': (500000, 800000), 'mid': (1000000, 1800000), 'senior': (1800000, 3500000)},
            'ai': {'junior': (500000, 800000), 'mid': (1000000, 1800000), 'senior': (1800000, 3500000)},
            'full stack': {'junior': (400000, 700000), 'mid': (700000, 1400000), 'senior': (1400000, 2800000)},
            'frontend': {'junior': (350000, 600000), 'mid': (600000, 1200000), 'senior': (1200000, 2400000)},
            'backend': {'junior': (400000, 700000), 'mid': (700000, 1400000), 'senior': (1400000, 2800000)},
            'devops': {'junior': (450000, 800000), 'mid': (800000, 1600000), 'senior': (1600000, 3200000)},
            'mobile': {'junior': (350000, 700000), 'mid': (700000, 1400000), 'senior': (1400000, 2800000)},
            'qa': {'junior': (250000, 500000), 'mid': (500000, 1000000), 'senior': (1000000, 2000000)},
            'ui': {'junior': (300000, 600000), 'mid': (600000, 1200000), 'senior': (1200000, 2400000)},
            'ux': {'junior': (300000, 600000), 'mid': (600000, 1200000), 'senior': (1200000, 2400000)}
        }
        
        # Find matching role
        role_lower = role.lower()
        matched_role = None
        for key in role_base_salaries.keys():
            if key in role_lower:
                matched_role = key
                break
        
        if matched_role and matched_role in role_base_salaries:
            min_sal, max_sal = role_base_salaries[matched_role][level]
            logger.info(f"✅ Salary calculated - Role: {matched_role}, Level: {level}, Range: ₹{min_sal:,} - ₹{max_sal:,}")
        else:
            # Default salary range
            min_sal, max_sal = (300000, 600000) if level == 'junior' else (600000, 1200000) if level == 'mid' else (1200000, 2400000)
            logger.info(f"⚠️ Using default salary - Level: {level}, Range: ₹{min_sal:,} - ₹{max_sal:,}")
        
            return {
                'range': f"₹{min_sal:,} - ₹{max_sal:,}",
            'level': level.title(),
            'currency': 'INR',
            'role_specific': matched_role is not None
            }
    
    def _analyze_location_advantage(self, location: str) -> str:
        """Analyze location advantage"""
        tech_hubs = ['bangalore', 'mumbai', 'delhi', 'hyderabad', 'chennai', 'pune']
        if location.lower() in tech_hubs:
            return 'High - Located in tech hub'
        else:
            return 'Medium - Consider remote opportunities'
    
    def _assess_competitiveness(self, skills: List[str], experience: int) -> str:
        """Assess competitiveness based on actual skills and experience"""
        logger.info(f"🏆 Assessing competitiveness - Skills: {len(skills)}, Experience: {experience}")
        
        if not skills:
            return 'Limited - No skills identified'
        
        # High-value skills that boost competitiveness
        high_value_skills = [
            'python', 'javascript', 'react', 'node.js', 'aws', 'docker', 'kubernetes',
            'machine learning', 'ai', 'tensorflow', 'pytorch', 'sql', 'mongodb',
            'git', 'jenkins', 'terraform', 'ansible', 'elasticsearch', 'redis'
        ]
        
        # Count high-value skills
        skill_lower = [skill.lower() for skill in skills if isinstance(skill, str)]
        high_value_count = sum(1 for skill in skill_lower if any(hv_skill in skill for hv_skill in high_value_skills))
        
        # Assess based on skills count, high-value skills, and experience
        if len(skills) >= 15 and high_value_count >= 5 and experience >= 3:
            competitiveness = 'Highly Competitive'
        elif len(skills) >= 10 and high_value_count >= 3 and experience >= 2:
            competitiveness = 'Competitive'
        elif len(skills) >= 5 and high_value_count >= 1 and experience >= 1:
            competitiveness = 'Moderately Competitive'
        else:
            competitiveness = 'Developing'
        
        logger.info(f"✅ Competitiveness assessed: {competitiveness} (Skills: {len(skills)}, High-value: {high_value_count})")
        return competitiveness
    
    def _assess_market_demand(self, role: str, experience: int) -> str:
        """Assess market demand based on role and experience"""
        role_lower = role.lower()
        
        # High demand roles
        if any(keyword in role_lower for keyword in ['data scientist', 'machine learning', 'ai', 'devops', 'cloud']):
            return 'Very High'
        elif any(keyword in role_lower for keyword in ['full stack', 'frontend', 'backend', 'mobile']):
            return 'High'
        elif any(keyword in role_lower for keyword in ['qa', 'test', 'ui', 'ux']):
            return 'Medium-High'
        else:
            return 'High'  # Default for other roles
    
    def _get_role_specificity(self, role: str, skills: List[str]) -> str:
        """Assess role specificity based on skills"""
        role_lower = role.lower()
        
        if 'full stack' in role_lower and len(skills) >= 15:
            return 'Highly Specialized'
        elif any(keyword in role_lower for keyword in ['data scientist', 'machine learning', 'ai']):
            return 'Highly Specialized'
        elif len(skills) >= 10:
            return 'Specialized'
        else:
            return 'General'
    
    def _assess_skill_market_value(self, skills: List[str], role: str) -> str:
        """Assess market value of skills"""
        high_value_skills = ['python', 'javascript', 'react', 'node.js', 'aws', 'docker', 'kubernetes', 'machine learning', 'ai']
        skill_lower = [skill.lower() for skill in skills if isinstance(skill, str)]
        
        high_value_count = sum(1 for skill in skill_lower if any(hv_skill in skill for hv_skill in high_value_skills))
        
        if high_value_count >= 5:
            return 'Very High'
        elif high_value_count >= 3:
            return 'High'
        elif high_value_count >= 1:
            return 'Medium'
        else:
            return 'Low'
    
    def _get_market_trends(self, role: str) -> List[str]:
        """Get market trends for role"""
        role_lower = role.lower()
        
        if 'data scientist' in role_lower or 'machine learning' in role_lower:
            return [
                'Generative AI and LLMs in high demand',
                'MLOps and production ML growing',
                'Real-time analytics becoming standard',
                'Ethical AI and responsible ML focus'
            ]
        elif 'full stack' in role_lower:
            return [
                'Serverless architecture adoption',
                'Edge computing and CDN optimization',
                'Progressive Web Apps (PWA) trend',
                'API-first development approach'
            ]
        elif 'frontend' in role_lower:
            return [
                'Web3 and blockchain interfaces',
                'AR/VR web experiences',
                'Voice interface integration',
                'Accessibility-first design'
            ]
        elif 'backend' in role_lower:
            return [
                'Serverless computing adoption',
                'GraphQL vs REST API evolution',
                'Event-driven architecture',
                'Zero-trust security models'
            ]
        elif 'devops' in role_lower:
            return [
                'GitOps workflow adoption',
                'Cloud-native security focus',
                'Observability and monitoring',
                'FinOps and cost optimization'
            ]
        elif 'mobile' in role_lower:
            return [
                'Cross-platform development growth',
                'AR/VR mobile integration',
                'IoT connectivity features',
                'Privacy-first mobile design'
            ]
        else:
            return [
                'Digital transformation acceleration',
                'Remote work becoming permanent',
                'AI integration across industries',
                'Cloud migration continuing'
            ]
    
    def _calculate_ai_score(self, resume_data: Dict[str, Any]) -> float:
        """Calculate AI score for resume"""
        try:
            score = 0.0
            
            # Experience score (30%)
            experience_data = resume_data.get('experience', {})
            if isinstance(experience_data, dict):
                experience = experience_data.get('total_years', 0)
            else:
                experience = 0
            
            if experience >= 5:
                score += 0.3
            elif experience >= 2:
                score += 0.2
            else:
                score += 0.1
            
            # Skills score (40%)
            skills_data = resume_data.get('skills', [])
            if isinstance(skills_data, list):
                skills = skills_data
            else:
                skills = []
            
            if len(skills) >= 15:
                score += 0.4
            elif len(skills) >= 10:
                score += 0.3
            elif len(skills) >= 5:
                score += 0.2
            else:
                score += 0.1
            
            # Completeness score (30%)
            required_fields = ['name', 'email', 'phone', 'role', 'location']
            completeness = sum(1 for field in required_fields if resume_data.get(field) and resume_data.get(field) != 'Not found')
            score += (completeness / len(required_fields)) * 0.3
            
            return round(score, 2)
        except Exception as e:
            logger.error(f"❌ AI score calculation error: {e}")
            return 0.0

# Initialize global AI resume analyzer
ai_resume_analyzer = AIResumeAnalyzer()
