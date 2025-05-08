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
    if instance.status.lower() == 'approved':
        update_fields = kwargs.get('update_fields') or set()
        if created or 'status' in update_fields:
            checklist = instance.checklist
            safety = checklist.safety
            recipient_email = safety.email

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
                plain_message = render_to_string('emails/checklist_approved_plain.txt', context)
                html_message = render_to_string('emails/checklist_approved.html', context)

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
    