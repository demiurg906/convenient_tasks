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
    return render(request, 'problems/tasks_search.html', {
        # TODO: fix
        'task': Task.objects.get(pk=1),
        'sections': Section.objects.all(),
        'subsections': Subsection.objects.all()
    })

# render(1, 'problems/task_button.html', {'task': Task.objects.get(pk=1)})
