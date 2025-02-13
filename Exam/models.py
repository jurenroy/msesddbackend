# checklist/models.py
from django.db import models
from django.contrib.auth.models import User


class Exam(models.Model):
    name = models.CharField(max_length=120, blank=True, null=True)
    topic = models.CharField(max_length=120, blank=True, null=True)
    number_of_questions = models.IntegerField( blank=True, null=True)
    time = models.IntegerField(help_text="Duration of exam in minutes", blank=True, null=True)
    required_score_to_pass = models.IntegerField(help_text="required score in %", blank=True, null=True)
    
    def __str__(self):  
        return f"{self.name} - {self.topic}"
    
    def get_questions(self):
        return self.questions.all()[:self.number_of_questions]
    
    class Meta:
        verbose_name_plural = "Exams"

class Question(models.Model):
    text = models.CharField(max_length=500)
    exam = models.ForeignKey(Exam, related_name='questions', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return str(self.text)
    
    def get_answers(self):
        return self.answers.all()

class Answer(models.Model):
    choices = models.CharField(max_length=500)
    correct = models.BooleanField(default=False)
    question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)  # Correctly defined

    def __str__(self):
        return f"question: {self.question.text}, answer: {self.choices}, correct: {self.correct}"
    
    
class Result(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.FloatField()

    def __str__(self):
        return str(self.pk) 
        

