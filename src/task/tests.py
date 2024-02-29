from django.test import TestCase
from task.models import Task

class TaskModelTest(TestCase):

    def test_task_model_exists(self):
        tasks = Task.objects.count()
        self.assertEqual(tasks, 0)

    def test_model_has_string_representation(self):
        priority_choices = Task().get_priority_choices()
        task = Task.objects.create(task="some task", priority=priority_choices[1][0])

        self.assertEqual(str(task), f"({task.priority}) {task.task}", "Task __str__ representation does not match the proper format")

class IndexPageTest(TestCase):

    def setUp(self):
        self.task = Task.objects.create(task="First Task", priority=1)

    def test_index_page_returns_correct_response(self):
        response = self.client.get("/tasks/")

        self.assertTemplateUsed(response, 'task/index.html')
        self.assertEqual(response.status_code, 200)

    def test_index_page_has_tasks(self):
        response = self.client.get('/tasks/')

        self.assertContains(response, self.task.task)

class DetailPageTest(TestCase):

    def setUp(self):
        self.task = Task.objects.create(
            task="Some Task",
            description="Some Description",
            priority=2
        )
        self.task2 = Task.objects.create(
            task="Some Task 2",
            description="Some Description 2",
            priority=2
        )

    def test_detail_page_returns_correct_response(self):
        response = self.client.get('/tasks/1/')
        self.assertTemplateUsed(response, 'task/detail.html')
        self.assertEqual(response.status_code, 200)
    
    def test_detail_page_has_correct_content(self):
        response = self.client.get('/tasks/1/')
        self.assertContains(response, self.task.task)
        self.assertContains(response, self.task.description)
        self.assertContains(response, self.task.priority)
        self.assertNotContains(response, self.task2.task)

    def test_detail_page_returns_404_response(self):
        response = self.client.get('/tasks/12/')
        self.assertEqual(response.status_code, 404)

