import {get_new_list} from "./tasks_list_panel";

export function initialize_pools_panel() {
    set_listeners_for_pool_buttons();
}

function set_listeners_for_pool_buttons() {
    $('#pools-list').children('button').each(function () {
        $(this).click(function () {
            console.log('hello ' + $(this).attr('pk'));
            $('#pools-list').attr('chosen_pool_pk', $(this).attr('pk'));
            get_new_list();
        });
    });
}