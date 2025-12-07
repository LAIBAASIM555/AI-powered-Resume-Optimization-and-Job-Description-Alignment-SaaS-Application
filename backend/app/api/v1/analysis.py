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
from app.ml.recommender import Recommender

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
        scorer = ATSScorer()
        score_result = scorer.calculate_score(
            resume_skills=resume.skills or [],
            resume_text=resume.raw_text or "",
            job_skills=job.required_skills or [],
            job_keywords=job.keywords or [],
            job_text=job.raw_text
        )
        
        recommender = Recommender()
        recommendations = recommender.get_recommendations(
            matched_skills=score_result["matched_skills"],
            missing_skills=score_result["missing_skills"],
            score_breakdown=score_result["breakdown"]
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

@router.get("/", response_model=List[AnalysisHistory])
async def get_analysis_history(
    limit: int = 10,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    analyses = db.query(Analysis).filter(Analysis.user_id == current_user.id).order_by(Analysis.created_at.desc()).limit(limit).all()
    
    result = []
    for analysis in analyses:
        resume = db.query(Resume).filter(Resume.id == analysis.resume_id).first()
        job = db.query(JobDescription).filter(JobDescription.id == analysis.job_id).first()
        
        result.append(AnalysisHistory(
            id=analysis.id,
            resume_filename=resume.filename if resume else "Unknown",
            job_title=job.title if job else "Unknown",
            ats_score=analysis.ats_score,
            created_at=analysis.created_at
        ))
    
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
