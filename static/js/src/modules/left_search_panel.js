import {get_new_list} from './tasks_list_panel';

export const section_button = $('#sections button');
export const subsection_button = $('#subsections button');

function set_listeners_for_sections_dropdown(name) {
    $('#' + name + ' li').click(function () {
        console.log($(this).text());
        $('#' + name + ' button').text($(this).text());
        get_new_list();
    });
}

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

    slider.on('slidechange', function( event, ui ) {
        get_new_list();
    } );
}

export function initialize_left_panel() {
    initialize_slider();
    set_listeners_for_sections_dropdown('sections');
    set_listeners_for_sections_dropdown('subsections');
}