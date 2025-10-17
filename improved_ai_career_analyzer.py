"""
Improved AI Career Analyzer
Enhanced career analysis with fresher detection and appropriate career paths
"""

import re
import logging
from datetime import datetime
from typing import Dict, List, Any, Tuple
import random

logger = logging.getLogger(__name__)

class ImprovedAICareerAnalyzer:
    """Improved AI-powered career analyzer with fresher detection"""
    
    def __init__(self):
        # Dynamic skill categories
        self.skill_categories = {
            'programming': ['java', 'python', 'javascript', 'c++', 'c#', 'go', 'rust', 'kotlin', 'swift'],
            'web': ['react', 'angular', 'vue', 'html', 'css', 'bootstrap', 'tailwind', 'sass'],
            'backend': ['spring', 'django', 'flask', 'express', 'node', 'fastapi', 'rails'],
            'database': ['mysql', 'postgresql', 'mongodb', 'redis', 'elasticsearch', 'oracle'],
            'cloud': ['aws', 'azure', 'gcp', 'docker', 'kubernetes', 'terraform', 'jenkins'],
            'mobile': ['android', 'ios', 'react native', 'flutter', 'xamarin'],
            'ai_ml': ['tensorflow', 'pytorch', 'scikit-learn', 'pandas', 'numpy', 'opencv'],
            'devops': ['git', 'ci/cd', 'ansible', 'chef', 'puppet', 'monitoring'],
            'testing': ['selenium', 'junit', 'testng', 'cypress', 'jest', 'mocha']
        }
        
        # Fresher-specific career paths
        self.fresher_career_paths = {
            'software_developer': {
                'entry_level': 'Fresher → Junior Developer → Mid Developer → Senior Developer',
                'timeline': '0-2 years → 2-4 years → 4-6 years → 6+ years',
                'skills_progression': [
                    'Learn programming fundamentals',
                    'Build portfolio projects',
                    'Master version control (Git)',
                    'Learn testing frameworks',
                    'Understand system design basics'
                ],
                'recommended_skills': ['Java', 'Python', 'JavaScript', 'HTML', 'CSS', 'SQL', 'Git'],
                'certifications': ['AWS Certified Developer', 'Oracle Java Certification', 'Microsoft Azure Fundamentals'],
                'next_steps': [
                    'Complete 2-3 personal projects',
                    'Contribute to open source',
                    'Build a strong GitHub profile',
                    'Practice coding problems daily',
                    'Learn version control (Git)',
                    'Understand basic system design'
                ]
            },
            'web_developer': {
                'entry_level': 'Fresher → Junior Web Developer → Mid Web Developer → Senior Web Developer',
                'timeline': '0-1 years → 1-3 years → 3-5 years → 5+ years',
                'skills_progression': [
                    'Master HTML/CSS/JavaScript',
                    'Learn a frontend framework (React/Vue/Angular)',
                    'Understand backend basics',
                    'Learn database fundamentals',
                    'Master responsive design'
                ],
                'recommended_skills': ['HTML', 'CSS', 'JavaScript', 'React', 'Node.js', 'MongoDB', 'Git'],
                'certifications': ['Google Web Developer Certification', 'Meta Frontend Developer Certificate'],
                'next_steps': [
                    'Build responsive websites',
                    'Learn a JavaScript framework',
                    'Create a portfolio website',
                    'Practice CSS animations',
                    'Learn API integration',
                    'Understand web performance'
                ]
            },
            'data_scientist': {
                'entry_level': 'Fresher → Junior Data Analyst → Data Scientist → Senior Data Scientist',
                'timeline': '0-1 years → 1-3 years → 3-5 years → 5+ years',
                'skills_progression': [
                    'Learn Python/R for data analysis',
                    'Master SQL and databases',
                    'Understand statistics and mathematics',
                    'Learn machine learning basics',
                    'Master data visualization'
                ],
                'recommended_skills': ['Python', 'R', 'SQL', 'Pandas', 'NumPy', 'Matplotlib', 'Scikit-learn'],
                'certifications': ['Google Data Analytics Certificate', 'IBM Data Science Certificate'],
                'next_steps': [
                    'Complete data analysis projects',
                    'Learn statistical concepts',
                    'Practice with real datasets',
                    'Build data visualization skills',
                    'Learn machine learning basics',
                    'Create a data science portfolio'
                ]
            }
        }
        
        # Experienced career paths
        self.experienced_career_paths = {
            'senior_developer': {
                'senior': 'Senior Developer → Tech Lead → Principal Engineer → Engineering Manager',
                'skills': ['System design', 'Architecture', 'Mentoring', 'Code review'],
                'next_level': 'Tech Lead',
                'timeline': '1-2 years'
            },
            'tech_lead': {
                'lead': 'Tech Lead → Principal Engineer → Engineering Manager → Director',
                'skills': ['Team leadership', 'Technical strategy', 'Project management', 'Stakeholder communication'],
                'next_level': 'Principal Engineer',
                'timeline': '2-3 years'
            },
            'manager': {
                'manager': 'Engineering Manager → Senior Manager → Director → VP Engineering',
                'skills': ['People management', 'Strategic planning', 'Budget management', 'Cross-functional collaboration'],
                'next_level': 'Senior Manager',
                'timeline': '2-4 years'
            }
        }
        
        # Dynamic salary ranges by experience
        self.salary_ranges = {
            0: {'min': 300000, 'max': 600000, 'currency': 'INR'},
            1: {'min': 400000, 'max': 800000, 'currency': 'INR'},
            2: {'min': 600000, 'max': 1200000, 'currency': 'INR'},
            3: {'min': 800000, 'max': 1500000, 'currency': 'INR'},
            4: {'min': 1000000, 'max': 2000000, 'currency': 'INR'},
            5: {'min': 1200000, 'max': 2500000, 'currency': 'INR'},
        }
    
    def analyze_resume(self, resume_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze resume and determine if fresher or experienced"""
        try:
            logger.info("🤖 Starting improved AI resume analysis...")
            
            # Extract key information
            name = resume_data.get('name', 'Unknown')
            role = resume_data.get('role', 'Unknown')
            skills = resume_data.get('skills', [])
            experience = resume_data.get('experience', {})
            location = resume_data.get('location', 'Unknown')
            
            # Determine if fresher
            is_fresher = self._is_fresher(experience, skills, role)
            
            if is_fresher:
                return self._analyze_fresher_resume(resume_data)
            else:
                return self._analyze_experienced_resume(resume_data)
                
        except Exception as e:
            logger.error(f"❌ Improved AI resume analysis error: {e}")
            return self._get_empty_analysis()
    
    def _is_fresher(self, experience: Dict[str, Any], skills: List[str], role: str) -> bool:
        """Determine if candidate is a fresher"""
        try:
            # Check experience data
            if experience.get('is_fresher', False):
                return True
            
            experience_years = experience.get('total_years', 0)
            if experience_years <= 1.0:
                return True
            
            # Check skills count
            if len(skills) <= 5:
                return True
            
            # Check role for fresher indicators
            role_lower = role.lower()
            fresher_indicators = ['fresher', 'fresh graduate', 'entry level', 'junior', 'trainee', 'intern']
            if any(indicator in role_lower for indicator in fresher_indicators):
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"❌ Error determining fresher status: {e}")
            return True  # Default to fresher if error
    
    def _analyze_fresher_resume(self, resume_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze fresher resume with appropriate career path"""
        try:
            logger.info("🎓 Analyzing fresher resume...")
            
            name = resume_data.get('name', 'Unknown')
            role = resume_data.get('role', 'Developer')
            skills = resume_data.get('skills', [])
            experience = resume_data.get('experience', {})
            location = resume_data.get('location', 'Unknown')
            
            # Determine career path based on skills and role
            career_path_type = self._determine_fresher_career_path(role, skills)
            career_path = self.fresher_career_paths.get(career_path_type, self.fresher_career_paths['software_developer'])
            
            # Analyze skills
            skill_analysis = self._analyze_fresher_skills(skills)
            
            # Generate fresher-specific recommendations
            recommendations = self._generate_fresher_recommendations(skills, career_path_type)
            
            # Salary projection for freshers
            salary_projection = self._project_fresher_salary(skills)
            
            return {
                'is_fresher': True,
                'candidate_profile': {
                    'name': name,
                    'role': role,
                    'experience_years': experience.get('total_years', 0),
                    'location': location,
                    'skills_count': len(skills),
                    'career_stage': 'Fresher',
                    'experience_level': 'Entry Level'
                },
                'fresher_career_path': career_path,
                'skill_analysis': skill_analysis,
                'recommendations': recommendations,
                'salary_projection': salary_projection,
                'ai_insights': {
                    'career_stage': 'Fresher',
                    'market_readiness': 'Ready for entry-level positions',
                    'growth_potential': 'High - Strong learning curve expected',
                    'recommended_actions': [
                        'Focus on building a strong portfolio',
                        'Learn industry-standard tools and technologies',
                        'Practice coding problems regularly',
                        'Contribute to open source projects',
                        'Network with industry professionals'
                    ]
                },
                'analysis_timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"❌ Fresher resume analysis error: {e}")
            return self._get_empty_fresher_analysis()
    
    def _analyze_experienced_resume(self, resume_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze experienced resume with advanced career insights"""
        try:
            logger.info("💼 Analyzing experienced resume...")
            
            name = resume_data.get('name', 'Unknown')
            role = resume_data.get('role', 'Developer')
            skills = resume_data.get('skills', [])
            experience = resume_data.get('experience', {})
            location = resume_data.get('location', 'Unknown')
            
            experience_years = experience.get('total_years', 0)
            
            # Determine career level
            career_level = self._determine_career_level(role, experience_years)
            career_path = self.experienced_career_paths.get(career_level, self.experienced_career_paths['senior_developer'])
            
            # Analyze skills
            skill_analysis = self._analyze_experienced_skills(skills, experience_years)
            
            # Generate experienced recommendations
            recommendations = self._generate_experienced_recommendations(skills, experience_years, career_level)
            
            # Salary projection for experienced
            salary_projection = self._project_experienced_salary(experience_years, skills)
            
            return {
                'is_fresher': False,
                'candidate_profile': {
                    'name': name,
                    'role': role,
                    'experience_years': experience_years,
                    'location': location,
                    'skills_count': len(skills),
                    'career_stage': self._get_career_stage(experience_years),
                    'experience_level': career_level.title()
                },
                'career_progression': career_path,
                'skill_analysis': skill_analysis,
                'recommendations': recommendations,
                'salary_projection': salary_projection,
                'ai_insights': {
                    'career_stage': self._get_career_stage(experience_years),
                    'market_readiness': 'Ready for senior roles',
                    'growth_potential': 'Excellent - Leadership opportunities available',
                    'recommended_actions': [
                        'Focus on leadership and mentoring skills',
                        'Learn advanced architecture patterns',
                        'Consider management track',
                        'Build cross-functional collaboration',
                        'Stay updated with latest technologies'
                    ]
                },
                'analysis_timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"❌ Experienced resume analysis error: {e}")
            return self._get_empty_experienced_analysis()
    
    def _determine_fresher_career_path(self, role: str, skills: List[str]) -> str:
        """Determine appropriate career path for fresher"""
        try:
            role_lower = role.lower()
            skills_lower = [skill.lower() for skill in skills]
            
            # Check for web development skills
            web_skills = ['html', 'css', 'javascript', 'react', 'angular', 'vue']
            if any(skill in skills_lower for skill in web_skills) or 'web' in role_lower:
                return 'web_developer'
            
            # Check for data science skills
            data_skills = ['python', 'r', 'sql', 'pandas', 'numpy', 'matplotlib', 'scikit-learn']
            if any(skill in skills_lower for skill in data_skills) or 'data' in role_lower:
                return 'data_scientist'
            
            # Default to software developer
            return 'software_developer'
            
        except Exception as e:
            logger.error(f"❌ Error determining fresher career path: {e}")
            return 'software_developer'
    
    def _analyze_fresher_skills(self, skills: List[str]) -> Dict[str, Any]:
        """Analyze skills for fresher"""
        try:
            skills_lower = [skill.lower() for skill in skills]
            
            # Categorize skills
            skill_categories = {}
            for category, category_skills in self.skill_categories.items():
                matches = [skill for skill in skills_lower if skill in category_skills]
                skill_categories[category] = {
                    'skills': matches,
                    'count': len(matches),
                    'coverage': len(matches) / len(category_skills) if category_skills else 0
                }
            
            # Identify skill gaps for freshers
            critical_gaps = ['git', 'testing', 'debugging', 'documentation']
            missing_critical = [gap for gap in critical_gaps if gap not in skills_lower]
            
            return {
                'skill_categories': skill_categories,
                'total_skills': len(skills),
                'skill_gaps': {
                    'critical_gaps': missing_critical,
                    'recommended_skills': ['Git', 'Testing', 'Debugging', 'Documentation', 'Code Review']
                },
                'skill_strength': 'Good foundation' if len(skills) >= 3 else 'Needs improvement'
            }
            
        except Exception as e:
            logger.error(f"❌ Error analyzing fresher skills: {e}")
            return {'skill_categories': {}, 'total_skills': 0, 'skill_gaps': {}, 'skill_strength': 'Unknown'}
    
    def _generate_fresher_recommendations(self, skills: List[str], career_path_type: str) -> Dict[str, Any]:
        """Generate recommendations for fresher"""
        try:
            skills_lower = [skill.lower() for skill in skills]
            
            recommendations = {
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
            
            return recommendations
            
        except Exception as e:
            logger.error(f"❌ Error generating fresher recommendations: {e}")
            return {'immediate_actions': [], 'skill_development': [], 'career_preparation': [], 'long_term_goals': []}
    
    def _project_fresher_salary(self, skills: List[str]) -> Dict[str, Any]:
        """Project salary for fresher"""
        try:
            base_range = self.salary_ranges[0]
            
            # Skill-based adjustments
            skill_bonus = len(skills) * 10000
            high_demand_skills = ['python', 'java', 'javascript', 'react', 'aws']
            high_demand_count = sum(1 for skill in skills if skill.lower() in high_demand_skills)
            high_demand_bonus = high_demand_count * 20000
            
            projected_min = base_range['min'] + skill_bonus + high_demand_bonus
            projected_max = base_range['max'] + skill_bonus + high_demand_bonus
            
            return {
                'current_range': {
                    'min': projected_min,
                    'max': projected_max,
                    'currency': base_range['currency']
                },
                'growth_potential': 'High - 15-20% annually for first 3 years',
                'factors': [
                    'Strong portfolio and projects',
                    'Relevant certifications',
                    'Internship experience',
                    'Technical interview performance'
                ]
            }
            
        except Exception as e:
            logger.error(f"❌ Error projecting fresher salary: {e}")
            return {'current_range': {'min': 300000, 'max': 600000, 'currency': 'INR'}, 'growth_potential': 'Medium'}
    
    def _determine_career_level(self, role: str, experience_years: int) -> str:
        """Determine career level for experienced candidate"""
        try:
            role_lower = role.lower()
            
            if 'manager' in role_lower or experience_years >= 8:
                return 'manager'
            elif 'lead' in role_lower or experience_years >= 5:
                return 'tech_lead'
            else:
                return 'senior_developer'
                
        except Exception as e:
            logger.error(f"❌ Error determining career level: {e}")
            return 'senior_developer'
    
    def _get_career_stage(self, experience_years: int) -> str:
        """Get career stage based on experience"""
        try:
            if experience_years <= 1:
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
            logger.error(f"❌ Error getting career stage: {e}")
            return 'Mid-Level'
    
    def _analyze_experienced_skills(self, skills: List[str], experience_years: int) -> Dict[str, Any]:
        """Analyze skills for experienced candidate"""
        try:
            skills_lower = [skill.lower() for skill in skills]
            
            # Categorize skills
            skill_categories = {}
            for category, category_skills in self.skill_categories.items():
                matches = [skill for skill in skills_lower if skill in category_skills]
                skill_categories[category] = {
                    'skills': matches,
                    'count': len(matches),
                    'coverage': len(matches) / len(category_skills) if category_skills else 0
                }
            
            # Identify advanced skill gaps
            advanced_gaps = ['architecture', 'system design', 'leadership', 'mentoring']
            missing_advanced = [gap for gap in advanced_gaps if gap not in skills_lower]
            
            return {
                'skill_categories': skill_categories,
                'total_skills': len(skills),
                'skill_gaps': {
                    'advanced_gaps': missing_advanced,
                    'recommended_skills': ['System Design', 'Architecture', 'Leadership', 'Mentoring', 'Strategic Thinking']
                },
                'skill_strength': 'Excellent' if len(skills) >= 10 else 'Good'
            }
            
        except Exception as e:
            logger.error(f"❌ Error analyzing experienced skills: {e}")
            return {'skill_categories': {}, 'total_skills': 0, 'skill_gaps': {}, 'skill_strength': 'Unknown'}
    
    def _generate_experienced_recommendations(self, skills: List[str], experience_years: int, career_level: str) -> Dict[str, Any]:
        """Generate recommendations for experienced candidate"""
        try:
            recommendations = {
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
            
            return recommendations
            
        except Exception as e:
            logger.error(f"❌ Error generating experienced recommendations: {e}")
            return {'immediate_actions': [], 'skill_development': [], 'career_advancement': [], 'long_term_goals': []}
    
    def _project_experienced_salary(self, experience_years: int, skills: List[str]) -> Dict[str, Any]:
        """Project salary for experienced candidate"""
        try:
            base_range = self.salary_ranges.get(min(experience_years, 5), self.salary_ranges[5])
            
            # Skill-based adjustments
            skill_bonus = len(skills) * 15000
            high_demand_skills = ['aws', 'kubernetes', 'docker', 'react', 'python', 'java']
            high_demand_count = sum(1 for skill in skills if skill.lower() in high_demand_skills)
            high_demand_bonus = high_demand_count * 30000
            
            projected_min = base_range['min'] + skill_bonus + high_demand_bonus
            projected_max = base_range['max'] + skill_bonus + high_demand_bonus
            
            return {
                'current_range': {
                    'min': projected_min,
                    'max': projected_max,
                    'currency': base_range['currency']
                },
                'growth_potential': 'Excellent - 10-15% annually',
                'factors': [
                    'Leadership and mentoring experience',
                    'Advanced technical skills',
                    'Strategic thinking and vision',
                    'Cross-functional collaboration'
                ]
            }
            
        except Exception as e:
            logger.error(f"❌ Error projecting experienced salary: {e}")
            return {'current_range': {'min': 1000000, 'max': 2000000, 'currency': 'INR'}, 'growth_potential': 'Good'}
    
    def _get_empty_analysis(self) -> Dict[str, Any]:
        """Return empty analysis"""
        return {
            'is_fresher': True,
            'candidate_profile': {
                'name': 'Unknown',
                'role': 'Unknown',
                'experience_years': 0,
                'location': 'Unknown',
                'skills_count': 0,
                'career_stage': 'Unknown',
                'experience_level': 'Unknown'
            },
            'error': 'Analysis failed'
        }
    
    def _get_empty_fresher_analysis(self) -> Dict[str, Any]:
        """Return empty fresher analysis"""
        return {
            'is_fresher': True,
            'candidate_profile': {
                'name': 'Unknown',
                'role': 'Developer',
                'experience_years': 0,
                'location': 'Unknown',
                'skills_count': 0,
                'career_stage': 'Fresher',
                'experience_level': 'Entry Level'
            },
            'fresher_career_path': self.fresher_career_paths['software_developer'],
            'skill_analysis': {'skill_categories': {}, 'total_skills': 0},
            'recommendations': {'immediate_actions': []},
            'salary_projection': {'current_range': {'min': 300000, 'max': 600000, 'currency': 'INR'}},
            'ai_insights': {'career_stage': 'Fresher'},
            'error': 'Fresher analysis failed'
        }
    
    def _get_empty_experienced_analysis(self) -> Dict[str, Any]:
        """Return empty experienced analysis"""
        return {
            'is_fresher': False,
            'candidate_profile': {
                'name': 'Unknown',
                'role': 'Developer',
                'experience_years': 0,
                'location': 'Unknown',
                'skills_count': 0,
                'career_stage': 'Mid-Level',
                'experience_level': 'Senior'
            },
            'career_progression': self.experienced_career_paths['senior_developer'],
            'skill_analysis': {'skill_categories': {}, 'total_skills': 0},
            'recommendations': {'immediate_actions': []},
            'salary_projection': {'current_range': {'min': 1000000, 'max': 2000000, 'currency': 'INR'}},
            'ai_insights': {'career_stage': 'Mid-Level'},
            'error': 'Experienced analysis failed'
        }

# Initialize global improved AI career analyzer
improved_ai_career_analyzer = ImprovedAICareerAnalyzer()
