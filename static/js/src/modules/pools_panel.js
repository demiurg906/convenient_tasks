import {get_new_list} from "./tasks_list_panel";

/**
 * Модуль с функциями панели со списком наборов задач
 */

/**
 * Функция, инициализирующая все элементы панели с наборами задач
 */
export function initialize_pools_panel() {
    set_listeners_for_pool_buttons();
}

/**
 * Эта функция устанавливает обработчики для элементов списка наборов
 */
function set_listeners_for_pool_buttons() {
    $('#pools-list').children('button').each(function () {
        $(this).click(function () {
            $('#pools-list').attr('chosen_pool_pk', $(this).attr('pk'));
            $('.pool-button.active').removeClass('active');
            $(this).addClass('active');
            get_new_list();
        });
    });
}