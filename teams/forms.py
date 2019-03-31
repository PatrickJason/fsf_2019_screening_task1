from django import forms
from teams import models
from django.contrib.auth.models import User
class TeamsForm(forms.ModelForm):
    class Meta:
        fields = ('name','description','team_members')
        model = models.Teams
        team_members = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,label="Notify and subscribe users to this post:",choices= [ (x.id,x) for x in User.objects.all()])

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        if user is not None:
            self.fields['team_members'].choices = [ (x.id,x) for x in User.objects.all()]
