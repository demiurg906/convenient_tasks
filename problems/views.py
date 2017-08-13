from django.shortcuts import render

from problems.models import Task, Section, Subsection


def task_detail(request, pk):
    return render(request, 'problems/task_detail.html', {
        'task': Task.objects.get(pk=pk),
    })


def task_search(request):
    return render(request, 'problems/tasks_search.html', {
        # TODO: fix
        'task': Task.objects.get(pk=1),
        'sections': Section.objects.all(),
        'subsections': Subsection.objects.all()
    })

# render(1, 'problems/task_button.html', {'task': Task.objects.get(pk=1)})
