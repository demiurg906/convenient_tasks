import json

from channels.message import Message
from django.template.loader import render_to_string

from tagging.models import Tag

from problems.models import Task, Grade

TASKS_LIST = 'tasks_list'
GET_TASK = 'get_task'


def generate_list_of_tasks(request):
    query_set = Task.objects\
        .filter(section__name=request['section'])\
        .filter(subsection__name=request['subsection'])\
        .filter(grades__in=Grade.objects.range(request['min_grade'], request['max_grade']))\
        .distinct()
    max_pk = request.get('max_pk', 0)
    if max_pk > 0:
        query_set = query_set.filter(pk__gt=max_pk)
    tasks_iter = query_set.iterator()
    n = min(query_set.count(), request['n'])
    tasks = [next(tasks_iter) for i in range(n)]
    if len(tasks) > 0:
        max_pk = tasks[-1].pk
    else:
        max_pk = 0
    return {
        'message_type': TASKS_LIST,
        'tasks': [render_to_string('problems/elements/task_button.html', {
            'task': task,
            'tags': Tag.objects.get_for_object(task)
        }) for task in tasks],
        'max_pk': max_pk,
        'action': request['action']
    }


def generate_task_template(request):
    pk = int(request['pk'])
    if pk > 0:
        task = Task.objects.get(pk=request['pk'])
        task_html = render_to_string('problems/elements/task_detail.html', {'task': task})
    else:
        task_html = render_to_string('problems/elements/no_task_placeholder.html')
    return {
        'message_type': GET_TASK,
        'task': task_html
    }


def send_reply(message: Message, data):
    message.reply_channel.send({'text': json.dumps(data)})


def ws_message(message: Message):
    request = json.loads(message.content['text'])
    if request['message_type'] == TASKS_LIST:
        response = generate_list_of_tasks(request)
    elif request['message_type'] == GET_TASK:
        response = generate_task_template(request)
    else:
        raise ValueError('неизвестный тип запроса')
    send_reply(message, response)
    print('received')

