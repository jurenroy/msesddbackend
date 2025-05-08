from django.db import models
from safety.models import Safety  # Adjust the import based on your project structure

class Checklist(models.Model):
    safety = models.ForeignKey(Safety, related_name='checklists', on_delete=models.CASCADE)

    # Application Form
    application_form = models.FileField(upload_to='checklist/application_forms/', blank=True, null=True)
    application_form_compliance = models.BooleanField(default=False)
    application_form_remarks = models.CharField(max_length=225, blank=True, null=True)

    # Educational credentials
    college_diploma = models.FileField(upload_to='checklist/college_diplomas/', blank=True, null=True)
    high_school_diploma = models.FileField(upload_to='checklist/high_school_diplomas/', blank=True, null=True)
    other_credentials = models.FileField(upload_to='checklist/other_credentials/', blank=True, null=True)
    college_diploma_compliance = models.BooleanField(default=False)
    college_diploma_remarks = models.CharField(max_length=225, blank=True, null=True)
    
    # Employment certificates
    present_employment = models.FileField(upload_to='checklist/present_employer/', blank=True, null=True)
    previous_employment = models.FileField(upload_to='checklist/previous_employer/', blank=True, null=True)
    present_employment_compliance = models.BooleanField(default=False)
    present_employment_remarks = models.CharField(max_length=225, blank=True, null=True)
    
    # Photo
    latest_photo = models.FileField(upload_to='checklist/photographs/', blank=True, null=True)
    latest_photo_compliance = models.BooleanField(default=False)
    latest_photo_remarks = models.CharField(max_length=225, blank=True, null=True)
    
    # Fees
    fee_permanent = models.FileField(upload_to='checklist/permanent_safety_fee/', blank=True, null=True)
    fee_temporary = models.FileField(upload_to='checklist/temporary_safety_fee/', blank=True, null=True)
    fee_compliance = models.BooleanField(default=False)
    fee_remarks = models.CharField(max_length=225, blank=True, null=True)
    
    # Endorsements
    endorsement_contractor = models.FileField(upload_to='checklist/contractor_officials/', blank=True, null=True)
    endorsement_safety_manager = models.FileField(upload_to='checklist/safety_manager/', blank=True, null=True)
    endorsement_compliance = models.BooleanField(default=False)
    endorsement_remarks = models.CharField(max_length=225, blank=True, null=True)
    
    # OSH Trainings
    osh_new = models.FileField(upload_to='checklist/new_application_training/', blank=True, null=True)
    osh_renewal = models.FileField(upload_to='checklist/renewal_application_training/', blank=True, null=True)
    osh_new_compliance = models.BooleanField(default=False)
    osh_new_remarks = models.CharField(max_length=225, blank=True, null=True)
    
    # Renewal permit
    renewal_permit = models.FileField(upload_to='checklist/last_safety_permit/', blank=True, null=True)
    renewal_permit_compliance = models.BooleanField(default=False)
    renewal_permit_remarks = models.CharField(max_length=225, blank=True, null=True)
    
    # Proofs of accomplishment
    proof_safety_inspection = models.FileField(upload_to='checklist/accident_reports/', blank=True, null=True)
    proof_osh_committee = models.FileField(upload_to='checklist/csh_committee_reports/', blank=True, null=True)
    proof_osh_program = models.FileField(upload_to='checklist/osh_shp_programs/', blank=True, null=True)
    proof_other_reports = models.FileField(upload_to='checklist/other_reports/', blank=True, null=True)
    other_reports_description = models.TextField(blank=True, null=True)
    proof_other_reports_compliance = models.BooleanField(default=False)
    proof_other_reports_remarks = models.CharField(max_length=225, blank=True, null=True)
    
    # Evaluation fields
    initial_evaluation = models.TextField(blank=True, null=True)
    reviewed_by = models.CharField(max_length=100, blank=True, null=True)
    
    # Created and updated timestamps
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return f"Checklist for {self.safety.name} - {self.safety.tracking_code}"



class ChecklistStatus(models.Model):
    checklist = models.ForeignKey(Checklist, related_name='status_history', on_delete=models.CASCADE)
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Checklist Status"
        verbose_name_plural = "Checklist Statuses"
    
    def __str__(self):
        return f"{self.checklist} - {self.status} on {self.created_at.strftime('%Y-%m-%d')}"
