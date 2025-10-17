"""
AI Experience Analyzer
Dynamic AI-powered experience extraction and analysis
"""

import re
import logging
from datetime import datetime, date
from typing import Dict, List, Any, Tuple
import math
from dynamic_experience_calculator import dynamic_experience_calculator

logger = logging.getLogger(__name__)

class AIExperienceAnalyzer:
    """AI-powered experience analyzer with dynamic learning"""
    
    def __init__(self):
        # Dynamic experience patterns that adapt to content
        self.experience_keywords = {
            'explicit': ['experience', 'exp', 'years', 'yrs', 'work', 'professional', 'career'],
            'time': ['since', 'from', 'started', 'began', 'joined', 'employed', 'working'],
            'duration': ['duration', 'period', 'timeline', 'span', 'length', 'term'],
            'position': ['developer', 'engineer', 'analyst', 'manager', 'consultant', 'specialist'],
            'level': ['junior', 'senior', 'lead', 'principal', 'staff', 'architect', 'director'],
            'achievement': ['led', 'managed', 'directed', 'supervised', 'mentored', 'trained'],
            'project': ['project', 'developed', 'built', 'created', 'designed', 'implemented'],
            'education': ['graduated', 'completed', 'finished', 'degree', 'bachelor', 'master']
        }
        
        # Dynamic skill progression indicators
        self.skill_progression = {
            'beginner': ['learning', 'introduction', 'basics', 'fundamentals', 'getting started'],
            'intermediate': ['working with', 'familiar with', 'comfortable', 'proficient'],
            'advanced': ['expert', 'master', 'specialist', 'deep knowledge', 'extensive'],
            'senior': ['senior', 'lead', 'principal', 'architect', 'mentor', 'trainer']
        }
        
        # Dynamic project complexity indicators
        self.project_complexity = {
            'simple': ['basic', 'simple', 'small', 'individual', 'personal'],
            'medium': ['medium', 'moderate', 'team', 'collaborative', 'standard'],
            'complex': ['complex', 'large', 'enterprise', 'scalable', 'distributed'],
            'advanced': ['advanced', 'sophisticated', 'cutting-edge', 'innovative', 'breakthrough']
        }
    
    def analyze_experience(self, text: str) -> Dict[str, Any]:
        """AI-powered experience analysis using dynamic calculation"""
        try:
            logger.info("🤖 Starting AI-powered experience analysis...")
            
            if not text or len(text.strip()) < 10:
                return self._get_empty_result()
            
            # Use dynamic experience calculator for accurate date-based calculation
            experience_result = dynamic_experience_calculator.calculate_experience(text)
            
            logger.info(f"✅ AI experience analysis completed: {experience_result['total_years']} years {experience_result['total_months']} months")
            return experience_result
            
        except Exception as e:
            logger.error(f"❌ AI experience analysis error: {e}")
            return self._get_empty_result()
    
    def _analyze_explicit_experience(self, text: str, text_lower: str) -> Dict[str, Any]:
        """Analyze explicit experience mentions"""
        try:
            patterns = [
                r'(\d+)\s*(?:to|-)?\s*(\d+)?\s*(?:years?|yrs?)\s*(?:of\s*)?(?:experience|exp)',
                r'(?:experience|exp)[:\s]*(\d+)\s*(?:to|-)?\s*(\d+)?\s*(?:years?|yrs?)',
                r'(\d+)\+?\s*(?:years?|yrs?)\s*(?:of\s*)?(?:experience|exp)',
                r'(?:total|overall)\s*(?:experience|exp)[:\s]*(\d+)\s*(?:years?|yrs?)',
                r'(\d+)\s*(?:to|-)?\s*(\d+)?\s*(?:years?|yrs?)\s*(?:of\s*)?(?:work|professional)',
                r'(?:work|professional)\s*(?:experience|exp)[:\s]*(\d+)\s*(?:to|-)?\s*(\d+)?\s*(?:years?|yrs?)',
                r'(?:over|more\s+than)\s+(\d+)\s*(?:years?|yrs?)',
                r'(\d+)\s*(?:years?|yrs?)\s*(?:plus|and\s+above)',
                r'(?:around|approximately|about)\s+(\d+)\s*(?:years?|yrs?)'
            ]
            
            for pattern in patterns:
                matches = re.findall(pattern, text_lower)
                for match in matches:
                    if isinstance(match, tuple):
                        years = int(match[0]) if match[0] else 0
                        if match[1]:
                            years = max(years, int(match[1]))
                    else:
                        years = int(match)
                    
                    if 0 < years <= 30:
                        return {
                            'years': years,
                            'confidence': 0.95,
                            'method': 'explicit_statement',
                            'evidence': f"Found explicit mention: {years} years"
                        }
            
            return {'years': 0, 'confidence': 0.0, 'method': 'none', 'evidence': 'No explicit experience found'}
            
        except Exception as e:
            logger.error(f"❌ Explicit analysis error: {e}")
            return {'years': 0, 'confidence': 0.0, 'method': 'error', 'evidence': str(e)}
    
    def _analyze_temporal_patterns(self, text: str, text_lower: str) -> Dict[str, Any]:
        """Analyze temporal patterns and dates"""
        try:
            # Date patterns
            date_patterns = [
                r'(\d{4})\s*(?:to|-)?\s*(?:present|current|now|\d{4})',
                r'(?:since|from)\s+(\d{4})',
                r'(?:started|began)\s+(?:in\s+)?(\d{4})',
                r'(?:joined|employed)\s+(?:in\s+)?(\d{4})',
                r'(?:working\s+since|employed\s+since)\s+(\d{4})',
                r'(?:career\s+started|professional\s+journey)\s+(\d{4})',
                r'(?:first\s+job|first\s+position)\s+(\d{4})',
                r'(?:entry\s+into\s+industry)\s+(\d{4})'
            ]
            
            dates = []
            for pattern in date_patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                for match in matches:
                    if isinstance(match, tuple):
                        dates.append(match[0])
                    else:
                        dates.append(match)
            
            if len(dates) >= 2:
                try:
                    years = []
                    for date_str in dates:
                        if len(date_str) == 4:  # Year only
                            years.append(int(date_str))
                    
                    if years:
                        current_year = datetime.now().year
                        if len(years) == 1:
                            years.append(current_year)
                        experience = max(years) - min(years)
                        if 0 < experience <= 30:
                            return {
                                'years': experience,
                                'confidence': 0.9,
                                'method': 'date_calculation',
                                'evidence': f"Calculated from dates: {min(years)} to {max(years)}"
                            }
                except:
                    pass
            
            return {'years': 0, 'confidence': 0.0, 'method': 'none', 'evidence': 'No temporal patterns found'}
            
        except Exception as e:
            logger.error(f"❌ Temporal analysis error: {e}")
            return {'years': 0, 'confidence': 0.0, 'method': 'error', 'evidence': str(e)}
    
    def _analyze_position_progression(self, text: str, text_lower: str) -> Dict[str, Any]:
        """Analyze position progression and career growth"""
        try:
            positions = []
            position_patterns = [
                r'(?:software\s+developer|engineer|analyst|manager|consultant|specialist|architect)',
                r'(?:junior|senior|lead|principal|staff)\s+(?:developer|engineer|analyst|manager)',
                r'(?:team\s+lead|project\s+manager|technical\s+lead)',
                r'(?:engineering\s+manager|development\s+manager)',
                r'(?:tech\s+lead|technical\s+architect)',
                r'(?:intern|internship|trainee|associate)',
                r'(?:freelancer|freelance|contractor|consultant)'
            ]
            
            for pattern in position_patterns:
                matches = re.findall(pattern, text_lower)
                positions.extend(matches)
            
            if positions:
                # AI-based position analysis
                position_scores = []
                for pos in positions:
                    pos_lower = pos.lower()
                    if 'intern' in pos_lower or 'trainee' in pos_lower:
                        position_scores.append(0.5)
                    elif 'junior' in pos_lower or 'associate' in pos_lower:
                        position_scores.append(1.5)
                    elif 'developer' in pos_lower or 'engineer' in pos_lower:
                        position_scores.append(2.5)
                    elif 'senior' in pos_lower:
                        position_scores.append(4.0)
                    elif 'lead' in pos_lower or 'manager' in pos_lower:
                        position_scores.append(6.0)
                    elif 'principal' in pos_lower or 'architect' in pos_lower:
                        position_scores.append(8.0)
                    elif 'director' in pos_lower:
                        position_scores.append(12.0)
                    else:
                        position_scores.append(2.0)
                
                avg_experience = sum(position_scores) / len(position_scores)
                return {
                    'years': int(avg_experience),
                    'confidence': 0.7,
                    'method': 'position_analysis',
                    'evidence': f"Analyzed {len(positions)} positions"
                }
            
            return {'years': 0, 'confidence': 0.0, 'method': 'none', 'evidence': 'No positions found'}
            
        except Exception as e:
            logger.error(f"❌ Position analysis error: {e}")
            return {'years': 0, 'confidence': 0.0, 'method': 'error', 'evidence': str(e)}
    
    def _analyze_skill_evolution(self, text: str, text_lower: str) -> Dict[str, Any]:
        """Analyze skill evolution and proficiency levels"""
        try:
            skill_indicators = {
                'beginner': 0,
                'intermediate': 0,
                'advanced': 0,
                'expert': 0
            }
            
            for level, keywords in self.skill_progression.items():
                for keyword in keywords:
                    skill_indicators[level] += text_lower.count(keyword)
            
            # Calculate experience based on skill progression
            if sum(skill_indicators.values()) > 0:
                weighted_score = (
                    skill_indicators['beginner'] * 1 +
                    skill_indicators['intermediate'] * 3 +
                    skill_indicators['advanced'] * 6 +
                    skill_indicators['expert'] * 8
                )
                total_indicators = sum(skill_indicators.values())
                avg_experience = weighted_score / total_indicators
                
                return {
                    'years': int(avg_experience),
                    'confidence': 0.6,
                    'method': 'skill_evolution',
                    'evidence': f"Skill indicators: {skill_indicators}"
                }
            
            return {'years': 0, 'confidence': 0.0, 'method': 'none', 'evidence': 'No skill indicators found'}
            
        except Exception as e:
            logger.error(f"❌ Skill analysis error: {e}")
            return {'years': 0, 'confidence': 0.0, 'method': 'error', 'evidence': str(e)}
    
    def _analyze_project_complexity(self, text: str, text_lower: str) -> Dict[str, Any]:
        """Analyze project complexity and scope"""
        try:
            project_indicators = {
                'simple': 0,
                'medium': 0,
                'complex': 0,
                'advanced': 0
            }
            
            for complexity, keywords in self.project_complexity.items():
                for keyword in keywords:
                    project_indicators[complexity] += text_lower.count(keyword)
            
            # Calculate experience based on project complexity
            if sum(project_indicators.values()) > 0:
                weighted_score = (
                    project_indicators['simple'] * 1 +
                    project_indicators['medium'] * 3 +
                    project_indicators['complex'] * 6 +
                    project_indicators['advanced'] * 8
                )
                total_projects = sum(project_indicators.values())
                avg_experience = weighted_score / total_projects
                
                return {
                    'years': int(avg_experience),
                    'confidence': 0.5,
                    'method': 'project_complexity',
                    'evidence': f"Project indicators: {project_indicators}"
                }
            
            return {'years': 0, 'confidence': 0.0, 'method': 'none', 'evidence': 'No project indicators found'}
            
        except Exception as e:
            logger.error(f"❌ Project analysis error: {e}")
            return {'years': 0, 'confidence': 0.0, 'method': 'error', 'evidence': str(e)}
    
    def _analyze_achievement_patterns(self, text: str, text_lower: str) -> Dict[str, Any]:
        """Analyze achievement patterns and leadership indicators"""
        try:
            achievement_patterns = [
                r'(?:led|managed|directed|supervised)\s+(\d+)\s*(?:team|people|members)',
                r'(?:mentored|guided|trained)\s+(\d+)\s*(?:junior|developers|engineers)',
                r'(?:team\s+size|team\s+of)\s+(\d+)\s*(?:members|people)',
                r'(?:project\s+team|development\s+team)\s+(\d+)\s*(?:members|people)',
                r'(?:award|recognition|achievement|accomplishment)',
                r'(?:successfully|effectively)\s+(?:managed|led|directed)',
                r'(?:years?\s+of\s+)?(?:leadership|management|supervision)',
                r'(?:promoted|elevated|advanced)\s+(?:to|as)\s+([A-Za-z\s]+)',
                r'(?:performance\s+rating|appraisal)\s+([A-Za-z\s]+)',
                r'(?:exceeded|surpassed|outperformed)\s+(?:expectations|targets|goals)'
            ]
            
            achievements = 0
            team_sizes = []
            
            for pattern in achievement_patterns:
                matches = re.findall(pattern, text_lower)
                achievements += len(matches)
                
                # Extract team sizes
                for match in matches:
                    if isinstance(match, tuple):
                        try:
                            team_size = int(match[0])
                            team_sizes.append(team_size)
                        except:
                            pass
                    else:
                        try:
                            team_size = int(match)
                            team_sizes.append(team_size)
                        except:
                            pass
            
            if achievements > 0:
                # Calculate experience based on achievements
                base_experience = achievements * 1.5
                if team_sizes:
                    avg_team_size = sum(team_sizes) / len(team_sizes)
                    team_bonus = min(avg_team_size * 0.5, 5)
                    base_experience += team_bonus
                
                return {
                    'years': min(int(base_experience), 15),
                    'confidence': 0.5,
                    'method': 'achievement_analysis',
                    'evidence': f"Found {achievements} achievements, avg team size: {sum(team_sizes)/len(team_sizes) if team_sizes else 0}"
                }
            
            return {'years': 0, 'confidence': 0.0, 'method': 'none', 'evidence': 'No achievements found'}
            
        except Exception as e:
            logger.error(f"❌ Achievement analysis error: {e}")
            return {'years': 0, 'confidence': 0.0, 'method': 'error', 'evidence': str(e)}
    
    def _analyze_education_timeline(self, text: str, text_lower: str) -> Dict[str, Any]:
        """Analyze education timeline and graduation year"""
        try:
            education_patterns = [
                r'(?:graduated|completed|finished)\s+(?:in\s+)?(\d{4})',
                r'(?:bachelor|master|phd|diploma|degree)\s+(?:in\s+)?\d{4}',
                r'(\d{4})\s*(?:batch|graduation|passout)',
                r'(?:class\s+of|batch\s+of)\s+(\d{4})',
                r'(?:b\.tech|m\.tech|b\.e|m\.e|b\.sc|m\.sc)\s+(\d{4})',
                r'(?:engineering|computer\s+science)\s+(\d{4})',
                r'(?:university|college)\s+(\d{4})',
                r'(?:institute|institution)\s+(\d{4})'
            ]
            
            graduation_years = []
            for pattern in education_patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                for match in matches:
                    if isinstance(match, tuple):
                        graduation_years.append(match[0])
                    else:
                        graduation_years.append(match)
            
            if graduation_years:
                try:
                    grad_year = int(graduation_years[0])
                    current_year = datetime.now().year
                    experience = current_year - grad_year
                    if 0 < experience <= 30:
                        return {
                            'years': experience,
                            'confidence': 0.8,
                            'method': 'education_timeline',
                            'evidence': f"Graduated in {grad_year}"
                        }
                except:
                    pass
            
            return {'years': 0, 'confidence': 0.0, 'method': 'none', 'evidence': 'No education timeline found'}
            
        except Exception as e:
            logger.error(f"❌ Education analysis error: {e}")
            return {'years': 0, 'confidence': 0.0, 'method': 'error', 'evidence': str(e)}
    
    def _analyze_contextual_indicators(self, text: str, text_lower: str) -> Dict[str, Any]:
        """Analyze contextual indicators and overall content"""
        try:
            # Count various indicators
            indicators = {
                'years_mentioned': len(re.findall(r'\d+\s*(?:years?|yrs?)', text_lower)),
                'positions': len(re.findall(r'(?:developer|engineer|analyst|manager)', text_lower)),
                'projects': len(re.findall(r'(?:project|developed|built|created)', text_lower)),
                'technologies': len(re.findall(r'(?:java|python|javascript|react|angular|spring|aws|docker)', text_lower)),
                'achievements': len(re.findall(r'(?:award|recognition|achievement|led|managed)', text_lower)),
                'companies': len(re.findall(r'(?:company|corporation|inc|ltd|pvt)', text_lower)),
                'certifications': len(re.findall(r'(?:certified|certification|certificate)', text_lower)),
                'publications': len(re.findall(r'(?:published|paper|article|blog)', text_lower))
            }
            
            # AI-based scoring
            total_score = 0
            total_weight = 0
            
            # Weighted scoring based on indicators
            weights = {
                'years_mentioned': 3.0,
                'positions': 2.0,
                'projects': 1.5,
                'technologies': 1.0,
                'achievements': 2.0,
                'companies': 1.5,
                'certifications': 1.0,
                'publications': 1.5
            }
            
            for indicator, count in indicators.items():
                if count > 0:
                    total_score += count * weights[indicator]
                    total_weight += weights[indicator]
            
            if total_weight > 0:
                avg_experience = total_score / total_weight
                return {
                    'years': min(int(avg_experience), 20),
                    'confidence': 0.4,
                    'method': 'contextual_analysis',
                    'evidence': f"Contextual indicators: {indicators}"
                }
            
            return {'years': 0, 'confidence': 0.0, 'method': 'none', 'evidence': 'No contextual indicators found'}
            
        except Exception as e:
            logger.error(f"❌ Contextual analysis error: {e}")
            return {'years': 0, 'confidence': 0.0, 'method': 'error', 'evidence': str(e)}
    
    def _ai_decision_engine(self, analysis_results: Dict[str, Any]) -> Dict[str, Any]:
        """AI decision engine to determine final experience"""
        try:
            # Collect all valid results
            valid_results = []
            for method, result in analysis_results.items():
                if result['years'] > 0 and result['confidence'] > 0:
                    valid_results.append(result)
            
            if not valid_results:
                return self._get_empty_result()
            
            # AI-weighted decision making
            if len(valid_results) == 1:
                final_result = valid_results[0]
            else:
                # Weighted average based on confidence
                total_weighted_years = 0
                total_confidence = 0
                
                for result in valid_results:
                    weight = result['confidence']
                    total_weighted_years += result['years'] * weight
                    total_confidence += weight
                
                if total_confidence > 0:
                    final_years = total_weighted_years / total_confidence
                    final_result = {
                        'years': int(final_years),
                        'confidence': min(total_confidence / len(valid_results), 1.0),
                        'method': 'ai_weighted_average',
                        'evidence': f"Combined {len(valid_results)} analysis methods"
                    }
                else:
                    final_result = valid_results[0]
            
            # Final validation and adjustment
            final_years = final_result['years']
            if final_years < 0:
                final_years = 0
            elif final_years > 30:
                final_years = 30
            
            return {
                'total_years': final_years,
                'total_months': final_years * 12,
                'display': f"{final_years} years" if final_years > 0 else "Experience not found",
                'extraction_method': final_result['method'],
                'confidence': final_result['confidence'],
                'ai_analysis': {
                    'methods_used': len(valid_results),
                    'confidence_score': final_result['confidence'],
                    'evidence': final_result['evidence'],
                    'analysis_timestamp': datetime.now().isoformat()
                }
            }
            
        except Exception as e:
            logger.error(f"❌ AI decision engine error: {e}")
            return self._get_empty_result()
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text.strip())
        
        # Remove special characters but keep basic punctuation
        text = re.sub(r'[^\w\s@\.\-\+\(\)]', ' ', text)
        
        # Normalize line breaks
        text = re.sub(r'\n+', '\n', text)
        
        return text
    
    def _get_empty_result(self) -> Dict[str, Any]:
        """Return empty result"""
        return {
            'total_years': 0,
            'total_months': 0,
            'display': 'Experience not found',
            'extraction_method': 'not_found',
            'confidence': 0.0,
            'ai_analysis': {
                'methods_used': 0,
                'confidence_score': 0.0,
                'evidence': 'No content found',
                'analysis_timestamp': datetime.now().isoformat()
            }
        }

# Initialize global AI experience analyzer
ai_experience_analyzer = AIExperienceAnalyzer()
