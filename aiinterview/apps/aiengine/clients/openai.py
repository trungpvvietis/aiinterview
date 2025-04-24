import requests
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
        model=model,
        messages=messages,
    )
    return response.choices[0].message.content


def transcribe(file_path):
    url = f"https://api.aimlapi.com/v1/stt/create"
    headers = {
        "Authorization": f"Bearer {settings.OPENAI_KEY}"
    }
    with open(file_path, "rb") as f:
        files = {"file": (file_path, f, "audio/webm")}
        data = {
            "model": "#g1_whisper-large",
        }
        response = requests.post(url, data=data, headers=headers, files=files)
        print("response = ", response.text)
        if response.status_code >= 400:
            return None
        return response.json()
