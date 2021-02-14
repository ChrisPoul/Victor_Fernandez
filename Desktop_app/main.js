const {app, BrowserWindow} = require('electron');
const fs = require('fs')
const path = require('path')
const os = require('os')


function print_window(window) {
    // Use default printing options
    window.webContents.printToPDF({}).then(data => {
        let file_name = window.webContents.getURL();
        const pdfPath = path.join(os.homedir(), 'Desktop', 'temp.pdf')
        fs.writeFile(pdfPath, data, (error) => {
        if (error) throw error
        console.log(`Wrote PDF successfully to ${pdfPath}`)
        })
    }).catch(error => {
        console.log(`Failed to write PDF to ${pdfPath}: `, error)
    })
}

function createWindow() {
    window = new BrowserWindow();
    setTimeout(() => { 
         window.loadURL('http://127.0.0.1:5000/'); 
        }, 150);
};

const { Menu, MenuItem } = require('electron')

const menu = new Menu()
menu.append(new MenuItem({
  label: 'Print',
  submenu: [{
    role: 'print',
    accelerator: process.platform === 'linux' ? 'Ctrl+P' : 'Ctrl+P',
    click: () => { 
        window = BrowserWindow.getFocusedWindow();
        print_window(window)
     }
  }]
}))

Menu.setApplicationMenu(menu)

app.on('ready', createWindow);

app.on('window-all-closed', () => {
    app.quit()
})