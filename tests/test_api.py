import requests

BASE_URL = "http://localhost:8197"  # Adjust this to your local URL if needed

def test_get_state():
    response = requests.get(f"{BASE_URL}/state")
    assert response.status_code == 200
    assert response.text in ["INITIALIZED", "IDLE", "ACTIVE", "TERMINATED"]

def test_set_state():
    headers = {"Content-Type": "text/plain"}
    # Ensure you're sending a valid state
    response = requests.put(f"{BASE_URL}/state", data="ACTIVE", headers=headers)
    assert response.status_code == 200
