import psycopg2

def test_db_connection():
    conn = psycopg2.connect("dbname=telegram_warehouse user=postgres password=postgres host=localhost port=5433")
    cur = conn.cursor()
    cur.execute("SELECT 1")
    assert cur.fetchone()[0] == 1
    cur.close()
    conn.close()