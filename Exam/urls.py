from django.urls import path
from .views import (
    ExamListCreateView, 
    ExamDetailView, 
    ResultListCreateView,
    exam_data_view,
    validate_exam_answers,
)

app_name = 'exam'

urlpatterns = [
    path('',ExamListCreateView.as_view(), name='exam-list-create'),
    path('<int:pk>/', ExamDetailView.as_view(), name='exam-detail'),
    path('<int:pk>/data/', exam_data_view, name='exam-data'),
    path('results/', ResultListCreateView.as_view(), name='result-list-create'),
    path('validate/', validate_exam_answers, name='validate-exam')
]   