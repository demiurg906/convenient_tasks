from django.contrib.auth.views import redirect_to_login
from django.shortcuts import render

from problems.models import Task, Section, Subsection, User


def task_detail(request, pk):
    if not request.user.is_authenticated():
        return redirect_to_login(request.path)
    return render(request, 'problems/task.html', {
        'task': Task.objects.get(pk=pk),
        'user': request.user
    })


def task_search(request):
    if not request.user.is_authenticated():
        return redirect_to_login('/tasks')
    return render(request, 'problems/tasks_search.html', {
        'sections': Section.objects.all(),
        'subsections': Subsection.objects.all(),
        'user': request.user
    })


def pools(request):
    if not request.user.is_authenticated():
        return redirect_to_login('/pools')
    return render(request, 'problems/pools.html', {
        'user': request.user
    })
