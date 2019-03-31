from django.utils import timezone
from django.test import TestCase
from tasks.models import Tasks,Comments
from teams.models import Teams
from django.contrib.auth.models import User
"""
Test the models of the teams app
1.Create a team
2.Delete a team
"""

class TasksTestCase(TestCase):


    def setUp(self):
        User.objects.create_user('Patrick2', 'jpatrickjason@gmail.com', 'patpassword')
        pat2 = User.objects.get(username='Patrick2')
        User.objects.create_user('Patrick1', 'jpatrickjason@gmail.com', 'patpassword')
        pat = User.objects.get(username='Patrick1')

    # Create a team and verify the data created
    def test_team_creation(self):
        pat = User.objects.get(username='Patrick1')
        pat2 = User.objects.get(username='Patrick2')
        team = Teams.objects.create(name="teamA",
            description="we are testing",
            created_by=pat,
        )
        self.assertEquals(team.created_by,pat)

    # Delete a team and verify the deletion
    def test_team_deletion(self):
        pat = User.objects.get(username='Patrick1')
        pat2 = User.objects.get(username='Patrick2')
        team = Teams.objects.create(name="teamA1",
            description="we are testing",
            created_by=pat,
        )
        team = Teams.objects.get(name="teamA1")
        team.delete()
        team = Teams.objects.filter(name="teamA1").first()
        self.assertEquals(team,None)
