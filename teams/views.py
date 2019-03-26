from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.mixins import(
    LoginRequiredMixin,
    PermissionRequiredMixin
)
from tasks.models import Tasks, Comments
from django.urls import reverse
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from django.views import generic
from teams.models import Teams
from . import models
from teams.forms import TeamsForm
class CreateTeams(LoginRequiredMixin, generic.CreateView):
    login_url = '/login/'
    template_name='teams/teams_form.html'
    redirect_field_name = 'tasks/'
    form_class = TeamsForm

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        # return super().get(request, *args, **kwargs)
        return super(CreateTeams, self).form_valid(form)
class SingleTeams(generic.DetailView):
    model = Teams
    def get_context_data(self, **kwargs):
        teams1=[]
        for t in Teams.objects.all():
        # t = Teams.objects.first()
        # application.positions.all()
            teams1.append([team for team in Teams.objects.all() if self.request.user in t.team_members.all()])
        teams_created = [team for team in Teams.objects.all() if self.request.user == team.created_by]
        tasks_created = [task for task in Tasks.objects.all() if self.request.user == task.task_creator]
        tasks_assigned = [task for task in Tasks.objects.all() if self.request.user == task.assignee]
        # team_mem = [ mem for mem in ]
        my_team_tasks = []
        for team in teams1:
            for task in Tasks.objects.all():
                if task.assigned_to_team == team:
                    my_team_tasks.append(task)
        context = super(SingleTeams, self).get_context_data(**kwargs)
        context['teams1'] = teams1
        context['teams_created']=teams_created
        context['tasks_created']=tasks_created
        context['tasks_assigned']=tasks_assigned
        context['my_team_tasks']=my_team_tasks
        return context


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
