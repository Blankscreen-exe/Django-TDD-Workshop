from django.urls import path
from .views import *

urlpatterns = [
    path("", index.as_view(), name='task-home'),
    path("<int:task_id>/", detail.as_view(), name='task-details')
    path("add/", addTask.as_view(), name='task-add')
]