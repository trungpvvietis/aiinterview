from django.contrib import admin

from .models import CandidateProfile, RecruiterProfile


@admin.register(CandidateProfile)
class CandidateProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone')


@admin.register(RecruiterProfile)
class RecruiterProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'organization', 'company', 'department', 'team')
