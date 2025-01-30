import requests

BASE_URL = "http://localhost:8197"  # Adjust this to your local URL if needed

def test_get_state():
    response = requests.get(f"{BASE_URL}/state")
    assert response.status_code == 200
    assert response.text in ["INITIALIZED", "PAUSED", "RUNNING", "SHUTDOWN"]

def test_set_state():
    headers = {"Content-Type": "text/plain"}
    # Ensure sending a valid state
    response = requests.put(f"{BASE_URL}/state", data="RUNNING", headers=headers)
    assert response.status_code == 200
