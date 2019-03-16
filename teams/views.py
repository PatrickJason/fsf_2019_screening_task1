from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.mixins import(
    LoginRequiredMixin,
    PermissionRequiredMixin
)

from django.urls import reverse
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from django.views import generic
from teams.models import Teams,TeamMember
from . import models

class CreateTeams(LoginRequiredMixin, generic.CreateView):
    fields = ("name", "description")
    model = Teams

class SingleTeams(generic.DetailView):
    model = Teams

class ListTeams(generic.ListView):
    model = Teams


class JoinTeams(LoginRequiredMixin, generic.RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return reverse("Teams:single",kwargs={"slug": self.kwargs.get("slug")})

    def get(self, request, *args, **kwargs):
        Teams = get_object_or_404(Teams,slug=self.kwargs.get("slug"))

        try:
            TeamsMember.objects.create(user=self.request.user,Teams=Teams)

        except IntegrityError:
            messages.warning(self.request,("Warning, already a member of {}".format(Teams.name)))

        else:
            messages.success(self.request,"You are now a member of the {} Teams.".format(Teams.name))

        return super().get(request, *args, **kwargs)


class LeaveTeams(LoginRequiredMixin, generic.RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return reverse("Teams:single",kwargs={"slug": self.kwargs.get("slug")})

    def get(self, request, *args, **kwargs):

        try:

            membership = models.TeamMember.objects.filter(
                user=self.request.user,
                Teams__slug=self.kwargs.get("slug")
            ).get()

        except models.TeamsMember.DoesNotExist:
            messages.warning(
                self.request,
                "You can't leave this Teams because you aren't in it."
            )
        else:
            membership.delete()
            messages.success(
                self.request,
                "You have successfully left this Teams."
            )
        return super().get(request, *args, **kwargs)
