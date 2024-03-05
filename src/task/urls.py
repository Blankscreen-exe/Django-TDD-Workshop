from django.urls import path
from .views import *

urlpatterns = [
    path("", index.as_view(), name='task-home'),
    path("<int:task_id>/", detail.as_view(), name='task-details'),
    path("add/", addTask.as_view(), name='task-add'),
    path("update/<int:pk>/", updateTask.as_view(), name='task-update'),
    path("delete/<int:pk>/", deleteTask.as_view(), name='task-delete'),
]