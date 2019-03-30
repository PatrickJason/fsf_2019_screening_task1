from django.test import TestCase,Client
from django.urls import reverse
from tasks.models import Tasks,Comments
from teams.models import Teams
from django.contrib.auth.models import User



class TestViews(TestCase):
    # Setting up the initial data to be tested
    def setUp(self):
        self.client = Client()
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
    # A test to add new task by POST method and asssert the response
    def test_CreateTasksView_list_post_add_new_task(self):
        pat = User.objects.get(username='Patrick')
        team = Teams.objects.get(name="team12")
        url = reverse('tasks:tasks_new')
        response = self.client.post(url,{
            'task_creator':pat,
            'title':"testing1",
            'description':'well well',
            'status':'testing bois',
            'assigned_to_team':team,
        })

        t2= Tasks.objects.get(id=1)
        self.assertEquals(t2.task_creator,pat)
        self.assertEquals(response.status_code,302)
        # self.assertEquals(self.project)


    def test_TasksDetailView(self):
        response = self.client.get(reverse('tasks:tasks_detail',kwargs={'pk':1}))
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response,'tasks/tasks_detail.html')

    def test_TasksDeleteView(self):
        response = self.client.get(reverse('tasks:tasks_remove',kwargs={'pk':1}))
        self.assertEquals(response.status_code,302)
