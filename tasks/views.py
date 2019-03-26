from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from tasks.models import Tasks
from django.utils import timezone
from tasks.forms import TasksForm, CommentsForm
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
        # for t in Teams.objects.None():
        i=1
        while(True):
            try:
                t = Teams.objects.get(id=i)
                i=i+1
                team_instance = t.team_members.all()
                for m in team_instance:
                    if str(m) == str(self.request.user):
                        temp_for_storing_teams.append(t)
                # temp =[team for team in Teams.objects.all() if self.request.user in t.team_members.all()]
                for var in temp_for_storing_teams:
                    if var not in teams:
                        teams.append(var)
            except ObjectDoesNotExist:
                print('team DoesNotExist')
                break
        print(teams)
        # t = Teams.objects.first()
        # application.positions.all()
        # t = Teams.objects.first()
        # application.positions.all()
        # teams = [team for team in Teams.objects.all() if self.request.user in t.team_members.all()]
        teams_created = [team for team in Teams.objects.all() if self.request.user == team.created_by]
        tasks_created = [task for task in Tasks.objects.all() if self.request.user == task.task_creator]
        tasks_assigned = [task for task in Tasks.objects.all() if self.request.user == task.assignee]
        my_team_tasks = []
        for team in teams:
            for task in Tasks.objects.all():
                if task.assigned_to_team == team:
                    my_team_tasks.append(task)
        temp_members=[]
        print('teams :',teams)
        print('members',temp_members)

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
    def form_valid(self, form):
        form.instance.task_creator = self.request.user
        form.instance.task_creator_str = str(self.request.user)
        return super(CreateTasksView, self).form_valid(form)


class TasksUpdateView(LoginRequiredMixin,UpdateView):
    login_url = '/login/'
    redirect_field_name = 'tasks/tasks_detail.html'

    form_class = TasksForm

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
