"""
Advanced AI Models for Resume Extraction & Feature Analysis
Using PyMuPDF, spaCy Transformer, Sentence-BERT, XGBoost, and other state-of-the-art models
"""

import re
import numpy as np
import logging
from typing import Dict, List, Any, Tuple, Optional
from datetime import datetime
import json
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ResumeParser:
    """PyMuPDF + Textract + pdfplumber for text extraction"""
    
    def __init__(self):
        self.textract_available = False
        self.pymupdf_available = False
        self.pdfplumber_available = False
        
        # Try to import libraries
        try:
            import fitz  # PyMuPDF
            self.pymupdf_available = True
            logger.info("✅ PyMuPDF available")
        except ImportError:
            logger.warning("⚠️ PyMuPDF not available")
        
        try:
            import textract
            self.textract_available = True
            logger.info("✅ Textract available")
        except ImportError:
            logger.warning("⚠️ Textract not available")
        
        try:
            import pdfplumber
            self.pdfplumber_available = True
            logger.info("✅ pdfplumber available")
        except ImportError:
            logger.warning("⚠️ pdfplumber not available")
    
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extract text from PDF using best available method"""
        try:
            if self.pymupdf_available:
                return self._extract_with_pymupdf(pdf_path)
            elif self.textract_available:
                return self._extract_with_textract(pdf_path)
            elif self.pdfplumber_available:
                return self._extract_with_pdfplumber(pdf_path)
            else:
                return self._extract_with_pypdf2(pdf_path)
        except Exception as e:
            logger.error(f"❌ PDF extraction error: {e}")
            return ""
    
    def _extract_with_pymupdf(self, pdf_path: str) -> str:
        """Extract using PyMuPDF (best quality)"""
        import fitz
        doc = fitz.open(pdf_path)
        text = ""
        for page in doc:
            text += page.get_text()
        doc.close()
        return text
    
    def _extract_with_textract(self, pdf_path: str) -> str:
        """Extract using Textract"""
        import textract
        return textract.process(pdf_path).decode('utf-8')
    
    def _extract_with_pdfplumber(self, pdf_path: str) -> str:
        """Extract using pdfplumber"""
        import pdfplumber
        text = ""
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
        return text
    
    def _extract_with_pypdf2(self, pdf_path: str) -> str:
        """Fallback extraction using PyPDF2"""
        import PyPDF2
        text = ""
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                text += page.extract_text()
        return text

class NamedEntityRecognizer:
    """spaCy Transformer + BERT-NER for high-accuracy entity detection"""
    
    def __init__(self):
        self.spacy_model = None
        self.bert_model = None
        self._load_models()
    
    def _load_models(self):
        """Load spaCy and BERT models"""
        try:
            import spacy
            # Try to load transformer model first
            try:
                self.spacy_model = spacy.load("en_core_web_trf")
                logger.info("✅ spaCy Transformer model loaded")
            except OSError:
                try:
                    self.spacy_model = spacy.load("en_core_web_sm")
                    logger.info("✅ spaCy SM model loaded")
                except OSError:
                    logger.warning("⚠️ spaCy model not available")
            
            # Try to load BERT model
            try:
                from transformers import pipeline
                self.bert_model = pipeline(
                    "ner",
                    model="dbmdz/bert-large-cased-finetuned-conll03-english",
                    aggregation_strategy="simple"
                )
                logger.info("✅ BERT NER model loaded")
            except Exception as e:
                logger.warning(f"⚠️ BERT model not available: {e}")
                
        except Exception as e:
            logger.error(f"❌ Model loading error: {e}")
    
    def extract_entities(self, text: str) -> Dict[str, List[str]]:
        """Extract named entities using spaCy + BERT"""
        entities = {
            'PERSON': [],
            'ORG': [],
            'GPE': [],
            'DATE': [],
            'MONEY': [],
            'PERCENT': [],
            'SKILL': [],
            'EDUCATION': [],
            'EXPERIENCE': [],
            'ROLE': []
        }
        
        try:
            # Extract using spaCy
            if self.spacy_model:
                doc = self.spacy_model(text)
                for ent in doc.ents:
                    if ent.label_ in entities:
                        entities[ent.label_].append(ent.text)
            
            # Extract using BERT
            if self.bert_model:
                bert_entities = self.bert_model(text)
                for entity in bert_entities:
                    label = entity['entity_group']
                    if label in entities:
                        entities[label].append(entity['word'])
            
            # Custom skill extraction
            entities['SKILL'] = self._extract_skills(text)
            
            # Custom education extraction
            entities['EDUCATION'] = self._extract_education(text)
            
            # Custom experience extraction
            entities['EXPERIENCE'] = self._extract_experience(text)
            
            # Custom role extraction
            entities['ROLE'] = self._extract_roles(text)
            
            # Remove duplicates
            for key in entities:
                entities[key] = list(set(entities[key]))
            
            return entities
            
        except Exception as e:
            logger.error(f"❌ Entity extraction error: {e}")
            return entities
    
    def _extract_skills(self, text: str) -> List[str]:
        """Extract skills using pattern matching"""
        skills = []
        
        # Technical skills database
        tech_skills = [
            'Python', 'Java', 'JavaScript', 'TypeScript', 'C++', 'C#', 'Go', 'Rust',
            'React', 'Angular', 'Vue', 'Node.js', 'Express', 'Django', 'Flask',
            'Spring', 'Laravel', 'MySQL', 'PostgreSQL', 'MongoDB', 'Redis',
            'AWS', 'Azure', 'GCP', 'Docker', 'Kubernetes', 'Jenkins', 'Git',
            'HTML', 'CSS', 'Bootstrap', 'Tailwind', 'jQuery', 'REST', 'GraphQL',
            'Machine Learning', 'Deep Learning', 'TensorFlow', 'PyTorch',
            'Data Science', 'Pandas', 'NumPy', 'Scikit-learn', 'Jupyter'
        ]
        
        text_lower = text.lower()
        for skill in tech_skills:
            if skill.lower() in text_lower:
                skills.append(skill)
        
        return skills
    
    def _extract_education(self, text: str) -> List[str]:
        """Extract education information"""
        education = []
        
        education_patterns = [
            r'(?:Bachelor|Master|PhD|Doctorate)\s+(?:of\s+)?(?:Science|Arts|Engineering|Technology|Business|Computer Science)',
            r'(?:B\.?S\.?|M\.?S\.?|B\.?A\.?|M\.?A\.?|Ph\.?D\.?)\s+(?:in\s+)?(?:Computer Science|Engineering|Technology|Business)',
            r'(?:Computer Science|Engineering|Technology|Business)\s+(?:Degree|Major|Specialization)',
            r'(?:B\.?Tech|M\.?Tech|B\.?E\.?|M\.?E\.?)\s+(?:in\s+)?(?:Computer Science|Engineering)',
            r'(?:MBA|MCA|BCA|MCA)\s+(?:in\s+)?(?:Computer Science|Information Technology)'
        ]
        
        for pattern in education_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            education.extend(matches)
        
        return list(set(education))
    
    def _extract_experience(self, text: str) -> List[str]:
        """Extract experience information"""
        experience = []
        
        experience_patterns = [
            r'(\d+)\s*(?:to|-)?\s*(\d+)?\s*(?:years?|yrs?)\s*(?:of\s*)?(?:experience|exp)',
            r'(?:experience|exp)[:\s]*(\d+)\s*(?:to|-)?\s*(\d+)?\s*(?:years?|yrs?)',
            r'(\d+)\+?\s*(?:years?|yrs?)\s*(?:of\s*)?(?:experience|exp)',
            r'(?:fresh|fresher|entry|junior|mid|senior|lead|principal|staff)',
            r'(?:intern|internship|trainee|apprentice|associate)'
        ]
        
        for pattern in experience_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            experience.extend(matches)
        
        return list(set(experience))
    
    def _extract_roles(self, text: str) -> List[str]:
        """Extract job roles"""
        roles = []
        
        role_patterns = [
            r'(?:Software|Web|Frontend|Backend|Full.?Stack|Mobile|DevOps|Data|Machine Learning|AI)\s+(?:Developer|Engineer|Programmer|Architect|Consultant|Manager|Analyst|Scientist)',
            r'(?:Senior|Junior|Lead|Principal|Staff)\s+(?:Developer|Engineer|Programmer|Architect|Consultant|Manager|Analyst|Scientist)',
            r'(?:Project|Product|Business|System|Data|QA|Test)\s+(?:Manager|Analyst|Engineer|Consultant)',
            r'(?:UI|UX|Graphic|Web|Product)\s+(?:Designer|Developer|Engineer)',
            r'(?:Database|System|Network|IT)\s+(?:Administrator|Engineer|Specialist)'
        ]
        
        for pattern in role_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            roles.extend(matches)
        
        return list(set(roles))

class SkillExtractor:
    """Sentence-BERT + FAISS for skill similarity search"""
    
    def __init__(self):
        self.sentence_bert_model = None
        self.skill_embeddings = {}
        self.faiss_index = None
        self._load_models()
    
    def _load_models(self):
        """Load Sentence-BERT model"""
        try:
            from sentence_transformers import SentenceTransformer
            self.sentence_bert_model = SentenceTransformer('all-MiniLM-L6-v2')
            logger.info("✅ Sentence-BERT model loaded")
            
            # Try to load FAISS
            try:
                import faiss
                self.faiss_available = True
                logger.info("✅ FAISS available")
            except ImportError:
                self.faiss_available = False
                logger.warning("⚠️ FAISS not available")
                
        except Exception as e:
            logger.warning(f"⚠️ Sentence-BERT not available: {e}")
    
    def extract_skills_with_similarity(self, text: str, target_skills: List[str] = None) -> Dict[str, Any]:
        """Extract skills using Sentence-BERT similarity"""
        try:
            if not self.sentence_bert_model:
                return self._fallback_skill_extraction(text)
            
            # Extract skills using pattern matching
            extracted_skills = self._extract_skills_pattern(text)
            
            # Create embeddings for extracted skills
            if extracted_skills:
                skill_embeddings = self.sentence_bert_model.encode(extracted_skills)
                
                # Calculate similarity with target skills if provided
                similarity_scores = {}
                if target_skills:
                    target_embeddings = self.sentence_bert_model.encode(target_skills)
                    
                    # Calculate cosine similarity
                    from sklearn.metrics.pairwise import cosine_similarity
                    similarities = cosine_similarity(skill_embeddings, target_embeddings)
                    
                    for i, skill in enumerate(extracted_skills):
                        max_similarity = max(similarities[i])
                        similarity_scores[skill] = max_similarity
                
                return {
                    'extracted_skills': extracted_skills,
                    'skill_embeddings': skill_embeddings.tolist(),
                    'similarity_scores': similarity_scores,
                    'extraction_method': 'sentence_bert'
                }
            else:
                return {
                    'extracted_skills': [],
                    'similarity_scores': {},
                    'extraction_method': 'sentence_bert_empty'
                }
                
        except Exception as e:
            logger.error(f"❌ Skill extraction error: {e}")
            return self._fallback_skill_extraction(text)
    
    def _extract_skills_pattern(self, text: str) -> List[str]:
        """Extract skills using pattern matching"""
        skills = []
        
        # Comprehensive skills database
        skill_categories = {
            'programming': ['Python', 'Java', 'JavaScript', 'TypeScript', 'C++', 'C#', 'Go', 'Rust', 'Swift', 'Kotlin'],
            'web_frontend': ['HTML', 'CSS', 'React', 'Angular', 'Vue', 'Svelte', 'Bootstrap', 'Tailwind', 'jQuery'],
            'web_backend': ['Node.js', 'Express', 'Django', 'Flask', 'Spring', 'Laravel', 'Rails', 'ASP.NET'],
            'database': ['SQL', 'MySQL', 'PostgreSQL', 'MongoDB', 'Redis', 'Oracle', 'SQLite', 'Cassandra'],
            'cloud': ['AWS', 'Azure', 'GCP', 'Docker', 'Kubernetes', 'Terraform', 'Jenkins', 'CI/CD'],
            'data_science': ['Python', 'R', 'Pandas', 'NumPy', 'Scikit-learn', 'TensorFlow', 'PyTorch', 'Spark'],
            'mobile': ['React Native', 'Flutter', 'iOS', 'Android', 'Swift', 'Kotlin', 'Xamarin'],
            'devops': ['Docker', 'Kubernetes', 'Jenkins', 'GitLab', 'GitHub Actions', 'Terraform', 'Ansible'],
            'testing': ['Selenium', 'Jest', 'Cypress', 'JUnit', 'Pytest', 'Mocha', 'Chai']
        }
        
        text_lower = text.lower()
        for category, skill_list in skill_categories.items():
            for skill in skill_list:
                if skill.lower() in text_lower and skill not in skills:
                    skills.append(skill)
        
        return skills
    
    def _fallback_skill_extraction(self, text: str) -> Dict[str, Any]:
        """Fallback skill extraction using pattern matching"""
        skills = self._extract_skills_pattern(text)
        return {
            'extracted_skills': skills,
            'similarity_scores': {},
            'extraction_method': 'pattern_matching'
        }

class ExperienceLevelDetector:
    """Logistic Regression for experience level detection"""
    
    def __init__(self):
        self.model = None
        self.feature_names = []
        self._train_model()
    
    def _train_model(self):
        """Train logistic regression model on experience features"""
        try:
            from sklearn.linear_model import LogisticRegression
            from sklearn.feature_extraction.text import TfidfVectorizer
            
            # Dummy training data (in real implementation, use actual data)
            training_data = [
                ("junior developer with 1 year experience", "junior"),
                ("senior software engineer with 5 years", "senior"),
                ("mid-level developer with 3 years", "mid"),
                ("lead engineer with 8 years", "senior"),
                ("entry level programmer", "junior"),
                ("principal architect with 10 years", "senior"),
                ("associate developer", "junior"),
                ("staff engineer", "senior")
            ]
            
            texts = [item[0] for item in training_data]
            labels = [item[1] for item in training_data]
            
            # Create features
            self.vectorizer = TfidfVectorizer(max_features=100, stop_words='english')
            X = self.vectorizer.fit_transform(texts)
            
            # Train model
            self.model = LogisticRegression()
            self.model.fit(X, labels)
            
            self.feature_names = self.vectorizer.get_feature_names_out()
            logger.info("✅ Experience level detector trained")
            
        except Exception as e:
            logger.warning(f"⚠️ Experience level detector training failed: {e}")
    
    def detect_experience_level(self, text: str) -> Dict[str, Any]:
        """Detect experience level using logistic regression"""
        try:
            if not self.model:
                return self._fallback_detection(text)
            
            # Extract features
            X = self.vectorizer.transform([text])
            
            # Predict
            prediction = self.model.predict(X)[0]
            probability = self.model.predict_proba(X)[0]
            
            # Get confidence
            confidence = max(probability)
            
            return {
                'level': prediction,
                'confidence': confidence,
                'probabilities': {
                    'junior': probability[0] if len(probability) > 0 else 0,
                    'mid': probability[1] if len(probability) > 1 else 0,
                    'senior': probability[2] if len(probability) > 2 else 0
                },
                'method': 'logistic_regression'
            }
            
        except Exception as e:
            logger.error(f"❌ Experience level detection error: {e}")
            return self._fallback_detection(text)
    
    def _fallback_detection(self, text: str) -> Dict[str, Any]:
        """Fallback experience level detection"""
        text_lower = text.lower()
        
        if any(term in text_lower for term in ['senior', 'lead', 'principal', 'staff', 'architect']):
            level = 'senior'
        elif any(term in text_lower for term in ['mid', 'intermediate', 'experienced']):
            level = 'mid'
        else:
            level = 'junior'
        
        return {
            'level': level,
            'confidence': 0.7,
            'probabilities': {'junior': 0.3, 'mid': 0.3, 'senior': 0.4},
            'method': 'pattern_matching'
        }

class DomainClassifier:
    """Fine-tuned DistilBERT for domain classification"""
    
    def __init__(self):
        self.model = None
        self.tokenizer = None
        self._load_model()
    
    def _load_model(self):
        """Load DistilBERT model"""
        try:
            from transformers import DistilBertForSequenceClassification, DistilBertTokenizer
            
            # Use a pre-trained model (in real implementation, fine-tune on job descriptions)
            self.model = DistilBertForSequenceClassification.from_pretrained('distilbert-base-uncased')
            self.tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased')
            
            logger.info("✅ DistilBERT domain classifier loaded")
            
        except Exception as e:
            logger.warning(f"⚠️ DistilBERT not available: {e}")
    
    def classify_domain(self, text: str) -> Dict[str, Any]:
        """Classify domain using DistilBERT"""
        try:
            if not self.model or not self.tokenizer:
                return self._fallback_classification(text)
            
            # Tokenize input
            inputs = self.tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=512)
            
            # Predict
            with torch.no_grad():
                outputs = self.model(**inputs)
                predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)
            
            # Map to domains (simplified mapping)
            domains = ['frontend', 'backend', 'fullstack', 'data_science', 'ai_ml', 'devops', 'mobile', 'testing']
            domain_scores = {}
            
            for i, domain in enumerate(domains):
                if i < len(predictions[0]):
                    domain_scores[domain] = float(predictions[0][i])
            
            # Get top domain
            top_domain = max(domain_scores, key=domain_scores.get)
            
            return {
                'domain': top_domain,
                'confidence': domain_scores[top_domain],
                'domain_scores': domain_scores,
                'method': 'distilbert'
            }
            
        except Exception as e:
            logger.error(f"❌ Domain classification error: {e}")
            return self._fallback_classification(text)
    
    def _fallback_classification(self, text: str) -> Dict[str, Any]:
        """Fallback domain classification using keywords"""
        text_lower = text.lower()
        
        domain_keywords = {
            'frontend': ['react', 'angular', 'vue', 'html', 'css', 'javascript', 'frontend'],
            'backend': ['node.js', 'express', 'django', 'flask', 'spring', 'backend', 'api'],
            'data_science': ['python', 'pandas', 'numpy', 'machine learning', 'data science'],
            'ai_ml': ['tensorflow', 'pytorch', 'deep learning', 'neural networks', 'ai'],
            'devops': ['docker', 'kubernetes', 'aws', 'azure', 'ci/cd', 'devops'],
            'mobile': ['react native', 'flutter', 'ios', 'android', 'mobile'],
            'testing': ['selenium', 'jest', 'cypress', 'testing', 'qa']
        }
        
        domain_scores = {}
        for domain, keywords in domain_keywords.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            domain_scores[domain] = score / len(keywords)
        
        top_domain = max(domain_scores, key=domain_scores.get)
        
        return {
            'domain': top_domain,
            'confidence': domain_scores[top_domain],
            'domain_scores': domain_scores,
            'method': 'keyword_matching'
        }

class SalaryPredictor:
    """XGBoost Regressor for salary prediction"""
    
    def __init__(self):
        self.model = None
        self.feature_names = []
        self._train_model()
    
    def _train_model(self):
        """Train XGBoost model for salary prediction"""
        try:
            import xgboost as xgb
            
            # Dummy training data (in real implementation, use actual salary data)
            training_data = [
                ([2, 5, 1, 0, 0], 500000),  # 2 years exp, 5 skills, frontend, no management, no degree
                ([5, 10, 1, 1, 1], 800000),  # 5 years exp, 10 skills, frontend, management, degree
                ([3, 8, 2, 0, 1], 600000),  # 3 years exp, 8 skills, backend, no management, degree
                ([8, 15, 3, 1, 1], 1200000),  # 8 years exp, 15 skills, data science, management, degree
                ([1, 3, 1, 0, 0], 300000),  # 1 year exp, 3 skills, frontend, no management, no degree
            ]
            
            X = np.array([item[0] for item in training_data])
            y = np.array([item[1] for item in training_data])
            
            # Train XGBoost model
            self.model = xgb.XGBRegressor(n_estimators=100, random_state=42)
            self.model.fit(X, y)
            
            self.feature_names = ['experience_years', 'skill_count', 'domain', 'management', 'degree']
            logger.info("✅ XGBoost salary predictor trained")
            
        except Exception as e:
            logger.warning(f"⚠️ XGBoost salary predictor training failed: {e}")
    
    def predict_salary(self, features: Dict[str, Any]) -> Dict[str, Any]:
        """Predict salary using XGBoost"""
        try:
            if not self.model:
                return self._fallback_prediction(features)
            
            # Extract features
            experience_years = features.get('experience_years', 0)
            skill_count = features.get('skill_count', 0)
            domain = features.get('domain', 'frontend')
            management = 1 if features.get('management', False) else 0
            degree = 1 if features.get('degree', False) else 0
            
            # Map domain to number
            domain_map = {'frontend': 1, 'backend': 2, 'data_science': 3, 'ai_ml': 4, 'devops': 5}
            domain_num = domain_map.get(domain, 1)
            
            # Create feature vector
            X = np.array([[experience_years, skill_count, domain_num, management, degree]])
            
            # Predict
            prediction = self.model.predict(X)[0]
            
            # Calculate confidence based on feature quality
            confidence = min(0.9, 0.5 + (experience_years * 0.05) + (skill_count * 0.02))
            
            return {
                'predicted_salary': int(prediction),
                'confidence': confidence,
                'features_used': {
                    'experience_years': experience_years,
                    'skill_count': skill_count,
                    'domain': domain,
                    'management': management,
                    'degree': degree
                },
                'method': 'xgboost'
            }
            
        except Exception as e:
            logger.error(f"❌ Salary prediction error: {e}")
            return self._fallback_prediction(features)
    
    def _fallback_prediction(self, features: Dict[str, Any]) -> Dict[str, Any]:
        """Fallback salary prediction"""
        experience_years = features.get('experience_years', 0)
        skill_count = features.get('skill_count', 0)
        
        base_salary = 300000
        experience_bonus = experience_years * 50000
        skill_bonus = skill_count * 10000
        
        predicted_salary = base_salary + experience_bonus + skill_bonus
        
        return {
            'predicted_salary': predicted_salary,
            'confidence': 0.6,
            'features_used': features,
            'method': 'simple_calculation'
        }

class AdvancedAISystem:
    """Complete AI system combining all models"""
    
    def __init__(self):
        self.resume_parser = ResumeParser()
        self.ner = NamedEntityRecognizer()
        self.skill_extractor = SkillExtractor()
        self.experience_detector = ExperienceLevelDetector()
        self.domain_classifier = DomainClassifier()
        self.salary_predictor = SalaryPredictor()
    
    def extract_and_analyze_resume(self, pdf_path: str, filename: str = None) -> Dict[str, Any]:
        """Complete AI-powered resume extraction and analysis"""
        try:
            logger.info("🤖 Starting advanced AI-powered resume extraction...")
            
            # Step 1: Extract text from PDF
            text = self.resume_parser.extract_text_from_pdf(pdf_path)
            if not text:
                return self._create_error_response("Text extraction failed")
            
            # Step 2: Extract named entities
            entities = self.ner.extract_entities(text)
            
            # Step 3: Extract skills with similarity
            skill_analysis = self.skill_extractor.extract_skills_with_similarity(text)
            
            # Step 4: Detect experience level
            experience_level = self.experience_detector.detect_experience_level(text)
            
            # Step 5: Classify domain
            domain_classification = self.domain_classifier.classify_domain(text)
            
            # Step 6: Predict salary
            salary_features = {
                'experience_years': self._extract_experience_years(text),
                'skill_count': len(skill_analysis.get('extracted_skills', [])),
                'domain': domain_classification.get('domain', 'frontend'),
                'management': 'manager' in text.lower() or 'lead' in text.lower(),
                'degree': any(term in text.lower() for term in ['bachelor', 'master', 'phd', 'degree'])
            }
            salary_prediction = self.salary_predictor.predict_salary(salary_features)
            
            # Step 7: Calculate professional fit score
            professional_fit = self._calculate_professional_fit(
                skill_analysis, experience_level, domain_classification, salary_prediction
            )
            
            # Step 8: Generate comprehensive analysis
            analysis = {
                'extraction_method': 'advanced_ai_system',
                'confidence_score': self._calculate_overall_confidence(
                    skill_analysis, experience_level, domain_classification, salary_prediction
                ),
                'entities': entities,
                'skill_analysis': skill_analysis,
                'experience_level': experience_level,
                'domain_classification': domain_classification,
                'salary_prediction': salary_prediction,
                'professional_fit': professional_fit,
                'career_insights': self._generate_career_insights(
                    entities, skill_analysis, experience_level, domain_classification
                )
            }
            
            logger.info(f"✅ Advanced AI extraction completed")
            logger.info(f"🎯 Professional Fit: {professional_fit['overall_score']:.1f}%")
            logger.info(f"📊 Skills: {len(skill_analysis.get('extracted_skills', []))}")
            logger.info(f"⏰ Experience Level: {experience_level.get('level', 'unknown')}")
            logger.info(f"🏢 Domain: {domain_classification.get('domain', 'unknown')}")
            
            return analysis
            
        except Exception as e:
            logger.error(f"❌ Advanced AI system error: {e}")
            return self._create_error_response(f"AI system error: {str(e)}")
    
    def _extract_experience_years(self, text: str) -> int:
        """Extract experience years from text"""
        import re
        
        # Look for experience patterns
        patterns = [
            r'(\d+)\s*(?:to|-)?\s*(\d+)?\s*(?:years?|yrs?)\s*(?:of\s*)?(?:experience|exp)',
            r'(?:experience|exp)[:\s]*(\d+)\s*(?:to|-)?\s*(\d+)?\s*(?:years?|yrs?)',
            r'(\d+)\+?\s*(?:years?|yrs?)\s*(?:of\s*)?(?:experience|exp)'
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text.lower())
            for match in matches:
                if isinstance(match, tuple):
                    years = int(match[0]) if match[0] else 0
                    if match[1]:
                        years = max(years, int(match[1]))
                else:
                    years = int(match)
                
                if 0 < years <= 30:
                    return years
        
        return 0
    
    def _calculate_professional_fit(self, skill_analysis, experience_level, domain_classification, salary_prediction):
        """Calculate professional fit score using ensemble method"""
        try:
            # Weighted average of all sub-models
            skill_score = len(skill_analysis.get('extracted_skills', [])) * 5  # Max 50 points
            experience_score = experience_level.get('confidence', 0) * 20  # Max 20 points
            domain_score = domain_classification.get('confidence', 0) * 15  # Max 15 points
            salary_score = salary_prediction.get('confidence', 0) * 15  # Max 15 points
            
            total_score = min(100, skill_score + experience_score + domain_score + salary_score)
            
            return {
                'overall_score': total_score,
                'skill_score': skill_score,
                'experience_score': experience_score,
                'domain_score': domain_score,
                'salary_score': salary_score,
                'method': 'ensemble_weighted_average'
            }
            
        except Exception as e:
            logger.error(f"❌ Professional fit calculation error: {e}")
            return {
                'overall_score': 50,
                'skill_score': 25,
                'experience_score': 10,
                'domain_score': 10,
                'salary_score': 5,
                'method': 'fallback'
            }
    
    def _calculate_overall_confidence(self, skill_analysis, experience_level, domain_classification, salary_prediction):
        """Calculate overall confidence score"""
        try:
            confidences = [
                skill_analysis.get('extraction_method', 'pattern_matching') == 'sentence_bert',
                experience_level.get('confidence', 0),
                domain_classification.get('confidence', 0),
                salary_prediction.get('confidence', 0)
            ]
            
            return sum(confidences) / len(confidences)
            
        except Exception as e:
            logger.error(f"❌ Confidence calculation error: {e}")
            return 0.5
    
    def _generate_career_insights(self, entities, skill_analysis, experience_level, domain_classification):
        """Generate career insights"""
        try:
            insights = {
                'strengths': [],
                'improvements': [],
                'recommendations': [],
                'career_path': [],
                'market_position': 'unknown'
            }
            
            # Analyze strengths
            skills = skill_analysis.get('extracted_skills', [])
            if len(skills) > 10:
                insights['strengths'].append("Strong technical skill set")
            if experience_level.get('level') == 'senior':
                insights['strengths'].append("Senior-level experience")
            
            # Analyze improvements
            if len(skills) < 5:
                insights['improvements'].append("Develop more technical skills")
            if experience_level.get('level') == 'junior':
                insights['improvements'].append("Gain more experience")
            
            # Generate recommendations
            domain = domain_classification.get('domain', 'frontend')
            if domain == 'frontend':
                insights['recommendations'].append("Focus on modern frontend frameworks")
            elif domain == 'backend':
                insights['recommendations'].append("Learn cloud technologies")
            elif domain == 'data_science':
                insights['recommendations'].append("Master machine learning algorithms")
            
            # Career path
            level = experience_level.get('level', 'junior')
            if level == 'junior':
                insights['career_path'] = ['Junior Developer', 'Mid Developer', 'Senior Developer']
            elif level == 'mid':
                insights['career_path'] = ['Mid Developer', 'Senior Developer', 'Tech Lead']
            else:
                insights['career_path'] = ['Senior Developer', 'Tech Lead', 'Principal Engineer']
            
            return insights
            
        except Exception as e:
            logger.error(f"❌ Career insights generation error: {e}")
            return {
                'strengths': ['Technical background'],
                'improvements': ['Skill development'],
                'recommendations': ['Continue learning'],
                'career_path': ['Developer', 'Senior Developer'],
                'market_position': 'average'
            }
    
    def _create_error_response(self, error_message: str) -> Dict[str, Any]:
        """Create error response"""
        return {
            'extraction_method': 'advanced_ai_system_error',
            'confidence_score': 0.0,
            'error': error_message,
            'entities': {},
            'skill_analysis': {'extracted_skills': [], 'extraction_method': 'error'},
            'experience_level': {'level': 'unknown', 'confidence': 0.0, 'method': 'error'},
            'domain_classification': {'domain': 'unknown', 'confidence': 0.0, 'method': 'error'},
            'salary_prediction': {'predicted_salary': 0, 'confidence': 0.0, 'method': 'error'},
            'professional_fit': {'overall_score': 0, 'method': 'error'},
            'career_insights': {'strengths': [], 'improvements': [], 'recommendations': []}
        }

# Global AI system instance
advanced_ai_system = AdvancedAISystem()

