import json

from channels.message import Message
from django.template.loader import render_to_string

from tagging.models import Tag

from problems.models import Task

TASKS_LIST = 'tasks_list'
GET_TASK = 'get_task'


def generate_list_of_tasks(n, max_pk=0):
    query_set = Task.objects
    if max_pk > 0:
        query_set = query_set.filter(pk__gt=max_pk)
    tasks_iter = query_set.iterator()
    tasks = [next(tasks_iter) for i in range(n)]
    return {
        'message_type': TASKS_LIST,
        'tasks': [render_to_string('problems/task_button.html', {
            'task': task,
            'tags': Tag.objects.get_for_object(task)
        }) for task in tasks],
        'max_pk': tasks[-1].pk
    }


def generate_task_template(pk):
    task = Task.objects.get(pk=pk)
    return {
        'message_type': GET_TASK,
        'task': render_to_string('problems/task_detail.html', {'task': task})
    }


def send_reply(message: Message, data):
    message.reply_channel.send({'text': json.dumps(data)})


def ws_message(message: Message):
    request = json.loads(message.content['text'])
    if request['message_type'] == TASKS_LIST:
        response = generate_list_of_tasks(request['n'], request['max_pk'])
    elif request['message_type'] == GET_TASK:
        response = generate_task_template(request['pk'])
    else:
        raise ValueError('неизвестный тип запроса')
    send_reply(message, response)
    print('received')

