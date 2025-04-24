import asyncio
from faster_whisper import WhisperModel
# import whisper
import aiofiles
from django.core.files import File
from django.conf import settings
import os
from django.db.models import Q
import json

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import InterviewSession, InterviewQuestion, InterviewAnswer
from apps.aiengine.services.generate_questions import generate_questions, async_generate_questions
from apps.aiengine.services.transcript import transcribe

from apps.jobs.models import JobInterviewConfig
from .constants import InterviewSessionStatusChoices, InterviewStatusChoices, InterviewAnswerStatusChoices

# model = whisper.load_model("turbo")
fw_model = WhisperModel("base", compute_type="float32")

class InterviewConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.current_question_id = None
        self.current_answer_file = None
        self.current_answer_file_path = None
        self.current_transcribe_answer_text = ""
        self.session_id = self.scope['url_route']['kwargs']["session_id"]
        self.room_group_name = f"interview_{self.session_id}"
        
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        
        await update_session_status(self.session_id, InterviewSessionStatusChoices.ACTIVE)

        # InterviewAnswer

        data_interview = await get_data_interview(self.session_id)
        self.current_question_id = data_interview.get("current_question")

        # prepare answer

        # update_or_create answer
        self.current_answer = await update_or_create_interview_answer(self.current_question_id)

        # prepare file
        if self.current_answer:
            file_name = f"{self.current_answer['interview_slug']}_{self.current_answer['id']}.webm"
            self.current_answer_file_path = os.path.join(settings.MEDIA_ROOT, "interviews/interview-answers/", file_name)
            
            os.makedirs(os.path.dirname(self.current_answer_file_path), exist_ok=True)
            
            self.current_answer_file = await aiofiles.open(self.current_answer_file_path, "ab")
            
            loop = asyncio.get_running_loop()
            transcript = await loop.run_in_executor(
                None, lambda: transcribe_file_sync(f"/home/trungbat/projects/aiinterview/aiinterview/{self.current_answer_file_path}")
            )
            await update_answer_text(self.current_answer['id'], transcript)
            print("transcript = ", transcript)

        await self.accept()
        await self.send(text_data=json.dumps({"message": data_interview, "type": "connect"}))

    async def disconnect(self, close_code):
        await self.current_answer_file.close()
        # Save filnal file

        await update_session_status(self.session_id, InterviewSessionStatusChoices.DISCONNECTED)
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, bytes_data=None, text_data=None):
        if bytes_data:
            print("receive bytes_data", self.current_question_id)
            if self.current_answer_file and self.current_answer_file_path:
                
                await self.current_answer_file.write(bytes_data)
                
                loop = asyncio.get_running_loop()
                transcript = await loop.run_in_executor(
                    None, lambda: transcribe_file_sync(f"/home/trungbat/projects/aiinterview/aiinterview/{self.current_answer_file_path}")
                )
                await update_answer_text(self.current_answer['id'], transcript)
                print("transcript = ", transcript)

        else:
            text_data_json = json.loads(text_data)
            message_type = text_data_json.get('type', None)
            if message_type == "start_interview":
                # Check status interview
                data_interview = await get_data_interview(self.session_id, True)
                self.current_question_id = data_interview.get("current_question")
        
                # prepare answer file
                self.current_answer = await update_or_create_interview_answer(self.current_question_id)

                # prepare file
                if self.current_answer:
                    file_name = f"{self.current_answer['interview_slug']}_{self.current_answer['id']}.webm"
                    self.current_answer_file_path = os.path.join(settings.MEDIA_ROOT, "interviews/interview-answers/", file_name)
                    os.makedirs(os.path.dirname(self.current_answer_file_path), exist_ok=True)
                    self.current_answer_file = await aiofiles.open(self.current_answer_file_path, "ab")
                    
                    loop = asyncio.get_running_loop()
                    transcript = await loop.run_in_executor(
                        None, lambda: transcribe_file_sync(f"/home/trungbat/projects/aiinterview/aiinterview/{self.current_answer_file_path}")
                    )
                    await update_answer_text(self.current_answer['id'], transcript)
                    print("transcript = ", transcript)

                await self.send(text_data=json.dumps({"message": data_interview, "type": message_type}))
            if message_type == "cancel_interview":
                interview = await get_interview(self.session_id)
                if interview.status != InterviewStatusChoices.IN_PROGRESS:
                    await self.send(text_data=json.dumps({"message": f"Trạng thái cuộc phỏng vấn đang là {interview.status} không thể cancel", "type": message_type}))
                else:
                    await update_interview_status(interview, InterviewStatusChoices.CANCELLED)
                    await self.send(text_data=json.dumps({"message": f"Cuộc phỏng vẫn đã được cancelled", "type": message_type}))


def transcribe_file_sync(file_path):
    try:
        segments, info = fw_model.transcribe(file_path, language="en")
        return " ".join(s.text for s in segments)
    except Exception as e:
        print(f"transcribe_file_sync error {e}")
        return ""


@database_sync_to_async
def update_answer_text(answer_id, transcript):
    InterviewAnswer.objects.filter(id=answer_id).update(transcript_text=transcript)


@database_sync_to_async
def update_or_create_interview_answer(question_id):
    if question_id is not None:
        question = InterviewQuestion.objects.get(id=question_id)
        interview_answer, _ = InterviewAnswer.objects.update_or_create(
            user=question.interview.user,
            interview=question.interview,
            question=question,
        )
        return {
            "interview_slug": interview_answer.interview.slug,
            "id": interview_answer.id,
        }



@database_sync_to_async
def update_interview_status(interview, status):
    interview.status = status
    interview.save()
    
    
@database_sync_to_async
def get_data_interview(session_id, auto_generate_question=False):
    data = {
        "current_question": None,
        "status": None,
    }
    interview = InterviewSession.objects.get(slug=session_id).interview
    data['status'] = interview.status
    if interview.status not in [InterviewStatusChoices.SCHEDULED, InterviewStatusChoices.IN_PROGRESS]:
        return data
    
    if interview.status == InterviewStatusChoices.SCHEDULED and auto_generate_question:
        interview.status = InterviewStatusChoices.IN_PROGRESS
        interview.save()
    
    interview_config = JobInterviewConfig.objects.get(job=interview.job)
    total_questions = InterviewQuestion.objects.filter(interview=interview).count()
    oldest_unanswered_interview_question = InterviewQuestion.objects.filter(interview=interview).filter(
        ~Q(interviewanswer__status=InterviewAnswerStatusChoices.ANSWERED)
    ).order_by("-id").first()
    
    if oldest_unanswered_interview_question:
        data["current_question"] = oldest_unanswered_interview_question.id
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
        data["current_question"] = next_interview_question.id
        data["next_interview_question"] = {
            "question_id": next_interview_question.id,
            "question_text": next_interview_question.question_text,
        }
        return data

    if total_questions >= interview_config.total_questions:
        print("total_questions >= interview_config.total_questions")

    return data
    

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
