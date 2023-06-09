from django.utils import timezone
from django.db import models
from jazzmin.templatetags.jazzmin import User

# Create your models here.
class Todo(models.Model):
    title=models.CharField(max_length=100)
    details=models.TextField()
    date=models.DateTimeField(default=timezone.now)
    created_by=models.ForeignKey(User,on_delete=models.CASCADE)

    
    def __str__(self):
        return self.title