import json
from apps.aiengine.clients.jan import chat
from apps.aiengine.clients.openai import chat as openai_chat
from apps.aiengine.models import Prompt
from apps.aiengine.constants import PromptTypeChoices
import logging

logger = logging.getLogger(__name__)

def parse_resume2(resume_text):
    prompt = Prompt.objects.filter(type=PromptTypeChoices.PARSE_RESUME).first()
    if not prompt:
        raise ValueError("Prompt not found!")
    content = prompt.render({"resume_text": resume_text})
    messages = [{
        "role": "user",
        "content": content,
    }]
    if prompt.system_message:
        messages.append({
            "role": "system",
            "content": prompt.system_message,
        })
    response = chat(messages)
    return json.loads(response['choices'][0]['message']['content'])


def parse_resume(resume_text):
    prompt = Prompt.objects.filter(type=PromptTypeChoices.PARSE_RESUME).first()
    if not prompt:
        raise ValueError("Prompt not found!")
    content = prompt.render({"resume_text": resume_text})
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
