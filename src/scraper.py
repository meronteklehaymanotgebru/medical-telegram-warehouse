import os, json, logging, asyncio
from datetime import datetime
from telethon import TelegramClient
from dotenv import load_dotenv

load_dotenv()

API_ID = os.getenv("TELEGRAM_API_ID")
API_HASH = os.getenv("TELEGRAM_API_HASH")

CHANNELS = [
    "CheMed",
    "LobeliaCosmetics",
    "TikvahPharma",
    "Lobelia_Pharmacy",          
    "RayaPharmaceutical",
    "PharmaMedEthiopia",
]

OUTPUT_DIR = "data/raw/telegram_messages"
IMAGE_DIR = "data/raw/images"
LOG_FILE = "logs/scraper.log"

logging.basicConfig(level=logging.INFO, filename=LOG_FILE, format="%(asctime)s %(message)s")

async def main():
    client = TelegramClient("session", API_ID, API_HASH)
    await client.start()

    for channel in CHANNELS:
        logging.info(f"Scraping {channel}")
        try:
            entity = await client.get_entity(channel)
            messages = await client.get_messages(entity, limit=100)  # increase later

            for msg in messages:
                if msg.message or msg.media:
                    date_str = msg.date.strftime("%Y-%m-%d")
                    out_path = os.path.join(OUTPUT_DIR, date_str)
                    os.makedirs(out_path, exist_ok=True)

                    data = {
                        "message_id": msg.id,
                        "channel_name": channel,
                        "date": msg.date.isoformat(),
                        "text": msg.message or "",
                        "has_media": msg.media is not None,
                        "views": msg.views or 0,
                        "forwards": msg.forwards or 0,
                    }

                    fname = os.path.join(out_path, f"{channel}.jsonl")
                    with open(fname, "a") as f:
                        f.write(json.dumps(data) + "\n")

                    if msg.photo:
                        img_dir = os.path.join(IMAGE_DIR, channel)
                        os.makedirs(img_dir, exist_ok=True)
                        img_path = os.path.join(img_dir, f"{msg.id}.jpg")
                        await msg.download_media(file=img_path)
                        data["image_path"] = img_path

        except Exception as e:
            logging.error(f"Error in {channel}: {e}")

    await client.disconnect()

if __name__ == "__main__":
    asyncio.run(main())