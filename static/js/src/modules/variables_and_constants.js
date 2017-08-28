/**
 * Этот модуль содержит общие константы,
 * а также логику сокета, по которому идет соединие с сервером
 */

/**
 * константы, дающие другим модулям понять, логиу какой страницы использовать
 */
export let POOL_PAGE = false;
export let SEARCH_PAGE = false;

/**
 * инициализирует страницу как страницу с наборами
 */
export function init_pool_page() {
    POOL_PAGE = true;
}

/**
 * инициализирует страницу как страницу поиска
 */
export function init_search_page() {
    SEARCH_PAGE = true;
}

/**
 * Возможные команды серверу
 */
export const TASKS_LIST = 'tasks_list';
export const GET_TASK = 'get_task';
export const  ADD_TO_POOL = 'add_to_pool';
export const NEW_POOL = 'new_pool';

// сам сокет
export let socket;

/**
 * Эта функция инициализирует сокет
 * @param address: адрес соединения
 * @param onopen: функция, вызываемая при открытии сокета,
 *                принимает булев параметр first_time, который
 *                позволяет определить логику, которая должна
 *                выполниться только при открытии страницы
 * @param receive_message: функция, вызываемая при получении
 *                сообщения от сервера
 * @param first_time: служебный булев параметр (см. onopen)
 */
export function connect(address, onopen, receive_message, first_time=true) {
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

/**
 * Дефолтный обработчик ответов от сервера, который исользуется
 * для неидентифицированных ответов
 * @param data
 */
export function default_handler(data){
    console.error('Incorrect message type: ' + data.message_type);
}

/**
 * Функция, которая отсылает сообщение серверу
 * @param data: само сообщение
 */
export function send(data) {
    socket.send(JSON.stringify(data));
}