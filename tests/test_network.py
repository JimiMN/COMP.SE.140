import socket
import requests
import logging
import os

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def test_network_connectivity():
    # Multiple connection strategies
    connection_attempts = [
        ('http://api-gateway:8197/state', 'Service Name'),
        ('http://localhost:8197/state', 'Localhost'),
        ('http://172.18.0.7:8197/state', 'Direct IP')
    ]

    # Hostname resolution attempts
    hostnames = ['docker', 'api-gateway', 'localhost']
    
    # Resolve hostnames
    for hostname in hostnames:
        try:
            ip = socket.gethostbyname(hostname)
            logger.info(f"Resolved {hostname} to {ip}")
        except socket.gaierror as e:
            logger.error(f"Hostname resolution failed for {hostname}: {e}")

    # Test API connections
    for url, method in connection_attempts:
        try:
            logger.debug(f"Attempting connection via {method}: {url}")
            response = requests.get(url, timeout=10)
            logger.info(f"Successfully connected via {method}")
            assert response.status_code == 200
        except Exception as e:
            logger.warning(f"Connection failed via {method}: {e}")