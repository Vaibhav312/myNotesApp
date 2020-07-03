from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.



class ContactUsInfo(models.Model):
    name=models.CharField(max_length=50)
    email=models.EmailField(unique=True)
    subject=models.CharField(max_length=100)
    message=models.CharField(max_length=1000)

    def __str__(self):
        return self.name

class NotesInfo(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,default=1)  
    add_notes=models.TextField(max_length=2000)
    
    def __str__(self):
        return self.add_notes

