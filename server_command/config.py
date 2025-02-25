"""Configuration settings for the server command client."""

import os
import sys
import logging

# Server configuration
SERVER_URL = "http://localhost:8765"

# Timeouts
DEFAULT_POLL_TIMEOUT = 30
POLL_INTERVAL = 2

# API configuration
API_KEY = os.environ.get("API_KEY", "DEFAULT_SECRET")

# File patterns
SCREENSHOT_FILENAME_PATTERN = "screenshot-%Y%m%d-%H%M%S.png"
HTML_FILENAME_PATTERN = "page-%Y%m%d-%H%M%S.html"

# Error messages
ERROR_NO_API_KEY = "Error: API_KEY environment variable must be set."
