from django.contrib import admin
from .models import Exam, Question, Answer, Result  # Import your models

# Register your models here
admin.site.register(Exam)
admin.site.register(Result)

# Admin import
class AnswerInLine(admin.TabularInline):
    model = Answer

class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInLine]

admin.site.register(Question, QuestionAdmin)