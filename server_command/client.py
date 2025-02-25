"""API client functionality for the server command client."""

import time
import sys
import os
import requests

# Add parent directory to path for direct script execution
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from .config import SERVER_URL, DEFAULT_POLL_TIMEOUT, POLL_INTERVAL
    from .logger import setup_logging
except ImportError:
    from server_command.config import SERVER_URL, DEFAULT_POLL_TIMEOUT, POLL_INTERVAL
    from server_command.logger import setup_logging

logger = setup_logging()

def send_command(api_key: str, command: dict) -> str:
    """
    Send the automation command to the REST API server.
    Returns the generated requestId.
    """
    command['apiKey'] = api_key
    url = f"{SERVER_URL}/command"
    logger.info("Sending automation command...")
    
    response = requests.post(url, json=command)
    if response.status_code != 200:
        logger.error(f"Failed to send command: {response.text}")
        sys.exit(1)
        
    data = response.json()
    requestId = data.get("requestId")
    logger.info(f"Command sent with Request ID: {requestId}")
    return requestId

def poll_for_answer(api_key: str, request_id: str, timeout: int = DEFAULT_POLL_TIMEOUT) -> dict:
    """
    Poll the REST API server for an answer corresponding to the given requestId.
    """
    url = f"{SERVER_URL}/command/{request_id}/answer"
    start_time = time.time()
    
    while time.time() - start_time < timeout:
        params = {"apiKey": api_key}
        response = requests.get(url, params=params)
        data = response.json()
        
        if data.get("success") and "answer" in data:
            logger.info("Received answer from server.")
            return data["answer"]
            
        logger.info("Answer not ready, polling again...")
        time.sleep(POLL_INTERVAL)
        
    logger.error("Timed out waiting for answer.")
    sys.exit(1)
