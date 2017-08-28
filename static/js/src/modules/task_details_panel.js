/**
 * Модуль с функциями панели со списком задач
 */

import {ADD_TO_POOL, NEW_POOL, POOL_PAGE, SEARCH_PAGE, send} from "./variables_and_constants";
import {get_new_list} from "./tasks_list_panel";

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
        if (SEARCH_PAGE) {
            // обновить иконку у набора
            let pool_id = '#' + message.pool_id;
            $(pool_id).replaceWith(message.pool_html);
        } else if (POOL_PAGE) {
            // заного получить список задач в наборе (без удаленной)
            get_new_list();
        }
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
    // кнопка удаления задачи из набора (страница наборов)
    $('#remove_task_button').click(() => send({
        message_type: ADD_TO_POOL,
        pool_pk: $('#pools-list').attr('chosen_pool_pk'),
        task_pk: $('#task-detail').attr('task_pk')
    }));
    // добавить в набор/удалить оттуда (страница поиска)
    $('.pool-list-dropdown-button').each(function () {
        $(this).click(() => send({
            message_type: ADD_TO_POOL,
            pool_pk: $(this).attr('pool_pk'),
            task_pk: $('#task-detail').attr('task_pk')
        }));
    });
    // добавить новый набор при нажатии Enter (страница поиска)
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