from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/status')
def status():
    return jsonify(message="Service 2 is running")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
