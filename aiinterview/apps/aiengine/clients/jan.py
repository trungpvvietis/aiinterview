import json
import requests
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

def chat(messages, max_tokens=4096, temperature=0.8):
    url = settings.JAN_API_URL
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "model": "llama3.2:3b",
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "response_format": {
            "type": "json_object"
        },
    }
    res = requests.post(url, headers=headers, json=data)
    try:
        return res.json()
    except Exception as e:
        logger.error(f"JAN chat error {res} - Exception {e}")
