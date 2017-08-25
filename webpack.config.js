var path = require('path');

module.exports = [
    {
        devtool: 'source-map',
        entry: './static/js/src/main_modules/base_main.js',
        output: {
            path: path.resolve(__dirname, 'static'),
            filename: 'js/base_main.bundle.js'
        }
    },
    {
        devtool: 'source-map',
        entry: './static/js/src/main_modules/task_search_main.js',
        output: {
            path: path.resolve(__dirname, 'static'),
            filename: 'js/task_search_main.bundle.js'
        }
    },
    {
        devtool: 'source-map',
        entry: './static/js/src/main_modules/pools_main.js',
        output: {
            path: path.resolve(__dirname, 'static'),
            filename: 'js/pools_main.bundle.js'
        }
    }
];
