import os, csv
from ultralytics import YOLO

# Load YOLOv8 nano model
model = YOLO("yolov8n.pt")

IMAGE_DIR = "data/raw/images"
RESULTS_DIR = "data/processed"
os.makedirs(RESULTS_DIR, exist_ok=True)

results_file = os.path.join(RESULTS_DIR, "yolo_results.csv")

with open(results_file, "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["message_id", "channel_name", "detected_class", "confidence", "image_category"])

    for channel in os.listdir(IMAGE_DIR):
        channel_path = os.path.join(IMAGE_DIR, channel)
        if not os.path.isdir(channel_path):
            continue
        for img_name in os.listdir(channel_path):
            if not img_name.endswith(".jpg"):
                continue
            message_id = img_name.replace(".jpg", "")
            img_path = os.path.join(channel_path, img_name)

            # Run YOLO detection
            results = model(img_path, verbose=False)
            boxes = results[0].boxes
            if boxes is None:
                continue

            # Gather detected classes and confidences
            classes = []
            confs = []
            for box in boxes:
                cls = int(box.cls[0])
                conf = float(box.conf[0])
                classes.append(model.names[cls])
                confs.append(conf)

            # Classification scheme
            has_person = "person" in classes
            has_product = any(c in ["bottle", "cup", "bowl", "cell phone", "book", "laptop", "tvmonitor"] for c in classes)  # adjust as needed
            if has_person and has_product:
                category = "promotional"
            elif has_product:
                category = "product_display"
            elif has_person:
                category = "lifestyle"
            else:
                category = "other"

            # Write one row per detection (or aggregated per image)
            for cls, conf in zip(classes, confs):
                writer.writerow([message_id, channel, cls, conf, category])