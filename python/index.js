

const { spawn } = require('child_process');

const buttons = document.querySelectorAll(".run-script");

buttons.forEach(function(button) {

    button.addEventListener("click", function () {
        // Get the argument from button's "data-arg" attribute
        const arg = this.getAttribute("data-arg");
        const script = spawn('python', ['-u', 'SerialPort_Connector.py', arg])

        script.stdout.on('data', function(data) {
            console.log('\nstdout: ' + data.toString());
        });

        script.stderr.on('data', function(data) {
            console.log('stderr: ' + data.toString());
        });

        script.stdout.on('close', function(code) {
            console.log('the child_process exited with err-code: ' + code.toString());
        });


    });
    
});
