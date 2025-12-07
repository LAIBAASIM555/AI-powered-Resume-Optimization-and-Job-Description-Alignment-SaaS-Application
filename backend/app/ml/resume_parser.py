"""
Resume parser for extracting text and structured data from resume files.
"""
import re
import uuid
from typing import Tuple, Dict, Any, List, Set
import fitz  # PyMuPDF
from docx import Document
import spacy

# Try to load spaCy model, download if not available
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    print("spaCy model 'en_core_web_sm' not found. Please install it with: python -m spacy download en_core_web_sm")
    nlp = None


class ResumeParser:
    """Parser for extracting and structuring resume data."""
    
    def __init__(self):
        """Initialize the resume parser."""
        # Load spaCy model
        if nlp is None:
            raise RuntimeError("spaCy model not loaded. Please install: python -m spacy download en_core_web_sm")
        
        # Define known skills set
        self.known_skills: Set[str] = {
            # Programming Languages
            "python", "java", "javascript", "typescript", "c++", "c#", "c", "go", "rust",
            "ruby", "php", "swift", "kotlin", "scala", "r", "matlab", "perl", "shell",
            "bash", "powershell",
            
            # Web Technologies
            "react", "angular", "vue", "node.js", "express", "django", "flask", "fastapi",
            "spring", "asp.net", "laravel", "symfony", "rails", "next.js", "nuxt.js",
            "html", "css", "sass", "less", "bootstrap", "tailwind", "jquery",
            
            # Databases
            "sql", "mysql", "postgresql", "mongodb", "redis", "cassandra", "elasticsearch",
            "oracle", "sqlite", "dynamodb", "neo4j", "firebase",
            
            # Cloud/DevOps
            "aws", "azure", "gcp", "docker", "kubernetes", "jenkins", "git", "github",
            "gitlab", "ci/cd", "terraform", "ansible", "chef", "puppet", "nginx",
            "apache", "linux", "unix",
            
            # Data Science
            "machine learning", "deep learning", "tensorflow", "pytorch", "keras",
            "pandas", "numpy", "scikit-learn", "jupyter", "data analysis", "data science",
            "nlp", "computer vision", "statistics",
            
            # Other
            "agile", "scrum", "kanban", "rest api", "graphql", "microservices",
            "api development", "testing", "tdd", "bdd"
        }
    
    def parse(self, file_path: str, file_type: str) -> Tuple[str, Dict[str, Any]]:
        """
        Main parsing method.
        
        Args:
            file_path: Path to the resume file
            file_type: Type of file ('pdf' or 'docx')
            
        Returns:
            Tuple of (raw_text, parsed_data dictionary)
        """
        # Extract text based on file type
        if file_type.lower() == "pdf":
            raw_text = self._extract_pdf_text(file_path)
        elif file_type.lower() == "docx":
            raw_text = self._extract_docx_text(file_path)
        else:
            raise ValueError(f"Unsupported file type: {file_type}")
        
        # Parse sections from text
        parsed_data = self._parse_sections(raw_text)
        
        return raw_text, parsed_data
    
    def _extract_pdf_text(self, file_path: str) -> str:
        """Extract text from PDF using PyMuPDF (fitz)."""
        try:
            doc = fitz.open(file_path)
            text = ""
            for page in doc:
                text += page.get_text()
            doc.close()
            return text
        except Exception as e:
            raise ValueError(f"Error extracting PDF text: {str(e)}")
    
    def _extract_docx_text(self, file_path: str) -> str:
        """Extract text from DOCX using python-docx."""
        try:
            doc = Document(file_path)
            text = ""
            for para in doc.paragraphs:
                text += para.text + "\n"
            return text
        except Exception as e:
            raise ValueError(f"Error extracting DOCX text: {str(e)}")
    
    def _parse_sections(self, text: str) -> Dict[str, Any]:
        """
        Parse resume into sections.
        
        Returns:
            Dictionary with parsed sections
        """
        return {
            "name": self._extract_name(text),
            "email": self._extract_email(text),
            "phone": self._extract_phone(text),
            "summary": self._extract_summary(text),
            "skills": self._extract_skills(text),
            "education": self._extract_education(text),
            "experience": self._extract_experience(text)
        }
    
    def _extract_name(self, text: str) -> str:
        """Extract name from first lines (usually 1-4 words, no email/phone)."""
        lines = text.split('\n')[:5]  # Check first 5 lines
        for line in lines:
            line = line.strip()
            if line and len(line.split()) <= 4:
                # Check if it doesn't contain email or phone patterns
                if not re.search(r'@|[\d\-\(\)]+', line):
                    return line
        return ""
    
    def _extract_email(self, text: str) -> str:
        """Extract email using regex pattern."""
        pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        match = re.search(pattern, text)
        return match.group(0) if match else ""
    
    def _extract_phone(self, text: str) -> str:
        """Extract phone number using multiple regex patterns."""
        patterns = [
            r'\+?1?[-.\s]?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',  # US format
            r'\+?\d{1,3}[-.\s]?\d{1,4}[-.\s]?\d{1,4}[-.\s]?\d{1,9}',  # International
            r'\(\d{3}\)\s?\d{3}[-.\s]?\d{4}',  # (123) 456-7890
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(0)
        return ""
    
    def _extract_summary(self, text: str) -> str:
        """Extract summary/objective section."""
        # Look for common section headers
        summary_patterns = [
            r'(?:summary|objective|profile|about)[:\s]+\n?(.+?)(?=\n\s*[A-Z][^:]+:|$)',
            r'(?:professional\s+summary|career\s+objective)[:\s]+\n?(.+?)(?=\n\s*[A-Z][^:]+:|$)'
        ]
        
        for pattern in summary_patterns:
            match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
            if match:
                summary = match.group(1).strip()
                # Limit to first 500 characters
                return summary[:500] if len(summary) > 500 else summary
        
        return ""
    
    def _extract_skills(self, text: str) -> List[str]:
        """
        Extract skills by matching against known_skills set and using spaCy.
        
        Returns:
            List of extracted skills
        """
        skills_found: Set[str] = set()
        text_lower = text.lower()
        
        # Match against known_skills set (case-insensitive word boundary match)
        for skill in self.known_skills:
            # Use word boundary to avoid partial matches
            pattern = r'\b' + re.escape(skill.lower()) + r'\b'
            if re.search(pattern, text_lower):
                skills_found.add(skill)
        
        # Use spaCy NER for ORG and PRODUCT entities
        if nlp:
            doc = nlp(text)
            for ent in doc.ents:
                if ent.label_ in ["ORG", "PRODUCT"]:
                    # Check if it's a known skill
                    ent_lower = ent.text.lower()
                    for skill in self.known_skills:
                        if skill.lower() in ent_lower or ent_lower in skill.lower():
                            skills_found.add(skill)
                            break
        
        return sorted(list(skills_found))
    
    def _extract_education(self, text: str) -> List[str]:
        """Extract education section."""
        education = []
        
        # Look for education section
        edu_pattern = r'(?:education|academic|qualifications)[:\s]+\n?(.+?)(?=\n\s*[A-Z][^:]+:|$)'
        match = re.search(edu_pattern, text, re.IGNORECASE | re.DOTALL)
        
        if match:
            edu_text = match.group(1)
            # Extract degree patterns
            degree_patterns = [
                r'(?:bachelor|master|phd|doctorate|m\.?b\.?a|b\.?s\.?c|m\.?s\.?c)[^\n]*',
                r'(?:degree|diploma|certificate)[^\n]*'
            ]
            
            for pattern in degree_patterns:
                matches = re.findall(pattern, edu_text, re.IGNORECASE)
                education.extend(matches)
        
        return education[:5]  # Limit to 5 entries
    
    def _extract_experience(self, text: str) -> List[str]:
        """Extract work experience section."""
        experience = []
        
        # Look for experience section
        exp_pattern = r'(?:experience|work\s+history|employment|career)[:\s]+\n?(.+?)(?=\n\s*[A-Z][^:]+:|$)'
        match = re.search(exp_pattern, text, re.IGNORECASE | re.DOTALL)
        
        if match:
            exp_text = match.group(1)
            # Extract bullet points and job entries
            # Look for lines starting with bullet points or dates
            lines = exp_text.split('\n')
            for line in lines:
                line = line.strip()
                if line and (line.startswith(('•', '-', '*', '·')) or re.match(r'\d{4}', line)):
                    experience.append(line)
        
        return experience[:10]  # Limit to 10 entries

