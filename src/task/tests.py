from django.test import TestCase
from task.models import Task
from task.forms import NewTaskForm, UpdateTaskForm

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

class AddTaskFromTest(TestCase):

    def setUp(self):
        self.form = NewTaskForm

    def test_new_page_returns_correct_response(self):
        response = self.client.get(f'/tasks/add/')

        self.assertTemplateUsed(response, 'task/addTask.html')
        self.assertEqual(response.status_code, 200)

    def test_form_can_be_valid(self):
        self.assertTrue(issubclass(self.form, NewTaskForm))
        self.assertTrue('task' in self.form.Meta.fields)
        self.assertTrue('description' in self.form.Meta.fields)

        form = self.form({
            'task': 'New title',
            'description': 'New description',
            'priority': 2
        })

        self.assertTrue(form.is_valid())

    def test_add_task_form_rendering(self):
        response = self.client.get('/tasks/add/')

        self.assertContains(response, '<form')
        self.assertContains(response, 'csrfmiddlewaretoken')
        self.assertContains(response, '<label for')

        response = self.client.post('/tasks/add/', {
            'task': '',
            'description': 'new desc 11',
            'priority': 1
        })

        self.assertContains(response, '<ul class=\"errorlist\">')
        self.assertContains(response, 'This field is required')

        # test valid forms
        response = self.client.post('/tasks/add/', {
            'task': 'new task 11',
            'description': 'new desc 11',
            'priority': 1
        })

        self.assertRedirects(response, expected_url='/tasks/')
        self.assertEqual(Task.objects.count(), 1)

class UpdateTaskTest(TestCase):

    def setUp(self):
        self.task = Task.objects.create(
            task='task 1',
            description="desc 1",
            priority=2
        )
        self.form = UpdateTaskForm
    
    def test_update_page_returns_correct_response(self):
        response = self.client.get(f'/tasks/update/{self.task.id}/')

        self.assertTemplateUsed(response, 'task/updateTask.html')
        self.assertEqual(response.status_code, 200)

    def test_form_can_be_valid(self):
        self.assertTrue(issubclass(self.form, UpdateTaskForm))
        self.assertTrue('task' in self.form.Meta.fields)
        self.assertTrue('description' in self.form.Meta.fields)
        self.assertTrue('priority' in self.form.Meta.fields)

        form = self.form({
            'task': 'some title abc',
            'description': 'some description abc',
            'priority': 3
        }, instance=self.task)

        self.assertTrue(form.is_valid())

        form.save()

        self.assertEqual(self.task.task, 'some title abc')

    def test_form_can_be_invalid(self):
        form = self.form({
            'task': '',
            'description': 'some data',
            'priority': 1
        })

        self.assertFalse(form.is_valid())

    def test_add_task_form_rendering(self):
        response = self.client.get(f'/tasks/update/{self.task.id}/')

        self.assertContains(response, '<form')
        self.assertContains(response, 'csrfmiddlewaretoken')
        self.assertContains(response, '<label for')

        response = self.client.post(f'/tasks/update/{self.task.id}/', {
            'id': self.task.id,
            'task': '',
            'description': 'new desc 11',
            'priority': 1
        }, instance=self.task)

        self.assertContains(response, '<ul class=\"errorlist\">')
        self.assertContains(response, 'This field is required')

        # test valid forms
        response = self.client.post(f'/tasks/update/{self.task.id}/', {
            'task': 'new task 11',
            'description': 'new desc 11',
            'priority': 1
        })

        self.assertRedirects(response, expected_url='/tasks/')
        self.assertEqual(Task.objects.count(), 1)
        self.assertEqual(Task.objects.first().task, 'new task 11')

class DeleteTaskTest(TestCase):

    def setUp(self) -> None:
        self.task = Task.objects.create(
            task="task 1",
            description="description 1",
            priority=1
        )
    
    def tearDown(self) -> None:
        return super().tearDown()
    
    def test_delete_page_deletes_task(self):
        self.assertEqual(Task.objects.count(), 1)

        response = self.client.post(f'/tasks/delete/{self.task.id}/')
        self.assertRedirects(response, expected_url='/tasks/')
        self.assertEqual(Task.objects.count(), 0)