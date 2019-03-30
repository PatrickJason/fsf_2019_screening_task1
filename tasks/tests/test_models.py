from django.utils import timezone
from django.test import TestCase
from tasks.models import Tasks,Comments
from teams.models import Teams
from django.contrib.auth.models import User




class TasksTestCase(TestCase):
    def setUp(self):
        User.objects.create_user('Patrick', 'jpatrickjason@gmail.com', 'patpassword')
        pat = User.objects.get(username='Patrick')
        Teams.objects.create(name="team12", created_by=pat,)
        team = Teams.objects.get(name="team12")
        self.task1=Tasks.objects.create(
            task_creator = pat,
            title ='testteam',
            description='lol',
            status='testing',
            assigned_to_team=team,
        )
    def test_task_creation(self):
        # User.objects.create_user('Patrick', 'jpatrickjason@gmail.com', 'patpassword')
        pat = User.objects.get(username='Patrick')
        Teams.objects.create(name="team123", created_by=pat,)
        team = Teams.objects.get(name="team12")
        self.task1=Tasks.objects.create(
            task_creator = pat,
            title ='testteam',
            description='lol',
            status='testing',
            assigned_to_team=team,
        )
        self.assertEquals(self.task1.task_creator,pat)
        self.assertEquals(self.task1.assigned_to_team,team)

    def test_task_deletion(self):

        self.task1.delete()
        task = Tasks.objects.filter(title='testteam').first()
        self.assertEquals(task,None)
class CommentsTestCase(TestCase):
    def setUp(self):
        User.objects.create_user('Patrick', 'jpatrickjason@gmail.com', 'patpassword')
    def test_comment_creation(self):
        pat = User.objects.get(username='Patrick')
        Teams.objects.create(name="team12", created_by=pat,)
        team = Teams.objects.get(name="team12")
        self.task1=Tasks.objects.create(
            task_creator = pat,
            title ='testteam',
            description='lol',
            status='testing',
            assigned_to_team=team,
        )
        comment = Comments.objects.create(task=self.task1,author= pat,text="testing")
        self.assertEquals(comment.text,"testing")
    def test_comment_deletion(self):
        pat = User.objects.get(username='Patrick')
        Teams.objects.create(name="team12", created_by=pat,)
        team = Teams.objects.get(name="team12")
        self.task1=Tasks.objects.create(
            task_creator = pat,
            title ='testteam',
            description='lol',
            status='testing',
            assigned_to_team=team,
        )
        comment = Comments.objects.create(task=self.task1,author= pat,text="testing")
        comment = Comments.objects.get(text="testing")
        comment.delete()
        comment = Comments.objects.filter(author=pat).first()
        self.assertEquals(comment,None)
