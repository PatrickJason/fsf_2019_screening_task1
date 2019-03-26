from django.db import models
from django.utils import timezone
from django.urls import reverse,reverse_lazy
from django.contrib import auth
from django.conf import settings
from django.contrib.auth.models import User
from teams.models import Teams
# Create your models here.
class Tasks(models.Model):
    task_creator = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete = models.CASCADE,related_name="creator")
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=200)
    task_creator_str = models.TextField(default = 1)
    assignee = models.ManyToManyField(User)
    assigned_to_team = models.ForeignKey(Teams,related_name="assigned_to_team",on_delete = models.CASCADE,null = True)
    last_modified = models.DateTimeField( auto_now=True, editable=False)
    def __str__(self):
        return str(self.title)

    def get_absolute_url(self):
        return reverse_lazy('tasks:tasks_detail',kwargs={'pk':self.pk})




class Comments(models.Model):
    task = models.ForeignKey(Tasks, related_name='comments',on_delete = models.CASCADE)
    # print(settings.AUTH_USER_MODEL)
    author = models.ForeignKey(settings.AUTH_USER_MODEL,related_name ='created_by',on_delete = models.PROTECT)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.text
