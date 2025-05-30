# checklist/serializers.py
from rest_framework import serializers
from .models import Exam, Question, Answer, Result, MatchingExercise, MatchingQuestion, MatchingPair, MatchingAnswer

class MatchingAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = MatchingAnswer
        fields = ['id', 'identifier', 'matching_exercise']

class MatchingPairSerializer(serializers.ModelSerializer):
    correct_answer = MatchingAnswerSerializer(read_only=True)

    class Meta:
        model = MatchingPair
        fields = ['id', 'question', 'correct_answer']

class MatchingQuestionSerializer(serializers.ModelSerializer):
    pairs = MatchingPairSerializer(many=True, read_only=True)

    class Meta:
        model = MatchingQuestion
        fields = ['id','letter','content','matching_exercise','pairs']

class MatchingExerciseSerializer(serializers.ModelSerializer):
    questions = MatchingQuestionSerializer(many=True, read_only=True)

    class Meta:
        model = MatchingExercise
        fields = '__all__'

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
    matching_questions = serializers.SerializerMethodField()

    class Meta:
        model = Exam
        fields = '__all__'

    def get_matching_questions(self, obj):
        if obj.exam_type in ['matching', 'mixed']:
            matching_questions = MatchingQuestion.objects.filter(
                matching_exercise__exam=obj
            )
            return MatchingQuestionSerializer(matching_questions, many=True).data
        return []

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        
        if instance.exam_type == 'multiple_choice':
            representation['questions'] = QuestionSerializer(
                Question.objects.filter(exam=instance), 
                many=True
            ).data
        elif instance.exam_type == 'matching':
            representation['questions'] = self.get_matching_questions(instance)
        elif instance.exam_type == 'mixed':
            # Combine multiple choice and matching questions
            multiple_choice = QuestionSerializer(
                Question.objects.filter(exam=instance), 
                many=True
            ).data
            matching = self.get_matching_questions(instance)
            representation['questions'] = multiple_choice + matching
        
        return representation

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
    # For multiple choice
    questions = serializers.ListField(
        child=serializers.DictField(),
        required=False
    )
    # For matching
    pairs = serializers.ListField(
        child=serializers.DictField(),
        required=False
    )
    
    def validate(self, data):
        exam_id = data.get('examId')
        try:
            exam = Exam.objects.get(id=exam_id)
            
            if exam.exam_type == 'multiple_choice' and not data.get('questions'):
                raise serializers.ValidationError("'questions' field is required for multiple choice exams")
            elif exam.exam_type == 'matching' and not data.get('pairs'):
                raise serializers.ValidationError("'pairs' field is required for matching exams")
            elif exam.exam_type == 'mixed':
                if not data.get('questions') and not data.get('pairs'):
                    raise serializers.ValidationError("At least one of 'questions' or 'pairs' must be provided")
        except Exam.DoesNotExist:
            raise serializers.ValidationError("Exam not found")
            
        return data
