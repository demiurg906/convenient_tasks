import {send, GET_TASK, TASKS_LIST} from '../modules/variables_and_constants';
import {get_grade_slider_values, section_button, subsection_button} from './left_search_panel'

/**
 * Модуль с функциями панели со списком задач
 */

/**
 * Команды серверу, определяющие, нужен новый список, или же продолжение старого
 */
const NEW_LIST = 'new_list';
const UPDATE_LIST = 'update_list';

/**
 * Максимальное количество задач в списке, который запрашивается у сервера
 */
const N = 10;

/**
 * Функция, которая отсылает запрос серверу для новых задач
 * определяется при инициализации, в зависимости от того,
 * какая логика используется -- задачи ищутся по запросу,
 * либо же требуются задачи из определенного набора
 */
let send_request;

/**
 * Эта функция включает кнопку "загрузить больше задач"
 */
function enable_more_tasks_button() {
    $('#give_me_more').prop('disabled', false);
}

/**
 * Эта функция выключает кнопку "загрузить больше задач"
 */
function disable_more_tasks_button() {
    $('#give-me-more').prop('disabled', true);
}

/**
 * Эта функция отсылает серверу запрос на задачи, которые
 * ищутся в поиске
 * @param action: NEW_LIST или UPDATE_LIST
 */
function send_request_for_search_list_of_tasks(action) {
    let grades = get_grade_slider_values();
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

/**
 * Эта функция отсылает серверу запрос на задачи из
 * определннного набора задач
 * @param action: NEW_LIST или UPDATE_LIST
 */
function send_request_for_tasks_of_pool(action) {
    send({
        message_type: TASKS_LIST,
        n: N,
        max_pk: $('#tasks-list').attr('max_pk'),
        pool_pk: $('#pools-list').attr('chosen_pool_pk'),
        action: action
    })
}

/**
 * Эта функция обновляет обработчики нажатия на кнопки
 * задач в списке
 */
function update_listeners() {
    $('.task-button').click(function () {
        $('.task-button.active').removeClass('active');
        $(this).addClass('active');
        get_task_description(this.getAttribute('pk'));
    });
}

/**
 * Эта функция отправляет запрос серверу на получение
 * деталей задачи
 * @param pk: номер задачи
 */
function get_task_description(pk) {
    send({
        message_type: GET_TASK,
        pk: pk
    })
}

/**
 * Эта функция обрабатывает ответ сервера на запрос об обновлении
 * списка задач --- добавляет плашки задач в список
 */
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
    // если был получен новый список, то активиурет первую задачу
    if (message.action === NEW_LIST) {
        let button = $('#tasks-list').find('button:first-child');
        if (button.length > 0) {
            button.click()
        } else {
            // если список пуст, то запрашивает у сервера заглушку
            get_task_description(-1);
            disable_more_tasks_button()
        }
    }
}

/**
 * Эта функция запрашивает у сервера новый список задач
 */
export function get_new_list() {
    let tasks_list = $('#tasks-list');
    tasks_list.attr('max_pk', 0);
    tasks_list.empty();
    enable_more_tasks_button();
    send_request(NEW_LIST);
}

/**
 * Эта функция инициализирует панель списка задач
 * @param search:
 *      True --- используется логика поиска задач
 *      False --- используется логика наборов задач
 */
export function initialize_tasks_list(search) {
    if (search) {
        send_request = send_request_for_search_list_of_tasks
    } else {
        send_request = send_request_for_tasks_of_pool
    }
    $('#give-me-more').click(function () {
        send_request(UPDATE_LIST);
    });
}