from django.contrib import admin
from .models import Checklist, ChecklistStatus  # Import your models

# Register your models here
admin.site.register(Checklist)
admin.site.register(ChecklistStatus)