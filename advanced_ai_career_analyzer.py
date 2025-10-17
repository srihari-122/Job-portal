"""
Advanced AI Career Analyzer
Comprehensive career analysis with detailed component and sub-component analysis
"""

import re
import logging
from datetime import datetime
from typing import Dict, List, Any, Tuple, Optional
import json

logger = logging.getLogger(__name__)

class AdvancedAICareerAnalyzer:
    """Advanced AI-powered career analyzer with comprehensive analysis"""
    
    def __init__(self):
        self.initialize_skill_databases()
        self.initialize_career_paths()
        self.initialize_industry_analysis()
        self.initialize_salary_data()
        
    def initialize_skill_databases(self):
        """Initialize comprehensive skill databases"""
        
        # Technical Skills Database
        self.technical_skills = {
            'programming_languages': {
                'high_demand': ['python', 'javascript', 'java', 'typescript', 'go', 'rust'],
                'medium_demand': ['c++', 'c#', 'php', 'ruby', 'swift', 'kotlin'],
                'emerging': ['dart', 'zig', 'nim', 'crystal', 'v', 'odin'],
                'legacy': ['cobol', 'fortran', 'pascal', 'ada', 'lisp', 'prolog'],
                'specialized': ['r', 'matlab', 'scala', 'clojure', 'erlang', 'elixir']
            },
            'web_technologies': {
                'frontend': ['react', 'angular', 'vue', 'svelte', 'ember', 'backbone'],
                'backend': ['node.js', 'express', 'django', 'flask', 'fastapi', 'spring'],
                'fullstack': ['next.js', 'nuxt.js', 'gatsby', 'sveltekit', 'remix'],
                'styling': ['css', 'sass', 'less', 'stylus', 'tailwind', 'bootstrap'],
                'build_tools': ['webpack', 'vite', 'parcel', 'rollup', 'esbuild']
            },
            'databases': {
                'relational': ['mysql', 'postgresql', 'oracle', 'sql server', 'sqlite'],
                'nosql': ['mongodb', 'cassandra', 'redis', 'dynamodb', 'couchdb'],
                'graph': ['neo4j', 'arangodb', 'amazon neptune'],
                'time_series': ['influxdb', 'timescaledb', 'prometheus'],
                'search': ['elasticsearch', 'solr', 'opensearch']
            },
            'cloud_platforms': {
                'aws': ['ec2', 's3', 'rds', 'lambda', 'dynamodb', 'cloudfront'],
                'azure': ['virtual machines', 'blob storage', 'sql database', 'functions'],
                'gcp': ['compute engine', 'cloud storage', 'cloud sql', 'cloud functions'],
                'containerization': ['docker', 'kubernetes', 'helm', 'rancher'],
                'serverless': ['aws lambda', 'azure functions', 'google cloud functions']
            },
            'ai_ml': {
                'frameworks': ['tensorflow', 'pytorch', 'keras', 'scikit-learn', 'fastai'],
                'libraries': ['pandas', 'numpy', 'opencv', 'nltk', 'spacy', 'transformers'],
                'tools': ['jupyter', 'mlflow', 'wandb', 'kubeflow', 'airflow'],
                'specializations': ['computer vision', 'nlp', 'deep learning', 'reinforcement learning']
            },
            'devops': {
                'ci_cd': ['jenkins', 'gitlab ci', 'github actions', 'azure devops'],
                'monitoring': ['prometheus', 'grafana', 'datadog', 'new relic'],
                'infrastructure': ['terraform', 'ansible', 'chef', 'puppet'],
                'security': ['vault', 'consul', 'istio', 'linkerd']
            }
        }
        
        # Soft Skills Database
        self.soft_skills = {
            'communication': ['verbal communication', 'written communication', 'presentation', 'public speaking'],
            'leadership': ['team leadership', 'project management', 'mentoring', 'coaching'],
            'problem_solving': ['analytical thinking', 'critical thinking', 'creative problem solving'],
            'collaboration': ['teamwork', 'cross-functional collaboration', 'stakeholder management'],
            'adaptability': ['flexibility', 'learning agility', 'change management'],
            'time_management': ['project planning', 'deadline management', 'prioritization']
        }
        
        # Industry-Specific Skills
        self.industry_skills = {
            'fintech': ['blockchain', 'cryptocurrency', 'payment systems', 'regulatory compliance'],
            'healthcare': ['hipaa compliance', 'medical imaging', 'electronic health records'],
            'ecommerce': ['payment gateways', 'inventory management', 'supply chain'],
            'gaming': ['game engines', '3d graphics', 'physics simulation', 'multiplayer networking'],
            'iot': ['embedded systems', 'sensor networks', 'edge computing', 'mqtt'],
            'cybersecurity': ['penetration testing', 'vulnerability assessment', 'incident response']
        }
        
    def initialize_career_paths(self):
        """Initialize comprehensive career paths"""
        
        self.career_paths = {
            'software_engineer': {
                'fresher': {
                    'entry_level': 'Junior Software Engineer',
                    'timeline': '0-2 years',
                    'skills_focus': ['Programming fundamentals', 'Version control', 'Testing', 'Debugging'],
                    'responsibilities': ['Code development', 'Bug fixes', 'Unit testing', 'Documentation'],
                    'salary_range': {'min': 300000, 'max': 600000, 'currency': 'INR'},
                    'next_level': 'Mid-Level Software Engineer'
                },
                'mid_level': {
                    'entry_level': 'Mid-Level Software Engineer',
                    'timeline': '2-5 years',
                    'skills_focus': ['System design', 'Architecture patterns', 'Code review', 'Mentoring'],
                    'responsibilities': ['Feature development', 'System design', 'Code review', 'Mentoring juniors'],
                    'salary_range': {'min': 600000, 'max': 1200000, 'currency': 'INR'},
                    'next_level': 'Senior Software Engineer'
                },
                'senior': {
                    'entry_level': 'Senior Software Engineer',
                    'timeline': '5-8 years',
                    'skills_focus': ['Technical leadership', 'System architecture', 'Performance optimization'],
                    'responsibilities': ['Technical decisions', 'Architecture design', 'Performance optimization', 'Team leadership'],
                    'salary_range': {'min': 1200000, 'max': 2000000, 'currency': 'INR'},
                    'next_level': 'Principal Engineer'
                },
                'principal': {
                    'entry_level': 'Principal Engineer',
                    'timeline': '8+ years',
                    'skills_focus': ['Technical strategy', 'Innovation', 'Cross-team collaboration'],
                    'responsibilities': ['Technical strategy', 'Innovation', 'Cross-team collaboration', 'Mentoring'],
                    'salary_range': {'min': 2000000, 'max': 3500000, 'currency': 'INR'},
                    'next_level': 'Engineering Manager'
                }
            },
            'data_scientist': {
                'fresher': {
                    'entry_level': 'Junior Data Analyst',
                    'timeline': '0-2 years',
                    'skills_focus': ['Data analysis', 'Statistics', 'SQL', 'Python/R'],
                    'responsibilities': ['Data cleaning', 'Basic analysis', 'Report generation', 'Dashboard creation'],
                    'salary_range': {'min': 400000, 'max': 700000, 'currency': 'INR'},
                    'next_level': 'Data Scientist'
                },
                'mid_level': {
                    'entry_level': 'Data Scientist',
                    'timeline': '2-5 years',
                    'skills_focus': ['Machine learning', 'Statistical modeling', 'Data visualization'],
                    'responsibilities': ['ML model development', 'Statistical analysis', 'Data visualization', 'Insights generation'],
                    'salary_range': {'min': 700000, 'max': 1500000, 'currency': 'INR'},
                    'next_level': 'Senior Data Scientist'
                },
                'senior': {
                    'entry_level': 'Senior Data Scientist',
                    'timeline': '5-8 years',
                    'skills_focus': ['Advanced ML', 'Deep learning', 'MLOps', 'Team leadership'],
                    'responsibilities': ['Advanced ML models', 'MLOps implementation', 'Team leadership', 'Strategic insights'],
                    'salary_range': {'min': 1500000, 'max': 2500000, 'currency': 'INR'},
                    'next_level': 'Principal Data Scientist'
                }
            },
            'devops_engineer': {
                'fresher': {
                    'entry_level': 'Junior DevOps Engineer',
                    'timeline': '0-2 years',
                    'skills_focus': ['Linux administration', 'Scripting', 'CI/CD basics', 'Monitoring'],
                    'responsibilities': ['Infrastructure maintenance', 'Deployment automation', 'Monitoring setup'],
                    'salary_range': {'min': 500000, 'max': 800000, 'currency': 'INR'},
                    'next_level': 'DevOps Engineer'
                },
                'mid_level': {
                    'entry_level': 'DevOps Engineer',
                    'timeline': '2-5 years',
                    'skills_focus': ['Containerization', 'Cloud platforms', 'Infrastructure as code'],
                    'responsibilities': ['Infrastructure automation', 'Cloud management', 'Security implementation'],
                    'salary_range': {'min': 800000, 'max': 1500000, 'currency': 'INR'},
                    'next_level': 'Senior DevOps Engineer'
                }
            }
        }
        
    def initialize_industry_analysis(self):
        """Initialize industry-specific analysis"""
        
        self.industry_analysis = {
            'technology': {
                'growth_rate': '15-20% annually',
                'key_trends': ['AI/ML adoption', 'Cloud migration', 'Remote work', 'Cybersecurity'],
                'hot_skills': ['Python', 'JavaScript', 'AWS', 'Docker', 'Kubernetes'],
                'salary_premium': 1.2
            },
            'fintech': {
                'growth_rate': '25-30% annually',
                'key_trends': ['Digital payments', 'Blockchain', 'RegTech', 'InsurTech'],
                'hot_skills': ['Blockchain', 'Payment systems', 'Regulatory compliance', 'Risk management'],
                'salary_premium': 1.3
            },
            'healthcare': {
                'growth_rate': '10-15% annually',
                'key_trends': ['Telemedicine', 'AI diagnostics', 'Electronic health records', 'IoT'],
                'hot_skills': ['HIPAA compliance', 'Medical imaging', 'Health informatics', 'IoT'],
                'salary_premium': 1.1
            },
            'ecommerce': {
                'growth_rate': '20-25% annually',
                'key_trends': ['Mobile commerce', 'Personalization', 'Supply chain optimization', 'AR/VR'],
                'hot_skills': ['Payment gateways', 'Inventory management', 'Customer analytics', 'Mobile development'],
                'salary_premium': 1.15
            }
        }
        
    def initialize_salary_data(self):
        """Initialize comprehensive salary data"""
        
        self.salary_data = {
            'by_experience': {
                0: {'min': 300000, 'max': 600000, 'median': 450000},
                1: {'min': 400000, 'max': 800000, 'median': 600000},
                2: {'min': 600000, 'max': 1200000, 'median': 900000},
                3: {'min': 800000, 'max': 1500000, 'median': 1150000},
                4: {'min': 1000000, 'max': 2000000, 'median': 1500000},
                5: {'min': 1200000, 'max': 2500000, 'median': 1850000},
                6: {'min': 1500000, 'max': 3000000, 'median': 2250000},
                7: {'min': 1800000, 'max': 3500000, 'median': 2650000},
                8: {'min': 2000000, 'max': 4000000, 'median': 3000000},
                9: {'min': 2500000, 'max': 5000000, 'median': 3750000},
                10: {'min': 3000000, 'max': 6000000, 'median': 4500000}
            },
            'by_location': {
                'bangalore': 1.2,
                'mumbai': 1.15,
                'delhi': 1.1,
                'hyderabad': 1.05,
                'chennai': 1.0,
                'pune': 1.05,
                'kolkata': 0.9,
                'ahmedabad': 0.85
            },
            'by_company_size': {
                'startup': 0.8,
                'mid_size': 1.0,
                'large': 1.2,
                'mnc': 1.3
            }
        }
        
    def analyze_resume(self, resume_data: Dict[str, Any]) -> Dict[str, Any]:
        """Comprehensive resume analysis with detailed component analysis"""
        try:
            logger.info("🧠 Starting advanced AI resume analysis...")
            
            # Extract components
            name = resume_data.get('name', 'Unknown')
            role = resume_data.get('role', 'Unknown')
            skills = resume_data.get('skills', [])
            experience = resume_data.get('experience', {})
            location = resume_data.get('location', 'Unknown')
            education = resume_data.get('education', [])
            
            # Determine if fresher
            is_fresher = self._is_fresher(experience, skills, role)
            
            # Comprehensive analysis
            analysis_result = {
                'is_fresher': is_fresher,
                'candidate_profile': self._analyze_candidate_profile(resume_data),
                'skill_analysis': self._analyze_skills_comprehensive(skills, is_fresher),
                'experience_analysis': self._analyze_experience_comprehensive(experience, skills),
                'career_path_analysis': self._analyze_career_path(role, experience, skills, is_fresher),
                'industry_analysis': self._analyze_industry_fit(skills, role, location),
                'salary_analysis': self._analyze_salary_comprehensive(experience, skills, location, role),
                'skill_gap_analysis': self._analyze_skill_gaps(skills, role, experience, is_fresher),
                'recommendations': self._generate_comprehensive_recommendations(resume_data, is_fresher),
                'ai_insights': self._generate_ai_insights(resume_data, is_fresher),
                'analysis_timestamp': datetime.now().isoformat()
            }
            
            logger.info("✅ Advanced AI resume analysis completed")
            return analysis_result
            
        except Exception as e:
            logger.error(f"❌ Advanced AI resume analysis error: {e}")
            return self._get_empty_analysis()
    
    def _analyze_candidate_profile(self, resume_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze candidate profile comprehensively"""
        try:
            name = resume_data.get('name', 'Unknown')
            role = resume_data.get('role', 'Unknown')
            skills = resume_data.get('skills', [])
            experience = resume_data.get('experience', {})
            location = resume_data.get('location', 'Unknown')
            education = resume_data.get('education', [])
            
            experience_years = experience.get('total_years', 0)
            is_fresher = experience.get('is_fresher', False)
            
            # Determine career stage
            career_stage = self._determine_career_stage(experience_years, is_fresher)
            
            # Determine experience level
            experience_level = self._determine_experience_level(experience_years, is_fresher)
            
            # Calculate profile strength
            profile_strength = self._calculate_profile_strength(skills, experience, education)
            
            return {
                'name': name,
                'role': role,
                'experience_years': experience_years,
                'location': location,
                'skills_count': len(skills),
                'career_stage': career_stage,
                'experience_level': experience_level,
                'profile_strength': profile_strength,
                'education_count': len(education),
                'is_fresher': is_fresher
            }
            
        except Exception as e:
            logger.error(f"❌ Error analyzing candidate profile: {e}")
            return {'name': 'Unknown', 'role': 'Unknown', 'experience_years': 0, 'career_stage': 'Unknown'}
    
    def _analyze_skills_comprehensive(self, skills: List[str], is_fresher: bool) -> Dict[str, Any]:
        """Comprehensive skill analysis"""
        try:
            skills_lower = [skill.lower() for skill in skills]
            
            # Categorize skills
            skill_categories = {}
            for category, subcategories in self.technical_skills.items():
                category_skills = []
                for subcategory, skill_list in subcategories.items():
                    matches = [skill for skill in skills_lower if skill in skill_list]
                    if matches:
                        category_skills.extend(matches)
                
                skill_categories[category] = {
                    'skills': category_skills,
                    'count': len(category_skills),
                    'coverage': len(category_skills) / sum(len(skill_list) for skill_list in subcategories.values()) if subcategories else 0
                }
            
            # Analyze soft skills
            soft_skills_analysis = {}
            for category, skill_list in self.soft_skills.items():
                matches = [skill for skill in skills_lower if skill in skill_list]
                soft_skills_analysis[category] = {
                    'skills': matches,
                    'count': len(matches),
                    'coverage': len(matches) / len(skill_list) if skill_list else 0
                }
            
            # Calculate skill diversity
            skill_diversity = self._calculate_skill_diversity(skills_lower)
            
            # Determine skill level
            skill_level = self._determine_skill_level(skills_lower, is_fresher)
            
            return {
                'technical_skills': skill_categories,
                'soft_skills': soft_skills_analysis,
                'total_skills': len(skills),
                'skill_diversity': skill_diversity,
                'skill_level': skill_level,
                'skill_strength': self._calculate_skill_strength(skills_lower, is_fresher)
            }
            
        except Exception as e:
            logger.error(f"❌ Error analyzing skills: {e}")
            return {'technical_skills': {}, 'soft_skills': {}, 'total_skills': 0}
    
    def _analyze_experience_comprehensive(self, experience: Dict[str, Any], skills: List[str]) -> Dict[str, Any]:
        """Comprehensive experience analysis"""
        try:
            experience_years = experience.get('total_years', 0)
            is_fresher = experience.get('is_fresher', False)
            experience_periods = experience.get('experience_periods', [])
            
            # Analyze experience quality
            experience_quality = self._analyze_experience_quality(experience_periods, skills)
            
            # Determine experience relevance
            experience_relevance = self._analyze_experience_relevance(experience_periods, skills)
            
            # Calculate experience progression
            experience_progression = self._analyze_experience_progression(experience_periods)
            
            return {
                'total_years': experience_years,
                'is_fresher': is_fresher,
                'experience_quality': experience_quality,
                'experience_relevance': experience_relevance,
                'experience_progression': experience_progression,
                'experience_periods': experience_periods,
                'experience_strength': self._calculate_experience_strength(experience_years, is_fresher, skills)
            }
            
        except Exception as e:
            logger.error(f"❌ Error analyzing experience: {e}")
            return {'total_years': 0, 'is_fresher': True, 'experience_quality': 'Unknown'}
    
    def _analyze_career_path(self, role: str, experience: Dict[str, Any], skills: List[str], is_fresher: bool) -> Dict[str, Any]:
        """Analyze career path comprehensively"""
        try:
            experience_years = experience.get('total_years', 0)
            
            # Determine career track
            career_track = self._determine_career_track(role, skills)
            
            # Get current level
            current_level = self._determine_current_level(role, experience_years, is_fresher)
            
            # Get career path
            career_path = self.career_paths.get(career_track, self.career_paths['software_engineer'])
            current_path = career_path.get(current_level, career_path['fresher'])
            
            # Generate progression timeline
            progression_timeline = self._generate_progression_timeline(career_track, current_level, experience_years)
            
            # Calculate career readiness
            career_readiness = self._calculate_career_readiness(skills, experience, role, is_fresher)
            
            return {
                'career_track': career_track,
                'current_level': current_level,
                'current_path': current_path,
                'progression_timeline': progression_timeline,
                'career_readiness': career_readiness,
                'next_steps': self._generate_career_next_steps(career_track, current_level, skills, is_fresher)
            }
            
        except Exception as e:
            logger.error(f"❌ Error analyzing career path: {e}")
            return {'career_track': 'software_engineer', 'current_level': 'fresher', 'career_readiness': 'Unknown'}
    
    def _analyze_industry_fit(self, skills: List[str], role: str, location: str) -> Dict[str, Any]:
        """Analyze industry fit"""
        try:
            skills_lower = [skill.lower() for skill in skills]
            role_lower = role.lower()
            
            # Determine industry
            industry = self._determine_industry(role_lower, skills_lower)
            
            # Get industry analysis
            industry_data = self.industry_analysis.get(industry, self.industry_analysis['technology'])
            
            # Calculate industry fit
            industry_fit = self._calculate_industry_fit(skills_lower, industry)
            
            # Analyze market demand
            market_demand = self._analyze_market_demand(skills_lower, industry)
            
            return {
                'industry': industry,
                'industry_data': industry_data,
                'industry_fit': industry_fit,
                'market_demand': market_demand,
                'growth_potential': industry_data.get('growth_rate', 'Unknown')
            }
            
        except Exception as e:
            logger.error(f"❌ Error analyzing industry fit: {e}")
            return {'industry': 'technology', 'industry_fit': 'Unknown', 'market_demand': 'Unknown'}
    
    def _analyze_salary_comprehensive(self, experience: Dict[str, Any], skills: List[str], location: str, role: str) -> Dict[str, Any]:
        """Comprehensive salary analysis"""
        try:
            experience_years = experience.get('total_years', 0)
            is_fresher = experience.get('is_fresher', False)
            
            # Base salary range
            base_range = self.salary_data['by_experience'].get(min(experience_years, 10), self.salary_data['by_experience'][10])
            
            # Location adjustment
            location_multiplier = self.salary_data['by_location'].get(location.lower(), 1.0)
            
            # Skill-based adjustments
            skill_multiplier = self._calculate_skill_multiplier(skills)
            
            # Role-based adjustments
            role_multiplier = self._calculate_role_multiplier(role)
            
            # Calculate projected salary
            projected_min = int(base_range['min'] * location_multiplier * skill_multiplier * role_multiplier)
            projected_max = int(base_range['max'] * location_multiplier * skill_multiplier * role_multiplier)
            projected_median = int(base_range['median'] * location_multiplier * skill_multiplier * role_multiplier)
            
            # Growth projections
            growth_projections = self._calculate_salary_growth(experience_years, skills, is_fresher)
            
            return {
                'current_range': {
                    'min': projected_min,
                    'max': projected_max,
                    'median': projected_median,
                    'currency': 'INR'
                },
                'growth_projections': growth_projections,
                'factors': {
                    'experience': experience_years,
                    'location': location,
                    'skills': len(skills),
                    'role': role
                },
                'market_position': self._determine_market_position(projected_median, experience_years)
            }
            
        except Exception as e:
            logger.error(f"❌ Error analyzing salary: {e}")
            return {'current_range': {'min': 300000, 'max': 600000, 'median': 450000, 'currency': 'INR'}}
    
    def _analyze_skill_gaps(self, skills: List[str], role: str, experience: Dict[str, Any], is_fresher: bool) -> Dict[str, Any]:
        """Comprehensive skill gap analysis"""
        try:
            skills_lower = [skill.lower() for skill in skills]
            experience_years = experience.get('total_years', 0)
            
            # Determine required skills based on role and experience
            required_skills = self._get_required_skills(role, experience_years, is_fresher)
            
            # Identify missing skills
            missing_skills = [skill for skill in required_skills if skill.lower() not in skills_lower]
            
            # Categorize missing skills
            missing_categories = self._categorize_missing_skills(missing_skills)
            
            # Prioritize skill gaps
            prioritized_gaps = self._prioritize_skill_gaps(missing_skills, role, experience_years, is_fresher)
            
            # Generate learning recommendations
            learning_recommendations = self._generate_learning_recommendations(missing_skills, role, is_fresher)
            
            return {
                'missing_skills': missing_skills,
                'missing_categories': missing_categories,
                'prioritized_gaps': prioritized_gaps,
                'learning_recommendations': learning_recommendations,
                'skill_gap_score': len(missing_skills) / len(required_skills) if required_skills else 0
            }
            
        except Exception as e:
            logger.error(f"❌ Error analyzing skill gaps: {e}")
            return {'missing_skills': [], 'prioritized_gaps': [], 'skill_gap_score': 0}
    
    def _generate_comprehensive_recommendations(self, resume_data: Dict[str, Any], is_fresher: bool) -> Dict[str, Any]:
        """Generate comprehensive recommendations"""
        try:
            skills = resume_data.get('skills', [])
            experience = resume_data.get('experience', {})
            role = resume_data.get('role', 'Unknown')
            
            experience_years = experience.get('total_years', 0)
            
            if is_fresher:
                return self._generate_fresher_recommendations(skills, role)
            else:
                return self._generate_experienced_recommendations(skills, experience_years, role)
                
        except Exception as e:
            logger.error(f"❌ Error generating recommendations: {e}")
            return {'immediate_actions': [], 'skill_development': [], 'career_advancement': []}
    
    def _generate_ai_insights(self, resume_data: Dict[str, Any], is_fresher: bool) -> Dict[str, Any]:
        """Generate AI insights"""
        try:
            skills = resume_data.get('skills', [])
            experience = resume_data.get('experience', {})
            role = resume_data.get('role', 'Unknown')
            
            experience_years = experience.get('total_years', 0)
            
            # Calculate overall score
            overall_score = self._calculate_overall_score(skills, experience, role, is_fresher)
            
            # Determine market readiness
            market_readiness = self._determine_market_readiness(skills, experience_years, is_fresher)
            
            # Determine growth potential
            growth_potential = self._determine_growth_potential(skills, experience_years, is_fresher)
            
            # Generate personalized insights
            personalized_insights = self._generate_personalized_insights(resume_data, is_fresher)
            
            return {
                'overall_score': overall_score,
                'market_readiness': market_readiness,
                'growth_potential': growth_potential,
                'career_stage': 'Fresher' if is_fresher else self._determine_career_stage(experience_years, is_fresher),
                'personalized_insights': personalized_insights,
                'recommended_actions': self._generate_recommended_actions(skills, experience_years, is_fresher)
            }
            
        except Exception as e:
            logger.error(f"❌ Error generating AI insights: {e}")
            return {'overall_score': 0.5, 'market_readiness': 'Unknown', 'growth_potential': 'Unknown'}
    
    # Helper methods
    def _is_fresher(self, experience: Dict[str, Any], skills: List[str], role: str) -> bool:
        """Determine if candidate is a fresher"""
        try:
            if experience.get('is_fresher', False):
                return True
            
            experience_years = experience.get('total_years', 0)
            if experience_years <= 1.0:
                return True
            
            if len(skills) <= 5:
                return True
            
            role_lower = role.lower()
            fresher_indicators = ['fresher', 'fresh graduate', 'entry level', 'junior', 'trainee', 'intern']
            if any(indicator in role_lower for indicator in fresher_indicators):
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"❌ Error determining fresher status: {e}")
            return True
    
    def _determine_career_stage(self, experience_years: int, is_fresher: bool) -> str:
        """Determine career stage"""
        try:
            if is_fresher or experience_years <= 1:
                return 'Fresher'
            elif experience_years <= 3:
                return 'Junior'
            elif experience_years <= 5:
                return 'Mid-Level'
            elif experience_years <= 8:
                return 'Senior'
            else:
                return 'Lead/Manager'
                
        except Exception as e:
            logger.error(f"❌ Error determining career stage: {e}")
            return 'Mid-Level'
    
    def _determine_experience_level(self, experience_years: int, is_fresher: bool) -> str:
        """Determine experience level"""
        try:
            if is_fresher or experience_years <= 1:
                return 'Entry Level'
            elif experience_years <= 3:
                return 'Junior Level'
            elif experience_years <= 5:
                return 'Mid Level'
            elif experience_years <= 8:
                return 'Senior Level'
            else:
                return 'Expert Level'
                
        except Exception as e:
            logger.error(f"❌ Error determining experience level: {e}")
            return 'Mid Level'
    
    def _calculate_profile_strength(self, skills: List[str], experience: Dict[str, Any], education: List[Dict[str, Any]]) -> str:
        """Calculate profile strength"""
        try:
            score = 0
            
            # Skills score
            score += min(len(skills) * 0.1, 0.4)
            
            # Experience score
            experience_years = experience.get('total_years', 0)
            score += min(experience_years * 0.1, 0.3)
            
            # Education score
            score += min(len(education) * 0.1, 0.3)
            
            if score >= 0.8:
                return 'Excellent'
            elif score >= 0.6:
                return 'Good'
            elif score >= 0.4:
                return 'Average'
            else:
                return 'Needs Improvement'
                
        except Exception as e:
            logger.error(f"❌ Error calculating profile strength: {e}")
            return 'Average'
    
    def _calculate_skill_diversity(self, skills_lower: List[str]) -> str:
        """Calculate skill diversity"""
        try:
            categories_covered = 0
            total_categories = len(self.technical_skills)
            
            for category, subcategories in self.technical_skills.items():
                for subcategory, skill_list in subcategories.items():
                    if any(skill in skills_lower for skill in skill_list):
                        categories_covered += 1
                        break
            
            diversity_score = categories_covered / total_categories
            
            if diversity_score >= 0.7:
                return 'High'
            elif diversity_score >= 0.4:
                return 'Medium'
            else:
                return 'Low'
                
        except Exception as e:
            logger.error(f"❌ Error calculating skill diversity: {e}")
            return 'Medium'
    
    def _determine_skill_level(self, skills_lower: List[str], is_fresher: bool) -> str:
        """Determine skill level"""
        try:
            if is_fresher:
                if len(skills_lower) >= 8:
                    return 'Advanced Fresher'
                elif len(skills_lower) >= 5:
                    return 'Intermediate Fresher'
                else:
                    return 'Beginner Fresher'
            else:
                if len(skills_lower) >= 15:
                    return 'Expert'
                elif len(skills_lower) >= 10:
                    return 'Advanced'
                elif len(skills_lower) >= 5:
                    return 'Intermediate'
                else:
                    return 'Beginner'
                    
        except Exception as e:
            logger.error(f"❌ Error determining skill level: {e}")
            return 'Intermediate'
    
    def _calculate_skill_strength(self, skills_lower: List[str], is_fresher: bool) -> str:
        """Calculate skill strength"""
        try:
            # Count high-demand skills
            high_demand_skills = []
            for category, subcategories in self.technical_skills.items():
                for subcategory, skill_list in subcategories.items():
                    if subcategory == 'high_demand':
                        high_demand_skills.extend(skill_list)
            
            high_demand_count = sum(1 for skill in skills_lower if skill in high_demand_skills)
            
            if is_fresher:
                if high_demand_count >= 3:
                    return 'Strong'
                elif high_demand_count >= 1:
                    return 'Good'
                else:
                    return 'Needs Improvement'
            else:
                if high_demand_count >= 5:
                    return 'Excellent'
                elif high_demand_count >= 3:
                    return 'Strong'
                elif high_demand_count >= 1:
                    return 'Good'
                else:
                    return 'Needs Improvement'
                    
        except Exception as e:
            logger.error(f"❌ Error calculating skill strength: {e}")
            return 'Good'
    
    def _generate_fresher_recommendations(self, skills: List[str], role: str) -> Dict[str, Any]:
        """Generate recommendations for fresher"""
        try:
            return {
                'immediate_actions': [
                    'Build 2-3 portfolio projects',
                    'Learn version control (Git)',
                    'Practice coding problems daily',
                    'Create a professional GitHub profile'
                ],
                'skill_development': [
                    'Master programming fundamentals',
                    'Learn industry-standard tools',
                    'Understand software development lifecycle',
                    'Practice code review and testing'
                ],
                'career_preparation': [
                    'Network with industry professionals',
                    'Attend tech meetups and conferences',
                    'Apply for internships or entry-level positions',
                    'Prepare for technical interviews'
                ],
                'long_term_goals': [
                    'Gain 1-2 years of professional experience',
                    'Develop specialization in chosen field',
                    'Build leadership and communication skills',
                    'Consider advanced certifications'
                ]
            }
        except Exception as e:
            logger.error(f"❌ Error generating fresher recommendations: {e}")
            return {'immediate_actions': [], 'skill_development': [], 'career_preparation': [], 'long_term_goals': []}
    
    def _generate_experienced_recommendations(self, skills: List[str], experience_years: int, role: str) -> Dict[str, Any]:
        """Generate recommendations for experienced candidate"""
        try:
            return {
                'immediate_actions': [
                    'Focus on leadership and mentoring skills',
                    'Learn advanced architecture patterns',
                    'Take on more strategic responsibilities',
                    'Build cross-functional collaboration'
                ],
                'skill_development': [
                    'Master system design and architecture',
                    'Develop team leadership skills',
                    'Learn business and product management',
                    'Stay updated with latest technologies'
                ],
                'career_advancement': [
                    'Consider management track',
                    'Lead technical initiatives',
                    'Mentor junior developers',
                    'Contribute to technical strategy'
                ],
                'long_term_goals': [
                    'Progress to senior management',
                    'Develop technical vision',
                    'Build industry recognition',
                    'Consider entrepreneurship'
                ]
            }
        except Exception as e:
            logger.error(f"❌ Error generating experienced recommendations: {e}")
            return {'immediate_actions': [], 'skill_development': [], 'career_advancement': [], 'long_term_goals': []}
    
    def _determine_career_track(self, role: str, skills: List[str]) -> str:
        """Determine career track"""
        try:
            role_lower = role.lower()
            skills_lower = [skill.lower() for skill in skills]
            
            if 'data' in role_lower or any(skill in skills_lower for skill in ['python', 'r', 'sql', 'pandas', 'numpy']):
                return 'data_scientist'
            elif 'devops' in role_lower or any(skill in skills_lower for skill in ['docker', 'kubernetes', 'aws', 'azure']):
                return 'devops_engineer'
            else:
                return 'software_engineer'
        except Exception as e:
            logger.error(f"❌ Error determining career track: {e}")
            return 'software_engineer'
    
    def _determine_current_level(self, role: str, experience_years: int, is_fresher: bool) -> str:
        """Determine current level"""
        try:
            if is_fresher:
                return 'fresher'
            elif experience_years <= 2:
                return 'fresher'
            elif experience_years <= 5:
                return 'mid_level'
            elif experience_years <= 8:
                return 'senior'
            else:
                return 'principal'
        except Exception as e:
            logger.error(f"❌ Error determining current level: {e}")
            return 'fresher'
    
    def _calculate_overall_score(self, skills: List[str], experience: Dict[str, Any], role: str, is_fresher: bool) -> float:
        """Calculate overall score"""
        try:
            score = 0.5  # Base score
            
            # Skills score
            score += min(len(skills) * 0.02, 0.3)
            
            # Experience score
            experience_years = experience.get('total_years', 0)
            score += min(experience_years * 0.05, 0.2)
            
            return min(score, 1.0)
        except Exception as e:
            logger.error(f"❌ Error calculating overall score: {e}")
            return 0.5
    
    def _determine_market_readiness(self, skills: List[str], experience_years: int, is_fresher: bool) -> str:
        """Determine market readiness"""
        try:
            if is_fresher:
                if len(skills) >= 5:
                    return 'Ready for entry-level positions'
                else:
                    return 'Needs skill development'
            else:
                if len(skills) >= 10:
                    return 'Ready for senior roles'
                else:
                    return 'Ready for mid-level roles'
        except Exception as e:
            logger.error(f"❌ Error determining market readiness: {e}")
            return 'Unknown'
    
    def _determine_growth_potential(self, skills: List[str], experience_years: int, is_fresher: bool) -> str:
        """Determine growth potential"""
        try:
            if is_fresher:
                return 'High - Strong learning curve expected'
            else:
                return 'Excellent - Leadership opportunities available'
        except Exception as e:
            logger.error(f"❌ Error determining growth potential: {e}")
            return 'Unknown'
    
    def _generate_personalized_insights(self, resume_data: Dict[str, Any], is_fresher: bool) -> List[str]:
        """Generate personalized insights"""
        try:
            insights = []
            skills = resume_data.get('skills', [])
            experience = resume_data.get('experience', {})
            
            if is_fresher:
                insights.append('Strong foundation for career growth')
                if len(skills) >= 5:
                    insights.append('Good technical skill diversity')
                else:
                    insights.append('Consider expanding technical skills')
            else:
                insights.append('Experienced professional with growth potential')
                if len(skills) >= 10:
                    insights.append('Excellent technical expertise')
                else:
                    insights.append('Consider specializing in key technologies')
            
            return insights
        except Exception as e:
            logger.error(f"❌ Error generating personalized insights: {e}")
            return ['Focus on continuous learning and skill development']
    
    def _generate_recommended_actions(self, skills: List[str], experience_years: int, is_fresher: bool) -> List[str]:
        """Generate recommended actions"""
        try:
            if is_fresher:
                return [
                    'Focus on building a strong portfolio',
                    'Learn industry-standard tools and technologies',
                    'Practice coding problems regularly',
                    'Contribute to open source projects',
                    'Network with industry professionals'
                ]
            else:
                return [
                    'Focus on leadership and mentoring skills',
                    'Learn advanced architecture patterns',
                    'Consider management track',
                    'Build cross-functional collaboration',
                    'Stay updated with latest technologies'
                ]
        except Exception as e:
            logger.error(f"❌ Error generating recommended actions: {e}")
            return ['Focus on skill development', 'Build portfolio', 'Network', 'Seek mentorship']

    def _analyze_experience_quality(self, experience_periods: List, skills: List[str]) -> Dict:
        """Analyze the quality and relevance of experience"""
        try:
            # Calculate total years from experience periods
            total_years = 0
            for period in experience_periods:
                if 'start_year' in period and 'end_year' in period:
                    total_years += period['end_year'] - period['start_year']
            
            is_fresher = total_years == 0
            
            if is_fresher or total_years == 0:
                return {
                    'quality_score': 0.3,
                    'relevance_score': 0.2,
                    'progression_score': 0.1,
                    'analysis': 'Fresher candidate with no professional experience'
                }
            elif total_years < 2:
                return {
                    'quality_score': 0.6,
                    'relevance_score': 0.5,
                    'progression_score': 0.4,
                    'analysis': 'Junior level with limited experience'
                }
            elif total_years < 5:
                return {
                    'quality_score': 0.8,
                    'relevance_score': 0.7,
                    'progression_score': 0.6,
                    'analysis': 'Mid-level professional with solid experience'
                }
            else:
                return {
                    'quality_score': 0.9,
                    'relevance_score': 0.8,
                    'progression_score': 0.7,
                    'analysis': 'Senior professional with extensive experience'
                }
        except Exception as e:
            logger.error(f"❌ Error analyzing experience quality: {str(e)}")
            return {
                'quality_score': 0.5,
                'relevance_score': 0.5,
                'progression_score': 0.5,
                'analysis': 'Experience analysis unavailable'
            }
    
    def _generate_progression_timeline(self, career_track: str, current_level: str, experience_years: float) -> Dict:
        """Generate career progression timeline"""
        try:
            if experience_years == 0:
                return {
                    'current_level': 'Entry Level',
                    'next_level': 'Junior',
                    'timeline': '0-2 years',
                    'key_milestones': [
                        'Complete first professional project',
                        'Learn industry best practices',
                        'Build portfolio of work'
                    ]
                }
            elif experience_years < 2:
                return {
                    'current_level': 'Junior',
                    'next_level': 'Mid-Level',
                    'timeline': '2-5 years',
                    'key_milestones': [
                        'Take on more complex projects',
                        'Mentor junior developers',
                        'Specialize in specific technologies'
                    ]
                }
            elif experience_years < 5:
                return {
                    'current_level': 'Mid-Level',
                    'next_level': 'Senior',
                    'timeline': '5-8 years',
                    'key_milestones': [
                        'Lead technical initiatives',
                        'Architect system solutions',
                        'Mentor multiple team members'
                    ]
                }
            else:
                return {
                    'current_level': 'Senior',
                    'next_level': 'Lead/Principal',
                    'timeline': '8+ years',
                    'key_milestones': [
                        'Drive technical strategy',
                        'Lead cross-functional teams',
                        'Contribute to industry standards'
                    ]
                }
        except Exception as e:
            logger.error(f"❌ Error generating progression timeline: {str(e)}")
            return {
                'current_level': 'Unknown',
                'next_level': 'Unknown',
                'timeline': 'Unknown',
                'key_milestones': []
            }
    
    def _determine_industry(self, role: str, skills: List[str]) -> str:
        """Determine the primary industry based on role and skills"""
        try:
            role_lower = role.lower()
            skills_lower = [skill.lower() for skill in skills]
            
            # Technology industry indicators
            tech_indicators = ['developer', 'engineer', 'programmer', 'architect', 'analyst']
            if any(indicator in role_lower for indicator in tech_indicators):
                return 'Technology'
            
            # Data science indicators
            data_indicators = ['data', 'analyst', 'scientist', 'machine learning', 'ai']
            if any(indicator in role_lower for indicator in data_indicators):
                return 'Data Science'
            
            # Finance indicators
            finance_indicators = ['finance', 'banking', 'investment', 'trading']
            if any(indicator in role_lower for indicator in finance_indicators):
                return 'Finance'
            
            # Healthcare indicators
            healthcare_indicators = ['healthcare', 'medical', 'pharmaceutical', 'biotech']
            if any(indicator in role_lower for indicator in healthcare_indicators):
                return 'Healthcare'
            
            # Default to Technology for software-related roles
            return 'Technology'
        except Exception as e:
            logger.error(f"❌ Error determining industry: {str(e)}")
            return 'Unknown'
    
    def _calculate_industry_fit(self, skills_lower: List[str], industry: str) -> Dict:
        """Calculate how well the candidate fits the industry"""
        try:
            # Industry-specific skill requirements
            industry_skills = {
                'technology': ['java', 'python', 'javascript', 'sql', 'git', 'html', 'css'],
                'data_science': ['python', 'r', 'sql', 'machine learning', 'statistics', 'pandas'],
                'finance': ['sql', 'excel', 'python', 'r', 'financial modeling', 'risk analysis'],
                'healthcare': ['sql', 'python', 'r', 'statistics', 'clinical data', 'regulatory']
            }
            
            required_skills = industry_skills.get(industry.lower(), industry_skills['technology'])
            matching_skills = [skill for skill in skills_lower if skill in required_skills]
            
            fit_score = len(matching_skills) / len(required_skills) if required_skills else 0
            
            if fit_score >= 0.8:
                fit_level = 'Excellent'
            elif fit_score >= 0.6:
                fit_level = 'Good'
            elif fit_score >= 0.4:
                fit_level = 'Moderate'
            else:
                fit_level = 'Low'
            
            return {
                'fit_score': fit_score,
                'fit_level': fit_level,
                'matching_skills': matching_skills,
                'missing_skills': [skill for skill in required_skills if skill not in skills_lower]
            }
        except Exception as e:
            logger.error(f"❌ Error calculating industry fit: {str(e)}")
            return {
                'fit_score': 0.5,
                'fit_level': 'Unknown',
                'matching_skills': [],
                'missing_skills': []
            }
    
    def _calculate_skill_multiplier(self, skills: List[str], role: str) -> float:
        """Calculate skill multiplier for salary calculation"""
        try:
            base_multiplier = 1.0
            
            # High-demand skills multiplier
            high_demand_skills = ['python', 'javascript', 'java', 'react', 'aws', 'docker', 'kubernetes']
            high_demand_count = sum(1 for skill in skills if skill.lower() in high_demand_skills)
            base_multiplier += high_demand_count * 0.1
            
            # Role-specific multiplier
            role_lower = role.lower()
            if 'senior' in role_lower or 'lead' in role_lower:
                base_multiplier += 0.3
            elif 'mid' in role_lower or 'intermediate' in role_lower:
                base_multiplier += 0.1
            
            return min(base_multiplier, 2.0)  # Cap at 2.0
        except Exception as e:
            logger.error(f"❌ Error calculating skill multiplier: {str(e)}")
            return 1.0
    
    def _get_required_skills(self, role: str, experience_years: float, is_fresher: bool) -> List[str]:
        """Get required skills for the role and experience level"""
        try:
            role_lower = role.lower()
            base_skills = []
            
            # Role-specific skills
            if 'java' in role_lower:
                base_skills = ['Java', 'Spring', 'Maven', 'SQL', 'Git']
            elif 'python' in role_lower:
                base_skills = ['Python', 'Django', 'Flask', 'SQL', 'Git']
            elif 'javascript' in role_lower or 'react' in role_lower:
                base_skills = ['JavaScript', 'React', 'Node.js', 'HTML', 'CSS']
            elif 'full stack' in role_lower:
                base_skills = ['JavaScript', 'React', 'Node.js', 'SQL', 'Git', 'HTML', 'CSS']
            else:
                base_skills = ['Programming', 'SQL', 'Git', 'Problem Solving']
            
            # Experience-based skills
            if experience_years >= 3:
                base_skills.extend(['System Design', 'Architecture', 'Mentoring'])
            if experience_years >= 5:
                base_skills.extend(['Leadership', 'Project Management', 'Technical Strategy'])
            
            return base_skills
        except Exception as e:
            logger.error(f"❌ Error getting required skills: {str(e)}")
            return ['Programming', 'Problem Solving', 'Communication']
    
    def _analyze_experience_relevance(self, experience_periods: List, skills: List[str]) -> Dict:
        """Analyze the relevance of experience to current role"""
        try:
            relevance_score = 0.5  # Default score
            
            # Check if experience periods exist
            if experience_periods:
                relevance_score += 0.3
            
            # Check if skills match experience
            if len(skills) >= 5:
                relevance_score += 0.2
            
            return {
                'relevance_score': min(relevance_score, 1.0),
                'analysis': 'Experience relevance analyzed',
                'periods_count': len(experience_periods),
                'skills_count': len(skills)
            }
        except Exception as e:
            logger.error(f"❌ Error analyzing experience relevance: {str(e)}")
            return {
                'relevance_score': 0.5,
                'analysis': 'Experience relevance analysis unavailable',
                'periods_count': 0,
                'skills_count': 0
            }
    
    def _calculate_career_readiness(self, skills: List[str], experience: Dict, role: str, is_fresher: bool) -> Dict:
        """Calculate career readiness score"""
        try:
            readiness_score = 0.5  # Base score
            
            # Skills factor
            if len(skills) >= 10:
                readiness_score += 0.3
            elif len(skills) >= 5:
                readiness_score += 0.2
            
            # Experience factor
            if not is_fresher:
                readiness_score += 0.2
            
            # Role match factor
            role_lower = role.lower()
            if any(skill.lower() in role_lower for skill in skills):
                readiness_score += 0.2
            
            return {
                'readiness_score': min(readiness_score, 1.0),
                'readiness_level': 'High' if readiness_score >= 0.8 else 'Medium' if readiness_score >= 0.6 else 'Low',
                'analysis': f'Career readiness: {readiness_score:.1%}'
            }
        except Exception as e:
            logger.error(f"❌ Error calculating career readiness: {str(e)}")
            return {
                'readiness_score': 0.5,
                'readiness_level': 'Unknown',
                'analysis': 'Career readiness analysis unavailable'
            }
    
    def _analyze_market_demand(self, skills_lower: List[str], industry: str) -> Dict:
        """Analyze market demand for skills"""
        try:
            # High-demand skills
            high_demand_skills = ['java', 'python', 'javascript', 'react', 'aws', 'docker', 'kubernetes', 'sql']
            high_demand_count = sum(1 for skill in skills_lower if skill in high_demand_skills)
            
            demand_score = high_demand_count / len(high_demand_skills) if high_demand_skills else 0
            
            return {
                'demand_score': demand_score,
                'demand_level': 'High' if demand_score >= 0.7 else 'Medium' if demand_score >= 0.4 else 'Low',
                'high_demand_skills': [skill for skill in skills_lower if skill in high_demand_skills],
                'analysis': f'Market demand: {demand_score:.1%}'
            }
        except Exception as e:
            logger.error(f"❌ Error analyzing market demand: {str(e)}")
            return {
                'demand_score': 0.5,
                'demand_level': 'Unknown',
                'high_demand_skills': [],
                'analysis': 'Market demand analysis unavailable'
            }
    
    def _categorize_missing_skills(self, missing_skills: List[str]) -> Dict:
        """Categorize missing skills by type"""
        try:
            categories = {
                'programming_languages': [],
                'frameworks': [],
                'databases': [],
                'tools': [],
                'soft_skills': []
            }
            
            for skill in missing_skills:
                skill_lower = skill.lower()
                if any(lang in skill_lower for lang in ['java', 'python', 'javascript', 'c++', 'c#']):
                    categories['programming_languages'].append(skill)
                elif any(fw in skill_lower for fw in ['spring', 'react', 'angular', 'django', 'flask']):
                    categories['frameworks'].append(skill)
                elif any(db in skill_lower for db in ['sql', 'mysql', 'postgresql', 'mongodb']):
                    categories['databases'].append(skill)
                elif any(tool in skill_lower for tool in ['git', 'docker', 'kubernetes', 'aws']):
                    categories['tools'].append(skill)
                else:
                    categories['soft_skills'].append(skill)
            
            return categories
        except Exception as e:
            logger.error(f"❌ Error categorizing missing skills: {str(e)}")
            return {
                'programming_languages': [],
                'frameworks': [],
                'databases': [],
                'tools': [],
                'soft_skills': []
            }

    def _get_empty_analysis(self) -> Dict[str, Any]:
        """Return empty analysis"""
        return {
            'is_fresher': True,
            'candidate_profile': {'name': 'Unknown', 'role': 'Unknown', 'experience_years': 0},
            'skill_analysis': {'technical_skills': {}, 'total_skills': 0},
            'experience_analysis': {'total_years': 0, 'is_fresher': True},
            'career_path_analysis': {'career_track': 'software_engineer', 'current_level': 'fresher'},
            'industry_analysis': {'industry': 'technology', 'industry_fit': 'Unknown'},
            'salary_analysis': {'current_range': {'min': 300000, 'max': 600000, 'currency': 'INR'}},
            'skill_gap_analysis': {'missing_skills': [], 'skill_gap_score': 0},
            'recommendations': {'immediate_actions': []},
            'ai_insights': {'overall_score': 0.5, 'market_readiness': 'Unknown'},
            'error': 'Analysis failed'
        }

# Initialize global advanced AI career analyzer
advanced_ai_career_analyzer = AdvancedAICareerAnalyzer()
