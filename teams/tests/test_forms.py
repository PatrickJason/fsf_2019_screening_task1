from django.test import SimpleTestCase
from django.test import TestCase,Client
from django.urls import reverse
from tasks.models import Tasks,Comments
from teams.models import Teams
from django.contrib.auth.models import User
from teams.forms import TeamsForm


class TestForms(TestCase):

    def test_teams_form_valid_data(self):
        User.objects.create_user('Patrick2', 'jpatrickjason@gmail.com', 'patpassword')
        pat2 = User.objects.get(username='Patrick2')
        User.objects.create_user('Patrick1', 'jpatrickjason@gmail.com', 'patpassword')
        pat = User.objects.get(username='Patrick1')
        Teams.objects.create(name="team12", created_by=pat,)
        team = Teams.objects.get(name="team12")
        form = TeamsForm(data={
            'name':"New team",
            'description':"i am testing",
            'created_by':pat,
            'team_members':[pat.id,pat2.id]
        }
        )
        print(form.errors)
        self.assertTrue(form.is_valid())
    def test_teams_form_valid_with_no_data(self):
        User.objects.create_user('Patrick2', 'jpatrickjason@gmail.com', 'patpassword')
        pat2 = User.objects.get(username='Patrick2')
        User.objects.create_user('Patrick1', 'jpatrickjason@gmail.com', 'patpassword')
        pat = User.objects.get(username='Patrick1')
        Teams.objects.create(name="team12", created_by=pat,)
        team = Teams.objects.get(name="team12")
        form = TeamsForm(data={
        }
        )
        print(form.errors)
        self.assertFalse(form.is_valid())
