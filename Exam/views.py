from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Exam, Question, Result, Answer, MatchingExercise, MatchingAnswer, Safety, MatchingPair
from .serializers import ExamSerializer, QuestionSerializer, ResultSerializer, AnswerSerializer, MatchingExerciseSerializer

class ExamListCreateView(generics.ListCreateAPIView):
    queryset = Exam.objects.all()
    serializer_class = ExamSerializer

class ExamDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Exam.objects.all()
    serializer_class = ExamSerializer

@api_view(['GET'])
def exam_data_view(request, pk):
    """
    API endpoint to get exam data including questions and answers for all exam types
    """
    try:
        exam = get_object_or_404(Exam, pk=pk)
        response_data = {
            'time': exam.time,
            'exam': {
                'id': exam.id,
                'name': exam.name,
                'topic': exam.topic,
                'required_score_to_pass': exam.required_score_to_pass,
                'exam_type': exam.exam_type, 
            }
        }
 
        # Handle different exam types
        if exam.exam_type == 'multiple_choice':
            questions = []
            for question in exam.get_questions():
                answers = []
                for answer in question.get_answers():
                    answers.append(answer.choices)
                questions.append({
                    question.text: answers
                })
            response_data['data'] = questions
  
        elif exam.exam_type == 'matching':
            # Handle matching exercises
            matching_exercises = MatchingExercise.objects.filter(exam=exam)
            matching_data = []
            for exercise in matching_exercises:
                exercise_data = {
                    'id': exercise.id,
                    'title': exercise.title,
                    'description': exercise.description,
                    'questions': [],
                    'answers': []
                }
    
                for question in exercise.questions.all():
                    exercise_data['questions'].append({
                        'id': question.id,
                        'letter': question.letter,
                        'content': question.content
                    })
                
                answers = MatchingAnswer.objects.filter(matching_exercise=exercise)
                for answer in answers:
                    exercise_data['answers'].append({
                        'id': answer.id,
                        'identifier': answer.identifier,
                        'content': answer.content
                    })
                matching_data.append(exercise_data)
            response_data['data'] = matching_data
            
        # Handle mixed format - include both types of data
        elif exam.exam_type == 'mixed':
            mc_questions = []
            for question in exam.get_questions():
                answers = []
                for answer in question.get_answers():
                    answers.append(answer.choices)
                mc_questions.append({
                    question.text: answers
                })
            matching_exercises = MatchingExercise.objects.filter(exam=exam)
            matching_data = []
            
            for exercise in matching_exercises:
                exercise_data = {
                    'id': exercise.id,
                    'title': exercise.title,
                    'description': exercise.description,
                    'questions': [],
                    'answers': []
                }
                # Get questions
                for question in exercise.questions.all():
                    exercise_data['questions'].append({
                        'id': question.id,
                        'letter': question.letter,
                        'content': question.content
                    })
                # Get answers
                answers = MatchingAnswer.objects.filter(matching_exercise=exercise)
                for answer in answers:
                    exercise_data['answers'].append({
                        'id': answer.id,
                        'identifier': answer.identifier,
                        'content': answer.content
                    })
                
                matching_data.append(exercise_data)
            
            response_data['data'] = {   
                'type': 'mixed',
                'multiple_choice': mc_questions,
                'matching': matching_data
            }
            
        return JsonResponse(response_data)
    
    except Exam.DoesNotExist:
        return JsonResponse({'error': 'Exam not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

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
        
        # Get tracking code record if exists
        safety_user = None
        if tracking_code:
            try:
                safety_user = Safety.objects.get(tracking_code=tracking_code)
            except Safety.DoesNotExist:
                return Response({'error': 'Safety record not found'}, status=404)
        
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
                question_text = answer_data['question']
                selected_answer = answer_data['selectedAnswer']
                
                # Get the question and its correct answer
                question = get_object_or_404(Question, text=question_text, exam=exam)
                correct_answer = question.answers.filter(correct=True).first()
                
                # Check if the selected answer matches the correct answer
                is_correct = correct_answer and selected_answer == correct_answer.choices
                if is_correct:
                    mc_correct_count += 1
                    
                mc_results.append({
                    'question': question_text,
                    'isCorrect': is_correct,
                    'correctAnswer': correct_answer.choices if correct_answer else None
                })
        
        # Process matching questions
        matching_questions = request.data.get('matching_questions', [])
        if matching_questions:
            matching_total_questions = len(matching_questions)
            
            # Create a dictionary to store correct pairings
            correct_pairings = {}
            
            # Get all matching exercises for this exam
            matching_exercises = MatchingExercise.objects.filter(exam=exam)
            
            # First, collect all matching pairs in one go to avoid repeated database queries
            for matching_exercise in matching_exercises:
                # Get all questions for this exercise
                questions = matching_exercise.questions.all()
                
                # For each question, find its correct answer
                for question in questions:
                    try:
                        # Get the matching pair for this question
                        matching_pair = MatchingPair.objects.get(question=question)
                        correct_pairings[question.id] = matching_pair.correct_answer.id
                    except MatchingPair.DoesNotExist:
                        # Log that no pair exists for this question
                        print(f"Warning: No matching pair found for question ID {question.id}")
                        continue
                    except Exception as e:
                        # Catch other potential errors
                        print(f"Error processing question ID {question.id}: {str(e)}")
                        continue
            
            # Now evaluate the user's answers
            for match_data in matching_questions:
                question_id = match_data['question_id']
                selected_answer_id = match_data['selected_answer_id']
                
                # Get the correct answer for this question
                correct_answer_id = correct_pairings.get(question_id)
                
                # Skip if we don't have a correct answer for this question
                if correct_answer_id is None:
                    print(f"Warning: Skipping evaluation for question ID {question_id} - no correct pairing found")
                    continue
                
                # Check if the selected answer matches the correct answer
                is_correct = selected_answer_id == correct_answer_id
                if is_correct:
                    matching_correct_count += 1
                
                matching_results.append({
                    'question_id': question_id,
                    'isCorrect': is_correct,
                    'correctAnswerId': correct_answer_id
                })
        
        # Calculate scores
        mc_score = (mc_correct_count / mc_total_questions) * 100 if mc_total_questions > 0 else 0
        matching_score = (matching_correct_count / matching_total_questions) * 100 if matching_total_questions > 0 else 0
        
        # Calculate combined score based on exam type
        if exam_type == "multiple_choice":
            combined_score = mc_score
        elif exam_type == "matching":
            combined_score = matching_score
        else:  # mixed exam type
            # Assuming equal weight for both parts
            combined_score = (mc_score + matching_score) / 2 if (mc_total_questions > 0 and matching_total_questions > 0) else (mc_score or matching_score)
        
        # Prepare response data
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
            
            'examName': exam.name,
            'passingScore': exam.required_score_to_pass,
            'passed': combined_score >= exam.required_score_to_pass,
            'trackingCode': tracking_code if tracking_code else None
        }
        
        # Save the result
        if tracking_code:
            # Create a Result object to save the exam results
            Result.objects.create(
                exam=exam,
                tracking_code=tracking_code,
                score=combined_score,
                exam_type=exam_type,
                details={
                    'mc_results': mc_results,
                    'matching_results': matching_results,
                    'mc_score': mc_score,
                    'matching_score': matching_score
                }
            )
        
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

class MatchingExerciseDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Result.objects.all()
    serializer_class = MatchingExerciseSerializer
