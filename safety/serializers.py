from rest_framework import serializers
from .models import Safety, EducationFile, BoardExamFile, WorkExperienceFile, TrainingFile, NotarizedFile

class SafetySerializer(serializers.ModelSerializer):
    educationFiles = serializers.ListField(
        child=serializers.FileField(), write_only=True, required=False
    )
    boardExamFiles = serializers.ListField(
        child=serializers.FileField(), write_only=True, required=False
    )
    workExperienceFiles = serializers.ListField(
        child=serializers.FileField(), write_only=True, required=False
    )
    trainingFiles = serializers.ListField(
        child=serializers.FileField(), write_only=True, required=False
    )
    notarizedFile = serializers.ListField(
        child=serializers.FileField(), write_only=True, required=False
    )

    class Meta:
        model = Safety
        fields = [
            'id', 'name', 'address', 'contactNo', 'age', 'civilStatus',
            'dateOfBirth', 'placeOfBirth', 'citizenship', 'howAcquired',
            'lastResidence', 'dateOfArrival', 'landingCertificateNo',
            'employmentContract', 'employmentNature', 'companyName',
            'presentCompanyName', 'presentCompanyAddress',
            'email',  # Include the email field
            'educationFiles', 'boardExamFiles', 'workExperienceFiles',
            'trainingFiles', 'notarizedFile',
            'education', 'boardExams', 'workExperience',
            'trainings', 'documents', 'compliance', 'understanding', 'certify',
            'permit_type', 'date', 'tracking_code', 'role'
        ]

    def create(self, validated_data):
        # Extract file lists from validated data
        educationFiles = validated_data.pop('educationFiles', [])
        boardExamFiles = validated_data.pop('boardExamFiles', [])
        workExperienceFiles = validated_data.pop('workExperienceFiles', [])
        trainingFiles = validated_data.pop('trainingFiles', [])
        notarizedFiles = validated_data.pop('notarizedFile', [])

        # Create the Safety instance
        safety_instance = Safety.objects.create(**validated_data)

        # Handle file uploads
        for file in educationFiles:
            EducationFile.objects.create(safety=safety_instance, file=file)

        for file in boardExamFiles:
            BoardExamFile.objects.create(safety=safety_instance, file=file)

        for file in workExperienceFiles:
            WorkExperienceFile.objects.create(safety=safety_instance, file=file)

        for file in trainingFiles:
            TrainingFile.objects.create(safety=safety_instance, file=file)

        for file in notarizedFiles:
            NotarizedFile.objects.create(safety=safety_instance, file=file)

        return safety_instance


class EducationFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = EducationFile
        fields = ['id', 'safety', 'file']  # Include any other fields you have

class BoardExamFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = BoardExamFile
        fields = ['id', 'safety', 'file']  # Include any other fields you have

class WorkExperienceFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkExperienceFile
        fields = ['id', 'safety', 'file']  # Include any other fields you have

class TrainingFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainingFile
        fields = ['id', 'safety', 'file']  # Include any other fields you have

class NotarizedFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotarizedFile
        fields = ['id', 'safety', 'file']  # Include any other fields you have