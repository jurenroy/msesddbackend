from django.contrib import admin
from .models import Safety, EducationFile, BoardExamFile, WorkExperienceFile, TrainingFile, NotarizedFile
 # Import your models

# Register your models here
admin.site.register(Safety)
admin.site.register(EducationFile)
admin.site.register(BoardExamFile)
admin.site.register(WorkExperienceFile)
admin.site.register(TrainingFile)
admin.site.register(NotarizedFile)