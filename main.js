const { app, BrowserWindow } = require('electron')
const path = require('node:path')
const { spawn } = require('child_process');

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
      width: 200,
      height: 200,
      alwaysOnTop: true,
    });
  mainWindow.loadFile(`index.html`);
  // mainWindow.setIgnoreMouseEvents(true);
  // mainWindow.setFocusable(false);
  // Execute the Python script on startup
  const pythonProcess = spawn('python', [path.join(__dirname, 'python_scripts/textExtractor.py')]);
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') app.quit()
});