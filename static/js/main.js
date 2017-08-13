const TASKS_LIST = 'tasks_list';
const GET_TASK = 'get_task';

$(document).ready(function(){
    let socket;
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

    let tasks_list = $("#tasks_list");
    tasks_list.max_pk = 0;

    function send(data) {
        socket.send(JSON.stringify(data));
    }

    $('#give_me_more').click(function (event) {
        send({
            message_type: TASKS_LIST,
            n: 10,
            max_pk: tasks_list.max_pk
        });
    });

    function update_listeners() {
        $('.task_button').click(function (event) {
            send({
                message_type: GET_TASK,
                pk: this.getAttribute('pk')
            })
        });
    }


    function receive_message(message) {
        let data = JSON.parse(message);
        if (data.message_type === TASKS_LIST) {
            for (let task of data.tasks) {
                tasks_list.append(task);
            }
            tasks_list.max_pk = data.max_pk;
            update_listeners();
        } else if (data.message_type === GET_TASK) {
            $('#task_detail').replaceWith(data.task);
        }
    };
});

