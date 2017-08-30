import pdfkit

from django.contrib.auth.views import redirect_to_login
from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string

from problems.models import Task, Section, Subsection, User, TaskPool


def task_detail(request, pk):
    if not request.user.is_authenticated():
        return redirect_to_login(request.path)
    return render(request, 'problems/pages/task.html', {
        'task': Task.objects.get(pk=pk),
        'user': request.user
    })


def task_search(request):
    if not request.user.is_authenticated():
        return redirect_to_login('/tasks')
    return render(request, 'problems/pages/tasks_search.html', {
        'sections': Section.objects.all(),
        'subsections': Subsection.objects.all(),
        'user': request.user
    })


def pools(request):
    if not request.user.is_authenticated():
        return redirect_to_login('/pools')
    return render(request, 'problems/pages/pools.html', {
        'user': request.user
    })


def pool_pdf(request):
    pool_pk = request.GET['pk']
    pool = TaskPool.objects.get(pk=pool_pk)
    pdf = generate_pdf('problems/pdf/pool.html', {'pool': pool})
    # render_to_string('problems/pdf/pool.html', {'pool': pool})
    return HttpResponse(pdf, content_type='application/pdf')


def generate_pdf(template_name, context):
    html = render_to_string(template_name, context)
    pdf = pdfkit.from_string(html, False)
    return pdf
