import {GET_TASK, TASKS_LIST} from "../main_modules/task_search_main";

const NEW_LIST = 'new_list';
const UPDATE_LIST = 'update_list';

const N = 10;

import {section_button, subsection_button} from "./left_search_panel"

function enable_more_tasks_button() {
    $('#give_me_more').prop('disabled', false);
}

function send_request_for_search_list_of_tasks(socket, action) {
    let grades = $('#grade_slider').data().uiSlider.options.values;
    send(socket, {
        message_type: TASKS_LIST,
        n: N,
        max_pk: $('#tasks_list').attr('max_pk'),
        section: section_button.text(),
        subsection: subsection_button.text(),
        min_grade: grades[0],
        max_grade: grades[1],
        action: action
    });
}

function send(socket, data) {
    socket.send(JSON.stringify(data));
}

function update_listeners(socket) {
    $('.task_button').click(function (event) {
        get_task_description(socket, this.getAttribute('pk'));
    });
}

function get_task_description(socket, pk) {
    send(socket, {
        message_type: GET_TASK,
        pk: pk
    })
}

function disable_more_tasks_button() {
    $('#give_me_more').prop('disabled', true);
}

export function receive_task_list_message(socket, message) {
    let tasks_list = $('#tasks_list');
    for (let task of message.tasks) {
        tasks_list.append(task);
    }
    tasks_list.attr('max_pk', message.max_pk);
    if (message.tasks.length < N) {
        disable_more_tasks_button()
    }
    update_listeners(socket);
    if (message.action === NEW_LIST) {
        let button = $('#tasks_list button:first-child');
        if (button.length > 0) {
            button.click()
        } else {
            get_task_description(socket, -1);
            disable_more_tasks_button()
        }
    }
}

export function receive_get_task_message(message) {
    $('#task_detail').replaceWith(message.task);
}

export function get_new_list(socket) {
    let tasks_list = $("#tasks_list");
    tasks_list.attr('max_pk', 0);
    // tasks_list.max_pk = 0;
    tasks_list.empty();
    enable_more_tasks_button();
    send_request_for_search_list_of_tasks(socket, NEW_LIST);
}

export function initialize_tasks_list(socket) {
    $('#give_me_more').click(function (event) {
        send_request_for_search_list_of_tasks(socket, UPDATE_LIST);
    });
}