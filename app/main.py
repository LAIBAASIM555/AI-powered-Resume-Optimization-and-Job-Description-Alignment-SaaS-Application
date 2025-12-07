from app.core.database import get_database, get_analyses_collection
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import fitz  # PyMuPDF
from docx import Document
import os
import io
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re

app = FastAPI(title="AI-based resume optimization SaaS platform")

# CORS (React se connect karne ke liye)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root endpoint
@app.get("/")
def read_root():
    return {
        "message": "Welcome to the AI-based resume optimization SaaS platform API!",
        "status": "running",
        "version": "1.0"
    }

# Health check
@app.get("/health")
def health_check():
    return {"status": "healthy"}

# Resume upload endpoint
@app.post("/api/upload-resume")
async def upload_resume(file: UploadFile = File(...)):
    try:
        # Check file type
        if not file.filename.endswith(('.pdf', '.docx')):
            raise HTTPException(
                status_code=400, 
                detail="Only PDF and DOCX files are allowed"
            )
        
        # Read file
        contents = await file.read()
        
        # Extract text based on file type
        if file.filename.endswith('.pdf'):
            text = extract_text_from_pdf(contents)
        else:
            text = extract_text_from_docx(contents)
        
        return {
            "success": True,
            "filename": file.filename,
            "text_length": len(text),
            "preview": text[:200] + "..." if len(text) > 200 else text
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# PDF text extraction
def extract_text_from_pdf(file_contents):
    doc = fitz.open(stream=file_contents, filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

# DOCX text extraction
def extract_text_from_docx(file_contents):
    doc = Document(io.BytesIO(file_contents))
    text = ""
    for para in doc.paragraphs:
        text += para.text + "\n"
    return text
    # Job Description upload endpoint
@app.post("/api/upload-job-description")
async def upload_job_description(file: UploadFile = File(...)):
    try:
        # Check file type
        if not file.filename.endswith(('.pdf', '.docx', '.txt')):
            raise HTTPException(
                status_code=400, 
                detail="Only PDF, DOCX and TXT files are allowed"
            )
        
        # Read file
        contents = await file.read()
        
        # Extract text based on file type
        if file.filename.endswith('.pdf'):
            text = extract_text_from_pdf(contents)
        elif file.filename.endswith('.docx'):
            text = extract_text_from_docx(contents)
        else:  # .txt file
            text = contents.decode('utf-8')
        
        # Extract basic info (we'll enhance this later with NLP)
        word_count = len(text.split())
        
        return {
            "success": True,
            "filename": file.filename,
            "text_length": len(text),
            "word_count": word_count,
            "preview": text[:300] + "..." if len(text) > 300 else text,
            "message": "Job description uploaded successfully"
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# AI Analysis endpoint
@app.post("/api/analyze")
async def analyze_resume(
    resume_file: UploadFile = File(...),
    job_desc_file: UploadFile = File(...)
):
    try:
        # Extract text from resume
        resume_contents = await resume_file.read()
        if resume_file.filename.endswith('.pdf'):
            resume_text = extract_text_from_pdf(resume_contents)
        elif resume_file.filename.endswith('.docx'):
            resume_text = extract_text_from_docx(resume_contents)
        else:
            resume_text = resume_contents.decode('utf-8')
        
        # Extract text from job description
        jd_contents = await job_desc_file.read()
        if job_desc_file.filename.endswith('.pdf'):
            jd_text = extract_text_from_pdf(jd_contents)
        elif job_desc_file.filename.endswith('.docx'):
            jd_text = extract_text_from_docx(jd_contents)
        else:
            jd_text = jd_contents.decode('utf-8')
        
        # Clean text
        resume_clean = clean_text(resume_text)
        jd_clean = clean_text(jd_text)
        
        # Calculate similarity score
        similarity_score = calculate_similarity(resume_clean, jd_clean)
        
        # Extract keywords from job description
        jd_keywords = extract_keywords(jd_text)
        resume_keywords = extract_keywords(resume_text)
        
        # Find missing keywords
        missing_keywords = list(set(jd_keywords) - set(resume_keywords))
        matching_keywords = list(set(jd_keywords) & set(resume_keywords))
        
        # Calculate ATS score
        ats_score = calculate_ats_score(
            similarity_score, 
            len(matching_keywords), 
            len(jd_keywords)
        )
        
        return {
            "success": True,
            "similarity_score": round(similarity_score * 100, 2),
            "ats_score": round(ats_score, 2),
            "matching_keywords": matching_keywords[:10],
            "missing_keywords": missing_keywords[:10],
            "total_jd_keywords": len(jd_keywords),
            "matched_count": len(matching_keywords),
            "missing_count": len(missing_keywords),
            "recommendation": get_recommendation(ats_score)
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Helper functions
def clean_text(text):
    """Clean and normalize text"""
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def calculate_similarity(text1, text2):
    """Calculate cosine similarity between two texts"""
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([text1, text2])
    similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
    return similarity[0][0]

def extract_keywords(text):
    """Extract important keywords using spaCy"""
    doc = nlp(text.lower())
    keywords = []
    
    # Extract nouns and proper nouns
    for token in doc:
        if token.pos_ in ['NOUN', 'PROPN'] and len(token.text) > 2:
            keywords.append(token.text)
    
    # Extract noun chunks
    for chunk in doc.noun_chunks:
        if len(chunk.text) > 3:
            keywords.append(chunk.text)
    
    return list(set(keywords))

def calculate_ats_score(similarity, matched_keywords, total_keywords):
    """Calculate ATS compatibility score"""
    keyword_match_ratio = matched_keywords / total_keywords if total_keywords > 0 else 0
    ats_score = (similarity * 0.6 + keyword_match_ratio * 0.4) * 100
    return ats_score

def get_recommendation(ats_score):
    """Get recommendation based on ATS score"""
    if ats_score >= 80:
        return "Excellent! Your resume is well-aligned with the job description."
    elif ats_score >= 60:
        return "Good match! Consider adding missing keywords to improve further."
    elif ats_score >= 40:
        return "Moderate match. Add more relevant skills and keywords."
    else:
        return "Low match. Significantly revise your resume to align with job requirements."