import requests

BASE_URL = "http://localhost:8197/"  # Adjust this to your local URL if needed


def test_put_init_state():
    headers = {"Content-Type": "text/plain"}
    response = requests.put(f"{BASE_URL}/state", data="INIT", headers=headers)
    assert response.status_code == 200

    # Verify the state is set to INIT
    response = requests.get(f"{BASE_URL}/state")
    assert response.status_code == 200
    assert response.text == "INIT"

    # Verify the system requires new login
    response = requests.get(f"{BASE_URL}/request")
    assert response.status_code != 200 

def test_put_paused_state():
    headers = {"Content-Type": "text/plain"}
    response = requests.put(f"{BASE_URL}/state", data="PAUSED", headers=headers)
    assert response.status_code == 200

    # Verify the state is set to PAUSED
    response = requests.get(f"{BASE_URL}/state")
    assert response.status_code == 200
    assert response.text == "PAUSED"

    # Test system behavior when PAUSED
    response = requests.get(f"{BASE_URL}/request")
    assert response.status_code != 200


def test_put_running_state():
    headers = {"Content-Type": "text/plain"}
    response = requests.put(f"{BASE_URL}/state", data="RUNNING", headers=headers)
    assert response.status_code == 200

    # Verify the state is set to RUNNING
    response = requests.get(f"{BASE_URL}/state")
    assert response.status_code == 200
    assert response.text == "RUNNING"

    # Test system behavior when RUNNING
    response = requests.get(f"{BASE_URL}/request")
    assert response.status_code == 200

def test_get_run_log():
    # Make state changes to generate logs
    headers = {"Content-Type": "text/plain"}

    # Set state to INIT
    response = requests.put(f"{BASE_URL}/state", data="INIT", headers=headers)
    assert response.status_code == 200

    # Set state to RUNNING
    response = requests.put(f"{BASE_URL}/state", data="RUNNING", headers=headers)
    assert response.status_code == 200

    # Set state to PAUSED
    response = requests.put(f"{BASE_URL}/state", data="PAUSED", headers=headers)
    assert response.status_code == 200

    # Set state back to RUNNING
    response = requests.put(f"{BASE_URL}/state", data="RUNNING", headers=headers)
    assert response.status_code == 200

    # Query /run-log and check for the state change logs
    response = requests.get(f"{BASE_URL}/run-log")
    assert response.status_code == 200

    # Check if the response contains the expected state transitions
    log = response.text
    assert "INIT->RUNNING" in log
    assert "RUNNING->PAUSED" in log
    assert "PAUSED->RUNNING" in log


def test_put_shutdown_state():
    headers = {"Content-Type": "text/plain"}
    response = requests.put(f"{BASE_URL}/state", data="SHUTDOWN", headers=headers)
    assert response.status_code == 200

    # Test system behavior when SHUTDOWN
    response = requests.get(f"{BASE_URL}/request")
    assert response.status_code != 200
