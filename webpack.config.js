var path = require('path');

module.exports = {
    devtool: 'source-map',
    entry: './js/main_modules/task_search_main.js',
    output: {
        path: path.resolve(__dirname, 'static'),
        filename: 'js/task_search_main.js'
    }
};
