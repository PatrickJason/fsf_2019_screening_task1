"""p1 path Configuration

The `pathpatterns` list routes paths to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/paths/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a path to pathpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a path to pathpatterns:  path('', Home.as_view(), name='home')
Including another pathconf
    1. Import the include() function: from django.paths import include, path
    2. Add a path to pathpatterns:  path('blog/', include('blog.paths'))
"""
from django.contrib import admin
from django.urls import re_path,include
from . import views

urlpatterns = [
    re_path(r"^$", views.HomePage.as_view(), name="home"),
    re_path(r"^test/$", views.TestPage.as_view(), name="test"),
    re_path(r"^admin/", admin.site.urls),
    re_path(r"^thanks/$", views.ThanksPage.as_view(), name="thanks"),
    re_path(r"^accounts/", include("accounts.urls", namespace="accounts")),
    re_path(r"^accounts/", include("django.contrib.auth.urls")),
    re_path(r"^tasks/", include("tasks.urls", namespace="tasks")),
    re_path(r"^teams/",include("teams.urls", namespace="teams")),
]
