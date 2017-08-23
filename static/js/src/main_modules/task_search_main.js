//TODO: добавить проверку версии браузера

import {initialize_slider, set_listeners_for_sections_dropdown} from "../modules/left_search_panel";
import {
    get_new_list, initialize_tasks_list, receive_add_to_pool_message, receive_get_task_message,
    receive_new_pool_message,
    receive_task_list_message
} from "../modules/tasks_list_panel"
import {socket, connect, ADD_TO_POOL, GET_TASK, NEW_POOL, TASKS_LIST} from "../modules/variables_and_constants";

$(document).ready(function() {
    connect('/problems/tasks/', function (first_time) {
        set_listeners_for_sections_dropdown(socket, 'sections');
        set_listeners_for_sections_dropdown(socket, 'subsections');
        if (first_time) {
            get_new_list(socket);
        }
    }, receive_message, true);
    initialize_slider();
    initialize_tasks_list();

    function receive_message(message) {
        let data = JSON.parse(message);
        if (data.message_type === TASKS_LIST) {
            receive_task_list_message(data)
        } else if (data.message_type === GET_TASK) {
            receive_get_task_message(data)
        } else if (data.message_type === ADD_TO_POOL) {
            receive_add_to_pool_message(data);
        } else if (data.message_type === NEW_POOL) {
            receive_new_pool_message(data)
        }
        else {
            console.log.error('Incorrect message type: ' + message.message_type)
        }
    }
});

