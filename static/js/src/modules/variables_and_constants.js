export const TASKS_LIST = 'tasks_list';
export const GET_TASK = 'get_task';
export const  ADD_TO_POOL = 'add_to_pool';
export const NEW_POOL = 'new_pool';

export let socket;

export function connect(address, onopen, receive_message, first_time) {
    socket = new WebSocket('ws://' + window.location.host + address);
    // Type of information received by websocket
    // socket.binaryType = 'arraybuffer';

    socket.onopen = () => onopen(first_time);

    socket.onmessage = (e) => receive_message(e.data);

    socket.onclose = () => {
        setTimeout(() => {
            connect(address, onopen, receive_message, false)
        }, 5000)
    };
}