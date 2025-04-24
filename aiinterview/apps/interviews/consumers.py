import json

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import InterviewSession, InterviewQuestion
from apps.aiengine.services.generate_questions import generate_questions, async_generate_questions
from apps.jobs.models import JobInterviewConfig
from .constants import InterviewSessionStatusChoices, InterviewStatusChoices

class InterviewConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.session_id = self.scope['url_route']['kwargs']["session_id"]
        self.room_group_name = f"interview_{self.session_id}"
        
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        
        await self.accept()

        await update_session_status(self.session_id, InterviewSessionStatusChoices.ACTIVE)

        data_interview = await get_data_interview(self.session_id)
        await self.send(text_data=json.dumps({"message": data_interview, "type": "connect"}))

    async def disconnect(self, close_code):
        await update_session_status(self.session_id, InterviewSessionStatusChoices.DISCONNECTED)
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, bytes_data=None, text_data=None):
        if bytes_data:
            print("receive bytes_data")
            return
        else:
            text_data_json = json.loads(text_data)
            message_type = text_data_json.get('type', None)
            if message_type == "start_interview":
                # Check status interview
                data_interview = await get_data_interview(self.session_id, True)
                await self.send(text_data=json.dumps({"message": data_interview, "type": message_type}))
            if message_type == "cancel_interview":
                interview = await get_interview(self.session_id)
                if interview.status != InterviewStatusChoices.IN_PROGRESS:
                    await self.send(text_data=json.dumps({"message": f"Trạng thái cuộc phỏng vấn đang là {interview.status} không thể cancel", "type": message_type}))
                else:
                    await update_interview_status(interview, InterviewStatusChoices.CANCELLED)
                    await self.send(text_data=json.dumps({"message": f"Cuộc phỏng vẫn đã được cancelled", "type": message_type}))


@database_sync_to_async
def update_interview_status(interview, status):
    interview.status = status
    interview.save()
    
    
@database_sync_to_async
def get_data_interview(session_id, auto_generate_question=False):
    data = {
        "status": None,
    }
    interview = InterviewSession.objects.get(slug=session_id).interview
    data['status'] = interview.status
    if interview.status not in [InterviewStatusChoices.SCHEDULED, InterviewStatusChoices.IN_PROGRESS]:
        return data
    
    interview_config = JobInterviewConfig.objects.get(job=interview.job)
    total_questions = InterviewQuestion.objects.filter(interview=interview).count()
    oldest_unanswered_interview_question = InterviewQuestion.objects.filter(interview=interview, interviewanswer__isnull=True).order_by("-id").first()
    
    if oldest_unanswered_interview_question:
        data["unanswered_question"] = {
            "question_id": oldest_unanswered_interview_question.id,
            "question_text": oldest_unanswered_interview_question.question_text,
        }
        return data
    
    is_generate_question = total_questions < interview_config.total_questions and (interview.status != InterviewStatusChoices.SCHEDULED or auto_generate_question)
    if is_generate_question:
        question_data = generate_questions(interview)
        next_interview_question = InterviewQuestion.objects.create(
             interview=interview,
             question_text=question_data["question"],
             question_type=question_data.get("type", None),
        )
        data["next_interview_question"] = {
            "question_id": next_interview_question.id,
            "question_text": next_interview_question.question_text,
        }
        return data
    if total_questions >= interview_config.total_questions:
        print("total_questions >= interview_config.total_questions")
    

@database_sync_to_async
def get_interview(interview_session_slug):
    return InterviewSession.objects.get(slug=interview_session_slug).interview


@database_sync_to_async
def update_session_status(slug, status):
    return InterviewSession.objects.filter(slug=slug).update(status=status)


@database_sync_to_async
def get_interview_session(slug):
    return InterviewSession.objects.select_related("interview", "interview__job", "interview__user").get(slug=slug)


@database_sync_to_async
def create_interview_questions(interview, question_data):
    return InterviewQuestion.objects.create(
             interview=interview,
             question_text=question_data["question"],
             question_type=question_data.get("type", None),
    )
