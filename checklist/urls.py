from django.urls import path
from .views import (
    ChecklistCreateView,
    ChecklistDetailView,
    ChecklistListView,
)

urlpatterns = [
    path('safety/<str:tracking_code>/checklist/', ChecklistCreateView.as_view(), name='checklist_create'),
    path('checklist/<str:tracking_code>/', ChecklistDetailView.as_view(), name='checklist_detail'),  # Use tracking_code
    # path('checklist/<int:pk>/', ChecklistDetailView.as_view(), name='checklist_detail'),
    path('checklists/', ChecklistListView.as_view(), name='checklist_list'),
]