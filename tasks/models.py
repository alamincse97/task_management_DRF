from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Task(models.Model):
    PRIORITY_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
    ]
    title = models.CharField(max_length=250)
    description = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField()
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES)
    is_complete = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    
    def __str__(self):
        return self.title
    
class Photo(models.Model):
    task = models.ForeignKey(
        Task, on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField(upload_to='photos/')
    
    def __str__(self):
        return self.image.name