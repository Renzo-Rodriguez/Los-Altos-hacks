const { app, BrowserWindow, globalShortcut } = require('electron')

const path = require('node:path')
const { spawn } = require('child_process');

let mainWindow;

app.whenReady().then(() => {
  mainWindow = new BrowserWindow({
    transparent: true,
    frame: false,
    width: 180,
    height: 180,
    alwaysOnTop: true,
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false,
      preload: path.join(__dirname, 'preload.js')
    }
  });
  mainWindow.loadFile(`index.html`);

  // Execute the Python script on startup
  const pythonProcess = spawn('python', [path.join(__dirname, 'python_scripts/textExtractor.py')]);

  mainWindow.webContents.on('did-finish-load', () => {
    mainWindow.webContents.insertCSS(css).then((key) => {
      // Store the key if needed for removal
      console.log('CSS injected'); // Placeholder for actual injection code
      cssInjected = true;
    
      cssKey = key;
    });
  })
  // call your function here
  // mainWindow.setIgnoreMouseEvents(true);
  // mainWindow.setFocusable(false);

})

// setInterval(function(){
//   // call your function here
//   var pos = mainWindow.getPosition();
//   console.log(pos[0]);
//   console.log(pos[1]);
//   mainWindow.setPosition(pos[0] + 10, pos[1] + 10);
// }, 1000);

let cssInjected = true;
let cssKey;

// CSS to inject
const css = `* {
  -webkit-user-select: none;
  -webkit-app-region: drag;
}`;

// Function to toggle CSS injection
function toggleCSS() {
  if (cssInjected) {
    // Assuming you have the CSS key, remove the CSS
    // This example simply toggles the state for simplicity
    // In a real implementation, you would use webContents.removeInsertedCSS(cssKey);
    mainWindow.webContents.removeInsertedCSS(cssKey);
    console.log('CSS removed'); // Placeholder for actual removal code
    cssInjected = false;
  } else {
    // Inject CSS and store the key
    mainWindow.webContents.insertCSS(css).then((key) => {
      // Store the key if needed for removal
      console.log('CSS injected'); // Placeholder for actual injection code
      cssInjected = true;

      cssKey = key;
    });
  }
}

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') app.quit()
})

app.on('ready', () => {
  // Register a global shortcut listener. For example, 'Ctrl+Shift+I'
  globalShortcut.register('Ctrl+Shift+M', () => {
    console.log('Global shortcut Ctrl+Shift+M is pressed, toggling css');
    toggleCSS();
  });
});

// Remember to unregister all global shortcuts when the app is about to quit
app.on('will-quit', () => {
  globalShortcut.unregisterAll();
});