from rest_framework import serializers
from .models import Safety, SafetyFile, Education, BoardExam, WorkExperience, Training

class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = ['id', 'school_name', 'degree', 'year_completed', 'major', 'document']

class BoardExamSerializer(serializers.ModelSerializer):
    class Meta:
        model = BoardExam
        fields = ['id', 'exam_name', 'date_taken', 'license_number', 'expiry_date', 'document']

class WorkExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkExperience
        fields = ['id', 'company_name', 'position', 'start_date', 'end_date', 'responsibilities', 'document']

class TrainingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Training
        fields = ['id', 'training_name', 'provider', 'date_completed', 'certificate_number', 'document']

class SafetyFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = SafetyFile
        fields = ['id', 'file', 'file_type', 'description', 'uploaded_at']

class SafetySerializer(serializers.ModelSerializer):
    education_records = EducationSerializer(many=True, read_only=True)
    board_exam_records = BoardExamSerializer(many=True, read_only=True)
    work_experience_records = WorkExperienceSerializer(many=True, read_only=True)
    training_records = TrainingSerializer(many=True, read_only=True)
    files = SafetyFileSerializer(many=True, read_only=True)
    
    # File upload fields
    educationFiles = serializers.ListField(
        child=serializers.FileField(),
        write_only=True,
        required=False
    )
    boardExamFiles = serializers.ListField(
        child=serializers.FileField(),
        write_only=True,
        required=False
    )
    workExperienceFiles = serializers.ListField(
        child=serializers.FileField(),
        write_only=True,
        required=False
    )
    trainingFiles = serializers.ListField(
        child=serializers.FileField(),
        write_only=True,
        required=False
    )
    notarizedFiles = serializers.ListField(
        child=serializers.FileField(),
        write_only=True,
        required=False
    )

    # Nested data for creation
    education_data = serializers.ListField(
        child=serializers.DictField(),
        write_only=True,
        required=False
    )
    board_exam_data = serializers.ListField(
        child=serializers.DictField(),
        write_only=True,
        required=False
    )
    work_experience_data = serializers.ListField(
        child=serializers.DictField(),
        write_only=True,
        required=False
    )
    training_data = serializers.ListField(
        child=serializers.DictField(),
        write_only=True,
        required=False
    )

    # File URLs
    educationFiles_url = serializers.SerializerMethodField()
    boardExamFiles_url = serializers.SerializerMethodField()
    workExperienceFiles_url = serializers.SerializerMethodField()
    trainingFiles_url = serializers.SerializerMethodField()
    notarizedFiles_url = serializers.SerializerMethodField()

    # JSON Fields
    education = serializers.JSONField(required=False)
    boardExams = serializers.JSONField(required=False)
    workExperience = serializers.JSONField(required=False)
    trainings = serializers.JSONField(required=False)

    class Meta:
        model = Safety
        fields = [
            'id', 'name', 'address', 'contactNo', 'age', 'civilStatus',
            'dateOfBirth', 'placeOfBirth', 'citizenship', 'howAcquired',
            'lastResidence', 'dateOfArrival', 'landingCertificateNo',
            'employmentContract', 'employmentNature', 'companyName',
            'presentCompanyName', 'presentCompanyAddress', 'email',
            'documents', 'compliance', 'understanding', 'certify',
            'permit_type', 'role', 'date', 'tracking_code',
            'education_records', 'board_exam_records', 'work_experience_records', 'training_records',
            'files',
            'educationFiles', 'boardExamFiles', 'workExperienceFiles',
            'trainingFiles', 'notarizedFiles',
            'education_data', 'board_exam_data', 'work_experience_data', 'training_data',
            'educationFiles_url', 'boardExamFiles_url', 'workExperienceFiles_url',
            'trainingFiles_url', 'notarizedFiles_url',
            'education', 'boardExams', 'workExperience', 'trainings'
        ]
        read_only_fields = ['tracking_code', 'date']

    def get_educationFiles_url(self, obj):
        if obj.educationFiles:
            return self.context['request'].build_absolute_uri(obj.educationFiles.url)
        return None

    def get_boardExamFiles_url(self, obj):
        if obj.boardExamFiles:
            return self.context['request'].build_absolute_uri(obj.boardExamFiles.url)
        return None

    def get_workExperienceFiles_url(self, obj):
        if obj.workExperienceFiles:
            return self.context['request'].build_absolute_uri(obj.workExperienceFiles.url)
        return None

    def get_trainingFiles_url(self, obj):
        if obj.trainingFiles:
            return self.context['request'].build_absolute_uri(obj.trainingFiles.url)
        return None

    def get_notarizedFiles_url(self, obj):
        if obj.notarizedFiles:
            return self.context['request'].build_absolute_uri(obj.notarizedFiles.url)
        return None

    def create(self, validated_data):
        # Extract nested data
        education_data = validated_data.pop('education_data', [])
        board_exam_data = validated_data.pop('board_exam_data', [])
        work_experience_data = validated_data.pop('work_experience_data', [])
        training_data = validated_data.pop('training_data', [])
        
        # Extract file data
        education_files = validated_data.pop('educationFiles', [])
        board_exam_files = validated_data.pop('boardExamFiles', [])
        work_experience_files = validated_data.pop('workExperienceFiles', [])
        training_files = validated_data.pop('trainingFiles', [])
        notarized_files = validated_data.pop('notarizedFiles', [])

        # Create Safety instance
        safety_instance = Safety.objects.create(**validated_data)

        # Create related records
        for edu_data in education_data:
            Education.objects.create(safety=safety_instance, **edu_data)
        
        for exam_data in board_exam_data:
            BoardExam.objects.create(safety=safety_instance, **exam_data)
        
        for exp_data in work_experience_data:
            WorkExperience.objects.create(safety=safety_instance, **exp_data)
        
        for train_data in training_data:
            Training.objects.create(safety=safety_instance, **train_data)

        # Handle file uploads
        for file in education_files:
            SafetyFile.objects.create(
                safety=safety_instance,
                file=file,
                file_type='education',
                description='Education Document'
            )

        for file in board_exam_files:
            SafetyFile.objects.create(
                safety=safety_instance,
                file=file,
                file_type='board_exam',
                description='Board Exam Document'
            )

        for file in work_experience_files:
            SafetyFile.objects.create(
                safety=safety_instance,
                file=file,
                file_type='work_experience',
                description='Work Experience Document'
            )

        for file in training_files:
            SafetyFile.objects.create(
                safety=safety_instance,
                file=file,
                file_type='training',
                description='Training Document'
            )

        for file in notarized_files:
            SafetyFile.objects.create(
                safety=safety_instance,
                file=file,
                file_type='notarized',
                description='Notarized Document'
            )

        return safety_instance

    def update(self, instance, validated_data):
        # Handle file fields first
        for field in ['application_form', 'photo', 'notarized_document', 'proof_document']:
            if field in validated_data:
                setattr(instance, field, validated_data.pop(field))

        # Update other fields
        for field, value in validated_data.items():
            if field not in ['education_data', 'board_exam_data', 'work_experience_data', 'training_data']:
                setattr(instance, field, value)

        instance.save()

        # Update related records if provided
        education_data = validated_data.pop('education_data', None)
        board_exam_data = validated_data.pop('board_exam_data', None)
        work_experience_data = validated_data.pop('work_experience_data', None)
        training_data = validated_data.pop('training_data', None)
        
        if education_data is not None:
            instance.education_records.all().delete()
            for edu_data in education_data:
                Education.objects.create(safety=instance, **edu_data)
        
        if board_exam_data is not None:
            instance.board_exam_records.all().delete()
            for exam_data in board_exam_data:
                BoardExam.objects.create(safety=instance, **exam_data)
        
        if work_experience_data is not None:
            instance.work_experience_records.all().delete()
            for exp_data in work_experience_data:
                WorkExperience.objects.create(safety=instance, **exp_data)
        
        if training_data is not None:
            instance.training_records.all().delete()
            for train_data in training_data:
                Training.objects.create(safety=instance, **train_data)

        # Handle file uploads if any
        education_files = validated_data.pop('educationFiles', [])
        board_exam_files = validated_data.pop('boardExamFiles', [])
        work_experience_files = validated_data.pop('workExperienceFiles', [])
        training_files = validated_data.pop('trainingFiles', [])
        notarized_files = validated_data.pop('notarizedFiles', [])

        for file in education_files:
            SafetyFile.objects.create(
                safety=instance,
                file=file,
                file_type='education',
                description='Education Document'
            )

        for file in board_exam_files:
            SafetyFile.objects.create(
                safety=instance,
                file=file,
                file_type='board_exam',
                description='Board Exam Document'
            )

        for file in work_experience_files:
            SafetyFile.objects.create(
                safety=instance,
                file=file,
                file_type='work_experience',
                description='Work Experience Document'
            )

        for file in training_files:
            SafetyFile.objects.create(
                safety=instance,
                file=file,
                file_type='training',
                description='Training Document'
            )

        for file in notarized_files:
            SafetyFile.objects.create(
                safety=instance,
                file=file,
                file_type='notarized',
                description='Notarized Document'
            )

        return instance