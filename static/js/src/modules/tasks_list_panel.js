import {socket, ADD_TO_POOL, GET_TASK, NEW_POOL, TASKS_LIST} from '../modules/variables_and_constants';

const NEW_LIST = 'new_list';
const UPDATE_LIST = 'update_list';

const N = 10;

// Переменная, определяющая, по какой логике отсылать запросы на список задач,
// по логике поиска или списка наборов
let send_request;

import {section_button, subsection_button} from './left_search_panel'

function enable_more_tasks_button() {
    $('#give_me_more').prop('disabled', false);
}

function send_request_for_search_list_of_tasks(action) {
    let grades = $('#grade-slider').data().uiSlider.options.values;
    send({
        message_type: TASKS_LIST,
        n: N,
        max_pk: $('#tasks-list').attr('max_pk'),
        section: section_button.text(),
        subsection: subsection_button.text(),
        min_grade: grades[0],
        max_grade: grades[1],
        action: action
    });
}

function send_request_for_tasks_of_pool(action) {
    send({
        message_type: TASKS_LIST,
        n: N,
        max_pk: $('#tasks-list').attr('max_pk'),
        pool_pk: $('#pools-list').attr('chosen_pool_pk'),
        action: action
    })
}

function send(data) {
    socket.send(JSON.stringify(data));
}

function update_listeners() {
    $('.task-button').click(function () {
        get_task_description(this.getAttribute('pk'));
    });
}

function get_task_description(pk) {
    send({
        message_type: GET_TASK,
        pk: pk
    })
}

function disable_more_tasks_button() {
    $('#give-me-more').prop('disabled', true);
}

export function receive_task_list_message(message) {
    let tasks_list = $('#tasks-list');
    for (let task of message.tasks) {
        tasks_list.append(task);
    }
    tasks_list.attr('max_pk', message.max_pk);
    if (message.tasks.length < N) {
        disable_more_tasks_button()
    }
    update_listeners();
    if (message.action === NEW_LIST) {
        let button = $('#tasks-list button:first-child');
        if (button.length > 0) {
            button.click()
        } else {
            get_task_description(-1);
            disable_more_tasks_button()
        }
    }
}

export function receive_get_task_message(message) {
    $('#task-detail').replaceWith(message.task);
    update_pool_buttons_listeners();
    $('#new-pool-button').keyup(function(e){
        if(e.keyCode === 13) {
            let pool_name = $(this).val();
            if (pool_name.length !== 0) {
                send({
                    message_type: NEW_POOL,
                    pool_name: pool_name,
                    task_pk: $('#task-detail').attr('task_pk')
                })
            }
            $(this).val('');
        }
    });
}

export function receive_add_to_pool_message(message) {
    if (message.status === 'OK') {
        let pool_id = '#' + message.pool_id;
        $(pool_id).replaceWith(message.pool_html);
        update_pool_buttons_listeners()
    }
}

export function receive_new_pool_message(message) {
    $('#pool-divider').before(message.pool_html);
    update_pool_buttons_listeners();
}

function update_pool_buttons_listeners() {
    $('.pool-button').each(function () {
        $(this).click(function () {
            send({
                message_type: ADD_TO_POOL,
                pool_pk: $(this).attr('pool_pk'),
                task_pk: $('#task-detail').attr('task_pk')
            })
        });
    });
}

export function get_new_list() {
    let tasks_list = $('#tasks-list');
    tasks_list.attr('max_pk', 0);
    tasks_list.empty();
    enable_more_tasks_button();
    send_request(NEW_LIST);
}

export function initialize_tasks_list(search) {
    if (search) {
        send_request = send_request_for_search_list_of_tasks
    } else {
        send_request = send_request_for_tasks_of_pool
    }
    $('#give-me-more').click(function (event) {
        send_request(UPDATE_LIST);
    });
}