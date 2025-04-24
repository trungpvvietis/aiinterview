from django.contrib import admin

from .models import Job, JobInterviewConfig


class JobInterviewConfigInline(admin.StackedInline):
    model = JobInterviewConfig
    can_delete = False
    verbose_name_plural = 'Job Interview Config'
    fk_name = 'job'


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    inlines = (JobInterviewConfigInline,)
    list_display = ('name', 'get_share_link', 'description', 'status', 'created_by', 'organization', 'company', 'department', 'team')
    readonly_fields = ("get_share_link",)

    def get_share_link(self, obj):
        return obj.get_share_link()
