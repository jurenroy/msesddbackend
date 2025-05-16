from django.db import models
from django.contrib.auth.models import User

#The postman works regarding about Token Authentication and JWT authentication but in the frontend server wont work idk why just reminding
class Note(models.Model):
    description = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='note')
