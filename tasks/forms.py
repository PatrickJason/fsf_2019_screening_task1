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
        """

        Constructor. Called in the URLconf; can contain helpful extra
        keyword arguments, and other things.
        """
        self.request = kwargs.pop("request")
        super(AddAssigneeForm, self).__init__(*args, **kwargs)
        teams=[]
        temp_for_storing_teams=[]
        # for t in Teams.objects.None():
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
            # temp =[team for team in Teams.objects.all() if self.request.user in t.team_members.all()]
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

        # Go through keyword arguments, and either save their values to our
        # instance, or raise an error.


class TasksForm(forms.ModelForm):
    class Meta:
        model = Tasks

        fields = ('title','description','status','assigned_to_team',)
        assigned_to_team = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,label="Notify and subscribe users to this post:")

    def __init__(self, *args, **kwargs):
        """
        Constructor. Called in the URLconf; can contain helpful extra
        keyword arguments, and other things.
        """
        user = kwargs.pop("user")
        # self.request = kwargs.pop("request")
        super(TasksForm, self).__init__(*args, **kwargs)
        teams=[]
        temp_for_storing_teams=[]
        # for t in Teams.objects.None():
        i=1
        memb =[]
        try:
            myid = self.instance.assigned_to_team_id
            print(myid)
            t = Teams.objects.get(id = myid)
            i=i
            team_instance = t.team_members.all()
            for m in team_instance:
                memb.append(m)
                if str(m) == str(self.request.user):
                    temp_for_storing_teams.append(t)
            # temp =[team for team in Teams.objects.all() if self.request.user in t.team_members.all()]
            for var in temp_for_storing_teams:
                if var not in teams:
                    teams.append(var)
        except ObjectDoesNotExist:
            print('team DoesNotExist')
        print('memb',memb)
        c=[]
        print('user','username',user,user.username)
        teams_created = [team for team in Teams.objects.all() if user.username == str(team.created_by)]
        i=0
        list_t=[]
        print(teams_created)
        for x in teams_created:
            i=i+1
            c.append((x.id,x))
            list_t.append(x)
        c=tuple(c)
        print(c,'user',user.id)
        val = [ (x.id,x) for x in User.objects.all()]
        print(val)
        query = "SELECT id,name FROM 'teams_teams' WHERE created_by_id ={}".format(str(user.id))
        # assigned_to_team = forms.ModelChoiceField(widget=forms.Select(),label="Notify and subscribe users to this post:",queryset =Teams.objects.raw(query) )
        self.fields['assigned_to_team'].choices = c
        # widgets = {
        # 'assignee': forms.HiddenInput()
        # }
    # def __init__(self, *args, **kwargs):
    #     user = kwargs.pop("user", None)
    #     super().__init__(*args, **kwargs)

        # if user is not None:
        print(query)
        # self.fields["assigned_to_team"].queryset =( Teams.objects.raw(query) )
    def _set_queryset(self, queryset):
        self._queryset = None if queryset is None else queryset
        self.widget.choices = self.choices
    def get_queryset(self):
        """
        Return the `QuerySet` that will be used to look up the object.
        This method is called by the default implementation of get_object() and
        may not be called if get_object() is overridden.
        """
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
