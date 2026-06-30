"""
Dagster pipeline definition for the Telegram Medical Data Warehouse.
Explicitly chains scraping, loading, dbt transformations, and YOLO enrichment,
and includes a daily schedule.
"""

from dagster import job, op, ScheduleDefinition


@op
def scrape_telegram_data():
    """Extract messages and images from Telegram channels."""
    import subprocess
    try:
        subprocess.run(["python", "src/scraper.py"], check=True)
    except subprocess.CalledProcessError as e:
        raise Exception(f"Scraping failed: {e}")


@op
def load_raw_to_postgres():
    """Load JSONL data from the data lake into PostgreSQL."""
    import subprocess
    try:
        subprocess.run(["python", "scripts/load_raw.py"], check=True)
    except subprocess.CalledProcessError as e:
        raise Exception(f"Loading raw data failed: {e}")


@op
def run_dbt_transformations():
    """Execute dbt models to build the star schema."""
    import subprocess
    try:
        subprocess.run(["dbt", "run"], cwd="medical_warehouse", check=True)
    except subprocess.CalledProcessError as e:
        raise Exception(f"dbt run failed: {e}")


@op
def load_yolo_results():
    """Load YOLO object detection results into PostgreSQL."""
    import subprocess
    try:
        subprocess.run(["python", "scripts/load_yolo.py"], check=True)
    except subprocess.CalledProcessError as e:
        raise Exception(f"Loading YOLO results failed: {e}")


@job
def telegram_pipeline():
    """Complete ELT pipeline: scrape → load raw → dbt → YOLO enrichment."""
    raw = scrape_telegram_data()
    loaded = load_raw_to_postgres(raw)          # scrape must finish first
    dbt_done = run_dbt_transformations(loaded)  # load must finish first
    load_yolo_results(dbt_done)                 # dbt must finish first


# Daily schedule – runs every morning at 6:00 AM
daily_schedule = ScheduleDefinition(
    job=telegram_pipeline,
    cron_schedule="0 6 * * *",
)