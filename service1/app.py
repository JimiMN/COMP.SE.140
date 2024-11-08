from flask import Flask
import time
import threading

app = Flask(__name__)

# A global flag to track whether the service is in "sleeping" mode.
is_sleeping = False

# Lock to ensure thread safety when checking and modifying the sleep state
sleep_lock = threading.Lock()

@app.route('/')
def index():
    return "Service 1 is ready"

@app.route('/request')
def request_handler():
    global is_sleeping

    with sleep_lock:
        # Check if the service is currently sleeping (i.e., after handling a request).
        if is_sleeping:
            return "Service 1 is temporarily unavailable. Please try again after a moment.", 503
    
        # Mark the service as sleeping after receiving the request.
        is_sleeping = True

    # Send the response after the 2-second sleep
    response = "Service 1 response"
    time.sleep(2)

    # Mark the service as ready again after responding
    with sleep_lock:
        is_sleeping = False

    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
