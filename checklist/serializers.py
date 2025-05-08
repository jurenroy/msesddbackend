
from rest_framework import serializers
from .models import Checklist, ChecklistStatus
from django.db.models.fields.files import FileField

class ChecklistStatusSerializer(serializers.ModelSerializer):
    checklist_info = serializers.SerializerMethodField()
    
    class Meta:
        model = ChecklistStatus
        fields = ('id', 'status', 'created_at', 'checklist', 'checklist_info')
        read_only_fields = ('created_at',)
    
    def get_checklist_info(self, obj):
        if obj.checklist:
            return {
                'id': obj.checklist.id,
                'tracking_code': obj.checklist.safety.tracking_code if obj.checklist.safety else None,
                'name': obj.checklist.safety.name if obj.checklist.safety else None
            }
        return None

class ChecklistStatusHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ChecklistStatus
        fields = ('id', 'status', 'created_at')
        read_only_fields = ('id', 'created_at')

class ChecklistWithStatusSerializer(serializers.ModelSerializer):
    current_status = serializers.SerializerMethodField()
    
    class Meta:
        model = Checklist
        fields = '__all__'
        read_only_fields = ('safety',)

    def get_current_status(self, obj):
        latest_status = obj.status_history.first()
        if latest_status:
            return {
                'status': latest_status.status,
            }
        return None

class ChecklistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Checklist
        fields = '__all__'
        read_only_fields = ('safety',) 

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        
        file_fields = [field.name for field in Checklist._meta.fields 
                      if isinstance(field, FileField)]
        
        request = self.context.get('request', None)
        for field_name in file_fields:
            file_field = getattr(instance, field_name)
            if file_field and file_field.name:
                representation[field_name] = file_field.url
            else:
                representation[field_name] = None
                
        return representation
    
    def update(self, instance, validated_data):
        file_fields = [field.name for field in Checklist._meta.fields 
                      if isinstance(field, FileField)]
        
        for field_name, value in validated_data.items():
            if field_name in file_fields:
                if value is not None:
                    setattr(instance, field_name, value)
            else:
                setattr(instance, field_name, value)
                
        instance.save()
        return instance



