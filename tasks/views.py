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
        try:
            for t in Teams.objects.all():
                team_instance = t.team_members.all()
                for m in team_instance:
                    if str(m) == str(self.request.user):
                        temp_for_storing_teams.append(t)
                for var in temp_for_storing_teams:
                    if var not in teams:
                        teams.append(var)
        except ObjectDoesNotExist:
            print('team DoesNotExist')
            # break
        print(teams)
        # t = Teams.objects.first()
        # application.positions.all()
        # t = Teams.objects.first()
        # application.positions.all()
        # teams = [team for team in Teams.objects.all() if self.request.user in t.team_members.all()]
        teams_created = [team for team in Teams.objects.all() if self.request.user == team.created_by]
        tasks_created = [task for task in Tasks.objects.all() if self.request.user == task.task_creator]
        for t in Tasks.objects.all():
            for i in t.assignee.all():
                print('assignee',i)
        tasks_assigned = [task for task in Tasks.objects.all() if self.request.user in task.assignee.all()]
        my_team_tasks = []
        for team in teams:
            for task in Tasks.objects.all():
                if task.assigned_to_team == team:
                    my_team_tasks.append(task)
        temp_members=[]
        print('teams :',teams)
        # for team in teams:
            # for mem in team.team_members.all():
                # temp_members.append(mem)
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
    def get_form_kwargs(self):
        kwargs = super(CreateTasksView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs
    # def __init__(self, **kwargs):
    #     """
    #     Constructor. Called in the URLconf; can contain helpful extra
    #     keyword arguments, and other things.
    #     """
    #     # Go through keyword arguments, and either save their values to our
    #     # instance, or raise an error.
    #     for key, value in kwargs.items():
    #         setattr(self, key, value)
    #         teams=[]
    #         temp_for_storing_teams=[]
    #         # for t in Teams.objects.None():
    #         i=1
    #         memb =[]
    #         try:
    #             myid = self.instance.assigned_to_team_id
    #             print(myid)
    #             t = Teams.objects.get(id = myid)
    #             i=i+1
    #             team_instance = t.team_members.all()
    #             for m in team_instance:
    #                 memb.append(m)
    #                 if str(m) == str(self.request.user):
    #                     temp_for_storing_teams.append(t)
    #             # temp =[team for team in Teams.objects.all() if self.request.user in t.team_members.all()]
    #             for var in temp_for_storing_teams:
    #                 if var not in teams:
    #                     teams.append(var)
    #         except ObjectDoesNotExist:
    #             print('team DoesNotExist')
    #         print('memb',memb)
    #         c=[]
    #         i=0
    #         teams_created = [team for team in Teams.objects.all() if request.user == team.created_by]
    #         for x in teams_created:
    #             i=i+1
    #             c.append((i,x))
    #         c=tuple(c)
    #         print(c)
    #         val = [ (x.id,x) for x in User.objects.all()]
    #         print(val)
    #         # assigned_to_team = forms.ChoiceField(widget=forms.Select(),label="Notify and subscribe users to this post:",choices= c)
    #         # self.fields['assigned_to_team'].choices = c
    #         # assigned_to_team = request.POST.get('assigned_to_team')
    #         # form.fields['assigned_to_team'].choices = c
    # def _set_queryset(self, queryset):
    #     self._queryset = None if queryset is None else queryset
    #     self.widget.choices = self.choices
    # def get_queryset(self):
    #     """
    #     Return the `QuerySet` that will be used to look up the object.
    #     This method is called by the default implementation of get_object() and
    #     may not be called if get_object() is overridden.
    #     """
    #     if self.queryset is None:
    #         if self.model:
    #             return self.model._default_manager.all()
    #         else:
    #             raise ImproperlyConfigured(
    #                 "%(cls)s is missing a QuerySet. Define "
    #                 "%(cls)s.model, %(cls)s.queryset, or override "
    #                 "%(cls)s.get_queryset()." % {
    #                     'cls': self.__class__.__name__
    #                 }
    #             )
    #     return self.queryset

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
