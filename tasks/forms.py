from django import forms
from teams.models import Teams
from . models import Tasks,Comments
from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model
User =get_user_model()


class AddAssigneeForm(forms.ModelForm):
    class Meta:
        model = Tasks
        fields =('title','description','assignee',)
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(AddAssigneeForm, self).__init__(*args, **kwargs)
        teams=[]
        temp_for_storing_teams=[]
        i=1
        memb =[]
        try:
            myid = self.instance.assigned_to_team_id
            print(myid)
            t = Teams.objects.get(id = int(myid))
            i=i+1
            team_instance = t.team_members.all()
            for m in team_instance:
                memb.append(m)
                if str(m) == str(self.request.user):
                    temp_for_storing_teams.append(t)
            for var in temp_for_storing_teams:
                if var not in teams:
                    teams.append(var)
        except ObjectDoesNotExist:
            print('team DoesNotExist')
        print('memb',memb)
        c=[]
        i=0
        for x in memb:
            i=i+1
            c.append((i,x))
        if self.request.user not in memb:
            c.append((i+1,str(self.request.user)))
        c=tuple(c)
        print(c)
        val = [ (x.id,x) for x in User.objects.all()]
        print(val)
        assignee = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,label="Notify and subscribe users to this post:",choices= c)
        self.fields['assignee'].choices = c



class TasksForm(forms.ModelForm):
    class Meta:
        model = Tasks

        fields = ('title','description','status','assigned_to_team',)
        assigned_to_team = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,label="Notify and subscribe users to this post:")

    def __init__(self, *args, **kwargs):

        user = kwargs.pop("user")
        super(TasksForm, self).__init__(*args, **kwargs)
        teams=[]
        temp_for_storing_teams=[]
        i=1
        memb =[]
        try:
            myid = self.instance.assigned_to_team_id
            t = Teams.objects.get(id = myid)
            i=i
            team_instance = t.team_members.all()
            for m in team_instance:
                memb.append(m)
                if str(m) == str(self.request.user):
                    temp_for_storing_teams.append(t)
            for var in temp_for_storing_teams:
                if var not in teams:
                    teams.append(var)
        except ObjectDoesNotExist:
            print('team DoesNotExist')
        c=[]
        teams_created = [team for team in Teams.objects.all() if user.username == str(team.created_by)]
        i=0
        list_t=[]
        for x in teams_created:
            i=i+1
            c.append((x.id,x))
            list_t.append(x)
        c=tuple(c)
        self.fields['assigned_to_team'].choices = c
    def _set_queryset(self, queryset):
        self._queryset = None if queryset is None else queryset
        self.widget.choices = self.choices
    def get_queryset(self):
        if self.queryset is None:
            if self.model:
                return self.model._default_manager.all()
            else:
                raise ImproperlyConfigured(
                    "%(cls)s is missing a QuerySet. Define "
                    "%(cls)s.model, %(cls)s.queryset, or override "
                    "%(cls)s.get_queryset()." % {
                        'cls': self.__class__.__name__
                    }
                )
        return self.queryset
class CommentsForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ('text',)
