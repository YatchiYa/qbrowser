"""Response handlers for the server command client."""

import base64
from datetime import datetime
import sys
import os

# Add parent directory to path for direct script execution
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from .logger import setup_logging
    from .config import SCREENSHOT_FILENAME_PATTERN, HTML_FILENAME_PATTERN
except ImportError:
    from server_command.logger import setup_logging
    from server_command.config import SCREENSHOT_FILENAME_PATTERN, HTML_FILENAME_PATTERN

logger = setup_logging()

def save_screenshot(data: str) -> str:
    """
    Decode a base64-encoded screenshot (with a data URI prefix)
    and save it to a PNG file.
    """
    if isinstance(data, dict) and "data" in data:
        data = data["data"]
    if isinstance(data, str) and data.startswith("data:image/png;base64,"):
        data = data.split(",", 1)[1]
    else:
        raise ValueError("Invalid screenshot data format")
    
    filename = datetime.now().strftime(SCREENSHOT_FILENAME_PATTERN)
    with open(filename, "wb") as f:
        f.write(base64.b64decode(data))
    return filename

def handle_response(response: dict) -> None:
    """
    Unwrap and display the final response.
    If a screenshot is provided, save it.
    """
    print("\nCommand Response:")
    print(f"Status: {response.get('success', False)}")
    print(f"Action: {response.get('action', 'unknown')}")
    print(f"Timestamp: {response.get('timestamp')}")
    
    if error := response.get("error"):
        print("\nError:")
        print(error)
        sys.exit(1)
        
    if response.get("action") == "get-html":
        print(f"URL: {response.get('url', 'N/A')}")
        print("HTML Content:")
        print(response.get('html', 'No HTML content retrieved'))
        return
        
    if html := response.get("html"):
        snippet = "\n".join(html.splitlines()[:50])
        print("\nHTML Content (first 50 lines):")
        print(snippet)
        filename = datetime.now().strftime(HTML_FILENAME_PATTERN)
        with open(filename, "w") as f:
            f.write(html)
        print(f"Full HTML saved to {filename}")
        
    if screenshot := response.get("screenshot"):
        try:
            filename = save_screenshot(screenshot)
            print(f"\nScreenshot saved as: {filename}")
        except Exception as e:
            print(f"\nError saving screenshot: {e}")
            
    if message := response.get("message"):
        print("\nMessage:")
        print(message)
