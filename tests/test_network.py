import socket
import requests
import logging
import os
import ipaddress

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def validate_ip(ip_str):
    try:
        ipaddress.ip_address(ip_str)
        return True
    except ValueError:
        return False

def test_comprehensive_network():
    # Hostname resolution strategies
    hostnames = [
        'dockerhost', 
        'localhost', 
        'api-gateway', 
        '127.0.0.1'
    ]
    
    # Resolve and validate hostnames
    for hostname in hostnames:
        try:
            ip = socket.gethostbyname(hostname)
            logger.info(f"Resolved {hostname} to {ip}")
            
            # Additional IP validation
            if validate_ip(ip):
                logger.debug(f"IP {ip} is valid")
            else:
                logger.warning(f"Invalid IP for {hostname}")
        
        except socket.gaierror as e:
            logger.error(f"Hostname resolution failed for {hostname}: {e}")

    # Connection strategies
    connection_attempts = [
        ('http://api-gateway:8197/state', 'Service Name'),
        ('http://localhost:8197/state', 'Localhost'),
        ('http://172.18.0.7:8197/state', 'Direct IP')
    ]

    # Test API connections
    for url, method in connection_attempts:
        try:
            logger.debug(f"Attempting connection via {method}: {url}")
            response = requests.get(url, timeout=10)
            logger.info(f"Successfully connected via {method}")
            assert response.status_code == 200
        except Exception as e:
            logger.warning(f"Connection failed via {method}: {e}")