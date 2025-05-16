from django.contrib import admin
from django.utils.html import format_html
from .models import Checklist, ChecklistStatus

# Custom admin for Checklist
class ChecklistAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'get_application_status', 'reviewed_by')
    search_fields = ('reviewed_by',)
    list_filter = ['application_form_compliance']
    
    def get_application_status(self, obj):
        # Check if this field exists
        if hasattr(obj, 'application_form_compliance'):
            if obj.application_form_compliance:
                return format_html(
                    '<div style="background-color:#4CAF50; color:white; padding:3px 10px; '
                    'text-align:center; border-radius:3px; width:60px;">Complete</div>'
                )
            return format_html(
                '<div style="background-color:#F44336; color:white; padding:3px 10px; '
                'text-align:center; border-radius:3px; width:60px;">Missing</div>'
            )
        return "N/A"
    get_application_status.short_description = 'Application Form'
    
    def get_diploma_status(self, obj):
        if hasattr(obj, 'college_diploma_compliance'):
            if obj.college_diploma_compliance:
                return format_html(
                    '<div style="background-color:#4CAF50; color:white; padding:3px 10px; '
                    'text-align:center; border-radius:3px; width:60px;">Complete</div>'
                )
            return format_html(
                '<div style="background-color:#F44336; color:white; padding:3px 10px; '
                'text-align:center; border-radius:3px; width:60px;">Missing</div>'
            )
        return "N/A"
    get_diploma_status.short_description = 'College Diploma'

# Custom admin for ChecklistStatus
class ChecklistStatusAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'get_status_bar')
    list_filter = ('status',)
    search_fields = ('status',)
    
    def get_status_bar(self, obj):
        status_colors = {
            'pending': '#FFC107',  # Yellow/amber for pending
            'approved': '#4CAF50', # Green for approved
            'rejected': '#F44336', # Red for rejected
            'review': '#2196F3',   # Blue for under review
        }
        
        # Default color if status doesn't match any known value
        color = status_colors.get(obj.status.lower() if hasattr(obj, 'status') else '', '#9E9E9E')
        
        return format_html(
            '<div style="background-color:{}; color:white; padding:3px 10px; '
            'text-align:center; border-radius:3px; width:80px;">{}</div>',
            color, obj.status.capitalize() if hasattr(obj, 'status') else 'Unknown'
        )
    get_status_bar.short_description = 'Status'

# Register with custom admin classes
admin.site.register(Checklist, ChecklistAdmin)
admin.site.register(ChecklistStatus, ChecklistStatusAdmin)