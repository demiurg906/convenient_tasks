from django.views.generic import DetailView

from problems.models import Task


class TaskDetailView(DetailView):
    model = Task
