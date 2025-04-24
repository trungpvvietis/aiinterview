from django.contrib import admin

from .models import Interview, InterviewQuestion, InterviewAnswer, InterviewScoreSummary, InterviewSession

@admin.register(Interview)
class InterviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'job', 'slug', 'status', 'interview_type')
    readonly_fields = ("share_token",)


@admin.register(InterviewQuestion)
class InterviewQuestionAdmin(admin.ModelAdmin):
    list_display = ('interview', 'question_text', 'question_image', 'question_type')


@admin.register(InterviewAnswer)
class InterviewAnswerAdmin(admin.ModelAdmin):
    list_display = ('interview', 'question', 'answer_text', 'transcript_text', 'status')


@admin.register(InterviewScoreSummary)
class InterviewScoreSummaryAdmin(admin.ModelAdmin):
    list_display = ('user', 'interview', 'overall_score')


@admin.register(InterviewSession)
class InterviewSessionAdmin(admin.ModelAdmin):
    list_display = ('slug', 'user', 'interview', 'status')
