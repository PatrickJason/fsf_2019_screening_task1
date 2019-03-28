from django.test import SimpleTestCase
from django.urls import reverse,resolve
from tasks.views import (CreateTasksView,
                        TasksListView,
                        TasksDetailView,
                        TasksUpdateView,
                        TasksDeleteView)



class TestUrls(SimpleTestCase):

    def test_list_url_is_resolved(self):
        url = reverse('tasks:tasks_detail', args =[])
        print(resolve(url))
        self.assertEquals(resolve(url).func.view_class,TasksDetailView)
