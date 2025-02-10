from django.db import models
from safety.models import Safety  # Adjust the import based on your project structure

class Checklist(models.Model):
    safety = models.ForeignKey(Safety, related_name='checklists', on_delete=models.CASCADE)

    # Checklist items as file uploads
    college_diploma = models.FileField(upload_to='checklist/college_diplomas/', blank=True, null=True)
    college_diploma_compliance = models.BooleanField(default=False)
    college_diploma_remarks = models.CharField(max_length=100, blank=True, null=True)

    high_school_diploma = models.FileField(upload_to='checklist/high_school_diplomas/', blank=True, null=True)
    high_school_diploma_compliance = models.BooleanField(default=False)
    high_school_diploma_remarks = models.CharField(max_length=100, blank=True, null=True)

    valid_prc_license = models.FileField(upload_to='checklist/prc_licenses/', blank=True, null=True)
    valid_prc_license_compliance = models.BooleanField(default=False)
    valid_prc_license_remarks = models.CharField(max_length=100, blank=True, null=True)

    other_credentials = models.FileField(upload_to='checklist/other_credentials/', blank=True, null=True)
    other_credentials_compliance = models.BooleanField(default=False)
    other_credentials_remarks = models.CharField(max_length=100, blank=True, null=True)

    present_employer_notarized = models.FileField(upload_to='checklist/present_employer/', blank=True, null=True)
    present_employer_notarized_compliance = models.BooleanField(default=False)
    present_employer_notarized_remarks = models.CharField(max_length=100, blank=True, null=True)

    previous_employer = models.FileField(upload_to='checklist/previous_employer/', blank=True, null=True)
    previous_employer_compliance = models.BooleanField(default=False)
    previous_employer_remarks = models.CharField(max_length=100, blank=True, null=True)

    permanent_safety_fee = models.FileField(upload_to='checklist/permanent_safety_fee/', blank=True, null=True)
    permanent_safety_fee_compliance = models.BooleanField(default=False)
    permanent_safety_fee_remarks = models.CharField(max_length=100, blank=True, null=True)

    temporary_safety_fee = models.FileField(upload_to='checklist/temporary_safety_fee/', blank=True, null=True)
    temporary_safety_fee_compliance = models.BooleanField(default=False)
    temporary_safety_fee_remarks = models.CharField(max_length=100, blank=True, null=True)

    contractor_officials = models.FileField(upload_to='checklist/contractor_officials/', blank=True, null=True)
    contractor_officials_compliance = models.BooleanField(default=False)
    contractor_officials_remarks = models.CharField(max_length=100, blank=True, null=True)

    safety_manager = models.FileField(upload_to='checklist/safety_manager/', blank=True, null=True)
    safety_manager_compliance = models.BooleanField(default=False)
    safety_manager_remarks = models.CharField(max_length=100, blank=True, null=True)

    new_application_training = models.FileField(upload_to='checklist/new_application_training/', blank=True, null=True)
    new_application_training_compliance = models.BooleanField(default=False)
    new_application_training_remarks = models.CharField(max_length=100, blank=True, null=True)

    renewal_application_training = models.FileField(upload_to='checklist/renewal_application_training/', blank=True, null=True)
    renewal_application_training_compliance = models.BooleanField(default=False)
    renewal_application_training_remarks = models.CharField(max_length=100, blank=True, null=True)

    last_safety_permit = models.FileField(upload_to='checklist/last_safety_permit/', blank=True, null=True)
    last_safety_permit_compliance = models.BooleanField(default=False)
    last_safety_permit_remarks = models.CharField(max_length=100, blank=True, null=True)

    accident_report = models.FileField(upload_to='checklist/accident_reports/', blank=True, null=True)
    accident_report_compliance = models.BooleanField(default=False)
    accident_report_remarks = models.CharField(max_length=100, blank=True, null=True)

    safety_inspection_audit_report = models.FileField(upload_to='checklist/safety_inspection_audit_reports/', blank=True, null=True)
    safety_inspection_audit_report_compliance = models.BooleanField(default=False)
    safety_inspection_audit_report_remarks = models.CharField(max_length=100, blank=True, null=True)

    csh_committee_report = models.FileField(upload_to='checklist/csh_committee_reports/', blank=True, null=True)
    csh_committee_report_compliance = models.BooleanField(default=False)
    csh_committee_report_remarks = models.CharField(max_length=100, blank=True, null=True)

    osh_shp_program = models.FileField(upload_to='checklist/osh_shp_programs/', blank=True, null=True)
    osh_shp_program_compliance = models.BooleanField(default=False)
    osh_shp_program_remarks = models.CharField(max_length=100, blank=True, null=True)

    other_reportsFile = models.FileField(upload_to='checklist/other_reports/', blank=True, null=True)
    other_reportsFile_compliance = models.BooleanField(default=False)
    other_reportsFile_remarks = models.CharField(max_length=100, blank=True, null=True)
    
    other_reports = models.TextField(blank=True, null=True)  # For specifying other reports

    # Evaluation fields
    complete_documents = models.BooleanField(default=False)
    incomplete_documents = models.BooleanField(default=True)

    # Name and signature fields
    name = models.CharField(max_length=100, blank=True, null=True)
    signature = models.CharField(max_length=1000, blank=True, null=True)  # Assuming signature is an image

    def __str__(self):
        return f"Checklist for {self.safety.name} - {self.safety.tracking_code}"



    


    

