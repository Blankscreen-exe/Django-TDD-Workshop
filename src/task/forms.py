from django import forms

from .models import Task

class NewTaskForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = ('task', 'description', 'priority')

class UpdateTaskForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = ('task', 'description', 'priority')