from flask import Flask, jsonify
import psutil
import os
import socket
import time
import requests

app = Flask(__name__)


def get_system_info():
    # IP 
    hostname = socket.gethostbyname(socket.gethostname())  # Get internal IP address

    # Processes
    processes = [proc.info for proc in psutil.process_iter(attrs=['pid', 'name'])]

    # Disk space
    disk_info = psutil.disk_usage('/')
    available_space = disk_info.free / (1024 ** 3)  # Convert to GB

    # Time since boot
    uptime = time.time() - psutil.boot_time()

    return {
        "IP Address": hostname,
        "Running Processes": processes,
        "Available Disk Space (GB)": available_space,
        "Time Since Last Boot (seconds)": uptime
    }

# Get info from service2
def get_service_info(service_url):
    retries = 5
    while True:
        try:
            response = requests.get(service_url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException:
            if retries == 0:
                return {"error": "Could not fetch service info"}
            retries -= 1
            time.sleep(0.5)

@app.route('/')
def info():
    #Service 1
    service1_info = get_system_info()

    #Service 2
    service2_info = get_service_info('http://service2:3000/system-info')

    response = {
        "Service 1": service1_info,
        "Service 2": service2_info
    }

    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
