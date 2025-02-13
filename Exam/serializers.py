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

    def validate_answers(self, value):
        if not any(answer['correct'] for answer in value):
            raise serializers.ValidationError("At least one answer must be marked as correct.")
        return value

class ExamSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Exam
        fields = '__all__' 

class ResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Result
        fields = '__all__'
        read_only_fields = ['user']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

class ExamAnswerSerializer(serializers.Serializer):
    question = serializers.CharField()
    selectedAnswer = serializers.CharField()

class ValidateExamAnswersSerializer(serializers.Serializer):
    examId = serializers.IntegerField()
    questions = ExamAnswerSerializer(many=True)

    def validate_questions(self, value):
        for question in value:
            if 'question' not in question or 'selectedAnswer' not in question:
                raise serializers.ValidationError("Each question must have a 'question' and 'selectedAnswer'.")
        return value