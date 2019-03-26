from django import forms
from teams import models
from django.contrib.auth.models import User
class TeamsForm(forms.ModelForm):
    class Meta:
        fields = ('name','description','team_members')
        model = models.Teams
        team_members = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,label="Notify and subscribe users to this post:",choices= [ (x.id,x) for x in User.objects.all()])
            #         # self.fields["team_members"].queryset = (
            #         # models.User.objects.none()
            #         #
        # i=0
        # c=((),)
        # for x in User.objects.none():
        #     i=i+1
        #     c.append(i,x)
        #
        # fields['team_members'].choices =  c
    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        # i=0
        # c=((),)
        # temp = User.objects.none()
        # for x in temp:
        #     i=i+1
        #     c.append(i,x)
        # STATUSES = (
        #     ('to-do', ('To Do')),
        #     ('planned', ('Planned')),
        #     ('in_progress', ('In Progress')),
        #     ('done', ('Done')),
        #     ('dismissed', ('Dismissed'))
        # )
        # self.fields.team_members = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,label="Notify and subscribe users to this post:")
        # self.fields['team_members'].choices = [ (x.id,x) for x in User.objects.all()]
        if user is not None:
            # self.fields["team_members"].queryset = (
            # models.User.objects.none()
            #     )
            self.fields['team_members'].choices = [ (x.id,x) for x in User.objects.all()]
