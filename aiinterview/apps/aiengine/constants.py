from django.db import models


class PromptTypeChoices(models.TextChoices):
    PARSE_RESUME = "parse_resume", "Parse Resume"
    PARSE_RESUME_SECTIONS = "parse_resume_sections", "Parse Resume Sections"
    SCORING_RESUME_JOB = "scoring_resume_job", "Scoring Resume Job"
    GENERATE_QUESTIONS = "generate_questions", "Generate Interview Questions"
