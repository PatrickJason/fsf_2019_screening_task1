from django.db import models
from django.urls import reverse

from django.contrib.auth import get_user_model
User = get_user_model()
# Create your models here.


class Teams(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(allow_unicode=True, unique=True)
    description = models.TextField(blank=True, default='')
    members = models.ManyToManyField(User,through="TeamMember")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("Teams:single", kwargs={"slug": self.slug})


    class Meta:
        ordering = ["name"]


class TeamMember(models.Model):
    team = models.ForeignKey(Teams, related_name="memberships",on_delete = models.CASCADE)
    user = models.ForeignKey(User,related_name='user_teams',on_delete = models.CASCADE)

    def __str__(self):
        return self.user.username

    class Meta:
        unique_together = ("team", "user")
