from openai import OpenAI
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

client = OpenAI(
    base_url="https://api.aimlapi.com/v1",
    api_key=settings.OPENAI_KEY,    
)

def chat(messages, model="gpt-4o"):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
    )
    return response.choices[0].message.content
