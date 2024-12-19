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

    # New email field
    email = models.EmailField(max_length=100, blank=True, null=True)  # Use EmailField for email addresses

    # File fields for uploads
    educationFiles = models.JSONField(default=list, blank=True, null=True)
    boardExamFiles = models.JSONField(default=list, blank=True, null=True)
    workExperienceFiles = models.JSONField(default=list, blank=True, null=True)
    trainingFiles = models.JSONField(default=list, blank=True, null=True)
    notarizedFiles = models.JSONField(default=list, blank=True, null=True)

    # JSON fields for structured data
    education = models.JSONField(default=list, blank=True, null=True)  # Store as JSON
    boardExams = models.JSONField(default=list, blank=True, null=True)  # Store as JSON
    workExperience = models.JSONField(default=list, blank=True, null=True)  # Store as JSON
    trainings = models.JSONField(default=list, blank=True, null=True)  # Store as JSON

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
        # Generate a unique tracking code
        return str(uuid.uuid4())[:10]  # Adjust length as needed


class EducationFile(models.Model):
    safety = models.ForeignKey(Safety, related_name='education_files', on_delete=models.CASCADE)
    file = models.FileField(upload_to='education/')
    
class BoardExamFile(models.Model):
    safety = models.ForeignKey(Safety, related_name='board_exam_files', on_delete=models.CASCADE)
    file = models.FileField(upload_to='board_exams/')

class WorkExperienceFile(models.Model):
    safety = models.ForeignKey(Safety, related_name='work_experience_files', on_delete=models.CASCADE)
    file = models.FileField(upload_to='work_experience/')

class TrainingFile(models.Model):
    safety = models.ForeignKey(Safety, related_name='training_files', on_delete=models.CASCADE)
    file = models.FileField(upload_to='training/')

class NotarizedFile(models.Model):
    safety = models.ForeignKey(Safety, related_name='notarized_files', on_delete=models.CASCADE)
    file = models.FileField(upload_to='notarized/')