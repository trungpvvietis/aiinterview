from celery import shared_task
from apps.resumes.models import Resume, CVScoreSummary
from apps.jobs.models import Job
from apps.aiengine.services.scoring_resume_job import scoring_resume_job
import logging

logger = logging.getLogger(__name__)


@shared_task
def scoring_resume_job_task(job_id, resume_id):
    try:
        job = Job.objects.filter(id=job_id).first()
        if not job:
            logger.error(f"Job with id {job_id} not found")
            return  
        resume = Resume.objects.filter(id=resume_id).first()
        if not resume:
            logger.error(f"Resume with id {resume_id} not found")
            return  
         
        try:
            scoring_resume_job_data = scoring_resume_job(job.description, resume.resume_text)
            
            logger.info(f"job_id={job_id}, resume_id ={resume_id}, scoring_resume_job_data = {scoring_resume_job_data}")
            
            CVScoreSummary.objects.update_or_create(
                resume = resume,
                job = job,
                defaults={
                    'education_score': scoring_resume_job_data.get("education_match", 0),
                    'skills_score': scoring_resume_job_data.get("skills_match", 0),
                    'experience_score': scoring_resume_job_data.get("experience_match", 0),
                    'overall_cv_score': scoring_resume_job_data.get("overall_score", 0),  
                }
            )
        except Exception as e:
            logger.error(f"scoring_resume_job_task error {e}")
            return
        
        logger.info(f"scoring_resume_job_task success resume_id = {resume_id }, job_id = {job_id}")
        
        return f"Scoring resume job: resume_id = {resume_id}, job_id = {job_id}"
    except Exception as e:
        return f"scoring_resume_job_task exception: {e}"
