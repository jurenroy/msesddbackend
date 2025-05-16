# signals.py
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.template.loader import render_to_string
from .models import Safety, Checklist, ChecklistStatus

@receiver(post_save, sender=Safety)
def create_checklist_for_safety(sender, instance, created, **kwargs):
    if created:
        # Create a new checklist for the newly created safety record
        checklist = Checklist.objects.create(safety=instance)

        ChecklistStatus.objects.create(
            checklist=checklist,
            status='pending',
            )

@receiver(post_save, sender=ChecklistStatus)
def send_approval_notification(sender, instance, created, **kwargs):
    print(f"ChecklistStatus signal triggered: status={instance.status}, created={created}")
    
    if instance.status.lower() == 'approved':
        update_fields = kwargs.get('update_fields') or set()
        print(f"Status is approved. update_fields={update_fields}")
        
        # Always process the email when status is 'approved', regardless of created or update_fields
        checklist = instance.checklist
        safety = checklist.safety
        recipient_email = safety.email

        print(f"Safety record: {safety.name}, Email: {recipient_email}")

        if not recipient_email:
            print(f"No email address found for {safety.name}. Email notification not sent.")
            return

        subject = f"Your Safety Checklist ({safety.tracking_code}) has been APPROVED"

        context = {
            'safety': safety,
            'checklist': checklist,
            'status': instance,
            'approval_date': getattr(instance, 'created_at', None).strftime('%B %d, %Y') if getattr(instance, 'created_at', None) else 'N/A',
        }

        try:
            # Fix the template paths to match the actual file names
            plain_message = render_to_string('email/checklist_approved._plain.txt', context)
            html_message = render_to_string('email/checklist_approved.html', context)

            print(f"Attempting to send email to {recipient_email} from {settings.DEFAULT_FROM_EMAIL}")
            
            send_mail(
                subject=subject,
                message=plain_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[recipient_email],
                html_message=html_message,
                fail_silently=False,
            )
            print(f"Approval email sent to {recipient_email}")
        except Exception as e:
            print(f"Failed to send approval email to {recipient_email}: {e}")
            # Print the exception traceback for debugging
            import traceback
            traceback.print_exc()
    