from flask import Flask, jsonify
import time

app = Flask(__name__)

@app.route('/')
def index():
    return "Service 1 response after 2 seconds"

@app.route('/request')
def request_handler():
    time.sleep(2)  # Simulate some processing time
    return "Service 1 response after 2 seconds"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

