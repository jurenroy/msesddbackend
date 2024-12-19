from django import forms
from .models import Safety

class SafetyForm(forms.ModelForm):
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
            'permitType', 'date', 'trackingCode'
        ]