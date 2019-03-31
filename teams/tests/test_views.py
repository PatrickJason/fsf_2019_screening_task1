from django.test import TestCase,Client
from django.urls import reverse
from tasks.models import Tasks,Comments
from teams.models import Teams
from teams.views import (CreateTeams,
                         SingleTeams,
                         TeamsDeleteView)
from django.contrib.auth.models import User

"""
Tests the views in teams app
1.CreateTeams view
2.SingleTeams view(DetailView)
3.DeleteTeams view
"""

class TestViews(TestCase):
    # Setting up the initial data to be tested
    def setUp(self):
        User.objects.create_user('Patrick2', 'jpatrickjason@gmail.com', 'patpassword')
        pat2 = User.objects.get(username='Patrick2')
        self.client = Client()
        User.objects.create_user('Patrick', 'jpatrickjason@gmail.com', 'patpassword')
        pat = User.objects.get(username='Patrick')
        Teams.objects.create(name="team12", created_by=pat,)
        team = Teams.objects.get(name="team12")

    # A test to add new task by POST method and asssert the response
    def test_CreateTeams_list_post_add_new_task(self):
        pat2 = User.objects.get(username='Patrick2')
        pat = User.objects.get(username='Patrick')
        team = Teams.objects.get(name="team12")
        url = reverse('tasks:tasks_new')
        response = self.client.post(url,{
            'created_by':pat,
            'name':"testingt1",
            'description':'well well',
            'members':[pat.id,pat2.id]
        })

        t2= Teams.objects.get(id=1)
        self.assertEquals(t2.created_by,pat)
        self.assertEquals(response.status_code,302)

    # Test for the SingleTeams detail view and verify the response
    def test_SingeTeamsView(self):
        response = self.client.get(reverse('teams:single',kwargs={'pk':1}))
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response,'teams/teams_detail.html')

    # Test for the TasksDeleteView and verify the response
    def test_TasksDeleteView(self):
        response = self.client.get(reverse('teams:teams_remove',kwargs={'pk':1}))
        self.assertEquals(response.status_code,302)
