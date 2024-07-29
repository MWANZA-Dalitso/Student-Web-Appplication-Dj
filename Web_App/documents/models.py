# documents/models.py
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from accounts.models import Profile
from chat.models import Notification

class Document(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    file = models.FileField(upload_to='documents/')

    def __str__(self):
        return f"Document for {self.profile.student_name}"

@receiver(post_save, sender=Document)
def document_missing(sender, instance, **kwargs):
    if not instance.file:
        Notification.objects.create(
            user=instance.profile.user,  # Assuming Profile has a OneToOneField to User
            notification_type='document',
            message=f'A document is missing for {instance.profile.student_name}.'
        )
