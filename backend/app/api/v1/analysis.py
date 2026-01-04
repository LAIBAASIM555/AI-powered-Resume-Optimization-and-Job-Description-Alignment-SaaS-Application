from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.models.resume import Resume
from app.models.job import JobDescription
from app.models.analysis import Analysis
from app.schemas.analysis import AnalysisRequest, AnalysisResponse, AnalysisHistory
from app.ml.scorer import ATSScorer
from app.ml.recommender import ResumeRecommender
from app.ml.jd_parser import JDParser

router = APIRouter()

@router.post("/analyze", response_model=AnalysisResponse, status_code=status.HTTP_201_CREATED)
async def analyze_resume(
    request: AnalysisRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    resume = db.query(Resume).filter(Resume.id == request.resume_id, Resume.user_id == current_user.id).first()
    if not resume:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resume not found")
    
    job = db.query(JobDescription).filter(JobDescription.id == request.job_id, JobDescription.user_id == current_user.id).first()
    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job description not found")
    
    try:
        # Parse job description if not already parsed
        if not job.required_skills or not job.keywords:
            jd_parser = JDParser()
            jd_data = jd_parser.parse(job.raw_text)
            
            # Update job record with parsed data
            job.required_skills = jd_data.get("required_skills", [])
            job.keywords = jd_data.get("keywords", [])
            # Store preferred_skills in parsed_data
            job.parsed_data = jd_data
            db.commit()
        
        # Calculate ATS score
        scorer = ATSScorer()
        # Get preferred_skills from parsed_data
        preferred_skills = (job.parsed_data or {}).get("preferred_skills", [])
        
        score_result = scorer.calculate_score(
            resume_skills=resume.skills or [],
            resume_text=resume.raw_text or "",
            job_skills=(job.required_skills or []) + preferred_skills,
            job_keywords=job.keywords or [],
            job_text=job.raw_text
        )
        
        # Generate recommendations using new ResumeRecommender
        recommender = ResumeRecommender()
        
        # Prepare job data for recommender
        job_data = {
            "required_skills": job.required_skills or [],
            "preferred_skills": preferred_skills,
            "keywords": job.keywords or [],
        }
        
        # Generate recommendations
        recommendations = recommender.generate_recommendations(
            resume_data=resume.parsed_data or {},
            job_data=job_data,
            score_data=score_result
        )
        
        original_summary = resume.parsed_data.get("summary", "") if resume.parsed_data else ""
        
        analysis = Analysis(
            user_id=current_user.id,
            resume_id=resume.id,
            job_id=job.id,
            ats_score=score_result["total_score"],
            score_breakdown=score_result["breakdown"],
            matched_skills=score_result["matched_skills"],
            missing_skills=score_result["missing_skills"],
            extra_skills=score_result.get("extra_skills", []),
            matched_keywords=score_result.get("matched_keywords", []),
            missing_keywords=score_result.get("missing_keywords", []),
            recommendations=recommendations,
            original_summary=original_summary,
            improved_summary=None
        )
        
        db.add(analysis)
        db.commit()
        db.refresh(analysis)
        
        return analysis
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error analyzing resume: {str(e)}")

from sqlalchemy.orm import joinedload

# ... (other imports)

@router.get("/", response_model=List[AnalysisHistory])
async def get_analysis_history(
    limit: int = 10,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    analyses = (
        db.query(Analysis)
        .options(
            joinedload(Analysis.resume),
            joinedload(Analysis.job_description)
        )
        .filter(Analysis.user_id == current_user.id)
        .order_by(Analysis.created_at.desc())
        .limit(limit)
        .all()
    )
    
    result = [
        AnalysisHistory(
            id=analysis.id,
            resume_filename=analysis.resume.filename if analysis.resume else "Unknown",
            job_title=analysis.job_description.title if analysis.job_description else "Unknown",
            ats_score=analysis.ats_score,
            created_at=analysis.created_at
        )
        for analysis in analyses
    ]
    
    return result

@router.get("/{analysis_id}", response_model=AnalysisResponse)
async def get_analysis(
    analysis_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    analysis = db.query(Analysis).filter(Analysis.id == analysis_id, Analysis.user_id == current_user.id).first()
    if not analysis:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Analysis not found")
    return analysis

@router.delete("/{analysis_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_analysis(
    analysis_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    analysis = db.query(Analysis).filter(Analysis.id == analysis_id, Analysis.user_id == current_user.id).first()
    if not analysis:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Analysis not found")
    
    db.delete(analysis)
    db.commit()
    return None
