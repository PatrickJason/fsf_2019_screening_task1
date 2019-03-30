from django.utils import timezone
from django.test import TestCase
from tasks.models import Tasks,Comments
from teams.models import Teams
from django.contrib.auth.models import User


class TasksTestCase(TestCase):


    def setUp(self):
        User.objects.create_user('Patrick2', 'jpatrickjason@gmail.com', 'patpassword')
        pat2 = User.objects.get(username='Patrick2')
        User.objects.create_user('Patrick1', 'jpatrickjason@gmail.com', 'patpassword')
        pat = User.objects.get(username='Patrick1')

    def test_team_creation(self):
        pat = User.objects.get(username='Patrick1')
        pat2 = User.objects.get(username='Patrick2')
        team = Teams.objects.create(name="teamA",
            description="we are testing",
            created_by=pat,
        )
        self.assertEquals(team.created_by,pat)


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
        
