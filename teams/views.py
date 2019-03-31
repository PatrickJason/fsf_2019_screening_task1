from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.mixins import(
    LoginRequiredMixin,
    PermissionRequiredMixin
)
from django.views.generic import DeleteView
from tasks.models import Tasks, Comments
from django.urls import reverse,reverse_lazy
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
        return super(CreateTeams, self).form_valid(form)
class SingleTeams(generic.DetailView):
    model = Teams
    def get_context_data(self, **kwargs):
        teams1=[]
        for t in Teams.objects.all():
            teams1.append([team for team in Teams.objects.all() if self.request.user in t.team_members.all()])
        # Store the teams created by the user
        teams_created = [team for team in Teams.objects.all() if self.request.user == team.created_by]
        # Store the tasks created by the user
        tasks_created = [task for task in Tasks.objects.all() if self.request.user == task.task_creator]
        # Store the tasks assigned to the user
        tasks_assigned = [task for task in Tasks.objects.all() if self.request.user == task.assignee]
        print(teams_created)
        team_str=[]
        for t in teams_created:
            team_str.append(str(t))
        print(team_str)
        # Store the tasks in the teams in which the user is a member
        my_team_tasks = []
        for team in teams1:
            for task in Tasks.objects.all():
                if task.assigned_to_team == team:
                    my_team_tasks.append(task)
        # Adding additional context to be used by the views
        context = super(SingleTeams, self).get_context_data(**kwargs)
        context['teams1'] = teams1
        context['teams_created']=teams_created
        context['tasks_created']=tasks_created
        context['tasks_assigned']=tasks_assigned
        context['my_team_tasks']=my_team_tasks
        context['team_str']= team_str
        return context


class ListTeams(generic.ListView):
    model = Teams


class TeamsDeleteView(LoginRequiredMixin,DeleteView):
    model = Teams
    success_url = reverse_lazy('tasks:tasks_list')
