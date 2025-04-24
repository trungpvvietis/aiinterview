import json
from apps.aiengine.clients.openai import chat as openai_chat
from apps.aiengine.models import Prompt
from channels.db import database_sync_to_async
from apps.aiengine.constants import PromptTypeChoices
import logging

logger = logging.getLogger(__name__)

async def async_generate_questions(interview):
    prompt = await async_get_prompt()
    if not prompt:
        raise ValueError("Prompt not found!")
    
    job = interview.job
    if not job:
        raise ValueError("Job not found!")
        
    candidate = interview.user
    if not candidate:
        raise ValueError("Candidate not found!")
    
    resume = await async_get_resume(candidate)
    if not resume:
        raise ValueError("Resume not found!")

    if not job or not candidate or not resume:
        raise ValueError("Prompt not found!")

    previous_interview_context = ""

    content = prompt.render({
        "job_description": job.description,
        "resume_text": resume.resume_text,
        "previous_interview_context": previous_interview_context,
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
    # response = openai_chat(messages)
    # return json.loads(response)
    return {
        "question": "haa",
        "type": "tech",
    }



@database_sync_to_async
def async_get_prompt():
    return Prompt.objects.filter(type=PromptTypeChoices.GENERATE_QUESTIONS).first()

@database_sync_to_async
def async_get_resume(candidate):
    return candidate.resume_set.first()


def generate_questions(interview):
    prompt = Prompt.objects.filter(type=PromptTypeChoices.GENERATE_QUESTIONS).first()
    if not prompt:
        raise ValueError("Prompt not found!")
    
    job = interview.job
    if not job:
        raise ValueError("Job not found!")
        
    candidate = interview.user
    if not candidate:
        raise ValueError("Candidate not found!")
    
    resume = candidate.resume_set.first()
    if not resume:
        raise ValueError("Resume not found!")

    if not job or not candidate or not resume:
        raise ValueError("Prompt not found!")

    previous_interview_context = ""

    content = prompt.render({
        "job_description": job.description,
        "resume_text": resume.resume_text,
        "previous_interview_context": previous_interview_context,
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
    # response = openai_chat(messages)
    # return json.loads(response)
    return {
        "question": "haa",
        "type": "tech",
    }
