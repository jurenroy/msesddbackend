from django.urls import path
from .views import ExamListCreateView, ExamDetailView, QuestionListCreateView, ResultListCreateView

app_name = 'exam'

urlpatterns = [
    path('exams/', ExamListCreateView.as_view(), name='exam-list-create'),
    path('exams/<int:pk>/', ExamDetailView.as_view(), name='exam-detail'),
    path('questions/', QuestionListCreateView.as_view(), name='question-list-create'),
    path('results/', ResultListCreateView.as_view(), name='result-list-create'),
]