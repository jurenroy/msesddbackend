from rest_framework import serializers
from .models import Checklist
from django.db.models.fields.files import FileField

class ChecklistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Checklist
        fields = '__all__'

    def to_representation(self, instance):
        # Get the default representation
        representation = super().to_representation(instance)
        
        # Automatically find all FileField instances in the model
        file_fields = [field.name for field in Checklist._meta.fields 
                      if isinstance(field, FileField)]
        
        # Process each file field
        for field_name in file_fields:
            file_field = getattr(instance, field_name)
            if file_field and file_field.name:  # Check if file exists and has a name
                # If the file field has an actual file, get the URL
                representation[field_name] = file_field.url.replace(
                    f"http://{self.context['request'].get_host()}/", "/media/")
            else:
                # If the file doesn't exist, set to null
                representation[field_name] = None
                
        return representation