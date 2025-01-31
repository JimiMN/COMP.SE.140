import socket
import requests
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def test_service_connection():
    connection_attempts = [
        ('http://api-gateway:8197/state', 'Service Name'),
        ('http://localhost:8197/state', 'Localhost'),
        ('http://172.18.0.7:8197/state', 'Direct IP')
    ]

    for url, method in connection_attempts:
        try:
            logger.debug(f"Attempting connection via {method}: {url}")
            response = requests.get(url, timeout=10)
            logger.info(f"Successfully connected via {method}")
            assert response.status_code == 200
            return
        except Exception as e:
            logger.warning(f"Connection failed via {method}: {e}")

    raise ConnectionError("Could not establish connection to API Gateway")

def test_hostname_resolution():
    try:
        ip = socket.gethostbyname('api-gateway')
        logger.info(f"Resolved api-gateway to IP: {ip}")
    except socket.gaierror as e:
        logger.error(f"Hostname resolution failed: {e}")
        raise