import os
import json
from typing import Dict, Any, Optional
from app.config import settings
import httpx


class AIGenerator:
    """Helper class for calling LLM APIs (Gemini) with fallback to local rules."""

    def __init__(self):
        self.google_api_key = settings.GOOGLE_API_KEY

    async def generate_summary(self, data: Dict[str, Any]) -> str:
        """
        Generates a professional summary using Gemini if available, 
        otherwise falls back to rule-based generation.
        """
        if not self.google_api_key:
            return self._generate_fallback_summary(data)

        try:
            prompt = self._build_summary_prompt(data)
            summary = await self._call_gemini(prompt)
            if summary:
                return summary.strip().replace('"', '')
            return self._generate_fallback_summary(data)
        except Exception as e:
            print(f"Gemini API error: {e}")
            return self._generate_fallback_summary(data)

    def _build_summary_prompt(self, data: Dict[str, Any]) -> str:
        """Builds a prompt tailored for the resume builder."""
        title = data.get("title") or "Professional"
        experience = data.get("experience", [])
        skills = data.get("skills", [])
        
        # Calculate total years (roughly) based on start/end dates if we wanted, 
        # but for now just count the jobs
        exp_count = len(experience)
        
        prompt = f"""
Write a highly professional, 2-3 sentence resume summary for a {title}. 
Do not use "I", "me", or "my". Use active voice and strong action verbs.
        
Background info:
- Job Title: {title}
- Skills: {', '.join(skills[:8]) if skills else 'various professional skills'}
- Recent Roles: {', '.join([e.get('title', '') for e in experience[:2] if e.get('title')])}

The summary should highlight expertise, value proposition, and drive for results.
Output ONLY the summary text, nothing else. No intro, no quotes.
"""
        return prompt

    async def _call_gemini(self, prompt: str) -> Optional[str]:
        """Calls the Gemini 2.5 Flash API directly using httpx."""
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={self.google_api_key}"
        
        payload = {
            "contents": [{
                "parts": [{"text": prompt}]
            }],
            "generationConfig": {
                "temperature": 0.7,
                "topK": 40,
                "topP": 0.95,
                "maxOutputTokens": 150,
            }
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload, timeout=10.0)
            
            if response.status_code != 200:
                print(f"Gemini error: {response.text}")
                return None
                
            data = response.json()
            try:
                text = data["candidates"][0]["content"]["parts"][0]["text"]
                return text
            except (KeyError, IndexError):
                return None

    def _generate_fallback_summary(self, data: Dict[str, Any]) -> str:
        """Generates a standard rule-based summary when AI is unavailable."""
        title = data.get("title", "professional").strip() or "professional"
        skills = data.get("skills", [])
        
        if len(skills) >= 3:
            skill_str = f"expertise in {skills[0]}, {skills[1]}, and {skills[2]}"
        elif len(skills) > 0:
            skill_str = f"expertise in {skills[0]}"
        else:
            skill_str = "strong analytical and problem-solving skills"
        return f"Dynamic and results-driven {title} with proven {skill_str}. Passionate about leveraging skills to drive measurable business outcomes, contribute to organizational success, and build innovative solutions."

    async def analyze_ats_match(self, resume_text: str, job_text: str) -> Optional[Dict[str, Any]]:
        """
        Uses Gemini to perform an intelligent ATS match between a resume and job description.
        Returns a dictionary with score, missing skills, matched skills, and recommendations.
        If API key is missing or fails, returns None (which triggers the local fallback).
        """
        if not self.google_api_key or not resume_text or not job_text:
            return None
            
        prompt = f"""
You are an expert AI Applicant Tracking System (ATS). Analyze the following resume against the job description.

Job Description:
{job_text[:3000]}

Resume:
{resume_text[:3000]}

Perform a strict analysis and return a JSON object with EXACTLY this structure (no markdown formatting, just raw JSON):
{{
    "ats_score": 0-100 integer representing the match quality,
    "score_breakdown": {{
        "skills_score": 0-100 integer,
        "experience_score": 0-100 integer,
        "keywords_score": 0-100 integer,
        "format_score": 0-100 integer,
        "achievements_score": 0-100 integer
    }},
    "matched_skills": ["skill1", "skill2"],
    "missing_skills": ["skill3", "skill4"],
    "recommendations": ["Actionable tip 1", "Actionable tip 2"]
}}

Be highly critical. Only list a skill as matched if it's explicitly in the resume or a very close synonym.
"""
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={self.google_api_key}"
            payload = {
                "contents": [{"parts": [{"text": prompt}]}],
                "generationConfig": {
                    "temperature": 0.2,
                    "topK": 40,
                    "topP": 0.95,
                    "maxOutputTokens": 1000,
                }
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.post(url, json=payload, timeout=15.0)
                
                if response.status_code != 200:
                    print(f"Gemini ATS error: {response.text}")
                    return None
                    
                data = response.json()
                text = data["candidates"][0]["content"]["parts"][0]["text"]
                
                # Clean up JSON if Gemini wrapped it in markdown blocks
                text = text.strip()
                if text.startswith("```json"):
                    text = text[7:]
                if text.startswith("```"):
                    text = text[3:]
                if text.endswith("```"):
                    text = text[:-3]
                    
                result = json.loads(text.strip())
                
                # Validate the structure loosely
                if "ats_score" in result and "matched_skills" in result:
                    return result
                return None
        except Exception as e:
            print(f"Gemini ATS match error: {e}")
            return None


# Singleton
ai_generator = AIGenerator()
