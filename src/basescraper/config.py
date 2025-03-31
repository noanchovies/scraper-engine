# src/basescraper/config.py (Cleaned, Generalized Template Version)
import os
from dotenv import load_dotenv
import logging
import sys

# Configure logging first (optional, but good practice)
# Get LOG_LEVEL from environment, default to INFO
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
logging.basicConfig(level=getattr(logging, LOG_LEVEL, logging.INFO),
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    force=True) # Use force=True if basicConfig might be called elsewhere

log = logging.getLogger(__name__) # Get logger instance

# Construct the path to the .env file
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
dotenv_path = os.path.join(project_root, '.env')

# Load environment variables from .env file
load_success = load_dotenv(dotenv_path=dotenv_path, override=True)

if load_success:
    log.debug(f".env file found at {dotenv_path} and loaded.")
else:
    log.debug(f".env file not found at {dotenv_path}, using environment vars or defaults.")

# --- Define configuration variables ---
# Default to the example site URL, can be overridden by .env or --url
BASE_URL = os.getenv("BASE_URL", "http://quotes.toscrape.com/scroll")
# Default to a generic output filename base
OUTPUT_FILENAME = os.getenv("OUTPUT_FILENAME", "scraped_data.csv")

# HEADLESS setting (same logic as before)
_headless_str = os.getenv("HEADLESS", "True")
HEADLESS = _headless_str.lower() in ('true', '1', 't', 'yes')

# DEFAULT_WAIT_TIME setting (same logic as before)
_wait_time_str = os.getenv("DEFAULT_WAIT_TIME", "10") # Increased default for potentially slower example site
try:
    DEFAULT_WAIT_TIME = int(_wait_time_str)
    if DEFAULT_WAIT_TIME < 0:
        log.warning(f"DEFAULT_WAIT_TIME cannot be negative ('{_wait_time_str}'), using default 10.")
        DEFAULT_WAIT_TIME = 10
except (ValueError, TypeError):
    log.warning(f"Invalid DEFAULT_WAIT_TIME env var ('{_wait_time_str}'), using default 10.")
    DEFAULT_WAIT_TIME = 10

# Log loaded config values at DEBUG level
log.debug(f"Config loaded: BASE_URL={BASE_URL}")
log.debug(f"Config loaded: OUTPUT_FILENAME={OUTPUT_FILENAME}")
log.debug(f"Config loaded: HEADLESS={HEADLESS}")
log.debug(f"Config loaded: DEFAULT_WAIT_TIME={DEFAULT_WAIT_TIME}")