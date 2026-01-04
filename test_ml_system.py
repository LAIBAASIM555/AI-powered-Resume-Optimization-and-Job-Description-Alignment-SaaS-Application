#!/usr/bin/env python3
"""
Test script for the complete ML system
Tests: Resume parsing, validation, job description parsing, scoring, and recommendations
"""

import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "backend"))

from app.ml.skills_database import find_skills_in_text, categorize_skills
from app.ml.resume_validator import ResumeValidator
from app.ml.resume_parser import ResumeParser
from app.ml.jd_parser import JDParser
from app.ml.scorer import ATSScorer
from app.ml.recommender import ResumeRecommender


def test_skills_database():
    """Test skills database"""
    print("\n" + "="*60)
    print("TEST 1: Skills Database")
    print("="*60)
    
    text = "I have experience with Python, React, Docker, AWS, and PostgreSQL"
    skills = find_skills_in_text(text)
    categorized = categorize_skills(skills)
    
    print(f"Found {len(skills)} skills: {skills}")
    print(f"\nCategorized:")
    for category, category_skills in categorized.items():
        if category != "all_skills" and category_skills:
            print(f"  {category}: {category_skills}")
    
    return len(skills) >= 5


def test_resume_validator():
    """Test resume validator"""
    print("\n" + "="*60)
    print("TEST 2: Resume Validator")
    print("="*60)
    
    validator = ResumeValidator()
    
    # Test valid resume
    valid_resume = """
    John Doe
    Email: john@example.com | Phone: (555) 123-4567
    
    PROFESSIONAL SUMMARY
    Senior Software Engineer with 5+ years of experience
    
    EXPERIENCE
    Senior Developer at Tech Corp
    Jan 2020 - Present
    - Developed web applications using React and Node.js
    - Improved system performance by 40%
    
    EDUCATION
    Bachelor of Science in Computer Science
    University of Tech, 2019
    
    SKILLS
    Python, JavaScript, React, Docker, AWS, PostgreSQL
    """
    
    result = validator.validate(valid_resume)
    print(f"Valid Resume Test:")
    print(f"  Is Valid: {result['is_valid']}")
    print(f"  Confidence: {result['confidence']}")
    print(f"  Reason: {result['reason']}")
    
    # Test job description (should reject)
    job_description = """
    Software Engineer - Remote
    
    We are looking for a talented Software Engineer to join our team.
    
    Requirements:
    - 5+ years of experience with Python
    - Strong knowledge of React and Node.js
    
    What We Offer:
    - Competitive salary
    - Health insurance
    - Remote work
    
    How to Apply:
    Submit your resume to jobs@company.com
    """
    
    result2 = validator.validate(job_description)
    print(f"\nJob Description Test (should reject):")
    print(f"  Is Valid: {result2['is_valid']}")
    print(f"  Confidence: {result2['confidence']}")
    print(f"  Reason: {result2['reason']}")
    
    return result['is_valid'] and not result2['is_valid']


def test_jd_parser():
    """Test job description parser"""
    print("\n" + "="*60)
    print("TEST 3: Job Description Parser")
    print("="*60)
    
    jd_text = """
    Senior Full-Stack Developer
    
    We are seeking a Senior Full-Stack Developer with 5+ years of experience.
    
    Required Skills:
    - Python, JavaScript, React
    - PostgreSQL, Docker
    - AWS or Azure
    
    Preferred Skills:
    - Kubernetes, Terraform
    - GraphQL
    
    Responsibilities:
    - Design and develop web applications
    - Collaborate with cross-functional teams
    - Mentor junior developers
    
    Requirements:
    - Bachelor's degree in Computer Science
    - 5+ years of professional experience
    """
    
    parser = JDParser()
    result = parser.parse(jd_text)
    
    print(f"Required Skills ({len(result['required_skills'])}): {result['required_skills'][:10]}")
    print(f"Preferred Skills ({len(result['preferred_skills'])}): {result['preferred_skills'][:10]}")
    print(f"Experience: {result['experience_years']}")
    print(f"Education: {result['education']}")
    print(f"Keywords ({len(result['keywords'])}): {result['keywords'][:15]}")
    
    return len(result['required_skills']) > 0 and result['experience_years']


def test_scorer():
    """Test ATS scorer"""
    print("\n" + "="*60)
    print("TEST 4: ATS Scorer")
    print("="*60)
    
    scorer = ATSScorer()
    
    resume_skills = ["Python", "JavaScript", "React", "PostgreSQL", "Docker"]
    resume_text = "Senior developer with Python and React experience. Improved performance by 40%."
    
    job_skills = ["Python", "React", "Docker", "AWS", "Kubernetes"]
    job_keywords = ["Python", "React", "cloud", "agile", "team"]
    job_text = "Looking for Python and React developer with cloud experience"
    
    result = scorer.calculate_score(
        resume_skills=resume_skills,
        resume_text=resume_text,
        job_skills=job_skills,
        job_keywords=job_keywords,
        job_text=job_text
    )
    
    print(f"Total Score: {result['total_score']}/100")
    print(f"\nBreakdown:")
    for key, value in result['breakdown'].items():
        print(f"  {key}: {value}")
    
    print(f"\nMatched Skills: {result['matched_skills']}")
    print(f"Missing Skills: {result['missing_skills']}")
    print(f"Matched Keywords: {result['matched_keywords'][:5]}")
    
    return result['total_score'] > 0


def test_recommender():
    """Test recommendation engine"""
    print("\n" + "="*60)
    print("TEST 5: Recommendation Engine")
    print("="*60)
    
    recommender = ResumeRecommender()
    
    resume_data = {
        "skills": {
            "all_skills": ["Python", "React", "PostgreSQL"]
        },
        "total_experience_years": 3,
        "experience": [
            {
                "achievements": ["Improved performance by 40%"]
            }
        ]
    }
    
    job_data = {
        "required_skills": ["Python", "React", "Docker", "AWS"],
        "preferred_skills": ["Kubernetes", "Terraform"],
        "keywords": ["cloud", "agile", "microservices"]
    }
    
    score_data = {
        "total_score": 65,
        "breakdown": {
            "skills_score": 50,
            "experience_score": 70,
            "keywords_score": 60,
            "achievements_score": 70,
            "format_score": 80
        },
        "matched_skills": ["Python", "React"],
        "missing_skills": ["Docker", "AWS"],
        "missing_keywords": ["cloud", "agile"]
    }
    
    recommendations = recommender.generate_recommendations(
        resume_data=resume_data,
        job_data=job_data,
        score_data=score_data
    )
    
    print(f"Generated {len(recommendations)} recommendations:\n")
    
    for i, rec in enumerate(recommendations[:5], 1):
        print(f"{i}. [{rec['priority'].upper()}] {rec['title']}")
        print(f"   {rec['description']}")
        print(f"   Action: {rec['action']}")
        print(f"   Impact: {rec.get('impact', 'N/A')}\n")
    
    return len(recommendations) > 0


def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("ML SYSTEM TEST SUITE")
    print("="*60)
    
    tests = [
        ("Skills Database", test_skills_database),
        ("Resume Validator", test_resume_validator),
        ("JD Parser", test_jd_parser),
        ("ATS Scorer", test_scorer),
        ("Recommender", test_recommender),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            passed = test_func()
            results.append((name, "✅ PASS" if passed else "❌ FAIL"))
        except Exception as e:
            results.append((name, f"❌ ERROR: {str(e)}"))
            print(f"\nError in {name}: {e}")
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    for name, status in results:
        print(f"{name}: {status}")
    
    passed = sum(1 for _, status in results if "PASS" in status)
    total = len(results)
    
    print(f"\nPassed: {passed}/{total}")
    
    if passed == total:
        print("\n🎉 All tests passed! ML system is ready.")
    else:
        print("\n⚠️ Some tests failed. Please review.")


if __name__ == "__main__":
    main()
