import fitz
from docx import Document
import logging

logger = logging.getLogger(__name__)


def read_resume(file_field):
    if not file_field:
        return ""
    
    file_type = file_field.name.lower().split('.')[-1]
    if file_type == 'pdf':
        resume_text = extract_text_from_pdf(file_field)
    elif file_type == 'docx':
        resume_text = extract_text_from_docx(file_field)
    else:
        resume_text = file_field.read().decode("utf-8")
    return resume_text
        

def extract_text_from_pdf(file):
    text = ""
    try:
        with fitz.open(stream=file.read(), filetype="pdf") as doc:
            for page in doc:
                text += page.get_text()
    except Exception as e:
        logger.error(f"extract_text_from_pdf error {e}")
    return text


def extract_text_from_docx(file):
    text = ""
    try:
        doc = Document(file)
        text = "\n".join(p.text for p in doc.paragraphs)
    except Exception as e:
        logger.error(f"extract_text_from_docx error {e}")
    return text
