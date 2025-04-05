# Template Base Scraper for Projects (Python/Selenium)

Reusable & Robust, designed for dynamic websites that may require browser interaction or JavaScript execution. Can handle common setup tasks, configuration management, browser automation, basic error handling, and data output, allowing you to focus primarily on the site-specific data extraction logic.

Built with Selenium, BeautifulSoup, and Typer.

## Tech Stack

* **Selenium & WebDriver Manager:** For automating browser interaction and handling dynamic content loaded via JavaScript.
* **BeautifulSoup4:** For parsing the HTML structure retrieved by Selenium.
* **Typer:** For creating a clean command-line interface (CLI).
* **python-dotenv:** For managing configuration (like target URLs and settings) via a `.env` file.
* **Built-in `csv` module:** For saving extracted data into timestamped CSV files.
* **Built-in `logging` module:** For informative console output during scraping.

An example implementation is included that scrapes quotes and authors from [http://quotes.toscrape.com/scroll](http://quotes.toscrape.com/scroll).

## Features

* Modular structure separating setup, scraping logic, and CLI.
* Handles Selenium WebDriver setup automatically using `webdriver-manager`.
* Configurable via `.env` file and CLI options (CLI overrides `.env`).
* Example `extract_data` and `handle_data` implementation provided (`quotes.toscrape.com/scroll`).
* Timestamped CSV file output (`outputfile_[YYYYMMDD_HHMMSS].csv`).
* Basic logging configured.
* Designed to be easily copied and adapted for new target websites.

## Setup & Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/noanchovies/scraper-engine.git](https://github.com/noanchovies/scraper-engine.git)
    cd scraper-engine
    ```
    *(Or download and extract the ZIP)*

2.  **Create a Virtual Environment:** (Recommended)
    ```bash
    python -m venv venv
    ```

3.  **Activate the Virtual Environment:**
    * Windows (PowerShell): `.\venv\Scripts\Activate.ps1`
    * Windows (Cmd Prompt): `.\venv\Scripts\activate.bat`
    * macOS/Linux (Bash/Zsh): `source venv/bin/activate`

4.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Configuration

Configuration is managed via a `.env` file in the project root.

1.  **Create `.env` file:** Copy the example file:
    ```bash
    # On Linux/macOS/Git Bash
    cp .env.example .env
    # On Windows Cmd/PowerShell
    copy .env.example .env
    ```
    *(Or just manually copy the file)*

2.  **Edit `.env`:** Open the `.env` file and modify the variables as needed for your target website:
    * `BASE_URL`: The starting URL of the website you want to scrape.
    * `OUTPUT_FILENAME`: The base name for the output CSV file (e.g., `my_scraped_data.csv`). A timestamp will be appended automatically.
    * `HEADLESS`: Set to `True` to run the browser without a visible window (recommended for automation/servers) or `False` to watch the browser operate.
    * `DEFAULT_WAIT_TIME`: Time (in seconds) the scraper should wait after the initial page load for dynamic content to potentially render before extracting data. Adjust based on the target site's speed and complexity.
    * `LOG_LEVEL`: (Optional) Set logging level (e.g., `DEBUG`, `INFO`, `WARNING`). Defaults to `INFO`.

## Running the Example

To run the pre-configured example which scrapes `http://quotes.toscrape.com/scroll`:

1.  Make sure your virtual environment is activated.
2.  Ensure you have a `.env` file (copying `.env.example` is sufficient for the example).
3.  Run the CLI command from the project root directory:
    ```bash
    python -m src.basescraper.cli
    ```
    *(Note: The package name is currently `src.basescraper`. If you rename the `basescraper` folder inside `src`, update this command accordingly.)*

This will launch the scraper (using default settings from `.env` or `config.py` if `.env` isn't set up), extract quotes and authors, and save them to a file named `scraped_data_[timestamp].csv` (or whatever `OUTPUT_FILENAME` is set to).

## Adapting for a New Project

This is the core process for using the template:

1.  **Copy or Clone:** Start with a fresh copy of this template project for your new target website.
2.  **Configure:** Create and configure your `.env` file with the target URL, output filename, etc.
3.  **Inspect Target Site:** Use your browser's Developer Tools (Right-click -> Inspect Element) on your *target website* to understand its HTML structure and find the CSS selectors for the data you want.
4.  **Modify `src/basescraper/scraper.py`:** This is where you'll spend most of your time.
    * **`extract_data(page_source)` function:**
        * **Delete the example logic/selectors** inside this function.
        * Use `BeautifulSoup` (the `soup` object) with methods like `soup.select(...)` or `soup.find_all(...)` using the **CSS selectors you found for your target site** to locate the elements containing your desired data (e.g., product containers, titles, prices, links).
        * Loop through the found elements (if necessary).
        * Extract the text, attributes (`href`, `src`), etc.
        * Clean the extracted data as needed.
        * Store the data for each item in a dictionary (e.g., `{'product_name': '...', 'price': '...'}`).
        * Append each dictionary to the `extracted_items` list.
        * Return the `extracted_items` list.
    * **`handle_data(data, output_file)` function:**
        * Locate the `fieldnames = [...]` list within this function.
        * **Update this list** so that the strings inside it exactly match the **keys** you used in the dictionaries created by *your* modified `extract_data` function. This ensures the CSV headers are correct.
5.  **Test:** Run `python -m src.basescraper.cli` and check the output CSV file and logs. Debug `extract_data` (usually selector issues) as needed.

*Note: The functions `setup_driver`, `Maps_to_url`, and `run_scraper` in `scraper.py`, as well as `config.py` and `cli.py`, generally do not need to be modified for basic adaptation.*

## Project Structure (Brief)

├── .env.example         # Example environment variables
├── .gitignore           # Files for Git to ignore
├── README.md            # This file
├── requirements.txt     # Python dependencies
└── src
└── basescraper      # Main scraper package (rename if desired)
├── init.py
├── cli.py       # Typer CLI interface
├── config.py    # Configuration loading (.env + defaults)
└── scraper.py   # Core scraping logic (MODIFY extract_data/handle_data HERE)

## Next Steps:

Save this content in your README.md file in the scraper-engine project.
Review it quickly to make sure it makes sense to you.
Proceed to Step 5: Commit these changes and push your new template to GitHub!


## Template Evolution: Challenges & Solutions

This template has evolved from practical application and incorporates solutions to common challenges encountered when integrating configuration, CLI arguments, and the core scraping logic. Understanding these might be helpful when adapting or debugging:

* **Challenge:** Passing configuration (URL, output file, settings) consistently from command-line arguments, `.env` files, and default values into the core scraper.
    * **Solution:**
        * Implemented robust fallback logic in `src/basescraper/cli.py`. It prioritizes CLI arguments (e.g., `--url`), then looks for values loaded from the `.env` file (via `config.py`), and finally uses hardcoded defaults in `config.py` if neither is present.
        * Standardized parameter names (like `target_url`, `output_file`) across the function calls between `cli.py` and `scraper.py` (`run_scraper`, `handle_data`) to avoid `TypeError` exceptions.
        * Ensured `src/basescraper/config.py` reliably loads the `.env` file using `python-dotenv` and defines expected variables (`BASE_URL`, `OUTPUT_FILENAME`, etc.) using `os.getenv("VAR", default_value)`. Diagnosed initial `.env` loading failures by checking file paths and existence within `config.py`.
    * **Files/Tools Involved:** `cli.py`, `config.py`, `scraper.py`, `.env`, `python-dotenv`, `typer`.

* **Challenge:** Ensuring correct Python module execution context and dependency management.
    * **Solution:** Confirmed that `python -m src.basescraper.cli` must be run from the **project root directory** (the folder containing the `src` directory), not from within `src` itself, to avoid `ModuleNotFoundError: No module named 'src'`. Emphasized activating the correct project-specific virtual environment (`venv`) and running `pip install -r requirements.txt` within that active environment for *each new project copy* to resolve `ModuleNotFoundError` for libraries like `typer`.
    * **Files/Tools Involved:** Terminal/Shell structure, `venv`, `pip`, `requirements.txt`.

* **Challenge:** Handling script exit codes and avoiding misleading error messages on successful runs.
    * **Solution:** Refined the `try...except` structure within the main `run` function in `cli.py`. The block now specifically catches errors *during* the `scraper.run_scraper()` execution. The final success/failure check (`if success:`) and the corresponding `typer.Exit(code=...)` calls are placed *outside* this main exception block. This prevents the intentional `typer.Exit(code=0)` on success from being caught by a general `except Exception:` block, which previously caused confusing "Unhandled exception" logs despite successful completion.
    * **Files/Tools Involved:** `cli.py`, `typer`, `try...except`, `logging`.

* **Challenge:** Proper Git setup for templates, ignoring sensitive/generated files, and resetting history.
    * **Solution:** Created a comprehensive `.gitignore` file to exclude `venv`, `.env`, `*.csv`, `*.log`, `__pycache__`, etc. Demonstrated resetting Git history for a template by deleting the existing `.git` folder (using `Remove-Item -Recurse -Force` in PowerShell or `rm -rf .git` in bash/zsh, *after* copying the project) and re-initializing with `git init`. Addressed differences between PowerShell and `cmd.exe` syntax.
    * **Files/Tools Involved:** `.gitignore`, `git`, PowerShell/Terminal.

This refined structure aims to provide a more stable and predictable foundation for new scraping projects based on this template.
