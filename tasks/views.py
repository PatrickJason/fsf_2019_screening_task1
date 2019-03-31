from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from tasks.models import Tasks
from django.utils import timezone
from tasks.forms import TasksForm, CommentsForm,AddAssigneeForm
from teams.models import Teams
from django.views.generic import (TemplateView,ListView,
                                  DetailView,CreateView,
                                  UpdateView,DeleteView)
from django.contrib.auth import get_user_model
User =get_user_model()
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.
class AboutView(TemplateView):
    template_name = 'about.html'

class TasksListView(ListView):
    model = Tasks
    def get_context_data(self, **kwargs):
        teams=[]
        temp_for_storing_teams=[]
        # Obtaining the teams in which the user is the member and storing in the 'teams' list
        try:
            for t in Teams.objects.all():
                team_instance = t.team_members.all()    # Creating an instance to iterate through it
                for m in team_instance:
                    if str(m) == str(self.request.user):    # Checking if user is a member of the current team instance
                        temp_for_storing_teams.append(t)
                for var in temp_for_storing_teams:
                    if var not in teams:
                        teams.append(var)
        except ObjectDoesNotExist:
            print('team DoesNotExist')
        # Store the teams created by the user
        teams_created = [team for team in Teams.objects.all() if self.request.user == team.created_by]
        # Store the tasks created by the user
        tasks_created = [task for task in Tasks.objects.all() if self.request.user == task.task_creator]
        # Store the tasks assigned to the user
        tasks_assigned = [task for task in Tasks.objects.all() if self.request.user in task.assignee.all()]
        # Store the tasks in the teams in which the user is a member
        my_team_tasks = []
        for team in teams:
            for task in Tasks.objects.all():
                if task.assigned_to_team == team:
                    my_team_tasks.append(task)
        temp_members=[]
        context = super(TasksListView, self).get_context_data(**kwargs)
        context['teams'] = teams
        context['teams_created']=teams_created
        context['tasks_created']=tasks_created
        context['tasks_assigned']=tasks_assigned
        context['my_team_tasks']=my_team_tasks
        return context

class TasksDetailView(DetailView):
    model = Tasks


class CreateTasksView(LoginRequiredMixin,CreateView):
    login_url = '/login/'

    redirect_field_name = 'tasks/tasks_detail.html'


    form_class = TasksForm
    model = Tasks

    def get_form_kwargs(self):
        print(self.request.body)
        kwargs = super(CreateTasksView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def form_valid(self, form):
        form.instance.task_creator = self.request.user
        form.instance.task_creator_str = str(self.request.user)
        return super(CreateTasksView, self).form_valid(form)

class PassRequestToFormViewMixin:

    def get_form_kwargs(self):
        kwargs = super(PassRequestToFormViewMixin, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

class TasksUpdateView(PassRequestToFormViewMixin,LoginRequiredMixin,UpdateView):
    login_url = '/login/'
    template_name = 'tasks/tasks_update.html'
    redirect_field_name = 'tasks/tasks_detail.html'

    form_class = AddAssigneeForm

    model = Tasks


class TasksDeleteView(LoginRequiredMixin,DeleteView):
    model = Tasks
    success_url = reverse_lazy('tasks:tasks_list')


@login_required
def add_comment_to_tasks(request, pk):
    task = get_object_or_404(Tasks, pk=pk)
    if request.method == "POST":
        form = CommentsForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.task = task
            comment.author = request.user
            comment.save()
            return redirect('tasks:tasks_detail', pk=task.pk)
    else:
        form = CommentsForm()
    return render(request, 'tasks/comment_form.html', {'form': form})

@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comments, pk=pk)
    post_pk = comments.task.pk
    comment.delete()
    return redirect('tasks:tasks_detail', pk=task.pk)
