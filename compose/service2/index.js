const express = require('express');
const os = require('os');
const { execSync } = require('child_process');
const app = express();
const port = 3000;

// Function to get IP address
function getIpAddress() {
    const interfaces = os.networkInterfaces();
    for (let interfaceName in interfaces) {
        for (let iface of interfaces[interfaceName]) {
            // Ignore internal (localhost) and IPv6 addresses
            if (iface.family === 'IPv4' && !iface.internal) {
                return iface.address; // Return the first found external IPv4 address
            }
        }
    }
    return 'Not Found'; // If no external IP found
}

// Endpoint to get system information
app.get('/system-info', (req, res) => {
    // Get running processes
    const processes = execSync('ps -eo pid,comm').toString().split('\n').slice(1).map(line => {
        const parts = line.trim().split(/\s+/);
        return { pid: parts[0], name: parts[1] };
    }).filter(proc => proc.name); // Filter out empty lines

    // Get IP address using the new function
    const ip = getIpAddress();

    // Get available disk space
    const diskUsage = execSync('df -h /').toString().split('\n')[1].split(/\s+/);
    const availableSpace = diskUsage[3]; // The available space in the 4th column

    // Get uptime
    const uptime = os.uptime(); // Uptime in seconds

    const systemInfo = {
        "IP Address": ip,
        "Running Processes": processes,
        "Available Disk Space": availableSpace,
        "Time Since Last Boot (seconds)": uptime
    };

    res.json(systemInfo);
});

app.listen(port, () => {
    console.log(`Node.js service listening at http://localhost:${port}`);
});
