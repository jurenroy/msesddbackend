from django.urls import path
from .views import (
    SafetyListView,
    SafetyCreateView,
    SafetyUpdateView,
    SafetyDetailView,
    SafetyFileListView,
    SafetyFileDetailView,
    EducationRecordView,
    BoardExamRecordView,
    WorkExperienceRecordView,
    TrainingRecordView,
    update_safety_email,
    test_email,
)

urlpatterns = [
    # Safety record endpoints
    path('safety/', SafetyListView.as_view(), name='safety_list'),
    path('add_safety/', SafetyCreateView.as_view(), name='safety_create'),
    path('safety/<str:trackingnumber>/', SafetyDetailView.as_view(), name='safety_detail'),
    path('update_safety/<str:trackingnumber>/', SafetyUpdateView.as_view(), name='safety_update'),

    # New endpoint for updating email via GET
    path('safety/update-email/<str:tracking_code>/', update_safety_email, name='update_safety_email'),
    
    # Test email endpoint
    path('test-email/', test_email, name='test_email'),

    # File management endpoints
    path('safety/<str:trackingnumber>/files/', SafetyFileListView.as_view(), name='safety-file-list'),
    path('files/<int:file_id>/', SafetyFileDetailView.as_view(), name='safety-file-detail'),

    # Education records
    path('safety/<str:trackingnumber>/education/', EducationRecordView.as_view(), name='education-records'),

    # Board exam records
    path('safety/<str:trackingnumber>/board-exams/', BoardExamRecordView.as_view(), name='board-exam-records'),

    # Work experience records
    path('safety/<str:trackingnumber>/work-experience/', WorkExperienceRecordView.as_view(), name='work-experience-records'),

    # Training records
    path('safety/<str:trackingnumber>/training/', TrainingRecordView.as_view(), name='training-records'),
]