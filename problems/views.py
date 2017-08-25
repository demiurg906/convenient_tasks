from django.contrib.auth.views import redirect_to_login
from django.shortcuts import render

from problems.models import Task, Section, Subsection, User


def task_detail(request, pk):
    # TODO: убрать дефолтного юзера
    user = User.objects.get(username='admin')
    return render(request, 'problems/elements/task_detail.html', {
        'task': Task.objects.get(pk=pk),
        'user': user
        # 'user': request.user
    })


def task_search(request):
    if not request.user.is_authenticated():
        return redirect_to_login('/tasks')
    return render(request, 'problems/tasks_search.html', {
        'sections': Section.objects.all(),
        'subsections': Subsection.objects.all()
    })


def pools(request):
    if not request.user.is_authenticated():
        return redirect_to_login('/pools')
    user = request.user
    return render(request, 'problems/pools.html', {
        'user': user
    })
