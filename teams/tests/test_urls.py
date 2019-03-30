from django.test import SimpleTestCase
from django.urls import reverse,resolve
from teams.views import (CreateTeams,
                         SingleTeams,
                         TeamsDeleteView)

class TestUrls(SimpleTestCase):
    #Test for DetailView Url
    def test_CreateTeams_url_is_resolved(self):
        url = reverse('teams:create', args =[])
        print(resolve(url))
        self.assertEquals(resolve(url).func.view_class,CreateTeams)
    #Test for CreateView Url
    def test_CreateTasksView_url_is_resolved(self):
        url = reverse('teams:single', args =[],kwargs ={'pk':1})
        print(resolve(url))
        self.assertEquals(resolve(url).func.view_class,SingleTeams)
    def test_TasksDeleteView_url_is_resolved(self):
        url = reverse('teams:teams_remove',args=None, kwargs ={'pk':1})
        print(resolve(url))
        self.assertEquals(resolve(url).func.view_class,TeamsDeleteView)
