//TODO: добавить проверку версии браузера

import {initialize_slider, set_listeners_for_sections_dropdown} from "../modules/left_search_panel";
import {get_new_list, receive_get_task_message, receive_task_list_message} from "../modules/tasks_list_panel"

export const TASKS_LIST = 'tasks_list';
export const GET_TASK = 'get_task';


$(document).ready(function(){
    let socket;
    function connect() {
        socket = new WebSocket('ws://' + window.location.host + '/problems/tasks/');
        // Type of information received by websocket
        // socket.binaryType = 'arraybuffer';

        socket.onopen = function (event) {
            set_listeners_for_sections_dropdown(socket, 'sections');
            set_listeners_for_sections_dropdown(socket, 'subsections');
            get_new_list(socket);
        };

        socket.onmessage = (e) => receive_message(e.data);

        socket.onclose = () => {
            setTimeout(() => {
                connect()
            }, 5000)
        };
    }

    connect();
    initialize_slider(socket);

    function receive_message(message) {
        let data = JSON.parse(message);
        if (data.message_type === TASKS_LIST) {
            receive_task_list_message(socket, data)
        } else if (data.message_type === GET_TASK) {
            receive_get_task_message(data)
        }
    }
});

