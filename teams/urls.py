from django.urls import re_path

from . import views

app_name = 'teams'

urlpatterns = [
    re_path(r"^$", views.ListTeams.as_view(), name="all"),
    re_path(r"^new/$", views.CreateTeams.as_view(), name="create"),
    re_path(r"^posts/in/(?P<pk>[-\w]+)/$",views.SingleTeams.as_view(),name="single"),
    re_path(r"join/(?P<slug>[-\w]+)/$",views.JoinTeams.as_view(),name="join"),
    re_path(r"leave/(?P<slug>[-\w]+)/$",views.LeaveTeams.as_view(),name="leave"),
    re_path(r'^teams/(?P<pk>\d+)/remove/$', views.TeamsDeleteView.as_view(), name='teams_remove'),
]
