from django.db import models
from django.urls import reverse
from django.conf import settings
from django.contrib.auth.models import User
# Create your models here.


class Teams(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, default='')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='team_created',
                                   on_delete=models.SET_NULL, null=True)
    team_members = models.ManyToManyField(User,related_name='member')

    def __str__(self):
        return self.name



    def get_absolute_url(self):
        return reverse("tasks:tasks_list")


    class Meta:
        ordering = ["name"]
