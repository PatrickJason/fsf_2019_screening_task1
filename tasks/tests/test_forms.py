from django.test import SimpleTestCase
from django.test import TestCase,Client
from django.urls import reverse
from tasks.models import Tasks,Comments
from teams.models import Teams
from django.contrib.auth.models import User
from tasks.forms import TasksForm,AddAssigneeForm,CommentsForm
from tasks.views import CreateTasksView
"""
Testing the task forms in tasks app:
1.  Test form validity with data
2.  Test form validity without data
"""

class TestForms(TestCase):


    def test_init(self):
        TasksForm(user= User.objects.create_user('Patrick', 'jpatrickjason@gmail.com', 'patpassword'))

    # Test form validity with data
    def test_task_form_valid_data(self):
        User.objects.create_user('Patrick1', 'jpatrickjason@gmail.com', 'patpassword')
        pat = User.objects.get(username='Patrick1')
        Teams.objects.create(name="team12", created_by=pat,)
        team = Teams.objects.get(name="team12")
        form = TasksForm(data={
            'title':"New task",
            'description':"i am testing",
            'status':"active",
            'assigned_to_team':team.id

        },
            user=pat
        )
        print(form.errors)
        self.assertTrue(form.is_valid())

    # Test form validity without data
    def test_task_form_check_valid_no_data(self):
        User.objects.create_user('Patrick1', 'jpatrickjason@gmail.com', 'patpassword')
        pat = User.objects.get(username='Patrick1')
        Teams.objects.create(name="team12", created_by=pat,)
        team = Teams.objects.get(name="team12")
        form = TasksForm(data={

        },user=pat
        )
        print(form.errors)
        self.assertFalse(form.is_valid())
"""
Testing the comments forms in tasks app:
1.  Test form validity with data
2.  Test form validity without data
"""

    # Test form validity with data
    def test_comment_form_valid_data(self):
        User.objects.create_user('Patrick1', 'jpatrickjason@gmail.com', 'patpassword')
        pat = User.objects.get(username='Patrick1')
        Teams.objects.create(name="team12", created_by=pat,)
        team = Teams.objects.get(name="team12")
        task = Tasks.objects.create(task_creator=pat,title="my new task",description="mine ",status="active",assigned_to_team = team)
        form = CommentsForm(data={
            'text':"i am testing",
        }
        )
        print(form.errors)
        self.assertTrue(form.is_valid())

    #   Test form validity without data
    def test_comment_form_valid_data_no_data(self):
        User.objects.create_user('Patrick1', 'jpatrickjason@gmail.com', 'patpassword')
        pat = User.objects.get(username='Patrick1')
        Teams.objects.create(name="team12", created_by=pat,)
        team = Teams.objects.get(name="team12")
        task = Tasks.objects.create(task_creator=pat,title="my new task",description="mine ",status="active",assigned_to_team = team)
        form = CommentsForm(data={
        }
        )
        print(form.errors)
        self.assertFalse(form.is_valid())
