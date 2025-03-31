# src/basescraper/cli.py (Corrected Structure)

import typer
from rich.console import Console
import logging
import sys
import os

# Import the main scraper function and config
try:
    from basescraper import scraper, config
except ImportError:
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)
    try:
        from src.basescraper import scraper, config
    except ImportError as e:
        print(f"Fatal Error: Could not import scraper or config. Path: {sys.path}, Error: {e}")
        sys.exit(1)

# --- Typer App Initialization ---
app = typer.Typer(help="A generic base scraper framework using Selenium.")
console = Console()

# Configure root logger (basic config happens in config.py now)
# We can still use logging here if needed
log = logging.getLogger(__name__) # Get logger instance

# --- CLI Command ---
@app.command()
def run(
    target_url_cli: str = typer.Option(None, "--url", "-u", help="Target URL to scrape. Overrides config/env.", show_default=False),
    output_file_cli: str = typer.Option(None, "--output", "-o", help="Output target (e.g., filename). Overrides config/env.", show_default=False),
    headless_cli: bool = typer.Option(None, "--headless/--no-headless", help="Run browser headless (or not). Overrides config/env.", show_default=False),
    wait_time_cli: int = typer.Option(None, "--wait", "-w", help="Wait time after page load (secs). Overrides config/env.", show_default=False)
):
    """
    Runs the Tink.de landing page scraper.
    Uses values from .env/config.py by default, but can be overridden by CLI options.
    """
    console.print(f"[bold green]Starting base scraper framework via CLI...[/bold green]")
    log.info("Resolving configuration settings...")

    # --- Resolve configuration: Prioritize CLI > Env/Config Defaults ---
    resolved_url = target_url_cli if target_url_cli is not None else config.BASE_URL
    resolved_output = output_file_cli if output_file_cli is not None else config.OUTPUT_FILENAME
    resolved_headless = headless_cli if headless_cli is not None else config.HEADLESS
    resolved_wait_time = wait_time_cli if wait_time_cli is not None else config.DEFAULT_WAIT_TIME

    log.info(f"  Target URL: {resolved_url}")
    log.info(f"  Output File Base: {resolved_output}")
    log.info(f"  Headless Mode: {resolved_headless}")
    log.info(f"  Wait Time: {resolved_wait_time}")

    # --- Validate essential parameters ---
    if not resolved_url or not isinstance(resolved_url, str):
        console.print(f"[bold red]Error:[/bold red] Target URL is missing or invalid ({resolved_url}). Provide via --url or set BASE_URL in .env/config.py.")
        log.error(f"Resolved URL is invalid: {resolved_url}")
        raise typer.Exit(code=1)
    if not resolved_output:
        console.print("[bold red]Error:[/bold red] Output filename is missing. Provide via --output or set OUTPUT_FILENAME in .env/config.py.")
        log.error(f"Resolved output filename is missing: {resolved_output}")
        raise typer.Exit(code=1)
    if not isinstance(resolved_wait_time, int) or resolved_wait_time < 0:
         log.warning(f"Invalid wait time ({resolved_wait_time}), using default 5.")
         resolved_wait_time = 5

    # --- Execute Scraper ---
    success = False # Default to False
    try:
        # ONLY the potentially failing scraper call is inside this try block
        success = scraper.run_scraper(
            target_url=resolved_url,
            output_file=resolved_output,
            headless=resolved_headless,
            wait_time=resolved_wait_time
        )
    except NotImplementedError as e:
        # Handle specific known error from base template design
        console.print(f"[bold red]Execution Failed:[/bold red] {e}")
        console.print("Ensure 'extract_data' and 'handle_data' are implemented in scraper.py.")
        log.error(f"NotImplementedError encountered: {e}", exc_info=True)
        raise typer.Exit(code=2) # Exit immediately for this specific setup error
    except Exception as e:
        # Catch *unexpected* errors ONLY during scraping execution
        console.print(f"[bold red]CLI Error: An unexpected exception occurred during scraping.[/bold red]")
        # Log the full traceback for debugging
        log.exception("Unhandled exception during scraper execution")
        # success remains False, flow continues to final exit logic below

    # --- Handle final exit status ---
    # This logic is now OUTSIDE the main try...except Exception block
    if success:
        console.print(f"[bold green]Framework finished successfully.[/bold green]")
        raise typer.Exit(code=0) # Exit cleanly with success code 0
    else:
        # This handles both explicit failure (run_scraper returned False)
        # and unexpected exceptions caught above (where success remains False)
        console.print(f"[bold yellow]Framework finished, but issues occurred (check logs or errors above).[/bold yellow]")
        raise typer.Exit(code=1) # Exit with failure code 1

# --- Entry point for CLI ---
if __name__ == "__main__":
    app()