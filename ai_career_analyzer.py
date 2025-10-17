"""
AI Career Analyzer
Dynamic AI-powered career analysis and insights
"""

import re
import logging
from datetime import datetime
from typing import Dict, List, Any, Tuple
import random

logger = logging.getLogger(__name__)

class AICareerAnalyzer:
    """AI-powered career analyzer with dynamic insights"""
    
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
        
        # Dynamic salary ranges by experience
        self.salary_ranges = {
            0: {'min': 300000, 'max': 600000, 'currency': 'INR'},
            1: {'min': 400000, 'max': 800000, 'currency': 'INR'},
            2: {'min': 600000, 'max': 1200000, 'currency': 'INR'},
            3: {'min': 800000, 'max': 1500000, 'currency': 'INR'},
            4: {'min': 1000000, 'max': 2000000, 'currency': 'INR'},
            5: {'min': 1200000, 'max': 2500000, 'currency': 'INR'},
            6: {'min': 1500000, 'max': 3000000, 'currency': 'INR'},
            7: {'min': 1800000, 'max': 3500000, 'currency': 'INR'},
            8: {'min': 2000000, 'max': 4000000, 'currency': 'INR'},
            9: {'min': 2500000, 'max': 5000000, 'currency': 'INR'},
            10: {'min': 3000000, 'max': 6000000, 'currency': 'INR'}
        }
        
        # Dynamic career paths
        self.career_paths = {
            'developer': {
                'junior': 'Junior Developer → Mid Developer → Senior Developer → Tech Lead',
                'skills': ['Programming fundamentals', 'Version control', 'Testing', 'Debugging'],
                'next_level': 'Mid Developer',
                'timeline': '6-12 months'
            },
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
        
        # Dynamic skill gap analysis
        self.skill_gaps = {
            'entry': ['Git basics', 'Testing fundamentals', 'Code review', 'Documentation'],
            'mid': ['System design', 'Performance optimization', 'Security basics', 'API design'],
            'senior': ['Architecture patterns', 'Scalability', 'Team leadership', 'Mentoring'],
            'lead': ['Strategic thinking', 'Cross-functional collaboration', 'Technical vision', 'Innovation']
        }
    
    def analyze_skills(self, skills: List[str]) -> Dict[str, Any]:
        """AI-powered skill gap analysis"""
        try:
            logger.info("🧠 Starting AI skill analysis...")
            
            if not skills:
                return self._get_empty_skill_analysis()
            
            skills_lower = [skill.lower() for skill in skills]
            
            # Analyze skill categories
            category_analysis = {}
            for category, category_skills in self.skill_categories.items():
                matches = [skill for skill in skills_lower if skill in category_skills]
                category_analysis[category] = {
                    'skills': matches,
                    'count': len(matches),
                    'coverage': len(matches) / len(category_skills) if category_skills else 0
                }
            
            # Determine experience level based on skills
            experience_level = self._determine_experience_level(skills_lower)
            
            # Identify skill gaps
            skill_gaps = self._identify_skill_gaps(skills_lower, experience_level)
            
            # Generate recommendations
            recommendations = self._generate_skill_recommendations(skills_lower, experience_level)
            
            analysis_result = {
                'skill_categories': category_analysis,
                'experience_level': experience_level,
                'skill_gaps': skill_gaps,
                'recommendations': recommendations,
                'total_skills': len(skills),
                'analysis_timestamp': datetime.now().isoformat()
            }
            
            logger.info("✅ AI skill analysis completed")
            return analysis_result
            
        except Exception as e:
            logger.error(f"❌ AI skill analysis error: {e}")
            return self._get_empty_skill_analysis()
    
    def project_salary(self, experience_years: int, skills: List[str]) -> Dict[str, Any]:
        """AI-powered salary projection"""
        try:
            logger.info("💰 Starting AI salary projection...")
            
            # Base salary range
            base_range = self.salary_ranges.get(min(experience_years, 10), self.salary_ranges[10])
            
            # Skill-based adjustments
            skill_multiplier = self._calculate_skill_multiplier(skills)
            
            # Experience-based adjustments
            experience_multiplier = self._calculate_experience_multiplier(experience_years)
            
            # Calculate projected salary
            base_min = base_range['min']
            base_max = base_range['max']
            
            projected_min = int(base_min * skill_multiplier * experience_multiplier)
            projected_max = int(base_max * skill_multiplier * experience_multiplier)
            
            # Market trends
            market_trends = self._analyze_market_trends(skills)
            
            projection_result = {
                'current_range': {
                    'min': projected_min,
                    'max': projected_max,
                    'currency': base_range['currency']
                },
                'next_year_projection': {
                    'min': int(projected_min * 1.1),
                    'max': int(projected_max * 1.1),
                    'currency': base_range['currency']
                },
                'skill_multiplier': skill_multiplier,
                'experience_multiplier': experience_multiplier,
                'market_trends': market_trends,
                'confidence': 0.8,
                'analysis_timestamp': datetime.now().isoformat()
            }
            
            logger.info("✅ AI salary projection completed")
            return projection_result
            
        except Exception as e:
            logger.error(f"❌ AI salary projection error: {e}")
            return self._get_empty_salary_projection()
    
    def suggest_career_path(self, role: str, experience_years: int) -> Dict[str, Any]:
        """AI-powered career path suggestion"""
        try:
            logger.info("🎯 Starting AI career path analysis...")
            
            # Determine current level
            current_level = self._determine_current_level(role, experience_years)
            
            # Get career path
            career_path = self.career_paths.get(current_level, self.career_paths['developer'])
            
            # Generate personalized path
            personalized_path = self._generate_personalized_path(role, experience_years, current_level)
            
            # Next steps
            next_steps = self._generate_next_steps(role, experience_years, current_level)
            
            # Timeline
            timeline = self._generate_timeline(role, experience_years, current_level)
            
            path_result = {
                'current_level': current_level,
                'career_path': career_path,
                'personalized_path': personalized_path,
                'next_steps': next_steps,
                'timeline': timeline,
                'confidence': 0.85,
                'analysis_timestamp': datetime.now().isoformat()
            }
            
            logger.info("✅ AI career path analysis completed")
            return path_result
            
        except Exception as e:
            logger.error(f"❌ AI career path analysis error: {e}")
            return self._get_empty_career_path()
    
    def analyze_location_growth(self, location: str, skills: List[str]) -> Dict[str, Any]:
        """AI-powered location growth analysis"""
        try:
            logger.info("📍 Starting AI location growth analysis...")
            
            # Location-based opportunities
            location_opportunities = self._analyze_location_opportunities(location)
            
            # Skill demand by location
            skill_demand = self._analyze_skill_demand_by_location(location, skills)
            
            # Growth projections
            growth_projections = self._analyze_growth_projections(location)
            
            # Recommendations
            recommendations = self._generate_location_recommendations(location, skills)
            
            growth_result = {
                'location': location,
                'opportunities': location_opportunities,
                'skill_demand': skill_demand,
                'growth_projections': growth_projections,
                'recommendations': recommendations,
                'confidence': 0.75,
                'analysis_timestamp': datetime.now().isoformat()
            }
            
            logger.info("✅ AI location growth analysis completed")
            return growth_result
            
        except Exception as e:
            logger.error(f"❌ AI location growth analysis error: {e}")
            return self._get_empty_location_growth()
    
    def _determine_experience_level(self, skills: List[str]) -> str:
        """Determine experience level based on skills"""
        try:
            # Count advanced skills
            advanced_skills = ['architecture', 'design', 'lead', 'senior', 'principal', 'manager']
            advanced_count = sum(1 for skill in skills if any(adv in skill for adv in advanced_skills))
            
            # Count total skills
            total_skills = len(skills)
            
            if total_skills < 5:
                return 'entry'
            elif total_skills < 10 or advanced_count < 2:
                return 'mid'
            elif total_skills < 15 or advanced_count < 4:
                return 'senior'
            else:
                return 'lead'
                
        except Exception as e:
            logger.error(f"❌ Experience level determination error: {e}")
            return 'mid'
    
    def _identify_skill_gaps(self, skills: List[str], experience_level: str) -> List[str]:
        """Identify skill gaps based on experience level"""
        try:
            gaps = self.skill_gaps.get(experience_level, self.skill_gaps['mid'])
            
            # Filter out skills already present
            missing_gaps = []
            for gap in gaps:
                if not any(gap.lower() in skill for skill in skills):
                    missing_gaps.append(gap)
            
            return missing_gaps[:5]  # Return top 5 gaps
            
        except Exception as e:
            logger.error(f"❌ Skill gap identification error: {e}")
            return []
    
    def _generate_skill_recommendations(self, skills: List[str], experience_level: str) -> List[str]:
        """Generate skill recommendations"""
        try:
            recommendations = []
            
            # Based on experience level
            if experience_level == 'entry':
                recommendations.extend([
                    'Focus on core programming fundamentals',
                    'Learn version control (Git)',
                    'Practice problem-solving on coding platforms',
                    'Build small projects to showcase skills'
                ])
            elif experience_level == 'mid':
                recommendations.extend([
                    'Learn system design principles',
                    'Improve testing and debugging skills',
                    'Explore cloud platforms (AWS/Azure)',
                    'Contribute to open source projects'
                ])
            elif experience_level == 'senior':
                recommendations.extend([
                    'Develop leadership and mentoring skills',
                    'Learn advanced architecture patterns',
                    'Focus on scalability and performance',
                    'Build cross-functional collaboration'
                ])
            else:  # lead
                recommendations.extend([
                    'Develop strategic thinking',
                    'Focus on innovation and vision',
                    'Build strong communication skills',
                    'Learn business and product management'
                ])
            
            return recommendations[:4]  # Return top 4 recommendations
            
        except Exception as e:
            logger.error(f"❌ Skill recommendation generation error: {e}")
            return ['Focus on continuous learning and skill development']
    
    def _calculate_skill_multiplier(self, skills: List[str]) -> float:
        """Calculate skill-based salary multiplier"""
        try:
            if not skills:
                return 1.0
            
            # High-demand skills
            high_demand = ['aws', 'kubernetes', 'docker', 'react', 'python', 'java', 'spring']
            high_demand_count = sum(1 for skill in skills if skill.lower() in high_demand)
            
            # Advanced skills
            advanced = ['architecture', 'design', 'lead', 'senior', 'principal', 'manager']
            advanced_count = sum(1 for skill in skills if any(adv in skill.lower() for adv in advanced))
            
            # Calculate multiplier
            multiplier = 1.0 + (high_demand_count * 0.1) + (advanced_count * 0.05)
            
            return min(multiplier, 1.5)  # Cap at 1.5x
            
        except Exception as e:
            logger.error(f"❌ Skill multiplier calculation error: {e}")
            return 1.0
    
    def _calculate_experience_multiplier(self, experience_years: int) -> float:
        """Calculate experience-based salary multiplier"""
        try:
            if experience_years <= 0:
                return 1.0
            elif experience_years <= 2:
                return 1.0
            elif experience_years <= 5:
                return 1.1
            elif experience_years <= 10:
                return 1.2
            else:
                return 1.3
                
        except Exception as e:
            logger.error(f"❌ Experience multiplier calculation error: {e}")
            return 1.0
    
    def _analyze_market_trends(self, skills: List[str]) -> Dict[str, Any]:
        """Analyze market trends for skills"""
        try:
            trends = {
                'hot_skills': ['AI/ML', 'Cloud Computing', 'DevOps', 'React', 'Python'],
                'growing_demand': ['Kubernetes', 'Docker', 'AWS', 'Data Science', 'Cybersecurity'],
                'stable_skills': ['Java', 'SQL', 'JavaScript', 'Git', 'Testing'],
                'declining_skills': ['Flash', 'Silverlight', 'VB.NET', 'Perl', 'COBOL']
            }
            
            # Match user skills with trends
            user_hot_skills = [skill for skill in skills if skill.lower() in [s.lower() for s in trends['hot_skills']]]
            user_growing_skills = [skill for skill in skills if skill.lower() in [s.lower() for s in trends['growing_demand']]]
            
            return {
                'trends': trends,
                'user_hot_skills': user_hot_skills,
                'user_growing_skills': user_growing_skills,
                'market_score': len(user_hot_skills) + len(user_growing_skills)
            }
            
        except Exception as e:
            logger.error(f"❌ Market trends analysis error: {e}")
            return {'trends': {}, 'user_hot_skills': [], 'user_growing_skills': [], 'market_score': 0}
    
    def _determine_current_level(self, role: str, experience_years: int) -> str:
        """Determine current career level"""
        try:
            role_lower = role.lower()
            
            if 'intern' in role_lower or 'trainee' in role_lower:
                return 'developer'
            elif 'junior' in role_lower or experience_years <= 2:
                return 'developer'
            elif 'senior' in role_lower or experience_years <= 5:
                return 'senior_developer'
            elif 'lead' in role_lower or experience_years <= 8:
                return 'tech_lead'
            elif 'manager' in role_lower or experience_years > 8:
                return 'manager'
            else:
                return 'developer'
                
        except Exception as e:
            logger.error(f"❌ Current level determination error: {e}")
            return 'developer'
    
    def _generate_personalized_path(self, role: str, experience_years: int, current_level: str) -> Dict[str, Any]:
        """Generate personalized career path"""
        try:
            personalized = {
                'immediate_next': f"Focus on {current_level} skills development",
                'short_term': f"Target {self.career_paths[current_level]['next_level']} role",
                'medium_term': f"Develop leadership and strategic thinking",
                'long_term': f"Progress to senior management or technical leadership"
            }
            
            return personalized
            
        except Exception as e:
            logger.error(f"❌ Personalized path generation error: {e}")
            return {'immediate_next': 'Focus on skill development', 'short_term': 'Career growth', 'medium_term': 'Leadership', 'long_term': 'Senior role'}
    
    def _generate_next_steps(self, role: str, experience_years: int, current_level: str) -> List[str]:
        """Generate next steps for career growth"""
        try:
            steps = [
                f"Enhance {current_level} skills",
                "Build a strong portfolio",
                "Network with industry professionals",
                "Seek mentorship opportunities",
                "Take on challenging projects"
            ]
            
            return steps
            
        except Exception as e:
            logger.error(f"❌ Next steps generation error: {e}")
            return ['Focus on skill development', 'Build portfolio', 'Network', 'Seek mentorship']
    
    def _generate_timeline(self, role: str, experience_years: int, current_level: str) -> Dict[str, str]:
        """Generate career growth timeline"""
        try:
            timeline = {
                'next_6_months': 'Skill enhancement and project experience',
                'next_1_year': f'Progress to {self.career_paths[current_level]["next_level"]}',
                'next_2_years': 'Develop leadership capabilities',
                'next_5_years': 'Senior management or technical leadership role'
            }
            
            return timeline
            
        except Exception as e:
            logger.error(f"❌ Timeline generation error: {e}")
            return {'next_6_months': 'Skill development', 'next_1_year': 'Career growth', 'next_2_years': 'Leadership', 'next_5_years': 'Senior role'}
    
    def _analyze_location_opportunities(self, location: str) -> Dict[str, Any]:
        """Analyze opportunities by location"""
        try:
            # Mock location analysis
            opportunities = {
                'tech_hubs': ['Bangalore', 'Mumbai', 'Delhi', 'Hyderabad', 'Pune'],
                'startup_ecosystem': ['Bangalore', 'Mumbai', 'Delhi', 'Chennai'],
                'enterprise_companies': ['Mumbai', 'Delhi', 'Bangalore', 'Hyderabad'],
                'remote_opportunities': 'High demand for remote work'
            }
            
            location_lower = location.lower()
            is_tech_hub = any(hub.lower() in location_lower for hub in opportunities['tech_hubs'])
            is_startup_hub = any(hub.lower() in location_lower for hub in opportunities['startup_ecosystem'])
            
            return {
                'is_tech_hub': is_tech_hub,
                'is_startup_hub': is_startup_hub,
                'opportunity_score': 8 if is_tech_hub else 6,
                'remote_friendly': True,
                'growth_potential': 'High' if is_tech_hub else 'Medium'
            }
            
        except Exception as e:
            logger.error(f"❌ Location opportunities analysis error: {e}")
            return {'is_tech_hub': False, 'is_startup_hub': False, 'opportunity_score': 5, 'remote_friendly': True, 'growth_potential': 'Medium'}
    
    def _analyze_skill_demand_by_location(self, location: str, skills: List[str]) -> Dict[str, Any]:
        """Analyze skill demand by location"""
        try:
            # Mock skill demand analysis
            demand_analysis = {
                'high_demand_skills': ['Python', 'Java', 'React', 'AWS', 'Docker'],
                'medium_demand_skills': ['Angular', 'Node.js', 'MongoDB', 'Kubernetes'],
                'emerging_skills': ['AI/ML', 'Blockchain', 'IoT', 'AR/VR'],
                'location_specific': {
                    'bangalore': ['Startup ecosystem', 'Fintech', 'E-commerce'],
                    'mumbai': ['Banking', 'Finance', 'Media'],
                    'delhi': ['Government', 'Consulting', 'Education'],
                    'hyderabad': ['Healthcare', 'Pharma', 'Manufacturing']
                }
            }
            
            location_lower = location.lower()
            location_specific = demand_analysis['location_specific'].get(location_lower, ['General tech'])
            
            return {
                'demand_analysis': demand_analysis,
                'location_specific': location_specific,
                'skill_match_score': len([s for s in skills if s.lower() in [d.lower() for d in demand_analysis['high_demand_skills']]])
            }
            
        except Exception as e:
            logger.error(f"❌ Skill demand analysis error: {e}")
            return {'demand_analysis': {}, 'location_specific': [], 'skill_match_score': 0}
    
    def _analyze_growth_projections(self, location: str) -> Dict[str, Any]:
        """Analyze growth projections for location"""
        try:
            projections = {
                'tech_growth': '15-20% annually',
                'job_market': 'Growing',
                'salary_growth': '10-15% annually',
                'startup_ecosystem': 'Thriving',
                'remote_work': 'Increasing adoption'
            }
            
            return projections
            
        except Exception as e:
            logger.error(f"❌ Growth projections analysis error: {e}")
            return {'tech_growth': '10% annually', 'job_market': 'Stable', 'salary_growth': '8% annually', 'startup_ecosystem': 'Growing', 'remote_work': 'Moderate'}
    
    def _generate_location_recommendations(self, location: str, skills: List[str]) -> List[str]:
        """Generate location-based recommendations"""
        try:
            recommendations = [
                'Explore local tech meetups and networking events',
                'Connect with local startups and companies',
                'Consider remote work opportunities',
                'Build a strong online presence',
                'Stay updated with local tech trends'
            ]
            
            return recommendations
            
        except Exception as e:
            logger.error(f"❌ Location recommendations generation error: {e}")
            return ['Focus on skill development', 'Network locally', 'Explore opportunities']
    
    def _get_empty_skill_analysis(self) -> Dict[str, Any]:
        """Return empty skill analysis"""
        return {
            'skill_categories': {},
            'experience_level': 'entry',
            'skill_gaps': [],
            'recommendations': ['Focus on skill development'],
            'total_skills': 0,
            'analysis_timestamp': datetime.now().isoformat()
        }
    
    def _get_empty_salary_projection(self) -> Dict[str, Any]:
        """Return empty salary projection"""
        return {
            'current_range': {'min': 300000, 'max': 600000, 'currency': 'INR'},
            'next_year_projection': {'min': 330000, 'max': 660000, 'currency': 'INR'},
            'skill_multiplier': 1.0,
            'experience_multiplier': 1.0,
            'market_trends': {},
            'confidence': 0.5,
            'analysis_timestamp': datetime.now().isoformat()
        }
    
    def _get_empty_career_path(self) -> Dict[str, Any]:
        """Return empty career path"""
        return {
            'current_level': 'developer',
            'career_path': {'junior': 'Junior Developer → Mid Developer → Senior Developer'},
            'personalized_path': {'immediate_next': 'Focus on skill development'},
            'next_steps': ['Skill development', 'Portfolio building'],
            'timeline': {'next_6_months': 'Skill enhancement'},
            'confidence': 0.5,
            'analysis_timestamp': datetime.now().isoformat()
        }
    
    def _get_empty_location_growth(self) -> Dict[str, Any]:
        """Return empty location growth"""
        return {
            'location': 'Unknown',
            'opportunities': {},
            'skill_demand': {},
            'growth_projections': {},
            'recommendations': ['Focus on skill development'],
            'confidence': 0.5,
            'analysis_timestamp': datetime.now().isoformat()
        }

# Initialize global AI career analyzer
ai_career_analyzer = AICareerAnalyzer()
