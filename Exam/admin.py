from django.contrib import admin
from .models import Exam, Question, Answer, Result, MatchingExercise, MatchingPair, MatchingQuestion, MatchingAnswer # Import your models

# Register your models here
admin.site.register(Exam)
admin.site.register(Result)
admin.site.register(Answer)
admin.site.register(MatchingExercise)
admin.site.register(MatchingPair)
admin.site.register(MatchingQuestion)
admin.site.register(MatchingAnswer)

# Admin import
class AnswerInLine(admin.TabularInline):
    model = Answer

class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInLine]

admin.site.register(Question, QuestionAdmin)