import socket
import requests
import logging
import ipaddress
import os

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def validate_network_connectivity():
    # Comprehensive connection strategies
    connection_attempts = [
        # Try multiple connection methods
        ('http://api-gateway:8197/state', 'Service Name'),
        ('http://localhost:8197/state', 'Localhost'),
        ('http://172.18.0.7:8197/state', 'Direct IP')
    ]

    # Hostname resolution strategies
    hostnames_to_check = [
        'localhost', 
        'api-gateway', 
        '127.0.0.1'
    ]

    # Resolve hostnames
    for hostname in hostnames_to_check:
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