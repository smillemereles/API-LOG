import requests
import random
from datetime import datetime, timezone
import json
import time

# Configuración
service_names = ['Service1', 'Service2', 'Service3', 'Service4', 'Service5']
log_levels = ['info', 'error', 'debug']
api_key = "secret_api_key"  

def get_random_item(array):
    return random.choice(array)

def generate_random_log():
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    service_name = get_random_item(service_names)
    log_level = get_random_item(log_levels)
    message = f"This is a {log_level} message from {service_name}"
    
    return {
        "timestamp": timestamp,
        "service_name": service_name,
        "log_level": log_level,
        "message": message
    }

def send_log(log):
    url = 'http://localhost:8080/logs'
    headers = {
        'Content-Type': 'application/json',
        'x-api-key': api_key  
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(log))
        response.raise_for_status()
        print('Log sent successfully', log)
    except requests.RequestException as e:
        print('Error sending log', str(e))

if __name__ == '__main__':  
    while True:
        log = generate_random_log()
        send_log(log)
        time.sleep(5)
