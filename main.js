const { app, BrowserWindow } = require('electron')
const path = require('node:path')

let mainWindow

// const createWindow = () => {
//   const win = new BrowserWindow({
//     width: 800,
//     height: 600,
//     webPreferences: {
//       preload: path.join(__dirname, 'preload.js')
//     }
//   })

//   win.loadFile('index.html')
// }

app.whenReady().then(() => {
  mainWindow = new BrowserWindow({
      transparent: true,
      frame: false,
      alwaysOnTop: true,
    });
  mainWindow.loadFile(`index.html`);
  // mainWindow.setIgnoreMouseEvents(true);
  // mainWindow.setFocusable(false);
})

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') app.quit()
})