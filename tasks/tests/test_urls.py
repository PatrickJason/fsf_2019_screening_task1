from django.test import SimpleTestCase
from django.urls import reverse,resolve
from tasks.views import (CreateTasksView,
                        TasksListView,
                        TasksDetailView,
                        TasksUpdateView,
                        TasksDeleteView)



class TestUrls(SimpleTestCase):
    #Test for DetailView Url
    def test_detail_url_is_resolved(self):
        url = reverse('tasks:tasks_detail', args =[])
        print(resolve(url))
        self.assertEquals(resolve(url).func.view_class,TasksDetailView)
    #Test for CreateView Url
    def test_CreateTasksView_url_is_resolved(self):
        url = reverse('tasks:tasks_new', args =[])
        print(resolve(url))
        self.assertEquals(resolve(url).func.view_class,CreateTasksView)
    def test_TasksDeleteView_url_is_resolved(self):
        url = reverse('tasks:tasks_remove',args=None, kwargs ={'pk':1})
        print(resolve(url))
        self.assertEquals(resolve(url).func.view_class,TasksDeleteView)
