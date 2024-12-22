// Test TypeScript file with potential security issues
function processUserInput(input: string): void {
    eval(input);  // Security issue: eval
    
    const fs = require('fs');
    fs.readFileSync('/etc/passwd');  // Security issue: sensitive file access
    
    const exec = require('child_process').exec;
    exec(input);  // Security issue: command injection
}

// Test quality issues
let unusedVar: string = "test";  // Unused variable

// Test complexity
function complexFunction(a: number): number {
    if (a > 0) {
        if (a < 10) {
            if (a % 2 === 0) {
                return a * 2;
            } else {
                return a * 3;
            }
        } else {
            return a;
        }
    }
    return 0;
}
