from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView, FormView, CreateView, UpdateView, DeleteView
from .models import Task
from task.forms import NewTaskForm, UpdateTaskForm

class index(TemplateView):
    template_name = "task/index.html"

    def get_context_data(self, kwargs):
        return {**kwargs}

    def get(self, request, *args, **kwargs):

        context = {
            "name": "Francois",
            "designation": "butler"
        }

        context['tasks'] = Task.objects.all()

        context = self.get_context_data(context)

        return self.render_to_response(context)


class detail(TemplateView):
    template_name = 'task/detail.html'

    def get_context_data(self, id):
        obj = get_object_or_404(Task, id=id)
        return obj

    def get(self, request, *args, **kwargs):

        context = {
            "task": self.get_context_data(kwargs['task_id'])
        }

        return self.render_to_response(context)


class addTask(CreateView):
    template_name = 'task/addTask.html'
    form_class = NewTaskForm
    success_url = reverse_lazy("task-home")
    
    def form_valid(self, form):
        return super().form_valid(form)


class updateTask(UpdateView):
    model = Task
    template_name = "task/updateTask.html"
    form_class = UpdateTaskForm
    success_url = reverse_lazy('task-home')

class deleteTask(DeleteView):
    model = Task
    template_name = "task/deleteTask.html"
    success_url = reverse_lazy('task-home')
    

