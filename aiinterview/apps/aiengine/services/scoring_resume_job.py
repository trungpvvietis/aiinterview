import json
from apps.aiengine.clients.openai import chat as openai_chat
from apps.aiengine.models import Prompt
from apps.aiengine.constants import PromptTypeChoices
import logging

logger = logging.getLogger(__name__)

def scoring_resume_job(job_description, resume_text):
    prompt = Prompt.objects.filter(type=PromptTypeChoices.SCORING_RESUME_JOB).first()
    if not prompt:
        raise ValueError("Prompt not found!")
    
    content = prompt.render({
        "job_description": job_description,
        "resume_text": resume_text,
    })
    messages = [{
        "role": "user",
        "content": content,
    }]
    if prompt.system_message:
        messages.append({
            "role": "system",
            "content": prompt.system_message,
        })
    response = openai_chat(messages)
    return json.loads(response)
