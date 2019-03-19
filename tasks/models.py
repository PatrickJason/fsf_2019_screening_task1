from django.db import models
from django.utils import timezone
from django.urls import reverse,reverse_lazy
from django.contrib import auth
from django.conf import settings
# Create your models here.
class Tasks(models.Model):
    assignee = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete = models.CASCADE,null = True,default = 1)
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=200)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse_lazy('tasks:tasks_detail',kwargs={'pk':self.pk})

class Comments(models.Model):
    task = models.ForeignKey('tasks.tasks', related_name='comments',on_delete = models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete = models.CASCADE,default = 1)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.text
