const {app, BrowserWindow} = require('electron');

function createWindow() {
    window = new BrowserWindow();
    window.loadFile('index.html')
};

app.on('ready', createWindow)

let {PythonShell} = require('python-shell');
const path = require('path');

var options = {
    scriptPath : __dirname,
    args: []
};

let pyshell = new PythonShell('run_app.py', options)

pyshell.on('message', function(message) {
    console.log(message);
    console.log(typeof message);
});

app.on('window-all-closed', () => {
    app.quit()
    pyshell.kill()
})