"""Command-related functions for the server command client."""

from datetime import datetime, timezone
import os
import sys

# Add parent directory to path for direct script execution
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from .client import send_command
    from .logger import setup_logging
except ImportError:
    from server_command.client import send_command
    from server_command.logger import setup_logging

logger = setup_logging()

def send_html(api_key: str, html_content: str, request_id: str = None) -> str:
    """
    Send an HTML command to be displayed in the current browser tab.
    
    Args:
        api_key (str): The API key for authentication
        html_content (str): The HTML content to be sent and displayed
        request_id (str, optional): A custom request ID. If not provided, one will be generated.
    
    Returns:
        str: The request ID for tracking the command's status
    """
    command = {
        "action": "send-html",
        "html": html_content
    }
    
    if request_id:
        command["requestId"] = request_id
    
    return send_command(api_key, command)

def get_html(api_key: str, request_id: str = None) -> str:
    """
    Retrieve HTML content from the current active browser tab.
    
    Args:
        api_key (str): The API key for authentication
        request_id (str, optional): A custom request ID. If not provided, one will be generated.
    
    Returns:
        str: The request ID for tracking the command's status
    """
    command = {
        "action": "get-html"
    }
    
    if request_id:
        command["requestId"] = request_id
    
    return send_command(api_key, command)

def create_command(args) -> dict:
    """Create a command dictionary from command line arguments."""
    command = {
        "action": args.action,
        "timestamp": args.timestamp or datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    }
    
    if args.xpath:
        command["xpath"] = args.xpath
    if args.text:
        command["text"] = args.text
    if args.x is not None:
        command["x"] = args.x
    if args.y is not None:
        command["y"] = args.y
    if args.url:
        command["url"] = args.url
        
    return command
