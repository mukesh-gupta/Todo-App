from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
# Create your models here.
from django.utils.timezone import datetime



class Todo(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    title=models.CharField(max_length=100)
    desc=models.TextField(blank=True)
    image=models.ImageField(upload_to='images/')
    created = models.DateTimeField(auto_now_add=True)
    important = models.BooleanField(default=False)
    datecompleted = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title













