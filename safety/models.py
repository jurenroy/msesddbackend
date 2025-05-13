import uuid
from django.db import models

class Safety(models.Model):
    name = models.CharField(max_length=100, null=True)
    address = models.CharField(max_length=255, null=True)
    contactNo = models.CharField(max_length=15, null=True)
    age = models.IntegerField(null=True)
    civilStatus = models.CharField(max_length=20, null=True)
    dateOfBirth = models.DateField(null=True)
    placeOfBirth = models.CharField(max_length=100, null=True)
    citizenship = models.CharField(max_length=50, null=True)
    howAcquired = models.CharField(max_length=100, null=True)
    lastResidence = models.CharField(max_length=255, null=True)
    dateOfArrival = models.DateField(null=True)
    landingCertificateNo = models.CharField(max_length=100, null=True)
    employmentContract = models.CharField(max_length=100, null=True)
    employmentNature = models.CharField(max_length=100, null=True)
    companyName = models.CharField(max_length=100, null=True)
    presentCompanyName = models.CharField(max_length=100, null=True)
    presentCompanyAddress = models.CharField(max_length=255, null=True)
    email = models.EmailField(max_length=100, blank=True, null=True)

    # File fields for uploads
    educationFiles = models.FileField(upload_to='education/', null=True, blank=True)
    boardExamFiles = models.FileField(upload_to='board_exams/', null=True, blank=True)
    workExperienceFiles = models.FileField(upload_to='work_experience/', null=True, blank=True)
    trainingFiles = models.FileField(upload_to='training/', null=True, blank=True)
    notarizedFiles = models.FileField(upload_to='notarized/', null=True, blank=True)
    
    # Additional document fields
    application_form = models.FileField(upload_to='application_forms/', null=True, blank=True)
    photo = models.FileField(upload_to='photos/', null=True, blank=True)
    notarized_document = models.FileField(upload_to='notarized_docs/', null=True, blank=True)
    proof_document = models.FileField(upload_to='proof_docs/', null=True, blank=True)

    # JSON fields for structured data
    education = models.JSONField(default=list, blank=True, null=True)
    boardExams = models.JSONField(default=list, blank=True, null=True)
    workExperience = models.JSONField(default=list, blank=True, null=True)
    trainings = models.JSONField(default=list, blank=True, null=True)
    
    documents = models.BooleanField(default=False, null=True)
    compliance = models.BooleanField(default=False, null=True)
    understanding = models.BooleanField(default=False, null=True)
    certify = models.BooleanField(default=False, null=True)
    permit_type = models.CharField(max_length=20, default='Permanent', null=True)
    role = models.CharField(max_length=20, null=True)
    date = models.DateField(auto_now_add=True, null=True)
    tracking_code = models.CharField(max_length=10, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.tracking_code:
            self.tracking_code = self.generate_unique_tracking_code()
        super().save(*args, **kwargs)

    def generate_unique_tracking_code(self):
        return str(uuid.uuid4())[:10]

    def __str__(self):
        return f"{self.name} - {self.tracking_code}"

class Education(models.Model):
    safety = models.ForeignKey(Safety, related_name='education_records', on_delete=models.CASCADE)
    school_name = models.CharField(max_length=255)
    degree = models.CharField(max_length=255)
    year_completed = models.IntegerField()
    major = models.CharField(max_length=255, blank=True, null=True)
    document = models.FileField(upload_to='safety_files/education/', null=True, blank=True)
    
    def __str__(self):
        return f"{self.safety.name} - {self.degree} from {self.school_name}"

class BoardExam(models.Model):
    safety = models.ForeignKey(Safety, related_name='board_exam_records', on_delete=models.CASCADE)
    exam_name = models.CharField(max_length=255)
    date_taken = models.DateField()
    license_number = models.CharField(max_length=100)
    expiry_date = models.DateField(null=True, blank=True)
    document = models.FileField(upload_to='safety_files/board_exams/', null=True, blank=True)
    
    def __str__(self):
        return f"{self.safety.name} - {self.exam_name}"

class WorkExperience(models.Model):
    safety = models.ForeignKey(Safety, related_name='work_experience_records', on_delete=models.CASCADE)
    company_name = models.CharField(max_length=255)
    position = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    responsibilities = models.TextField(blank=True, null=True)
    document = models.FileField(upload_to='safety_files/work_experience/', null=True, blank=True)
    
    def __str__(self):
        return f"{self.safety.name} - {self.position} at {self.company_name}"

class Training(models.Model):
    safety = models.ForeignKey(Safety, related_name='training_records', on_delete=models.CASCADE)
    training_name = models.CharField(max_length=255)
    provider = models.CharField(max_length=255)
    date_completed = models.DateField()
    certificate_number = models.CharField(max_length=100, blank=True, null=True)
    document = models.FileField(upload_to='safety_files/training/', null=True, blank=True)
    
    def __str__(self):
        return f"{self.safety.name} - {self.training_name}"

class SafetyFile(models.Model):
    safety = models.ForeignKey(Safety, related_name='files', on_delete=models.CASCADE)
    file = models.FileField(upload_to='safety_files/')
    file_type = models.CharField(max_length=50, choices=[
        ('education', 'Education'),
        ('board_exam', 'Board Exam'),
        ('work_experience', 'Work Experience'),
        ('training', 'Training'),
        ('notarized', 'Notarized'),
        ('application', 'Application Form'),
        ('photo', 'Photograph'),
        ('fee', 'Fee Payment'),
        ('endorsement', 'Endorsement'),
        ('permit', 'Permit'),
        ('proof', 'Proof Document')
    ])
    description = models.CharField(max_length=255, blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

class TrainingFile(models.Model):
    safety = models.ForeignKey(Safety, related_name='training_files', on_delete=models.CASCADE)
    file = models.FileField(upload_to='training/')

    def __str__(self):
        return f"{self.safety.name} - {self.file_type} - {self.description}"

    