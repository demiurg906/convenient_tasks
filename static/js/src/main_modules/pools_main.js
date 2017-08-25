import {
    ADD_TO_POOL, connect, default_handler, GET_TASK, NEW_POOL,
    TASKS_LIST
} from "../modules/variables_and_constants";
import {set_listeners_for_pool_buttons} from "../modules/pools_panel";
import {
    initialize_tasks_list,
    receive_add_to_pool_message, receive_get_task_message, receive_new_pool_message,
    receive_task_list_message
} from "../modules/tasks_list_panel";

$(document).ready(function () {
    connect('/problems/pools/', function (first_time) {
        set_listeners_for_pool_buttons();
        if (first_time) {
            $('#pool-favorite').click();
        }
    }, receive_message, true);

    initialize_tasks_list(false);

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