from flask import Flask
import time
import threading

app = Flask(__name__)

is_sleeping = False

sleep_lock = threading.Lock()

@app.route('/')
def index():
    return "Service 1 is ready"

@app.route('/request')
def request_handler():
    global is_sleeping

    with sleep_lock:

        if is_sleeping:
            return "Service 1 is temporarily unavailable. Please try again after a moment.", 503
    

        is_sleeping = True


    response = "Service 1 response"
    time.sleep(2)


    with sleep_lock:
        is_sleeping = False

    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
