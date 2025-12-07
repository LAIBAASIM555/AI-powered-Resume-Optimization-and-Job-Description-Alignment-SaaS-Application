"""
ATS (Applicant Tracking System) scoring engine.
"""
from typing import List, Dict, Any
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re


class ATSScorer:
    """Calculate ATS compatibility scores between resumes and job descriptions."""
    
    def __init__(self):
        """Initialize the ATS scorer."""
        self.vectorizer = TfidfVectorizer(stop_words='english', max_features=1000)
        
        # Score weights (must sum to 1.0)
        self.weights = {
            "skills": 0.40,      # 40% weight
            "experience": 0.25,  # 25% weight
            "keywords": 0.20,    # 20% weight
            "achievements": 0.10, # 10% weight
            "format": 0.05       # 5% weight
        }
    
    def calculate_score(
        self,
        resume_skills: List[str],
        resume_text: str,
        job_skills: List[str],
        job_keywords: List[str],
        job_text: str
    ) -> Dict[str, Any]:
        """
        Calculate comprehensive ATS score.
        
        Args:
            resume_skills: List of skills from resume
            resume_text: Full resume text
            job_skills: List of required skills from job description
            job_keywords: List of keywords from job description
            job_text: Full job description text
            
        Returns:
            Dictionary with score breakdown and analysis
        """
        # Calculate individual scores
        skills_result = self._calculate_skills_score(resume_skills, job_skills)
        keywords_result = self._calculate_keywords_score(resume_text, job_keywords)
        semantic_similarity = self._calculate_semantic_similarity(resume_text, job_text)
        achievements_score = self._calculate_achievements_score(resume_text)
        format_score = self._calculate_format_score(resume_text)
        
        # Use semantic similarity for experience score
        experience_score = semantic_similarity * 100
        
        # Calculate weighted total score
        total_score = (
            skills_result["score"] * self.weights["skills"] +
            experience_score * self.weights["experience"] +
            keywords_result["score"] * self.weights["keywords"] +
            achievements_score * self.weights["achievements"] +
            format_score * self.weights["format"]
        )
        
        # Ensure score is between 0 and 100
        total_score = max(0, min(100, total_score))
        
        return {
            "total_score": round(total_score, 2),
            "breakdown": {
                "skills_score": round(skills_result["score"], 2),
                "experience_score": round(experience_score, 2),
                "keywords_score": round(keywords_result["score"], 2),
                "achievements_score": round(achievements_score, 2),
                "format_score": round(format_score, 2)
            },
            "matched_skills": skills_result["matched"],
            "missing_skills": skills_result["missing"],
            "extra_skills": skills_result["extra"],
            "matched_keywords": keywords_result["matched"],
            "missing_keywords": keywords_result["missing"]
        }
    
    def _calculate_skills_score(self, resume_skills: List[str], job_skills: List[str]) -> Dict:
        """
        Calculate skills match score.
        
        Returns:
            Dictionary with score, matched, missing, and extra skills
        """
        if not job_skills:
            return {
                "score": 100.0,
                "matched": [],
                "missing": [],
                "extra": resume_skills
            }
        
        # Normalize skills to lowercase for comparison
        resume_skills_lower = [s.lower() for s in resume_skills]
        job_skills_lower = [s.lower() for s in job_skills]
        
        # Find matches (case-insensitive)
        matched = []
        missing = []
        
        for job_skill in job_skills_lower:
            found = False
            for resume_skill in resume_skills_lower:
                # Check for exact match or substring match
                if job_skill in resume_skill or resume_skill in job_skill:
                    matched.append(job_skill)
                    found = True
                    break
            if not found:
                missing.append(job_skill)
        
        # Find extra skills (in resume but not in job)
        extra = []
        for resume_skill in resume_skills_lower:
            found = False
            for job_skill in job_skills_lower:
                if job_skill in resume_skill or resume_skill in job_skill:
                    found = True
                    break
            if not found:
                extra.append(resume_skill)
        
        # Calculate score: (matched / total required) * 100
        score = (len(matched) / len(job_skills)) * 100 if job_skills else 0
        
        return {
            "score": min(100, score),
            "matched": matched,
            "missing": missing,
            "extra": extra
        }
    
    def _calculate_keywords_score(self, resume_text: str, job_keywords: List[str]) -> Dict:
        """
        Calculate keywords match score.
        
        Returns:
            Dictionary with score, matched, and missing keywords
        """
        if not job_keywords:
            return {
                "score": 100.0,
                "matched": [],
                "missing": []
            }
        
        resume_text_lower = resume_text.lower()
        matched = []
        missing = []
        
        for keyword in job_keywords:
            keyword_lower = keyword.lower()
            # Check if keyword appears in resume (word boundary match)
            pattern = r'\b' + re.escape(keyword_lower) + r'\b'
            if re.search(pattern, resume_text_lower):
                matched.append(keyword)
            else:
                missing.append(keyword)
        
        # Calculate score: (matched / total keywords) * 100
        score = (len(matched) / len(job_keywords)) * 100 if job_keywords else 0
        
        return {
            "score": min(100, score),
            "matched": matched,
            "missing": missing
        }
    
    def _calculate_semantic_similarity(self, resume_text: str, job_text: str) -> float:
        """
        Calculate semantic similarity using TF-IDF + cosine similarity.
        
        Returns:
            Similarity value between 0 and 1
        """
        if not resume_text or not job_text:
            return 0.0
        
        try:
            # Fit vectorizer and transform texts
            tfidf_matrix = self.vectorizer.fit_transform([resume_text, job_text])
            
            # Calculate cosine similarity
            similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
            
            return float(similarity)
        except Exception:
            return 0.0
    
    def _calculate_achievements_score(self, resume_text: str) -> float:
        """
        Calculate achievements score based on quantifiable achievements.
        
        Returns:
            Score between 0 and 100
        """
        if not resume_text:
            return 50.0
        
        base_score = 50.0
        achievements_count = 0
        
        # Look for percentages (X%)
        percentages = re.findall(r'\d+%', resume_text)
        achievements_count += len(percentages)
        
        # Look for dollar amounts ($X, $XK, $XM)
        dollar_amounts = re.findall(r'\$[\d,]+[KM]?', resume_text, re.IGNORECASE)
        achievements_count += len(dollar_amounts)
        
        # Look for numbers with achievement context
        achievement_patterns = [
            r'(?:increased|improved|reduced|saved|achieved|delivered)\s+(?:by\s+)?\d+',
            r'\d+\s*(?:times|fold|x)',
            r'(?:over|more than|up to)\s+\d+'
        ]
        
        for pattern in achievement_patterns:
            matches = re.findall(pattern, resume_text, re.IGNORECASE)
            achievements_count += len(matches)
        
        # Add points for each achievement (max 50 additional points)
        additional_points = min(50, achievements_count * 5)
        score = base_score + additional_points
        
        return min(100, score)
    
    def _calculate_format_score(self, resume_text: str) -> float:
        """
        Calculate format score based on structure and word count.
        
        Returns:
            Score between 0 and 100
        """
        if not resume_text:
            return 60.0
        
        base_score = 60.0
        word_count = len(resume_text.split())
        
        # Check for common sections
        section_keywords = {
            "experience": ["experience", "work history", "employment", "career"],
            "education": ["education", "academic", "qualifications", "degree"],
            "skills": ["skills", "technical skills", "competencies"],
            "summary": ["summary", "objective", "profile", "about"]
        }
        
        sections_found = 0
        text_lower = resume_text.lower()
        
        for section, keywords in section_keywords.items():
            for keyword in keywords:
                if keyword in text_lower:
                    sections_found += 1
                    break
        
        # Add points for sections found (max 20 points)
        section_points = min(20, sections_found * 5)
        
        # Check word count (optimal: 300-1500 words)
        word_count_score = 0
        if 300 <= word_count <= 1500:
            word_count_score = 10
        elif 150 <= word_count < 300 or 1500 < word_count <= 2000:
            word_count_score = 5
        
        score = base_score + section_points + word_count_score
        
        return min(100, score)

