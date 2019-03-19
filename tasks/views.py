from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from tasks.models import Tasks, Comments
from django.utils import timezone
from tasks.forms import TasksForm, CommentsForm

from django.views.generic import (TemplateView,ListView,
                                  DetailView,CreateView,
                                  UpdateView,DeleteView)

from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.
class AboutView(TemplateView):
    template_name = 'about.html'

class TasksListView(ListView):
    model = Tasks

    def get_queryset(self):
        return Tasks.objects.filter(created_date__lte=timezone.now()).order_by('-created_date')

class TasksDetailView(DetailView):
    model = Tasks


class CreateTasksView(LoginRequiredMixin,CreateView):
    login_url = '/login/'

    redirect_field_name = 'tasks/tasks_detail.html'

    form_class = TasksForm

    model = Tasks
    def form_valid(self, form):
        form.instance.assignee = self.request.user
        return super(CreateTasksView, self).form_valid(form)
    # def get_initial(self):
    #     return {
    #         'assignee': self.request.user
    #     }
    # def get_success_url(self):
    #     return reverse_lazy("tasks_detail")

class TasksUpdateView(LoginRequiredMixin,UpdateView):
    login_url = '/login/'
    redirect_field_name = 'tasks/tasks_detail.html'

    form_class = TasksForm

    model = Tasks


class TasksDeleteView(LoginRequiredMixin,DeleteView):
    model = Tasks
    success_url = reverse_lazy('tasks_list')


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
