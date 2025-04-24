from celery import shared_task
from apps.resumes.models import Resume, ParsedResumeData
from apps.resumes.constants import ResumeParseStatusChoices
from apps.aiengine.services.parse_resume import parse_resume
import logging

logger = logging.getLogger(__name__)


@shared_task
def parse_resume_task(resume_id):
    try:
        resume = Resume.objects.filter(id=resume_id).first()
        if not resume:
            logger.error(f"Resume with id {resume_id} not found")
            return        
        try:
            resume_data = parse_resume(resume.resume_text)
        except Exception as e:
            logger.error(f"parse_resume error {e}")
            return
        
        logger.info(f"resume_id = {resume_id }, resume_data = {resume_data}")
        
        if resume_data:
            # Create & Update ParsedResumeData
            ParsedResumeData.objects.update_or_create(
                resume=resume,
                defaults={
                    "full_name": resume_data.get("full_name", None),
                    "email": resume_data.get("email", None),
                    "phone_number": resume_data.get("phone_number", None),
                    "address": resume_data.get("address"),
                    "linkedin_url": resume_data.get("linkedin_url", None),
                    "github_url": resume_data.get("github_url", None),
                    "birthdate": resume_data.get("birthdate", None),
                    "total_years_experience": resume_data.get("total_years_experience", None),
                    "recent_position": resume_data.get("recent_position", None),
                    "recent_company": resume_data.get("recent_company", None),
                }
            )
            # Update Resume status
            resume.parse_status = ResumeParseStatusChoices.PARSED
            resume.parse_attempts = (resume.parse_attempts or 0) + 1
            resume.save()
        logger.info(f"Parsed resume success {resume_id}")
        return f"Parsed resume success: {resume_id}"
    except Exception as e:
        logger.error(f"parse_resume_task exception {e}")
        return f"Resume not found: {resume_id}"
