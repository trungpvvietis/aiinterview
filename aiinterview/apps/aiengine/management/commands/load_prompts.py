from django.core.management.base import BaseCommand

from apps.aiengine.models import Prompt
from apps.aiengine.constants import PromptTypeChoices


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        self.stdout.write("Delete Prompt...")
        Prompt.objects.all().delete()
        
        self.stdout.write("Creating Prompt...")
        prompt_data = [
            (
                "Parse Resume",
                PromptTypeChoices.PARSE_RESUME,
                "",
                '''## Instruction: You are a AI resume parser. Extracts structured data from resumes.
Important:
- Always return only a valid JSON object.
- Do NOT include any text outside the JSON.
- Do NOT wrap with backticks, markdown, or explanation.
- If a field is missing, return null.\n
Fields to extract:
- full_name (string)
- phone_number (string)
- email (string)
- address (string)
- birth_date (string in YYYY-MM-DD format if available)
- total_years_experience (number)
- recent_position
- recent_company
- linkedin_url
- github_url

## Resume content:
{{resume_text}}

## Response:'''
,
            ),
            (
                "Parse Resume Sections",
                PromptTypeChoices.PARSE_RESUME_SECTIONS,
                "",
                '''## Instruction: You are a professional resume parser.

Your task is to extract structured information from the resume content below.

Extract and return only the following three sections:
- `skills`: a list of specific skills mentioned (e.g., Python, Django, Excel)
- `education`: a list of education records, including degree, school name, and graduation year if available
- `experience`: a list of past job experiences, including position title, company, and years if provided

Important rules:
- Only extract data that is explicitly present in the resume.
- Do not guess, generate, or infer any missing data.
- If a section is missing from the resume, return `null` for that section.
- Respond in **valid JSON format only** with keys: `skills`, `education`, and `experience`.

## Example format:
{
  "skills": string,
  "education": string,
  "experience": string
}

## Resume content:
""" {{resume_text}} """

## Response:'''
,
            ),
            (
                "Scoring Resume Job",
                PromptTypeChoices.SCORING_RESUME_JOB,
                "",
                '''## Instruction: You are an AI evaluator for job applications.

Your task is to compare a candidate's resume with a job description and score how well the candidate matches the job in four categories:

1. `skills_match` — how closely the candidate’s skills match the required skills  
2. `education_match` — how relevant the education is  
3. `experience_match` — how relevant the work experience is  
4. `overall_score` — overall fitness for the role (not just an average; you may weigh key aspects more)

Scoring rules:
- Return only a plain JSON object as your response.
- Do not include code blocks, markdown syntax (like ```json), or any explanations.  
- Each score must be a number between **0 and 100**
- Use integers or 1-decimal precision floats
- Do **not** generate or guess any missing info — only score based on content

## Example format:
{
  "skills_match": 0,
  "education_match": 0,
  "experience_match": 0,
  "overall_score": 0
}

## Resume content:
""" {{resume_text}} """

## Job description:
""" {{job_description}} """

## Response:'''
,
            ), 
            (
                "Generate Interview Questions",
                PromptTypeChoices.GENERATE_QUESTIONS,
                "",
                '''You are an AI Interview Assistant.

Your task is to generate the next best interview question based on:
1. The job description (this is the primary source of context)
2. The previous questions and the candidate's answers (if available)
3. The candidate’s resume content (skills, experience, education)

Please:
- Return only a plain JSON object as your response.
- Do not include code blocks, markdown syntax (like ```json), or any explanations. 
- Questions must be relevant and diverse
- You may include behavioral, technical, or scenario-based questions
- Prioritize what’s important for the job
- Use previous answers to ask follow-up questions when possible
- Match the tone and difficulty to the candidate’s resume
- Do **not repeat** previous question

---

Job Description:
{{job_description}}

---

Resume Content:
{{resume_text}}

---

Previous Interview Context:
{{previous_interview_context}}
---

Return your response as a JSON object:
{
  "question": "The question text here",
  "tags": "comma-separated keywords",
  "type": "technical | behavioral | follow-up"
}

---

Now generate the next best question for the interview.'''
,
            ), 
        ]
        for prompt in prompt_data:
            Prompt.objects.create(
                name=prompt[0],
                type=prompt[1],
                system_message=prompt[2],
                template=prompt[3],
            )
