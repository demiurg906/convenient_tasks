const TASKS_LIST = 'tasks_list';
const GET_TASK = 'get_task';

const NEW_LIST = 'new_list';
const UPDATE_LIST = 'update_list';

const N = 10;

$(document).ready(function(){
    // Слайдер для выбора класса
    $( "#grade_slider" ).slider({
        values: [7, 9],
        min: 1,
        max: 11,
        step: 1,
        range: true,
        slide: function( event, ui ) {
            $( "#amount" ).val( "$" + ui.values[ 0 ] + " - $" + ui.values[ 1 ] );
        }
    }).each(function() {
        var opt = $(this).data().uiSlider.options;
        var vals = opt.max - opt.min;
        for (var i = 0; i <= vals; i++) {
            var el = $('<label>' + (i + opt.min) + '</label>').css('left', (i/vals*100) + '%');
            $("#grade_slider").append(el);
        }
    });
    $('#grade_slider').on('slidechange', function( event, ui ) {
        get_new_list();
    } );

    let socket;
    let section_button = $('#sections button');
    let subsection_button = $('#subsections button');
    function connect() {
        socket = new WebSocket('ws://' + window.location.host + '/problems/tasks/');
        // Type of information received by websocket
        // socket.binaryType = 'arraybuffer';
        // register handler of the incoming messages
        socket.onmessage = (e) => receive_message(e.data);

        socket.onclose = () => {
            setTimeout(() => { connect() }, 5000)
        };
    };
    connect();
    socket.onopen = socket.onopen = function (event) {
        set_listeners_for_sections_dropdown('sections');
        set_listeners_for_sections_dropdown('subsections');
        get_new_list();
    };

    let tasks_list = $("#tasks_list");

    function send(data) {
        socket.send(JSON.stringify(data));
    }

    function send_request_for_list_of_tasks(action) {
        let grades = $('#grade_slider').data().uiSlider.options.values;
        send({
            message_type: TASKS_LIST,
            n: N,
            max_pk: tasks_list.max_pk,
            section: section_button.text(),
            subsection: subsection_button.text(),
            min_grade: grades[0],
            max_grade: grades[1],
            action: action
        });
    }

    function get_new_list() {
        tasks_list.max_pk=0;
        tasks_list.empty();
        enable_more_tasks_button();
        send_request_for_list_of_tasks(NEW_LIST);
    }

    $('#give_me_more').click(function (event) {
        send_request_for_list_of_tasks(UPDATE_LIST);
    });

    function disable_more_tasks_button() {
        $('#give_me_more').prop('disabled', true);
    }

    function enable_more_tasks_button() {
        $('#give_me_more').prop('disabled', false);
    }

    function get_task_description(pk) {
        send({
            message_type: GET_TASK,
            pk: pk
        })
    }

    function update_listeners() {
        $('.task_button').click(function (event) {
            get_task_description(this.getAttribute('pk'));
        });
    }

    function receive_message(message) {
        let data = JSON.parse(message);
        if (data.message_type === TASKS_LIST) {
            for (let task of data.tasks) {
                tasks_list.append(task);
            }
            tasks_list.max_pk = data.max_pk;
            if (data.tasks.length < N) {
                disable_more_tasks_button()
            }
            update_listeners();
            if (data.action === NEW_LIST) {
                button = $('#tasks_list button:first-child');
                if (button.length > 0) {
                    button.click()
                } else {
                    get_task_description(-1);
                    disable_more_tasks_button()
                }
            }
        } else if (data.message_type === GET_TASK) {
            $('#task_detail').replaceWith(data.task);
        }
    };

    function set_listeners_for_sections_dropdown(name) {
        $('#' + name + ' li').click(function () {
            console.log($(this).text());
            $('#' + name + ' button').text($(this).text());
            get_new_list();
        });
    };
});

