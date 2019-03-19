from django import forms

from . models import Tasks,Comments

class TasksForm(forms.ModelForm):
    class Meta:
        model = Tasks
        fields = ('title','description','status',)
        widgets = {
        'assignee': forms.HiddenInput()
        }

class CommentsForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ('text',)
