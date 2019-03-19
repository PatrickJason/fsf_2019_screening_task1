from django.conf.urls import re_path
from . import views

app_name = 'tasks'
urlpatterns = [
    re_path(r'^$',views.TasksListView.as_view(),name='tasks_list'),
    re_path(r'^about/$',views.AboutView.as_view(),name='about'),
    re_path(r'^tasks/new/$', views.CreateTasksView.as_view(), name='tasks_new'),
    re_path(r'^tasks/(?P<pk>\d+)$', views.TasksDetailView.as_view(), name='tasks_detail'),
    re_path(r'^tasks/(?P<pk>\d+)/edit/$', views.TasksUpdateView.as_view(), name='tasks_edit'),
    re_path(r'^tasks/(?P<pk>\d+)/remove/$', views.TasksDeleteView.as_view(), name='tasks_remove'),
    re_path(r'^tasks/(?P<pk>\d+)/comment/$', views.add_comment_to_tasks, name='add_comment_to_tasks'),
    re_path(r'^comment/(?P<pk>\d+)/remove/$', views.comment_remove, name='comment_remove'),
]
