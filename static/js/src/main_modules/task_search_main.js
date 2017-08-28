import {initialize_left_panel} from "../modules/left_search_panel";
import {
    connect, default_handler, ADD_TO_POOL, GET_TASK, NEW_POOL, TASKS_LIST, init_search_page
} from "../modules/variables_and_constants";
import {
    get_new_list, initialize_tasks_list, receive_task_list_message} from "../modules/tasks_list_panel"
import {
    receive_add_to_pool_message, receive_get_task_message,
    receive_new_pool_message
} from "../modules/task_details_panel";

/**
 * Основной скрипт для страницы с наборами задач
 */

$(document).ready(function() {
    init_search_page();
    connect('/problems/tasks/', function (first_time) {
        if (first_time) {
            get_new_list();
        }
    }, receive_message);

    initialize_left_panel();
    initialize_tasks_list(true);

    let handlers = {};
    handlers[TASKS_LIST] = receive_task_list_message;
    handlers[GET_TASK] = receive_get_task_message;
    handlers[ADD_TO_POOL] = receive_add_to_pool_message;
    handlers[NEW_POOL] = receive_new_pool_message;

    function receive_message(message) {
        let data = JSON.parse(message);
        let handler = handlers[data.message_type] || default_handler;
        handler(data);
    }
});