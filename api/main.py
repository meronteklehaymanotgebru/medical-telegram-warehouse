from fastapi import FastAPI, Query
from sqlalchemy import text
from api.database import SessionLocal
from api.schemas import TopProduct, ChannelActivity, MessageResult, VisualStats
from typing import List

app = FastAPI(title="Medical Telegram Warehouse API")

@app.get("/api/reports/top-products", response_model=List[TopProduct])
def top_products(limit: int = Query(10, ge=1, le=100)):
    db = SessionLocal()
    try:
        result = db.execute(text("""
            SELECT word, COUNT(*) as cnt FROM (
                SELECT regexp_split_to_table(LOWER(message_text), '\\s+') as word
                FROM raw.fct_messages
                WHERE message_text IS NOT NULL
            ) t
            WHERE length(word) > 2 AND word NOT IN ('the','and','for','that','with','this','have','from')
            GROUP BY word
            ORDER BY cnt DESC
            LIMIT :limit
        """), {"limit": limit})
        return [{"term": row[0], "count": row[1]} for row in result]
    finally:
        db.close()

@app.get("/api/channels/{channel_name}/activity", response_model=List[ChannelActivity])
def channel_activity(channel_name: str):
    db = SessionLocal()
    try:
        result = db.execute(text("""
            SELECT d.full_date, COUNT(*) as posts, AVG(f.views) as avg_views
            FROM raw.fct_messages f
            JOIN raw.dim_dates d ON f.date_key = d.date_key
            JOIN raw.dim_channels c ON f.channel_key = c.channel_key
            WHERE c.channel_name = :ch
            GROUP BY d.full_date
            ORDER BY d.full_date
        """), {"ch": channel_name})
        return [{"date": str(row[0]), "posts": row[1], "avg_views": float(row[2])} for row in result]
    finally:
        db.close()

@app.get("/api/search/messages", response_model=List[MessageResult])
def search_messages(query: str, limit: int = Query(20, ge=1, le=100)):
    db = SessionLocal()
    try:
        result = db.execute(text("""
            SELECT f.message_id, f.message_text, c.channel_name, d.full_date
            FROM raw.fct_messages f
            JOIN raw.dim_channels c ON f.channel_key = c.channel_key
            JOIN raw.dim_dates d ON f.date_key = d.date_key
            WHERE f.message_text ILIKE :q
            LIMIT :lim
        """), {"q": f"%{query}%", "lim": limit})
        return [{"message_id": row[0], "text": row[1][:200], "channel": row[2], "date": str(row[3])} for row in result]
    finally:
        db.close()

@app.get("/api/reports/visual-content", response_model=List[VisualStats])
def visual_content():
    db = SessionLocal()
    try:
        result = db.execute(text("""
            SELECT c.channel_name,
                   COUNT(*) as total,
                   SUM(CASE WHEN f.has_media THEN 1 ELSE 0 END) as img_posts,
                   ROUND(100.0 * SUM(CASE WHEN f.has_media THEN 1 ELSE 0 END) / COUNT(*), 1) as pct
            FROM raw.fct_messages f
            JOIN raw.dim_channels c ON f.channel_key = c.channel_key
            GROUP BY c.channel_name
            ORDER BY pct DESC
        """))
        return [{"channel_name": row[0], "total_posts": row[1], "image_posts": row[2], "image_percentage": row[3]} for row in result]
    finally:
        db.close()