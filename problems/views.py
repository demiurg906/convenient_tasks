from django.shortcuts import render
from django.template.loader import render_to_string
from django.views.generic import DetailView
from django import views

from problems.models import Task, Section, Subsection


def task_search(request, pk):
    context = {
        'task': Task.objects.get(pk=pk),
        'sections': Section.objects.all(),
        'subsections': Subsection.objects.all()
    }
    html = render_to_string('problems/task_detail.html', context)
    return render(request, 'problems/task_detail.html', context)


class TaskDetailView(DetailView):
    model = Task
