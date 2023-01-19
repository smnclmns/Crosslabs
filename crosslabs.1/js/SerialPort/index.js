const { readFile, readFileSync } = require('fs');

const txt = readFileSync('crosslabs.1/js/SerialPort/hello.txt', 'utf8')

readFile('crosslabs.1/js/SerialPort/hello.txt', 'utf8', (err, txt) => {
    console.log(txt)
});

console.log(txt)

console.log('do this ASAP')