from django.contrib import admin

from .models import Resume, ParsedResumeData, CVScoreSummary


@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ('user', 'file', 'is_active', 'parse_status')
    readonly_fields = ("resume_text",)


@admin.register(ParsedResumeData)
class ParsedResumeDataAdmin(admin.ModelAdmin):
    list_display = ('resume', 'full_name', 'email', 'phone_number')


@admin.register(CVScoreSummary)
class CVScoreSummaryAdmin(admin.ModelAdmin):
    list_display = ('resume', 'job', 'overall_cv_score')
