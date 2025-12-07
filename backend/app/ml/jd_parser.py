"""
Job Description parser for extracting structured data from job postings.
"""
import re
from typing import Dict, Any, List, Set
import spacy

# Try to load spaCy model
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    print("spaCy model 'en_core_web_sm' not found. Please install it with: python -m spacy download en_core_web_sm")
    nlp = None


class JDParser:
    """Parser for extracting structured data from job descriptions."""
    
    def __init__(self):
        """Initialize the JD parser."""
        if nlp is None:
            raise RuntimeError("spaCy model not loaded. Please install: python -m spacy download en_core_web_sm")
        
        # Define known skills set (same as ResumeParser)
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
        
        # Requirement indicators
        self.requirement_indicators = [
            "required", "must have", "essential", "mandatory", "necessary",
            "prerequisite", "requirement", "needed"
        ]
        
        # Preferred indicators
        self.preferred_indicators = [
            "preferred", "nice to have", "bonus", "plus", "advantage",
            "desirable", "optional", "helpful"
        ]
    
    def parse(self, text: str) -> Dict[str, Any]:
        """
        Parse job description and return structured data.
        
        Args:
            text: Raw job description text
            
        Returns:
            Dictionary with parsed data
        """
        return {
            "required_skills": self._extract_skills(text, is_required=True),
            "preferred_skills": self._extract_skills(text, is_required=False),
            "experience_years": self._extract_experience_years(text),
            "education": self._extract_education_requirements(text),
            "responsibilities": self._extract_responsibilities(text),
            "keywords": self._extract_keywords(text)
        }
    
    def _extract_skills(self, text: str, is_required: bool = True) -> List[str]:
        """Extract skills matching known_skills set."""
        skills_found: Set[str] = set()
        text_lower = text.lower()
        
        # Determine which section to look in based on requirement type
        if is_required:
            # Look for required skills section
            section_pattern = r'(?:required|must have|essential|mandatory)[^.]*?[:]?\s*(.+?)(?=\n\n|\n(?:preferred|nice|bonus)|$)'
        else:
            # Look for preferred skills section
            section_pattern = r'(?:preferred|nice to have|bonus|plus)[^.]*?[:]?\s*(.+?)(?=\n\n|$)'
        
        match = re.search(section_pattern, text, re.IGNORECASE | re.DOTALL)
        section_text = match.group(1) if match else text
        
        # Match against known_skills set
        for skill in self.known_skills:
            pattern = r'\b' + re.escape(skill.lower()) + r'\b'
            if re.search(pattern, section_text.lower()):
                skills_found.add(skill)
        
        # Also search entire text if section not found
        if not skills_found:
            for skill in self.known_skills:
                pattern = r'\b' + re.escape(skill.lower()) + r'\b'
                if re.search(pattern, text_lower):
                    skills_found.add(skill)
        
        return sorted(list(skills_found))
    
    def _extract_experience_years(self, text: str) -> str:
        """Extract experience requirements using patterns."""
        patterns = [
            r'(\d+)\+?\s*years?\s*(?:of\s*)?experience',
            r'(\d+)[-\s](\d+)\s*years?\s*(?:of\s*)?experience',
            r'minimum\s*of\s*(\d+)\s*years?',
            r'at\s*least\s*(\d+)\s*years?'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                if len(match.groups()) == 2:
                    return f"{match.group(1)}-{match.group(2)} years"
                else:
                    return f"{match.group(1)}+ years"
        
        return ""
    
    def _extract_education_requirements(self, text: str) -> List[str]:
        """Extract education requirements (degree patterns)."""
        education = []
        
        degree_patterns = [
            r'(?:bachelor|b\.?s\.?|b\.?a\.?|b\.?e\.?)\s*(?:degree|in)?',
            r'(?:master|m\.?s\.?|m\.?a\.?|m\.?b\.?a)\s*(?:degree|in)?',
            r'(?:phd|ph\.?d\.?|doctorate)\s*(?:degree|in)?',
            r'(?:associate|a\.?a\.?|a\.?s\.?)\s*(?:degree|in)?'
        ]
        
        for pattern in degree_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                education.extend([m.strip() for m in matches if m.strip()])
        
        return list(set(education))  # Remove duplicates
    
    def _extract_responsibilities(self, text: str) -> List[str]:
        """Extract bullet points and numbered list items."""
        responsibilities = []
        
        # Look for responsibilities section
        resp_pattern = r'(?:responsibilities|duties|key\s+responsibilities)[:\s]+\n?(.+?)(?=\n\s*[A-Z][^:]+:|$)'
        match = re.search(resp_pattern, text, re.IGNORECASE | re.DOTALL)
        
        section_text = match.group(1) if match else text
        
        # Extract bullet points
        bullet_pattern = r'(?:^|\n)\s*[•\-\*·]\s*(.+?)(?=\n\s*[•\-\*·]|\n\n|$)'
        bullets = re.findall(bullet_pattern, section_text, re.MULTILINE)
        responsibilities.extend([b.strip() for b in bullets if b.strip()])
        
        # Extract numbered items
        numbered_pattern = r'(?:^|\n)\s*\d+[\.\)]\s*(.+?)(?=\n\s*\d+[\.\)]|\n\n|$)'
        numbered = re.findall(numbered_pattern, section_text, re.MULTILINE)
        responsibilities.extend([n.strip() for n in numbered if n.strip()])
        
        return responsibilities[:15]  # Limit to 15 items
    
    def _extract_keywords(self, text: str) -> List[str]:
        """
        Extract keywords using spaCy noun chunks, named entities, and known skills.
        """
        keywords: Set[str] = set()
        
        # Add skills from known_skills
        text_lower = text.lower()
        for skill in self.known_skills:
            if re.search(r'\b' + re.escape(skill.lower()) + r'\b', text_lower):
                keywords.add(skill)
        
        # Use spaCy for noun chunks and named entities
        if nlp:
            doc = nlp(text)
            
            # Extract noun chunks (phrases)
            for chunk in doc.noun_chunks:
                if len(chunk.text) > 3 and chunk.text.lower() not in ['the', 'a', 'an']:
                    keywords.add(chunk.text.lower())
            
            # Extract named entities (ORG, PRODUCT)
            for ent in doc.ents:
                if ent.label_ in ["ORG", "PRODUCT", "TECH"]:
                    keywords.add(ent.text.lower())
        
        # Filter out common stop words
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}
        keywords = {k for k in keywords if k not in stop_words and len(k) > 2}
        
        return sorted(list(keywords))[:50]  # Limit to top 50 keywords

