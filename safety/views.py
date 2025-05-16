from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError
from .models import Safety, SafetyFile, Education, BoardExam, WorkExperience, Training
from .serializers import (
    SafetySerializer, SafetyFileSerializer, 
    EducationSerializer, BoardExamSerializer,
    WorkExperienceSerializer, TrainingSerializer
)
from django.core.mail import send_mail
from django.conf import settings
from rest_framework.decorators import api_view
from django.template.loader import render_to_string

class SafetyListView(APIView):
    def get(self, request):
        try:
            print("DEBUG: Accessing SafetyListView")
            print(f"DEBUG: Request path: {request.path}")
            print(f"DEBUG: Request method: {request.method}")
            print(f"DEBUG: Request headers: {dict(request.headers)}")
            
            safety_records = Safety.objects.all()
            print(f"DEBUG: Found {safety_records.count()} safety records")
            
            serializer = SafetySerializer(safety_records, many=True, context={'request': request})
            serialized_data = serializer.data
            print("DEBUG: Successfully serialized data")
            
            return Response(serialized_data)
        except Exception as e:
            import traceback
            print(f"ERROR in SafetyListView: {str(e)}")
            print("Traceback:")
            print(traceback.format_exc())
            return Response(
                {
                    "error": "An error occurred while fetching safety records.",
                    "detail": str(e),
                    "path": request.path
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
class SafetyCreateView(APIView):
    def post(self, request):
        serializer = SafetySerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            safety_record = serializer.save()
            try:
                recipient_email = serializer.validated_data.get('email')
                tracking_code = safety_record.tracking_code
                name = safety_record.name or "Applicant"
                
                if recipient_email:
                    subject = f"Safety Application Submitted: {tracking_code}"
                    
                    # Context for email templates
                    context = {
                        'name': name,
                        'tracking_code': tracking_code
                    }
                    
                    # Use Django's template system to render the email content
                    from django.template.loader import render_to_string
                    
                    # Render the HTML and plain text templates
                    html_message = render_to_string('email/safety_application_submitted.html', context)
                    plain_message = render_to_string('email/safety_application_submitted.txt', context)
                 
                    from_email = settings.DEFAULT_FROM_EMAIL
                    send_mail(
                        subject=subject,
                        message=plain_message,
                        from_email=from_email,
                        recipient_list=[recipient_email],
                        html_message=html_message,
                        fail_silently=False, 
                    )
                    print(f"Email sent to {recipient_email} with tracking code {tracking_code}")
                    
                else:
                    print("No email provided, skipping email notification")
            except Exception as e:
                print(f"Failed to send email: {e}")
                import traceback
                traceback.print_exc()

            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

class SafetyUpdateView(APIView):
    def put(self, request, trackingnumber):
        try:
            safety_record = Safety.objects.get(tracking_code=trackingnumber)
            serializer = SafetySerializer(safety_record, data=request.data, partial=True, context={'request': request})
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
            serializer = SafetySerializer(safety_record, context={'request': request})
            return Response(serializer.data)
        except Safety.DoesNotExist:
            return Response({"error": "Safety record not found."}, status=404)

# New views for handling records and files

class SafetyFileListView(APIView):
    def get(self, request, trackingnumber):
        try:
            safety_record = Safety.objects.get(tracking_code=trackingnumber)
            files = SafetyFile.objects.filter(safety=safety_record)
            serializer = SafetyFileSerializer(files, many=True)
            return Response(serializer.data)
        except Safety.DoesNotExist:
            return Response({"error": "Safety record not found."}, status=404)

    def post(self, request, trackingnumber):
        try:
            safety_record = Safety.objects.get(tracking_code=trackingnumber)
            files = request.FILES.getlist('files')
            file_types = request.POST.getlist('file_types', [])
            descriptions = request.POST.getlist('descriptions', [])

            if not files:
                return Response({"error": "No files provided."}, status=400)

            uploaded_files = []
            for i, file in enumerate(files):
                file_type = file_types[i] if i < len(file_types) else 'other'
                description = descriptions[i] if i < len(descriptions) else ''
                
                file_instance = SafetyFile.objects.create(
                    safety=safety_record,
                    file=file,
                    file_type=file_type,
                    description=description
                )
                uploaded_files.append(SafetyFileSerializer(file_instance).data)

            return Response(uploaded_files, status=201)
        except Safety.DoesNotExist:
            return Response({"error": "Safety record not found."}, status=404)

class SafetyFileDetailView(APIView):
    def get(self, request, file_id):
        try:
            file = SafetyFile.objects.get(id=file_id)
            serializer = SafetyFileSerializer(file)
            return Response(serializer.data)
        except SafetyFile.DoesNotExist:
            return Response({"error": "File not found."}, status=404)

    def delete(self, request, file_id):
        try:
            file = SafetyFile.objects.get(id=file_id)
            file.delete()
            return Response(status=204)
        except SafetyFile.DoesNotExist:
            return Response({"error": "File not found."}, status=404)

class EducationRecordView(APIView):
    def get(self, request, trackingnumber):
        try:
            safety_record = Safety.objects.get(tracking_code=trackingnumber)
            education_records = Education.objects.filter(safety=safety_record)
            serializer = EducationSerializer(education_records, many=True)
            return Response(serializer.data)
        except Safety.DoesNotExist:
            return Response({"error": "Safety record not found."}, status=404)

    def post(self, request, trackingnumber):
        try:
            safety_record = Safety.objects.get(tracking_code=trackingnumber)
            data = request.data.copy()
            data['safety'] = safety_record.id
            serializer = EducationSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=201)
            return Response(serializer.errors, status=400)
        except Safety.DoesNotExist:
            return Response({"error": "Safety record not found."}, status=404)

class BoardExamRecordView(APIView):
    def get(self, request, trackingnumber):
        try:
            safety_record = Safety.objects.get(tracking_code=trackingnumber)
            board_exam_records = BoardExam.objects.filter(safety=safety_record)
            serializer = BoardExamSerializer(board_exam_records, many=True)
            return Response(serializer.data)
        except Safety.DoesNotExist:
            return Response({"error": "Safety record not found."}, status=404)

    def post(self, request, trackingnumber):
        try:
            safety_record = Safety.objects.get(tracking_code=trackingnumber)
            data = request.data.copy()
            data['safety'] = safety_record.id
            serializer = BoardExamSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=201)
            return Response(serializer.errors, status=400)
        except Safety.DoesNotExist:
            return Response({"error": "Safety record not found."}, status=404)

class WorkExperienceRecordView(APIView):
    def get(self, request, trackingnumber):
        try:
            safety_record = Safety.objects.get(tracking_code=trackingnumber)
            work_experience_records = WorkExperience.objects.filter(safety=safety_record)
            serializer = WorkExperienceSerializer(work_experience_records, many=True)
            return Response(serializer.data)
        except Safety.DoesNotExist:
            return Response({"error": "Safety record not found."}, status=404)

    def post(self, request, trackingnumber):
        try:
            safety_record = Safety.objects.get(tracking_code=trackingnumber)
            data = request.data.copy()
            data['safety'] = safety_record.id
            serializer = WorkExperienceSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=201)
            return Response(serializer.errors, status=400)
        except Safety.DoesNotExist:
            return Response({"error": "Safety record not found."}, status=404)

class TrainingRecordView(APIView):
    def get(self, request, trackingnumber):
        try:
            safety_record = Safety.objects.get(tracking_code=trackingnumber)
            training_records = Training.objects.filter(safety=safety_record)
            serializer = TrainingSerializer(training_records, many=True)
            return Response(serializer.data)
        except Safety.DoesNotExist:
            return Response({"error": "Safety record not found."}, status=404)

    def post(self, request, trackingnumber):
        try:
            safety_record = Safety.objects.get(tracking_code=trackingnumber)
            data = request.data.copy()
            data['safety'] = safety_record.id
            serializer = TrainingSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=201)
            return Response(serializer.errors, status=400)
        except Safety.DoesNotExist:
            return Response({"error": "Safety record not found."}, status=404)

@api_view(['GET'])
def update_safety_email(request, tracking_code):
    """
    Update the email address for a safety record using GET request
    """
    try:
        email = request.query_params.get('email', None)
        if not email:
            return Response({"error": "Email parameter is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        safety = Safety.objects.get(tracking_code=tracking_code)
        safety.email = email
        safety.save()
        
        return Response({"success": True, "message": f"Email updated to {email}"})
    
    except Safety.DoesNotExist:
        return Response({"error": "Safety record not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def test_email(request):
    """
    Test email sending functionality
    """
    try:
        email = request.query_params.get('email', None)
        if not email:
            return Response({"error": "Email parameter is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        print(f"Testing email sending to {email}")
        
        # Get current time
        from django.utils import timezone
        current_time = timezone.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Send a test email
        subject = "MSESDD Test Email"
        message = "This is a test email from the MSESDD system to verify email functionality."
        html_message = f"""
        <html>
        <body>
            <h2 style="color: #4CAF50;">Test Email from MSESDD System</h2>
            <p>This is a test email sent to {email} to verify that the email system is working correctly.</p>
            <p>If you're receiving this, the email configuration is working!</p>
            <p>Time sent: {current_time}</p>
        </body>
        </html>
        """
        
        from django.core.mail import send_mail
        from django.conf import settings
        
        result = send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            html_message=html_message,
            fail_silently=False
        )
        
        print(f"Email send result: {result}")
        
        return Response({
            "success": True, 
            "message": f"Test email sent to {email}",
            "send_result": result,
            "email_settings": {
                "backend": settings.EMAIL_BACKEND,
                "host": settings.EMAIL_HOST,
                "port": settings.EMAIL_PORT,
                "user": settings.EMAIL_HOST_USER,
                "from_email": settings.DEFAULT_FROM_EMAIL,
                "use_tls": settings.EMAIL_USE_TLS
            }
        })
    
    except Exception as e:
        import traceback
        print(f"Error sending test email: {e}")
        traceback.print_exc()
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)