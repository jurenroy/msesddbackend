# checklist/serializers.py
from rest_framework import serializers
from .models import Exam, Question, Answer, Result

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = '__all__'  

class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = '__all__' 

class ExamSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Exam
        fields = '__all__' 

class ResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Result
        fields = '__all__'  