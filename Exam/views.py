from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Exam, Question, Result, Answer
from .serializers import ExamSerializer, QuestionSerializer, ResultSerializer, AnswerSerializer

class ExamListCreateView(generics.ListCreateAPIView):
    queryset = Exam.objects.all()
    serializer_class = ExamSerializer

class ExamDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Exam.objects.all()
    serializer_class = ExamSerializer

@api_view(['GET'])
def exam_data_view(request, pk):
    """
    API endpoint to get exam data including questions and answers
    """
    try:
        exam = get_object_or_404(Exam, pk=pk)
        questions = []
        
        for question in exam.get_questions():
            answers = []
            for answer in question.get_answers():
                answers.append(answer.choices)
            questions.append({
                question.text: answers
            })
            
        response_data = {
            'data': questions,
            'time': exam.time,
            'exam': {
                'id': exam.id,
                'name': exam.name,
                'topic': exam.topic,
                'required_score_to_pass': exam.required_score_to_pass,
            }
        }
        
        return JsonResponse(response_data)
    
    except Exam.DoesNotExist:
        return JsonResponse({'error': 'Exam not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@api_view(['POST'])
def validate_exam_answers(request):
    """
    API endpoint to validate exam answers and return results
    """
    try:
        exam_id = request.data.get('examId')
        exam = get_object_or_404(Exam, id=exam_id)
        exam_data = request.data.get('questions', [])
        
        correct_count = 0
        total_questions = len(exam_data)
        results = []
        
        for answer_data in exam_data:
            question_text = answer_data['question']
            selected_answer = answer_data['selectedAnswer']
            
            # Get the question and its correct answer
            question = get_object_or_404(Question, text=question_text, exam=exam)
            correct_answer = question.answers.filter(correct=True).first()
            
            # Check if the selected answer matches the correct answer
            is_correct = correct_answer and selected_answer == correct_answer.choices
            if is_correct:
                correct_count += 1
                
            results.append({
                'question': question_text,
                'isCorrect': is_correct,
                'correctAnswer': correct_answer.choices if correct_answer else None
            })
        
        score_percentage = (correct_count / total_questions) * 100 if total_questions > 0 else 0
        
        # Save result if user is authenticated
        if request.user.is_authenticated:
            Result.objects.create(
                exam=exam,
                user=request.user,
                score=score_percentage
            )
        
        response_data = {
            'score': score_percentage,
            'correctAnswers': correct_count,
            'totalQuestions': total_questions,
            'results': results,
            'examName': exam.name,
            'passingScore': exam.required_score_to_pass,
            'passed': score_percentage >= exam.required_score_to_pass
        }
        
        return Response(response_data)
        
    except Question.DoesNotExist:
        return Response({'error': 'Question not found'}, status=404)
    except Exam.DoesNotExist:
        return Response({'error': 'Exam not found'}, status=404)
    except Exception as e:
        return Response({'error': str(e)}, status=500)

class QuestionListCreateView(generics.ListCreateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

class ResultListCreateView(generics.ListCreateAPIView):
    queryset = Result.objects.all()
    serializer_class = ResultSerializer

class AnswerListCreateView(generics.ListCreateAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer