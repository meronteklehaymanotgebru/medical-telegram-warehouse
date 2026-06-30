from dagster import job, op

@op
def scrape_telegram_data():
    import subprocess
    subprocess.run(["python", "src/scraper.py"], check=True)

@op
def load_raw_to_postgres():
    import subprocess
    subprocess.run(["python", "scripts/load_raw.py"], check=True)

@op
def run_dbt_transformations():
    import subprocess
    subprocess.run(["dbt", "run"], cwd="medical_warehouse", check=True)

@op
def load_yolo_results():
    import subprocess
    subprocess.run(["python", "scripts/load_yolo.py"], check=True)

@job
def telegram_pipeline():
    run_dbt_transformations()
    load_yolo_results()