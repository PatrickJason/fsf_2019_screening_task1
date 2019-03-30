from django.test import SimpleTestCase
from django.test import TestCase,Client
from django.urls import reverse
from tasks.models import Tasks,Comments
from teams.models import Teams
from django.contrib.auth.models import User
from tasks.forms import TasksForm,AddAssigneeForm



class TestForms(TestCase):
    def test_get_form_kwargs(self):
        kwargs = super(CreateTasksView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs
    def test_init(self):
        TasksForm(user= User.objects.create_user('Patrick', 'jpatrickjason@gmail.com', 'patpassword'))
    def test_task_form_valid_data(self):
        User.objects.create_user('Patrick1', 'jpatrickjason@gmail.com', 'patpassword')
        pat = User.objects.get(username='Patrick1')
        Teams.objects.create(name="team12", created_by=pat,)
        team = Teams.objects.get(name="team12")
        form = TasksForm(data={

            'title':"New task",
            'description':"i am testing",
            'status':"active",
            'assigned_to_team':team

        },user=pat
        )
        self.assertTrue(form.is_valid())
