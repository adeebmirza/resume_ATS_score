import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import docx
import re
import PyPDF2

nlp = spacy.load("en_core_web_sm")

# Parse resume from different formats (PDF, DOCX, Text)
def parse_resume(resume_file):
    resume_text = ""
    if resume_file.filename.endswith('.docx'):
        doc = docx.Document(resume_file)
        resume_text = '\n'.join([para.text for para in doc.paragraphs])
    elif resume_file.filename.endswith('.pdf'):
        pdf_reader = PyPDF2.PdfReader(resume_file)
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            resume_text += page.extract_text()
    else:
        resume_text = resume_file.read().decode('utf-8')
    
    return resume_text

# Calculate ATS score based on resume and job description
def calculate_ats_score(resume_text, job_description):
    resume_doc = nlp(resume_text)
    job_doc = nlp(job_description)
    
    # Extract key phrases from both
    resume_keywords = ' '.join([chunk.text for chunk in resume_doc.noun_chunks])
    job_keywords = ' '.join([chunk.text for chunk in job_doc.noun_chunks])
    
    # Use TF-IDF to compare text similarity
    vectorizer = TfidfVectorizer().fit_transform([resume_keywords, job_keywords])
    vectors = vectorizer.toarray()
    
    cosine_sim = cosine_similarity(vectors)
    return round(cosine_sim[0][1] * 100, 2)  # Return score as a percentage
