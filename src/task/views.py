from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView
from .models import Task

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
