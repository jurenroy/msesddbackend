from rest_framework import generics, views
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .models import Checklist, ChecklistStatus
from safety.models import Safety
from .serializers import  (
    ChecklistSerializer,
    ChecklistStatusSerializer,
    ChecklistWithStatusSerializer,
    ChecklistStatusHistorySerializer

)   
from rest_framework.exceptions import NotFound

class ChecklistCreateView(generics.CreateAPIView):
    serializer_class = ChecklistSerializer

    def post(self, request, tracking_code, *args, **kwargs):
        try:
            safety_record = Safety.objects.get(tracking_code=tracking_code)
        except Safety.DoesNotExist:
            return Response({"error": "Safety record not found."}, status=status.HTTP_404_NOT_FOUND)

        # Check if a checklist already exists for the given safety record
        checklist, created = Checklist.objects.get_or_create(safety=safety_record)

        # If a checklist exists, update it  otherwise create a new one
        serializer = ChecklistSerializer(checklist, data=request.data)
        if serializer.is_valid():
            serializer.save()
            if created:
                return Response(serializer.data, status=status.HTTP_201_CREATED) 
            else:
                return Response(serializer.data, status=status.HTTP_200_OK)  
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ChecklistDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ChecklistSerializer

    def get_object(self, tracking_code):
        try:
            # Get the Safety record using the tracking code
            safety_record = Safety.objects.get(tracking_code=tracking_code)
            
            try:
                checklist = Checklist.objects.get(safety=safety_record)
            except Checklist.DoesNotExist:
                checklist = Checklist.objects.create(safety=safety_record)

            return checklist
        except Safety.DoesNotExist:
            raise NotFound("Safety record not found.")

    def get(self, request, tracking_code, *args, **kwargs):
        checklist = self.get_object(tracking_code)
        serializer = self.get_serializer(checklist, context={'request': request})
        return Response(serializer.data)

    def put(self, request, tracking_code, *args, **kwargs):
        checklist = self.get_object(tracking_code)
        serializer = self.get_serializer(checklist, data=request.data, partial=True, context={'request': request})
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, tracking_code, *args, **kwargs):
        checklist = self.get_object(tracking_code)
        checklist.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class ChecklistListView(generics.ListAPIView):
    queryset = Checklist.objects.all()
    serializer_class = ChecklistSerializer

class ChecklistStatusUpdateView(views.APIView):
    def post(self, request, tracking_code=None, pk=None):
        checklist = None
        
        if tracking_code:
            try:
                safety = Safety.objects.get(tracking_code=tracking_code)
                checklist = Checklist.objects.get(safety=safety)
            except Safety.DoesNotExist:
                return Response({"error": "Safety record not found."}, status=status.HTTP_404_NOT_FOUND)
            except Checklist.DoesNotExist:
                return Response({"error": "Checklist record not found."}, status=status.HTTP_404_NOT_FOUND)
        elif pk:
            try:
                checklist = Checklist.objects.get(pk=pk)
            except Checklist.DoesNotExist:
                return Response({"error": "Checklist not found."}, status=status.HTTP_404_NOT_FOUND)
        
        if checklist is None:
            return Response({"error": "Either tracking_code or pk must be provided."}, status=status.HTTP_400_BAD_REQUEST)

        # Check if a status value is provided
        status_data = request.data.get('status')
        if not status_data:
            return Response({"error": "Status data is required."}, status=status.HTTP_400_BAD_REQUEST)
            
        # Always create a new status record to get a new timestamp
        new_status = ChecklistStatus.objects.create(
            checklist=checklist,
            status=status_data,
        )
        
        serializer = ChecklistStatusSerializer(new_status)
        
        return Response({
            "status": "created", 
            "data": serializer.data,
            "message": f"Checklist status changed to {status_data} on {new_status.created_at.strftime('%Y-%m-%d %H:%M:%S')}"
        }, status=status.HTTP_201_CREATED)


class ChecklistStatusHistoryView(generics.ListAPIView):
    serializer_class = ChecklistStatusHistorySerializer
    
    def get_queryset(self):
        pk = self.kwargs.get('pk')
        tracking_code = self.kwargs.get('tracking_code')
        
        if pk:
            return ChecklistStatus.objects.filter(checklist_id=pk).order_by('-created_at')
        elif tracking_code:
            return ChecklistStatus.objects.filter(
                checklist__safety__tracking_code=tracking_code
            ).order_by('-created_at')
        
        return ChecklistStatus.objects.none()
        
class ChecklistStatusListView(generics.ListAPIView):
    queryset = ChecklistStatus.objects.all()
    serializer_class = ChecklistStatusSerializer
    
    def get_queryset(self):
        """
        Optionally restricts the returned statuses by filtering against query parameters
        """
        queryset = ChecklistStatus.objects.all().select_related('checklist')
        
        # Add filtering options if needed
        checklist_id = self.request.query_params.get('checklist_id', None)
        status = self.request.query_params.get('status', None)
        
        if checklist_id:
            queryset = queryset.filter(checklist_id=checklist_id)
        if status:
            queryset = queryset.filter(status=status)
            
        return queryset
    
class MinimalChecklistStatusListView(generics.ListAPIView):
    queryset = ChecklistStatus.objects.all()
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        data = [
            {
                'id': status.id,
                'status': status.status,
                'checklist_id': status.checklist_id
            }
            for status in queryset
        ]
        return Response(data)
        
