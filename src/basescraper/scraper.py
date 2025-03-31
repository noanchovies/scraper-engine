# src/basescraper/scraper.py (Generalized Template Version)
# -*- coding: utf-8 -*-

import logging
import time
import re # Keep re in case needed for future cleaning
import csv
from datetime import datetime
import os

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

try:
    from . import config
except ImportError:
    import config

log = logging.getLogger(__name__) # Use module-level logger

# --- Selenium Setup Function (Keep as is) ---
def setup_driver(headless=True):
    log.info(f"Setting up WebDriver (Headless: {headless})...")
    options = webdriver.ChromeOptions()
    if headless: options.add_argument("--headless")
    options.add_argument("--disable-gpu"); options.add_argument("--window-size=1920,1080")
    options.add_argument("--no-sandbox"); options.add_argument("--disable-dev-shm-usage")
    try:
        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        log.info("WebDriver setup successful.")
        return driver
    except Exception as e:
        log.error(f"Error setting up WebDriver: {e}", exc_info=True); raise

# --- Navigation Function (Keep as is, but maybe improve wait) ---
def navigate_to_url(driver, url, wait_time=config.DEFAULT_WAIT_TIME):
    log.info(f"Navigating to URL: {url}")
    try:
        driver.get(url)
        # Example: Wait for the first quote element to be present for the example site
        # WebDriverWait(driver, wait_time).until(
        #     EC.presence_of_element_located((By.CSS_SELECTOR, "div.quote"))
        # )
        # Using a simple time.sleep might be okay for the template, or keep body wait
        WebDriverWait(driver, wait_time).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        log.info(f"Page loaded. Waiting {wait_time} seconds for dynamic content (if any)...")
        time.sleep(wait_time) # Allow time for initial JS load/scroll effects
        log.info("Initial wait complete. Proceeding.")
        return driver.page_source
    except Exception as e:
        log.error(f"Error navigating to {url} or waiting: {e}", exc_info=True); raise


# --- Data Extraction Function (EXAMPLE for quotes.toscrape.com/scroll) --- NEW ---
def extract_data(page_source: str) -> list[dict]:
    """
    EXAMPLE IMPLEMENTATION: Parses HTML of quotes.toscrape.com/scroll.
    REPLACE THIS LOGIC with selectors and parsing for your specific target website.

    Args:
        page_source (str): The HTML content of the page.

    Returns:
        A list of dictionaries, where each dictionary represents a scraped item.
        Example: [{'quote': 'The world as we have created it is a process of our thinking...', 'author': 'Albert Einstein'}]
    """
    log.info("Attempting to extract data using EXAMPLE (quotes.toscrape.com) logic...")
    soup = BeautifulSoup(page_source, 'html.parser')
    extracted_items = []
    # Selector for the div containing each quote and author
    quote_divs = soup.select("div.quote")

    if not quote_divs:
        log.warning("No quote divs found using selector 'div.quote'. Example site structure may have changed or page didn't load correctly.")
        return []

    log.info(f"Found {len(quote_divs)} quote elements in current view.")

    for quote_div in quote_divs:
        item = {}
        # Selector for the quote text within the div
        text_element = quote_div.select_one("span.text")
        # Selector for the author name within the div
        author_element = quote_div.select_one("span small.author")

        # Clean text potentially removing fancy quotes if needed
        item['quote'] = text_element.text.strip().replace('“', '').replace('”', '') if text_element else None
        item['author'] = author_element.text.strip() if author_element else None

        # Only add item if essential data was found
        if item['quote'] and item['author']:
            extracted_items.append(item)
        else:
             log.debug(f"Skipping quote div, missing text or author: {quote_div.text[:100].strip()}")

    log.info(f"Successfully extracted data for {len(extracted_items)} quotes using EXAMPLE logic.")
    return extracted_items

# --- Data Handling Function (EXAMPLE for quotes data) --- NEW ---
def handle_data(data: list[dict], output_file: str):
    """
    EXAMPLE IMPLEMENTATION: Handles the extracted quote data, saving to timestamped CSV.
    Adapts fieldnames based on the example extraction ('quote', 'author').
    MODIFY THIS if your extract_data function returns different dictionary keys.

    Args:
        data: A list of dictionaries from extract_data.
        output_file: The base path/filename for the output CSV file.
    """
    if not data:
        log.warning("No data extracted, skipping CSV file writing.")
        return

    # Fieldnames specific to the quotes example
    # IMPORTANT: Change this list to match the keys in the dictionaries returned by YOUR extract_data
    fieldnames = ['quote', 'author']

    # --- Timestamped filename logic (Keep as is) ---
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    base_name, extension = os.path.splitext(output_file)
    if not extension: extension = ".csv"
    final_filename = f"{base_name}_{timestamp}{extension}"
    log.info(f"Preparing to save data to: {final_filename}")

    # --- Write data to CSV (Keep as is, uses fieldnames list) ---
    try:
        output_dir = os.path.dirname(final_filename)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir); log.info(f"Created output directory: {output_dir}")

        with open(final_filename, 'w', newline='', encoding='utf-8') as csvfile:
            # Use extrasaction='ignore' to prevent errors if data dict has extra keys
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, extrasaction='ignore')
            # Check if fieldnames are actually in the first data item (optional robustness)
            if data and not all(key in data[0] for key in fieldnames):
                 log.warning(f"Mismatch between defined fieldnames {fieldnames} and keys in extracted data {list(data[0].keys())}. Writing may be incomplete.")

            writer.writeheader()
            writer.writerows(data)
        log.info(f"Data successfully saved to {final_filename}")
    # More specific exception catching can be useful
    except IOError as e: log.error(f"Error writing data to {final_filename}: {e}", exc_info=True)
    except Exception as e: log.error(f"An unexpected error occurred during CSV writing: {e}", exc_info=True)


# --- Main Orchestration Function (Keep as is) ---
def run_scraper(target_url: str, output_file: str, headless: bool, wait_time: int):
    """
    Orchestrates the scraping process: setup, navigate, extract, handle data.
    This function is called by cli.py.
    # ... (rest of docstring) ...
    """
    log.info("Starting the scraping process via run_scraper...")
    driver = None; success = False
    try:
        driver = setup_driver(headless=headless)
        page_html = navigate_to_url(driver, target_url, wait_time)
        if page_html:
            extracted_info = extract_data(page_html) # Calls the EXAMPLE extract_data
            handle_data(extracted_info, output_file) # Calls the EXAMPLE handle_data
            log.info("Scraping process completed successfully.")
            success = True
        else: log.error("Failed to retrieve page HTML."); success = False
    except Exception as e: log.error(f"Scraping process failed: {e}", exc_info=True); success = False
    finally:
        if driver: driver.quit(); log.info("WebDriver closed.")
    return success