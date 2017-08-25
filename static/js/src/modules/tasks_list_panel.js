import {send, ADD_TO_POOL, GET_TASK, NEW_POOL, TASKS_LIST} from '../modules/variables_and_constants';
import {section_button, subsection_button} from './left_search_panel'

/**
 * Модуль с функциями панели со списком задач
 * @type {string}
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
        let button = $('#tasks-list button:first-child');
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
 * Эта функция обрабатывает ответ сервера на запрос
 * информации о задаче
 */
export function receive_get_task_message(message) {
    $('#task-detail').replaceWith(message.task);
    update_pool_buttons_listeners();
}

/**
 * Эта функция обрабатывает ответ сервера на запрос
 * на добавление задачи в набор / удаление ее оттуда
 * @param message
 */
export function receive_add_to_pool_message(message) {
    if (message.status === 'OK') {
        let pool_id = '#' + message.pool_id;
        $(pool_id).replaceWith(message.pool_html);
        update_pool_buttons_listeners()
    }
}

/**
 * Эта функция обрабатывает ответ сервера на запрос
 * на добавление нового набора в список наборов пользователя
 * @param message
 */
export function receive_new_pool_message(message) {
    $('#pool-divider').before(message.pool_html);
    update_pool_buttons_listeners();
}

/**
 * Эта функция обновляет обработчики нажатий на кнопки
 * наборов задач
 */
function update_pool_buttons_listeners() {
    $('.pool-list-dropdown-button').each(function () {
        $(this).click(function () {
            send({
                message_type: ADD_TO_POOL,
                pool_pk: $(this).attr('pool_pk'),
                task_pk: $('#task-detail').attr('task_pk')
            })
        });
    });
    // добавить новый набор при нажатии Enter
    $('#new-pool-dropdown-button').keyup(function(e){
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
    $('#give-me-more').click(function (event) {
        send_request(UPDATE_LIST);
    });
}