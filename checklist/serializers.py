from rest_framework import serializers
from .models import Checklist

class ChecklistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Checklist
        fields = '__all__'  # Or specify the fields you want to include

    def to_representation(self, instance):
        # Get the default representation
        representation = super().to_representation(instance)

        # Modify the file fields to return only the media paths
        for field in representation:
            file_field = getattr(instance, field)
            if hasattr(file_field, 'url'):
                # If the file field is a FileField, get the URL and remove the domain
                representation[field] = file_field.url.replace(f"http://{self.context['request'].get_host()}/", "/media/")
            elif isinstance(file_field, str):
                # If the file field is a string, it means it is already a relative path
                representation[field] = file_field

        return representation




    