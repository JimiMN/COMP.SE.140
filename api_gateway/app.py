from flask import Flask, request, Response
from enum import Enum
from datetime import datetime
import docker

# Initialize Flask app
app = Flask(__name__)

# Define the system states using Enum
class SystemState(Enum):
    INIT = "INIT"
    PAUSED = "PAUSED"
    RUNNING = "RUNNING"
    SHUTDOWN = "SHUTDOWN"

# State manager to handle transitions and actions
class SystemManager:
    def __init__(self):
        self.current_state = SystemState.INIT
        self.history = []
        self.docker_client = docker.from_env()

    def update_state(self, new_state):
        if isinstance(new_state, str):
            try:
                new_state = SystemState[new_state.upper()]
            except KeyError:
                return False, "Invalid state"

        # If requested state is the same as the current state, do nothing
        if new_state == self.current_state:
            return True, "State remains the same"

        # Log the state change with a timestamp
        timestamp = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + "Z"
        log_entry = f"{timestamp}: {self.current_state.value}->{new_state.value}"
        self.history.append(log_entry)

        # Handle shutdown scenario
        if new_state == SystemState.SHUTDOWN:
            try:
                containers = self.docker_client.containers.list()
                for container in containers:
                    container.stop()
                self.current_state = new_state
                return True, "All containers stopped"
            except docker.errors.APIError as e:
                return False, f"Failed to stop containers: {e}"

        # Handle init scenario (reset application state)
        if new_state == SystemState.INIT:
            self.current_state = new_state
            return True, "Application state reset. New login required."

        # Handle other state transitions (PAUSED, RUNNING)
        self.current_state = new_state
        return True, "State updated successfully"

    def get_state(self):
        return self.current_state.value

    def get_history(self):
        return "\n".join(self.history)

# Initialize the state manager
system_manager = SystemManager()

# Endpoint to get and update system state
@app.route('/state', methods=['GET', 'PUT'])
def state_controller():
    if request.method == 'GET':
        return Response(system_manager.get_state(), mimetype='text/plain')
    elif request.method == 'PUT':
        requested_state = request.data.decode('utf-8').strip()
        success, message = system_manager.update_state(requested_state)
        if success:
            return Response(message, status=200)
        return Response(message, status=400)

# Endpoint to get the system's state change history
@app.route('/run-log', methods=['GET'])
def run_log_controller():
    return Response(system_manager.get_history(), mimetype='text/plain')

# Endpoint to simulate a request (similar to the REQUEST button in the GUI)
@app.route('/request', methods=['GET'])
def execute_request():
    if system_manager.current_state != SystemState.RUNNING:
        return Response("System is not in RUNNING state", status=503)

    # Here we can implement logic to forward a request, similar to a proxy or backend request
    return Response("Request executed", mimetype='text/plain')

# Run the Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8197)
