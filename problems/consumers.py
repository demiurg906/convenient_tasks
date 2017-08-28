import json
import logging

from functools import partial

from channels.auth import channel_session_user_from_http, channel_session_user
from channels.message import Message
from django.template.loader import render_to_string

from tagging.models import Tag

from problems.models import Task, Grade, User, TaskPool

logger = logging.getLogger(__name__)

TASKS_LIST = 'tasks_list'
GET_TASK = 'get_task'
ADD_TO_POOL = 'add_to_pool'
NEW_POOL = 'new_pool'


def generate_list_of_tasks(request, user: User, *args, search=False):
    if search:
        query_set = Task.objects \
            .filter(section__name=request['section']) \
            .filter(subsection__name=request['subsection']) \
            .filter(grades__in=Grade.objects.range(request['min_grade'], request['max_grade'])) \
            .distinct()
    else:
        query_set = user.taskpool_set \
            .get(pk=request['pool_pk'])\
            .tasks.all()
    max_pk = int(request.get('max_pk', 0))
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
        'tasks': [render_to_string('problems/elements/tasks_list_element.html', {
            'task': task,
            'tags': Tag.objects.get_for_object(task)
        }) for task in tasks],
        'max_pk': max_pk,
        'action': request['action']
    }


def generate_task_template(request, user, template='problems/elements/task_detail.html'):
    pk = int(request['pk'])
    if pk > 0:
        task = Task.objects.get(pk=request['pk'])
        task_html = render_to_string(template, {'task': task, 'user': user})
    else:
        task_html = render_to_string('problems/elements/no_task_placeholder.html')
    return {
        'message_type': GET_TASK,
        'task': task_html
    }


def add_task_to_pool(request, user: User):
    pool_html = ''
    pool_id = ''
    try:
        pool_pk = request['pool_pk']
        task_pk = request['task_pk']
        if not user.taskpool_set.filter(pk=pool_pk).exists():
            raise Exception('Пользователь меняет не свой пул')
        pool = TaskPool.objects.get(pk=pool_pk)
        task = Task.objects.get(pk=task_pk)
        if pool.tasks.filter(pk=task.pk).exists():
            pool.tasks.remove(task)
        else:
            pool.tasks.add(task)
        pool_html = render_to_string('problems/elements/pool_list_element.html', {
            'user': user,
            'task': task,
            'pool': pool
        })
        pool_id = f'pool-{pool.pk}'
        status = 'OK'
    except Exception as e:
        logger.exception(e)
        status = 'Error'
    return {
        'message_type': ADD_TO_POOL,
        'status': status,
        'pool_html': pool_html,
        'pool_id': pool_id,
    }


def create_new_pool(request, user: User):
    pool = TaskPool.objects.create(name=request['pool_name'], user=user)
    task = Task.objects.get(pk=request['task_pk'])
    return {
        'message_type': NEW_POOL,
        'pool_html': render_to_string('problems/elements/pool_list_element.html', {
            'pool': pool,
            'task': task
        })
    }


def send_reply(message: Message, data):
    message.reply_channel.send({'text': json.dumps(data)})


@channel_session_user_from_http
def ws_connect(message):
    message.reply_channel.send({"accept": True})


@channel_session_user
def ws_search_message(message: Message):
    handlers = {
        TASKS_LIST: partial(generate_list_of_tasks, search=True),
        GET_TASK: partial(generate_task_template, template='problems/elements/task_detail_search.html'),
        ADD_TO_POOL: add_task_to_pool,
        NEW_POOL: create_new_pool
    }
    ws_message(message, handlers)


@channel_session_user
def ws_pools_message(message: Message):
    handlers = {
        TASKS_LIST: partial(generate_list_of_tasks, search=False),
        GET_TASK: partial(generate_task_template, template='problems/elements/task_detail_pools.html'),
        ADD_TO_POOL: add_task_to_pool,
        NEW_POOL: create_new_pool
    }
    ws_message(message, handlers)


def ws_message(message, handlers):
    request = json.loads(message.content['text'])
    message_type = request['message_type']
    if message_type in handlers:
        response = handlers[message_type](request, message.user)
        send_reply(message, response)
    else:
        logger.error(f'Неизвестный тип запроса')
