import base64
import io
from PIL import Image
import numpy as np
from ultralytics import YOLO
from config.config import MODEL_PATH

model = YOLO(MODEL_PATH)

def pred_img(image: str):
    # Decode base64 string to bytes
    image_bytes = base64.b64decode(image)
    
    # Convert bytes to image
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    image_np = np.array(image)

    # Run YOLO inference
    class_counts = {}
    results = model(image_np)

    for result in results:
        class_ids = result.boxes.cls.tolist()
        for class_id in class_ids:
            class_name = model.names[int(class_id)]
            class_counts[class_name] = class_counts.get(class_name, 0) + 1

    return class_counts
