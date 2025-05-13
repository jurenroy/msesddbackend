from django.contrib import admin
from django.utils.html import format_html
from .models import Exam, Question, Answer, Result, MatchingExercise, MatchingPair, MatchingQuestion, MatchingAnswer

@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ['tracking_code', 'exam_title', 'score_display', 'status_badge', 'created_at_display']
    list_filter = ['passed', 'exam', 'created_at']
    search_fields = ['tracking_code', 'exam__title']
    readonly_fields = ['created_at']
    ordering = ['-created_at']
    
    def exam_title(self, obj):
        return obj.exam.title
    exam_title.short_description = 'Exam'
    
    def score_display(self, obj):
        width = min(obj.score, 100)
        color = '#28a745' if obj.passed else '#dc3545'
        score = int(obj.score)
        return format_html(
            '<div style="width: 100px; background-color: #f0f0f0; border-radius: 10px;">'
            '<div style="width: {}px; background-color: {}; height: 20px; border-radius: 10px;">'
            '<div style="padding-left: 5px; color: black;">{}</div>'
            '</div></div>',
            width,
            color,
            f"{score}%"
        )
    score_display.short_description = 'Score'

    def status_badge(self, obj):
        if obj.passed:
            return format_html(
                '<span style="background-color: #28a745; color: white; padding: 3px 10px; '
                'border-radius: 10px;">PASSED</span>'
            )
        return format_html(
            '<span style="background-color: #dc3545; color: white; padding: 3px 10px; '
            'border-radius: 10px;">FAILED</span>'
        )
    status_badge.short_description = 'Status'

    def created_at_display(self, obj):
        from django.utils import timezone
        
        if obj.created_at:
            now = timezone.now()
            time_diff = now - obj.created_at
            
            if time_diff.days == 0:
                if time_diff.seconds < 3600:
                    minutes = time_diff.seconds // 60
                    return f"{minutes} minutes ago"
                else:
                    hours = time_diff.seconds // 3600
                    return f"{hours} hours ago"
            elif time_diff.days == 1:
                return "Yesterday"
            elif time_diff.days < 7:
                return f"{time_diff.days} days ago"
            else:
                return obj.created_at.strftime("%Y-%m-%d %H:%M")
        return "-"
    created_at_display.short_description = 'Taken'

@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ['title', 'exam_type', 'question_count', 'time_limit', 'required_score_to_pass']
    list_filter = ['exam_type', 'created_at']
    search_fields = ['title', 'description']
    
    def question_count(self, obj):
        count = obj.get_questions_count()
        return format_html(
            '<span style="background-color: #17a2b8; color: white; padding: 3px 10px; '
            'border-radius: 10px;">{}</span>',
            count
        )
    question_count.short_description = 'Questions'

class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 4

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['text', 'exam', 'answer_count']
    list_filter = ['exam']
    search_fields = ['text', 'exam__title']
    inlines = [AnswerInline]
    
    def answer_count(self, obj):
        count = obj.answers.count()
        return format_html(
            '<span style="background-color: #6c757d; color: white; padding: 3px 10px; '
            'border-radius: 10px;">{}</span>',
            count
        )
    answer_count.short_description = 'Answers'

# Register remaining models
admin.site.register(Answer)
admin.site.register(MatchingExercise)
admin.site.register(MatchingPair)
admin.site.register(MatchingQuestion)
admin.site.register(MatchingAnswer)