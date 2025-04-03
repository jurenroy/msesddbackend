from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Exam, Question, Result, Answer, MatchingExercise, MatchingAnswer, Safety, MatchingPair
from .serializers import ExamSerializer, QuestionSerializer, ResultSerializer, AnswerSerializer, MatchingExerciseSerializer
import math

class ExamListCreateView(generics.ListCreateAPIView):
    queryset = Exam.objects.all()
    serializer_class = ExamSerializer

class ExamDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Exam.objects.all()
    serializer_class = ExamSerializer

@api_view(['GET'])
def exam_data_view(request):
    """
    API endpoint to get a list of all exams using Django REST Framework
    """
    try:
        # Retrieve all exams
        exams = Exam.objects.all()
        
        # Prepare the response data
        exam_list = []
        for exam in exams:
            exam_data = {
                'id': exam.id,
                'title': exam.title,
                'description': exam.description,
                'exam_type': exam.exam_type,
                'time_limit': exam.time_limit,
                'required_score_to_pass': exam.required_score_to_pass,
                'questions_count': exam.get_questions_count(),
                'total_marks': exam.get_total_marks(),
                'created_at': exam.created_at.isoformat() if exam.created_at else None,
                'updated_at': exam.updated_at.isoformat() if exam.updated_at else None
            }
            exam_list.append(exam_data)
        
        return Response({
            'exams': exam_list,
            'total_exams': len(exam_list)
        })

    except Exception as e:
        return Response(
            {'error': str(e)}
        )

@api_view(['POST'])
def validate_exam_answers(request):
    """
    API endpoint to validate both multiple-choice and matching exam answers
    """
    try:
        exam_id = request.data.get('examId')
        tracking_code = request.data.get('trackingCode')
        exam_type = request.data.get('exam_type', 'multiple_choice')
        
        exam = get_object_or_404(Exam, id=exam_id)
        
        # Initialize result counters
        mc_correct_count = 0
        mc_total_questions = 0
        matching_correct_count = 0
        matching_total_questions = 0
        mc_results = []
        matching_results = []
        
        # Process multiple-choice questions
        mc_questions = request.data.get('questions', [])
        if mc_questions:
            mc_total_questions = len(mc_questions)
            
            for answer_data in mc_questions:
                question_id = answer_data.get('question_id')
                question_text = answer_data.get('question')
                selected_answer = answer_data.get('selectedAnswer')
        
                if selected_answer is None:
                    continue
                
                # Get the question using id or text
                if question_id:
                    question = get_object_or_404(Question, id=question_id, exam=exam)
                else:
                    question = get_object_or_404(Question, text=question_text, exam=exam)
                    
                correct_answer = question.answers.filter(correct=True).first()
                
                # Check if the selected answer matches the correct answer
                is_correct = False
                if correct_answer and selected_answer:
                    is_correct = selected_answer == correct_answer.choices
                
                if is_correct:
                    mc_correct_count += 1
                    
                mc_results.append({
                    'question': question_text,
                    'isCorrect': is_correct,
                    'correctAnswer': correct_answer.choices if correct_answer else None
                })
        
        matching_questions = request.data.get('matching_questions', [])
        if matching_questions:
            matching_total_questions = len(matching_questions)

            # Create to store correct pairings
            correct_pairings = {}
            matching_exercises = MatchingExercise.objects.filter(exam=exam)
            
            for matching_exercise in matching_exercises:
                questions = matching_exercise.questions.all()
                
                # For each question, find its correct answer
                for question in questions:
                    try:
                        matching_pair = MatchingPair.objects.get(question=question)
                        correct_pairings[question.id] = matching_pair.correct_answer.id
                    except MatchingPair.DoesNotExist:
                        print(f"Warning: No matching pair found for question ID {question.id}")
                        continue
                    except Exception as e:
                        print(f"Error processing question ID {question.id}: {str(e)}")
                        continue
            
            # Now evaluate the user's answers
            for match_data in matching_questions:
                question_id = match_data.get('question_id')
                prompt_id = match_data.get('prompt_id')
                selected_answer_id = match_data.get('selected_answer_id')
                
                # Skip if any required field is missing
                if question_id is None or selected_answer_id is None:
                    continue
                
                # Get the correct answer for this question
                correct_answer_id = correct_pairings.get(prompt_id if prompt_id is not None else question_id)
                
                # Skip if we dont have a correct answer for this question
                if correct_answer_id is None:
                    continue
                
                # Check if the selected answer matches the correct answer
                is_correct = selected_answer_id == correct_answer_id
                if is_correct:
                    matching_correct_count += 1
                
                matching_results.append({
                    'question_id': question_id,
                    'prompt_id': prompt_id,
                    'isCorrect': is_correct,
                    'correctAnswerId': correct_answer_id
                })
        
        # Calculate scores
        mc_score = round((mc_correct_count / mc_total_questions) * 100) if mc_total_questions > 0 else 0
        matching_score = round((matching_correct_count / matching_total_questions) * 100) if matching_total_questions > 0 else 0

        # Calculate combined score based on exam type
        if exam_type == "multiple_choice":
            combined_score = mc_score
        elif exam_type == "matching":
            combined_score = matching_score
        else: 
            combined_score = round((mc_score + matching_score) / 2) if (mc_total_questions > 0 and matching_total_questions > 0) else (mc_score or matching_score)

        response_data = {
            'combinedScore': combined_score,
            'mcScore': mc_score,
            'mcCorrectAnswers': mc_correct_count,
            'mcTotalQuestions': mc_total_questions,
            'results': mc_results,
            
            
            'matchingScore': matching_score,
            'matchingCorrectAnswers': matching_correct_count,
            'matchingTotalQuestions': matching_total_questions,
            'matchingResults': matching_results,
            
            'examName': exam.title,
            'passingScore': exam.required_score_to_pass,
            'passed': combined_score >= exam.required_score_to_pass,
            'trackingCode': tracking_code
        }
        
        # Save the result if tracking code is provided
        if tracking_code:
            try:
                    Result.objects.create(
                        exam=exam,
                        tracking_code=tracking_code,
                        score=combined_score,
                        details={
                            'examName': exam.title,
                            'mc_results': mc_results,
                            'matching_results': matching_results,
                            'mc_score': mc_score,
                            'matching_score': matching_score
                        }
                    )
            except Exception as e:
                print(f"Error saving exam result: {str(e)}")
        
        return Response(response_data)
        
    except Question.DoesNotExist:
        return Response({'error': 'Question not found'}, status=404)
    except Exam.DoesNotExist:
        return Response({'error': 'Exam not found'}, status=404)
    except Exception as e:
        print(f"API Error: {str(e)}")
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

class MatchingExerciseDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Result.objects.all()
    serializer_class = MatchingExerciseSerializer
