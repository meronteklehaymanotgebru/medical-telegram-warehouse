import os, json, psycopg2

conn = psycopg2.connect("dbname=telegram_warehouse user=postgres password=postgres host=localhost port=5433")
cur = conn.cursor()

cur.execute("CREATE SCHEMA IF NOT EXISTS raw;")
cur.execute("""
CREATE TABLE IF NOT EXISTS raw.telegram_messages (
    message_id BIGINT,
    channel_name TEXT,
    date TIMESTAMP,
    text TEXT,
    has_media BOOLEAN,
    views INT,
    forwards INT,
    image_path TEXT
);
""")

for root, dirs, files in os.walk("data/raw/telegram_messages"):
    for f in files:
        if f.endswith(".jsonl"):
            with open(os.path.join(root, f)) as fh:
                for line in fh:
                    data = json.loads(line)
                    cur.execute("""
                        INSERT INTO raw.telegram_messages VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
                    """, (data['message_id'], data['channel_name'], data['date'],
                          data['text'], data['has_media'], data['views'],
                          data['forwards'], data.get('image_path')))
conn.commit()
cur.close()
conn.close()
print("Data loaded successfully.")