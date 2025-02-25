#!/usr/bin/env python3
"""
Command-line interface for the server command client.

A command-line client to send browser automation commands via a REST API
and poll for the answer by request-id if needed.

Usage as an automation command:
    ./cli.py --action screenshot [--xpath XPATH] [--text TEXT] [--url URL]

Usage as a query (retrieve a stored answer):
    ./cli.py --query <requestId>

Make sure the API_KEY environment variable is set.
"""

import argparse
import sys
import os

# Add parent directory to path for direct script execution
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    # Try relative import first (when run as module)
    from .config import API_KEY, ERROR_NO_API_KEY
    from .client import send_command, poll_for_answer
    from .commands import send_html, get_html, create_command
    from .handlers import handle_response
    from .logger import setup_logging
except ImportError:
    # Fall back to absolute import (when run as script)
    from server_command.config import API_KEY, ERROR_NO_API_KEY
    from server_command.client import send_command, poll_for_answer
    from server_command.commands import send_html, get_html, create_command
    from server_command.handlers import handle_response
    from server_command.logger import setup_logging

logger = setup_logging()

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Send browser automation commands via a REST API."
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--action", help="Command action (e.g. screenshot, click, etc.)")
    group.add_argument("--query", help="Query a response using a request-id")
    group.add_argument("--html", type=str, help="HTML content to send to the browser")
    group.add_argument("--get-html", action='store_true', help='Get HTML content from the current tab')
    
    parser.add_argument("--xpath", help="XPath selector for an element")
    parser.add_argument("--text", help="Text to type into an element")
    parser.add_argument("--x", type=float, help="X coordinate for a click")
    parser.add_argument("--y", type=float, help="Y coordinate for a click")
    parser.add_argument("--url", help="URL to navigate to")
    parser.add_argument("--timestamp", help="Optional ISO timestamp")
    
    return parser.parse_args()

def main():
    """Main entry point for the command-line interface."""
    args = parse_args()
    
    if not API_KEY:
        logger.error(ERROR_NO_API_KEY)
        sys.exit(1)
    
    if args.query:
        # Poll for answer directly using the provided request id
        answer = poll_for_answer(API_KEY, args.query)
        handle_response(answer)
    elif args.get_html:
        request_id = get_html(API_KEY)
        logger.info(f"Sent get-html command. Request ID: {request_id}")
        
        response = poll_for_answer(API_KEY, request_id)
        handle_response(response)
    elif args.html:
        request_id = send_html(API_KEY, args.html)
        logger.info(f"Sent HTML command. Request ID: {request_id}")
        
        response = poll_for_answer(API_KEY, request_id)
        handle_response(response)
    else:
        command = create_command(args)
        request_id = send_command(API_KEY, command)
        logger.info("Polling for answer...")
        answer = poll_for_answer(API_KEY, request_id)
        handle_response(answer)

if __name__ == "__main__":
    main()
