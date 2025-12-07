"""
Recommendation engine for resume optimization suggestions.
"""
from typing import List, Dict, Any


class Recommender:
    """Generate prioritized recommendations for resume optimization."""
    
    def get_recommendations(
        self,
        matched_skills: List[str],
        missing_skills: List[str],
        score_breakdown: Dict[str, float]
    ) -> List[Dict[str, Any]]:
        """
        Generate prioritized recommendations.
        
        Args:
            matched_skills: List of skills that matched
            missing_skills: List of skills that are missing
            score_breakdown: Dictionary with individual scores
            
        Returns:
            List of recommendation dictionaries with priority, category, message, and details
        """
        recommendations = []
        
        # 1. Add recommendations for top 5 missing skills (high priority for first 2)
        if missing_skills:
            top_missing = missing_skills[:5]
            for i, skill in enumerate(top_missing):
                priority = "high" if i < 2 else "medium"
                recommendations.append({
                    "priority": priority,
                    "category": "skills",
                    "message": f"Add '{skill}' to your resume",
                    "details": f"'{skill}' is listed as a required skill in the job description but is missing from your resume. Consider adding it to your skills section or highlighting relevant experience with this skill."
                })
        
        # 2. If skills_score < 70: add skills improvement recommendation
        skills_score = score_breakdown.get("skills_score", 0)
        if skills_score < 70:
            recommendations.append({
                "priority": "high",
                "category": "skills",
                "message": "Improve skills alignment",
                "details": f"Your skills match score is {skills_score:.1f}%. Focus on adding more required skills from the job description to improve your ATS compatibility."
            })
        
        # 3. If keywords_score < 60: add keywords recommendation
        keywords_score = score_breakdown.get("keywords_score", 0)
        if keywords_score < 60:
            recommendations.append({
                "priority": "medium",
                "category": "keywords",
                "message": "Include more relevant keywords",
                "details": f"Your keyword match score is {keywords_score:.1f}%. Incorporate more keywords from the job description naturally throughout your resume, especially in your experience and skills sections."
            })
        
        # 4. If achievements_score < 60: add quantifiable achievements recommendation
        achievements_score = score_breakdown.get("achievements_score", 0)
        if achievements_score < 60:
            recommendations.append({
                "priority": "medium",
                "category": "achievements",
                "message": "Add quantifiable achievements",
                "details": f"Your achievements score is {achievements_score:.1f}%. Include specific metrics like percentages (e.g., 'increased sales by 25%'), dollar amounts, or numbers to demonstrate your impact."
            })
        
        # 5. If experience_score < 60: add experience alignment recommendation
        experience_score = score_breakdown.get("experience_score", 0)
        if experience_score < 60:
            recommendations.append({
                "priority": "medium",
                "category": "experience",
                "message": "Better align your experience",
                "details": f"Your experience alignment score is {experience_score:.1f}%. Tailor your experience descriptions to use similar language and terminology as the job description."
            })
        
        # 6. If format_score < 70: add format improvement recommendation
        format_score = score_breakdown.get("format_score", 0)
        if format_score < 70:
            recommendations.append({
                "priority": "low",
                "category": "format",
                "message": "Improve resume format",
                "details": f"Your format score is {format_score:.1f}%. Ensure your resume includes all standard sections (Experience, Education, Skills, Summary) and maintains an optimal length (300-1500 words)."
            })
        
        # 7. Add general best practices if < 3 recommendations
        if len(recommendations) < 3:
            recommendations.append({
                "priority": "low",
                "category": "general",
                "message": "Follow ATS best practices",
                "details": "Use standard section headings, avoid graphics and complex formatting, include relevant keywords naturally, and ensure your resume is easily parseable by ATS systems."
            })
        
        # Sort by priority (high → medium → low)
        priority_order = {"high": 0, "medium": 1, "low": 2}
        recommendations.sort(key=lambda x: priority_order.get(x["priority"], 3))
        
        return recommendations

