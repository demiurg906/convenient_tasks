import {get_new_list} from './tasks_list_panel';

/**
 * Модуль с функциями панели с параметрами поиска
 */

// ссылки на кнопки выбора секций
export const section_button = $('#sections button');
export const subsection_button = $('#subsections button');

/**
 * Эта функция устанавливает обработчики для выпажающих списков секций и подсекций
 * @param name имя элемента
 */
function set_listeners_for_sections_dropdown(name) {
    $('#' + name + ' li').click(function () {
        console.log($(this).text());
        $('#' + name + ' button').text($(this).text());
        get_new_list();
    });
}

/**
 * Эта функция инициализирует слайдер для выбора классов
 */
function initialize_slider() {
    let slider = $('#grade-slider');

    slider.slider({
        values: [7, 9],
        min: 1,
        max: 11,
        step: 1,
        range: true,
        slide: function( event, ui ) {
            $( '#amount' ).val( '$' + ui.values[ 0 ] + ' - $' + ui.values[ 1 ] );
        }
    }).each(function() {
        let opt = $(this).data().uiSlider.options;
        let vals = opt.max - opt.min;
        for (let i = 0; i <= vals; i++) {
            let el = $('<label>' + (i + opt.min) + '</label>').css('left', (i / vals * 100) + '%');
            $('#grade_slider').append(el);
        }
    });

    slider.on('slidechange', function() {
        get_new_list();
    } );
}

/**
 * Функция, инициализирующая все элементы панели поиска
 */
export function initialize_left_panel() {
    initialize_slider();
    set_listeners_for_sections_dropdown('sections');
    set_listeners_for_sections_dropdown('subsections');
}

/**
 * Эта функция возвращает значения слайдера
 */
export function get_grade_slider_values() {
    return $('#grade-slider').data().uiSlider.options.values;
}