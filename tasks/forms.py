from django import forms
from teams.models import Teams
from . models import Tasks,Comments
from django.db import models

class TasksForm(forms.ModelForm):
    class Meta:
        model = Tasks
        fields = ('title','description','status','assigned_to_team',)
        # widgets = {
        # 'assignee': forms.HiddenInput()
        # }
    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        if user is not None:
            self.fields["assigned_to_team"].queryset = (
                Teams.objects.filter(
                    pk__in=user.teams.values_list("teams__pk")
                )
            )
class CommentsForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ('text',)
