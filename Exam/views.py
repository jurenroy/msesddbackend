# checklist/views.py
from rest_framework import generics
from .models import Exam, Question, Result
from .serializers import ExamSerializer, QuestionSerializer, ResultSerializer

class ExamListCreateView(generics.ListCreateAPIView):
    queryset = Exam.objects.all()
    serializer_class = ExamSerializer

class ExamDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Exam.objects.all()
    serializer_class = ExamSerializer

class QuestionListCreateView(generics.ListCreateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

class ResultListCreateView(generics.ListCreateAPIView):
    queryset = Result.objects.all()
    serializer_class = ResultSerializer