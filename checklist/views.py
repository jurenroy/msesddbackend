from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .models import Checklist
from safety.models import Safety
from .serializers import ChecklistSerializer

class ChecklistCreateView(generics.CreateAPIView):
    serializer_class = ChecklistSerializer

    def post(self, request, *args, **kwargs):
        # Extract the tracking code from the request data
        tracking_code = request.data.get('tracking_code')
        
        # Check if the safety record exists
        try:
            safety_record = Safety.objects.get(tracking_code=tracking_code)
            serializer = SafetySerializer(safety_record)
            return Response(serializer.data)
        except Safety.DoesNotExist:
            return Response({"error": "Safety record not found."}, status=404)


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
    queryset = Checklist.objects.all()
    serializer_class = ChecklistSerializer

class ChecklistListView(generics.ListAPIView):
    queryset = Checklist.objects.all()
    serializer_class = ChecklistSerializer