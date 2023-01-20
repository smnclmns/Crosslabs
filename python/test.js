const { spawn } = require('child_process');

const script = spawn('python', ['-u', 'SerialPort_Connector.py', 'arg1']);

script.stdout.on('data', (data) => {
    console.log("stdout: " + data.toString());
});

script.stderr.on('data', (data) => {
    console.log("`stderr: " + data.toString());
});

script.on('close', (code) => {
    console.log("child process exited with code " + code.toString());
});