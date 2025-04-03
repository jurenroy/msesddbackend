# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Safety, Checklist

@receiver(post_save, sender=Safety)
def create_checklist_for_safety(sender, instance, created, **kwargs):
    if created:
        # Create a new checklist for the newly created safety record
        Checklist.objects.create(
            safety=instance,
            
            )