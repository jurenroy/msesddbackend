from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Safety, EducationFile, BoardExamFile, WorkExperienceFile, TrainingFile, NotarizedFile
from .serializers import SafetySerializer, EducationFileSerializer, BoardExamFileSerializer, WorkExperienceFileSerializer, TrainingFileSerializer, NotarizedFileSerializer
from django.core.mail import send_mail
from django.conf import settings

class SafetyListView(APIView):
    def get(self, request):
        safety_records = Safety.objects.all()
        serializer = SafetySerializer(safety_records, many=True)
        return Response(serializer.data)
    
class SafetyCreateView(APIView):
    def post(self, request):
        serializer = SafetySerializer(data=request.data)
        if serializer.is_valid():
            safety_record = serializer.save()
            try:
                recipient_email = serializer.data['email']
                tracking_code = serializer.data['tracking_code']
                
                if recipient_email:
                    subject = f"Safety Record Created: {tracking_code}"
                    message = f"""Dear Applicant,

Thank you for submitting your safety record application. Your tracking code is: {tracking_code}

Please keep this code for future reference. You can use it to check the status of your application.

Best regards,
Safety Department
"""
                    send_mail(
                        subject=subject,
                        message=message,
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[recipient_email],
                        fail_silently=False, 
                    )
                else:
                    print("No email provided, skipping email notification")
            except Exception as e:
                print(f"Failed to send email: {e}")
            
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class SafetyUpdateView(APIView):
    def put(self, request, trackingnumber):
        try:
            safety_record = Safety.objects.get(tracking_code=trackingnumber)
            serializer = SafetySerializer(safety_record, data=request.data, partial=True)  # Allow partial updates
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=200)
            return Response(serializer.errors, status=400)
        except Safety.DoesNotExist:
            return Response({"error": "Safety record not found."}, status=404)

class SafetyDetailView(APIView):
    def get(self, request, trackingnumber):
        try:
            safety_record = Safety.objects.get(tracking_code=trackingnumber)
            serializer = SafetySerializer(safety_record)
            return Response(serializer.data)
        except Safety.DoesNotExist:
            return Response({"error": "Safety record not found."}, status=404)

# New views for handling files

class EducationFileListView(APIView):
    def get(self, request, trackingnumber):
        try:
            safety_record = Safety.objects.get(tracking_code=trackingnumber)
            education_files = EducationFile.objects.filter(safety=safety_record)
            serializer = EducationFileSerializer(education_files, many=True)
            return Response(serializer.data)
        except Safety.DoesNotExist:
            return Response({"error": "Safety record not found."}, status=404)

class EducationFileDetailView(APIView):
    def get(self, request, file_id):
        try:
            education_file = EducationFile.objects.get(id=file_id)
            serializer = EducationFileSerializer(education_file)
            return Response(serializer.data)
        except EducationFile.DoesNotExist:
            return Response({"error": "Education file not found."}, status=404)

class BoardExamFileListView(APIView):
    def get(self, request, trackingnumber):
        try:
            safety_record = Safety.objects.get(tracking_code=trackingnumber)
            board_exam_files = BoardExamFile.objects.filter(safety=safety_record)
            serializer = BoardExamFileSerializer(board_exam_files, many=True)
            return Response(serializer.data)
        except Safety.DoesNotExist:
            return Response({"error": "Safety record not found."}, status=404)

class BoardExamFileDetailView(APIView):
    def get(self, request, file_id):
        try:
            board_exam_file = BoardExamFile.objects.get(id=file_id)
            serializer = BoardExamFileSerializer(board_exam_file)
            return Response(serializer.data)
        except BoardExamFile.DoesNotExist:
            return Response({"error": "Board exam file not found."}, status=404)

class WorkExperienceFileListView(APIView):
    def get(self, request, trackingnumber):
        try:
            safety_record = Safety.objects.get(tracking_code=trackingnumber)
            work_experience_files = WorkExperienceFile.objects.filter(safety=safety_record)
            serializer = WorkExperienceFileSerializer(work_experience_files, many=True)
            return Response(serializer.data)
        except Safety.DoesNotExist:
            return Response({"error": "Safety record not found."}, status=404)

class WorkExperienceFileDetailView(APIView):
    def get(self, request, file_id):
        try:
            work_experience_file = WorkExperienceFile.objects.get(id=file_id)
            serializer = WorkExperienceFileSerializer(work_experience_file)
            return Response(serializer.data)
        except WorkExperienceFile.DoesNotExist:
            return Response({"error": "Work experience file not found."}, status=404)

class TrainingFileListView(APIView):
    def get(self, request, trackingnumber):
        try:
            safety_record = Safety.objects.get(tracking_code=trackingnumber)
            training_files = TrainingFile.objects.filter(safety=safety_record)
            serializer = TrainingFileSerializer(training_files, many=True)
            return Response(serializer.data)
        except Safety.DoesNotExist:
            return Response({"error": "Safety record not found."}, status=404)

class TrainingFileDetailView(APIView):
    def get(self, request, file_id):
        try:
            training_file = TrainingFile.objects.get(id=file_id)
            serializer = TrainingFileSerializer(training_file)
            return Response(serializer.data)
        except TrainingFile.DoesNotExist:
            return Response({"error": "Training file not found."}, status=404)

class NotarizedFileCreateView(APIView):
    def post(self, request, trackingnumber):
        try:
            # Get the Safety record based on the tracking number
            safety_record = Safety.objects.get(tracking_code=trackingnumber)
            files = request.FILES.getlist('notarizedFiles')  # Get the list of uploaded files

            if not files:
                return Response({"error": "No files provided."}, status=status.HTTP_400_BAD_REQUEST)

            # Iterate over the files and save each one
            for file in files:
                serializer = NotarizedFileSerializer(data={'file': file, 'safety': safety_record.id})
                if serializer.is_valid():
                    serializer.save()  # Save the file associated with the safety record
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            return Response({"message": "Files uploaded successfully!"}, status=status.HTTP_201_CREATED)
        except Safety.DoesNotExist:
            return Response({"error": "Safety record not found."}, status=status.HTTP_404_NOT_FOUND)

class NotarizedFileListView(APIView):
    def get(self, request, trackingnumber):
        try:
            print(trackingnumber)
            safety_record = Safety.objects.get(tracking_code=trackingnumber)
            notarized_files = NotarizedFile.objects.filter(safety=safety_record)
            serializer = NotarizedFileSerializer(notarized_files, many=True)
            return Response(serializer.data)
        except Safety.DoesNotExist:
            return Response({"error": "Safety record not found."}, status=404)

class NotarizedFileDetailView(APIView):
    def get(self, request, file_id):
        try:
            notarized_file = NotarizedFile.objects.get(id=file_id)
            serializer = NotarizedFileSerializer(notarized_file)
            return Response(serializer.data)
        except NotarizedFile.DoesNotExist:
            return Response({"error": "Notarized file not found."}, status=404)