from django.db import models
from safety.models import Safety 

#The Primary Table for Exam
class Exam(models.Model):
    name = models.CharField(max_length=120, blank=True, null=True)
    topic = models.CharField(max_length=120, blank=True, null=True)
    number_of_questions = models.IntegerField( blank=True, null=True)
    time = models.IntegerField(help_text="Duration of exam in minutes", blank=True, null=True)
    required_score_to_pass = models.IntegerField(help_text="required score in %", blank=True, null=True)
    
    EXAM_TYPES = [
        ('multiple_choice', 'Multiple Choice'),
        ('matching', 'Matching Exercise'),
        ('mixed', 'Mixed Format'),
    ]
    exam_type = models.CharField(max_length=20, choices=EXAM_TYPES, default='multiple_choice')
    
    def __str__(self):  
        return f"{self.name} - {self.topic}"
    
    def get_questions(self):
        return self.questions.all()[:self.number_of_questions]
    
    class Meta:
        verbose_name_plural = "Exams"

#primary table for questions
class Question(models.Model):
    text = models.CharField(max_length=500)
    exam = models.ForeignKey(Exam, related_name='questions', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return str(self.text)
    
    def get_answers(self):
        return self.answers.all()

#multiple choices answer
class Answer(models.Model):
    choices = models.CharField(max_length=500)
    correct = models.BooleanField(default=False)
    question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)  

    def __str__(self):
        return f"question: {self.question.text}, answer: {self.choices}, correct: {self.correct}"

#results of all exams
class Result(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    tracking_code = models.CharField(max_length=100, unique=True, blank=True)
    score = models.FloatField()

    EXAM_TYPES = [
        ('multiple_choice', 'Multiple Choice'),
        ('matching', 'Matching Exercise'),
        ('Mixed', 'Mixed Combined'),
    ]

    exam_type = models.CharField(max_length=20, choices=EXAM_TYPES, default='multiple_choice')
    details = models.JSONField(null=True, blank=True, help_text="Detailed results in JSON format")

    def __str__(self):
        return f"{self.tracking_code} - {self.exam.name} - {self.score}"

    class Meta:
        indexes = [
            models.Index(fields=['tracking_code']),
            models.Index(fields=['exam']),
        ]

#for matching Exam Type
class MatchingExercise(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    title = models.CharField(max_length=500)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return (self.title)
    
class MatchingQuestion(models.Model):
    matching_exercise = models.ForeignKey(MatchingExercise, related_name='questions', on_delete=models.CASCADE)
    letter = models.CharField(max_length=5, help_text="Identifier like A, B, C, etc.")
    content = models.CharField(max_length=500)

    def __str__(self):
        return f"{self.letter}. {self.content[:30]}..."

class MatchingAnswer(models.Model):
    matching_exercise = models.ForeignKey(MatchingExercise, on_delete=models.CASCADE)
    identifier = models.CharField(max_length=5, help_text="Identifier like A, B, C, etc.")
    content = models.CharField(max_length=500)

    def __str__(self):
        return f"Answer {self.identifier}" 
    
class MatchingPair(models.Model):
    question = models.ForeignKey(MatchingQuestion, on_delete=models.CASCADE, related_name='pairs')
    correct_answer = models.ForeignKey(MatchingAnswer, on_delete=models.CASCADE, related_name='pairs')

    class Meta:
        unique_together = [['question', 'correct_answer']]
    
    def __str__(self):
        return f"{self.question.letter} -> {self.correct_answer.identifier}"

