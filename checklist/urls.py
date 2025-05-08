from django.urls import path, include
from .views import (
    ChecklistCreateView,
    ChecklistDetailView,
    ChecklistListView,
    ChecklistStatusUpdateView,
    ChecklistStatusHistoryView,
    ChecklistStatusListView,
    MinimalChecklistStatusListView,
)

urlpatterns = [
    #Checklist
    path('safety/<str:tracking_code>/checklist/', ChecklistCreateView.as_view(), name='checklist_create'),
    path('checklist/<str:tracking_code>/', ChecklistDetailView.as_view(), name='checklist_detail'),  
    path('checklist/<int:pk>/', ChecklistDetailView.as_view(), name='checklist_detail'),
    path('checklists/', ChecklistListView.as_view(), name='checklist_list'),


    #ChecklistStatus
    path('checklist/<int:pk>/status/', ChecklistStatusUpdateView.as_view(), name='checklist_status_update'),
    path('checklist/<str:tracking_code>/status/', ChecklistStatusUpdateView.as_view(), name='checklist_status_update_by_code'),
    

    #intial history just incase its needed ;> goodluck pi 
    path('checklist/<int:pk>/status_history/', ChecklistStatusHistoryView.as_view(), name='checklist_status_history'),
    path('checklist/<str:tracking_code>/status_history/', ChecklistStatusHistoryView.as_view(), name='checklist_status_history_by_code'),
    path('checklist-statuses/', ChecklistStatusListView.as_view(), name='checklist_status_list'),

    #Testing purposes only
    path('minimal-checklist-statuses/', MinimalChecklistStatusListView.as_view(), name='minimal_checklist_status_list'),
]