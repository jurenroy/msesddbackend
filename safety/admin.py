from django.contrib import admin
from django.utils.html import format_html
from .models import Safety, SafetyFile, Education, BoardExam, WorkExperience, Training

@admin.register(Safety)
class SafetyAdmin(admin.ModelAdmin):
    list_display = ['name', 'tracking_code', 'email', 'date', 'age', 'permit_status', 'file_count']
    list_display_links = ['name', 'tracking_code']  # Make these fields clickable
    search_fields = ['name', 'tracking_code', 'email']
    list_filter = ['permit_type', 'date', 'compliance', 'understanding']
    ordering = ['-date']  # Newest first
    list_per_page = 20   # Records per page
    
    def permit_status(self, obj):
        if obj.compliance and obj.understanding and obj.certify:
            return format_html('<span style="color: green;">✓ Complete</span>')
        return format_html('<span style="color: red;">✗ Incomplete</span>')
    permit_status.short_description = 'Status'

    def file_count(self, obj):
        count = obj.files.count()
        return format_html('<b>{}</b> files', count)
    file_count.short_description = 'Files'

@admin.register(SafetyFile)
class SafetyFileAdmin(admin.ModelAdmin):
    list_display = ['safety', 'file_type', 'description', 'uploaded_at', 'file_preview']
    list_filter = ['file_type', 'uploaded_at']
    search_fields = ['safety__name', 'safety__tracking_code', 'description']
    ordering = ['-uploaded_at']
    list_per_page = 20

    def file_preview(self, obj):
        if obj.file:
            return format_html('<a href="{}" target="_blank">View File</a>', obj.file.url)
        return "No file"
    file_preview.short_description = 'Preview'

@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ['safety', 'school_name', 'degree', 'year_completed', 'major']
    search_fields = ['safety__name', 'school_name', 'degree']
    list_filter = ['year_completed']
    ordering = ['-year_completed']
    list_per_page = 20

@admin.register(BoardExam)
class BoardExamAdmin(admin.ModelAdmin):
    list_display = ['safety', 'exam_name', 'date_taken', 'license_number', 'expiry_status']
    search_fields = ['safety__name', 'exam_name', 'license_number']
    list_filter = ['date_taken', 'expiry_date']
    ordering = ['-date_taken']
    list_per_page = 20

    def expiry_status(self, obj):
        from django.utils import timezone
        if obj.expiry_date:
            if obj.expiry_date < timezone.now().date():
                return format_html('<span style="color: red;">Expired</span>')
            return format_html('<span style="color: green;">Valid</span>')
        return "No expiry date"
    expiry_status.short_description = 'Status'

@admin.register(WorkExperience)
class WorkExperienceAdmin(admin.ModelAdmin):
    list_display = ['safety', 'company_name', 'position', 'duration', 'current_job']
    search_fields = ['safety__name', 'company_name', 'position']
    list_filter = ['start_date', 'end_date']
    ordering = ['-start_date']
    list_per_page = 20

    def duration(self, obj):
        if obj.end_date:
            duration = obj.end_date - obj.start_date
            return f"{duration.days // 365} years, {(duration.days % 365) // 30} months"
        return "Ongoing"
    duration.short_description = 'Duration'

    def current_job(self, obj):
        return not obj.end_date
    current_job.boolean = True
    current_job.short_description = 'Current'

@admin.register(Training)
class TrainingAdmin(admin.ModelAdmin):
    list_display = ['safety', 'training_name', 'provider', 'date_completed', 'has_certificate']
    search_fields = ['safety__name', 'training_name', 'provider']
    list_filter = ['date_completed']
    ordering = ['-date_completed']
    list_per_page = 20

    def has_certificate(self, obj):
        return bool(obj.certificate_number)
    has_certificate.boolean = True
    has_certificate.short_description = 'Certificate'