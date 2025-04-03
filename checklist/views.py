from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .models import Checklist
from safety.models import Safety
from .serializers import ChecklistSerializer
from rest_framework.exceptions import NotFound

class ChecklistCreateView(generics.CreateAPIView):
    serializer_class = ChecklistSerializer

    def post(self, request, tracking_code, *args, **kwargs):
        # Extract the tracking code from the request data
        # tracking_code = request.data.get('tracking_code')
        
        # Check if the safety record exists
        try:
            safety_record = Safety.objects.get(tracking_code=tracking_code)
        except Safety.DoesNotExist:
            return Response({"error": "Safety record not found."}, status=status.HTTP_404_NOT_FOUND)

        # Check if a checklist already exists for the given safety record
        checklist, created = Checklist.objects.get_or_create(safety=safety_record)

        # If a checklist exists, update it; otherwise, create a new one
        serializer = ChecklistSerializer(checklist, data=request.data)
        if serializer.is_valid():
            serializer.save()
            if created:
                return Response(serializer.data, status=status.HTTP_201_CREATED)  # Created a new checklist
            else:
                return Response(serializer.data, status=status.HTTP_200_OK)  # Updated existing checklist
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
        except Checklist.DoesNotExist:
            raise NotFound("Checklist not found.")

    def get(self, request, tracking_code, *args, **kwargs):
        checklist = self.get_object(tracking_code)
        serializer = self.get_serializer(checklist)
        return Response(serializer.data)

    def put(self, request, tracking_code, *args, **kwargs):
        checklist = self.get_object(tracking_code)
        serializer = self.get_serializer(checklist, data=request.data, partial=True)
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


