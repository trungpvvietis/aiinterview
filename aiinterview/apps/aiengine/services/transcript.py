import json
from apps.aiengine.clients.openai import chat as openai_chat, transcribe as openai_transcribe
from apps.aiengine.models import Prompt
from channels.db import database_sync_to_async
from apps.aiengine.constants import PromptTypeChoices
import logging

logger = logging.getLogger(__name__)

def transcribe(file_path):
    response = openai_transcribe(file_path)
    return response