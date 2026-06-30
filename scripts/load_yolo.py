import csv, psycopg2

conn = psycopg2.connect("dbname=telegram_warehouse user=postgres password=postgres host=localhost port=5433")
cur = conn.cursor()
cur.execute("""
CREATE TABLE IF NOT EXISTS raw.yolo_results (
    message_id BIGINT,
    channel_name TEXT,
    detected_class TEXT,
    confidence FLOAT,
    image_category TEXT
);
""")
with open("data/processed/yolo_results.csv") as f:
    reader = csv.reader(f)
    next(reader)  # skip header
    for row in reader:
        cur.execute("INSERT INTO raw.yolo_results VALUES (%s,%s,%s,%s,%s)", row)
conn.commit()
cur.close()
conn.close()