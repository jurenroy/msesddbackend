from django.urls import path
from .views import (
    SafetyListView,
    SafetyCreateView,
    SafetyUpdateView,
    SafetyDetailView,
    EducationFileListView,
    EducationFileDetailView,
    BoardExamFileListView,
    BoardExamFileDetailView,
    WorkExperienceFileListView,
    WorkExperienceFileDetailView,
    TrainingFileListView,
    TrainingFileDetailView,
    NotarizedFileCreateView,
    NotarizedFileListView,
    NotarizedFileDetailView,
    )

urlpatterns = [
    path('safety/', SafetyListView.as_view(), name='safety_list'),
    path('add_safety/', SafetyCreateView.as_view(), name='safety_create'),
    path('safety/<str:trackingnumber>/', SafetyDetailView.as_view(), name='safety_detail'),
    path('update_safety/<str:trackingnumber>/', SafetyUpdateView.as_view(), name='safety_update'),

    # Education Files
    path('safety/<str:trackingnumber>/education-files/', EducationFileListView.as_view(), name='education-file-list'),
    path('education-file/<int:file_id>/', EducationFileDetailView.as_view(), name='education-file-detail'),

    # Board Exam Files
    path('safety/<str:trackingnumber>/board-exam-files/', BoardExamFileListView.as_view(), name='board-exam-file-list'),
    path('board-exam-file/<int:file_id>/', BoardExamFileDetailView.as_view(), name='board-exam-file-detail'),

    # Work Experience Files
    path('safety/<str:trackingnumber>/work-experience-files/', WorkExperienceFileListView.as_view(), name='work-experience-file-list'),
    path('work-experience-file/<int:file_id>/', WorkExperienceFileDetailView.as_view(), name='work-experience-file-detail'),

    # Training Files
    path('safety/<str:trackingnumber>/training-files/', TrainingFileListView.as_view(), name='training-file-list'),
    path('training-file/<int:file_id>/', TrainingFileDetailView.as_view(), name='training-file-detail'),

    # Notarized Files
    path('safety/<str:trackingnumber>/notarized-file/', NotarizedFileCreateView.as_view(), name='notarized-file-create'),
    path('safety/<str:trackingnumber>/notarized-files/', NotarizedFileListView.as_view(), name='notarized-file-list'),
    path('notarized-file/<int:file_id>/', NotarizedFileDetailView.as_view(), name='notarized-file-detail'),
]