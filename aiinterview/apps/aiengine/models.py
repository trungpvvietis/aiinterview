from jinja2 import Template
from django.db import models
from apps.core.models import Timestampable
from .constants import PromptTypeChoices


class Prompt(Timestampable):
    name = models.CharField(max_length=100, unique=True)
    type = models.CharField(max_length=50, choices=PromptTypeChoices.choices)
    system_message = models.TextField(blank=True, help_text="Optional system prompt to set assistant behavior")
    template = models.TextField(help_text="Jinja2 or plain-text prompt with variables like {{ resume_text }}")
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name

    def render(self, context: dict):
        return Template(self.template).render(context)
 