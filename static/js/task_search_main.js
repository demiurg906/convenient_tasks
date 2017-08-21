/******/ (function(modules) { // webpackBootstrap
/******/ 	// The module cache
/******/ 	var installedModules = {};
/******/
/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {
/******/
/******/ 		// Check if module is in cache
/******/ 		if(installedModules[moduleId]) {
/******/ 			return installedModules[moduleId].exports;
/******/ 		}
/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = installedModules[moduleId] = {
/******/ 			i: moduleId,
/******/ 			l: false,
/******/ 			exports: {}
/******/ 		};
/******/
/******/ 		// Execute the module function
/******/ 		modules[moduleId].call(module.exports, module, module.exports, __webpack_require__);
/******/
/******/ 		// Flag the module as loaded
/******/ 		module.l = true;
/******/
/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}
/******/
/******/
/******/ 	// expose the modules object (__webpack_modules__)
/******/ 	__webpack_require__.m = modules;
/******/
/******/ 	// expose the module cache
/******/ 	__webpack_require__.c = installedModules;
/******/
/******/ 	// define getter function for harmony exports
/******/ 	__webpack_require__.d = function(exports, name, getter) {
/******/ 		if(!__webpack_require__.o(exports, name)) {
/******/ 			Object.defineProperty(exports, name, {
/******/ 				configurable: false,
/******/ 				enumerable: true,
/******/ 				get: getter
/******/ 			});
/******/ 		}
/******/ 	};
/******/
/******/ 	// getDefaultExport function for compatibility with non-harmony modules
/******/ 	__webpack_require__.n = function(module) {
/******/ 		var getter = module && module.__esModule ?
/******/ 			function getDefault() { return module['default']; } :
/******/ 			function getModuleExports() { return module; };
/******/ 		__webpack_require__.d(getter, 'a', getter);
/******/ 		return getter;
/******/ 	};
/******/
/******/ 	// Object.prototype.hasOwnProperty.call
/******/ 	__webpack_require__.o = function(object, property) { return Object.prototype.hasOwnProperty.call(object, property); };
/******/
/******/ 	// __webpack_public_path__
/******/ 	__webpack_require__.p = "";
/******/
/******/ 	// Load entry module and return exports
/******/ 	return __webpack_require__(__webpack_require__.s = 0);
/******/ })
/************************************************************************/
/******/ ([
/* 0 */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
Object.defineProperty(__webpack_exports__, "__esModule", { value: true });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__modules_left_search_panel__ = __webpack_require__(1);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1__modules_tasks_list_panel__ = __webpack_require__(2);
//TODO: добавить проверку версии браузера




const TASKS_LIST = 'tasks_list';
/* harmony export (immutable) */ __webpack_exports__["TASKS_LIST"] = TASKS_LIST;

const GET_TASK = 'get_task';
/* harmony export (immutable) */ __webpack_exports__["GET_TASK"] = GET_TASK;



$(document).ready(function(){
    let socket;
    function connect() {
        socket = new WebSocket('ws://' + window.location.host + '/problems/tasks/');
        // Type of information received by websocket
        // socket.binaryType = 'arraybuffer';

        socket.onopen = function (event) {
            Object(__WEBPACK_IMPORTED_MODULE_0__modules_left_search_panel__["c" /* set_listeners_for_sections_dropdown */])(socket, 'sections');
            Object(__WEBPACK_IMPORTED_MODULE_0__modules_left_search_panel__["c" /* set_listeners_for_sections_dropdown */])(socket, 'subsections');
            Object(__WEBPACK_IMPORTED_MODULE_1__modules_tasks_list_panel__["a" /* get_new_list */])(socket);
        };

        socket.onmessage = (e) => receive_message(e.data);

        socket.onclose = () => {
            setTimeout(() => {
                connect()
            }, 5000)
        };
    }

    connect();
    Object(__WEBPACK_IMPORTED_MODULE_0__modules_left_search_panel__["a" /* initialize_slider */])(socket);

    function receive_message(message) {
        let data = JSON.parse(message);
        if (data.message_type === TASKS_LIST) {
            Object(__WEBPACK_IMPORTED_MODULE_1__modules_tasks_list_panel__["c" /* receive_task_list_message */])(socket, data)
        } else if (data.message_type === GET_TASK) {
            Object(__WEBPACK_IMPORTED_MODULE_1__modules_tasks_list_panel__["b" /* receive_get_task_message */])(data)
        }
    }
});



/***/ }),
/* 1 */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (immutable) */ __webpack_exports__["c"] = set_listeners_for_sections_dropdown;
/* harmony export (immutable) */ __webpack_exports__["a"] = initialize_slider;
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__tasks_list_panel__ = __webpack_require__(2);


const section_button = $('#sections button');
/* harmony export (immutable) */ __webpack_exports__["b"] = section_button;

const subsection_button = $('#subsections button');
/* harmony export (immutable) */ __webpack_exports__["d"] = subsection_button;


function set_listeners_for_sections_dropdown(socket, name) {
    $('#' + name + ' li').click(function () {
        console.log($(this).text());
        $('#' + name + ' button').text($(this).text());
        Object(__WEBPACK_IMPORTED_MODULE_0__tasks_list_panel__["a" /* get_new_list */])(socket);
    });
}

function initialize_slider(socket) {
    let slider = $( "#grade_slider" );

    slider.slider({
        values: [7, 9],
        min: 1,
        max: 11,
        step: 1,
        range: true,
        slide: function( event, ui ) {
            $( "#amount" ).val( "$" + ui.values[ 0 ] + " - $" + ui.values[ 1 ] );
        }
    }).each(function() {
        let opt = $(this).data().uiSlider.options;
        let vals = opt.max - opt.min;
        for (let i = 0; i <= vals; i++) {
            let el = $('<label>' + (i + opt.min) + '</label>').css('left', (i / vals * 100) + '%');
            $("#grade_slider").append(el);
        }
    });

    slider.on('slidechange', function( event, ui ) {
        Object(__WEBPACK_IMPORTED_MODULE_0__tasks_list_panel__["a" /* get_new_list */])(socket);
    } );
}

/***/ }),
/* 2 */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (immutable) */ __webpack_exports__["c"] = receive_task_list_message;
/* harmony export (immutable) */ __webpack_exports__["b"] = receive_get_task_message;
/* harmony export (immutable) */ __webpack_exports__["a"] = get_new_list;
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__main_modules_task_search_main__ = __webpack_require__(0);
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1__left_search_panel__ = __webpack_require__(1);


const NEW_LIST = 'new_list';
const UPDATE_LIST = 'update_list';

const N = 10;



function enable_more_tasks_button() {
    $('#give_me_more').prop('disabled', false);
}

function send_request_for_search_list_of_tasks(socket, action) {
    let grades = $('#grade_slider').data().uiSlider.options.values;
    send(socket, {
        message_type: __WEBPACK_IMPORTED_MODULE_0__main_modules_task_search_main__["TASKS_LIST"],
        n: N,
        max_pk: $('#tasks_list').max_pk,
        section: __WEBPACK_IMPORTED_MODULE_1__left_search_panel__["b" /* section_button */].text(),
        subsection: __WEBPACK_IMPORTED_MODULE_1__left_search_panel__["d" /* subsection_button */].text(),
        min_grade: grades[0],
        max_grade: grades[1],
        action: action
    });
}

function send(socket, data) {
    socket.send(JSON.stringify(data));
}

function update_listeners(socket) {
    $('.task_button').click(function (event) {
        get_task_description(socket, this.getAttribute('pk'));
    });
}

function get_task_description(socket, pk) {
    send(socket, {
        message_type: __WEBPACK_IMPORTED_MODULE_0__main_modules_task_search_main__["GET_TASK"],
        pk: pk
    })
}

function disable_more_tasks_button() {
    $('#give_me_more').prop('disabled', true);
}

function receive_task_list_message(socket, message) {
    let tasks_list = $('#tasks_list');
    for (let task of message.tasks) {
        tasks_list.append(task);
    }
    tasks_list.max_pk = message.max_pk;
    if (message.tasks.length < N) {
        disable_more_tasks_button()
    }
    update_listeners(socket);
    if (message.action === NEW_LIST) {
        let button = $('#tasks_list button:first-child');
        if (button.length > 0) {
            button.click()
        } else {
            get_task_description(socket, -1);
            disable_more_tasks_button()
        }
    }
}

function receive_get_task_message(message) {
    $('#task_detail').replaceWith(message.task);
}

function get_new_list(socket) {
    let tasks_list = $("#tasks_list");
    tasks_list.max_pk=0;
    tasks_list.empty();
    enable_more_tasks_button();
    send_request_for_search_list_of_tasks(socket, NEW_LIST);
}


/***/ })
/******/ ]);
//# sourceMappingURL=task_search_main.js.map