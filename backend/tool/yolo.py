import cv2
import os
import shutil
from ultralytics import YOLO
from pathlib import Path
from config import YOLO_MODEL_PATH

model = YOLO(YOLO_MODEL_PATH)


def run_detection(image_path: str):
    # ==========================================
    # 1. MASK THE GPS AREA
    # ==========================================
    try:
        img = cv2.imread(image_path)
        if img is not None:
            h, w, _ = img.shape
            cv2.rectangle(img, (0, int(h * 0.6)), (w, h), (0, 0, 0), -1)

            base, ext = os.path.splitext(image_path)
            masked_path = f"{base}_masked{ext}"
            cv2.imwrite(masked_path, img)
        else:
            masked_path = image_path
    except Exception as e:
        print("Masking error:", e)
        masked_path = image_path

    # ==========================================
    # 2. RUN YOLO ON MASKED IMAGE
    # ==========================================
    # Removed conf threshold so we don't miss the 0.51 garbage!
    results = model(masked_path, save=True)
    r = results[0]
    detections = len(r.boxes)

    clean_image_path = str(image_path).replace("\\", "/")

    if detections == 0:
        return {
            "issue": None,
            "confidence": 0,
            "bbox": None,
            "area": 0,
            "detections": 0,
            "annotated_image": clean_image_path,
        }

    # ==========================================
    # 3. FIND HIGHEST CONFIDENCE
    # ==========================================
    best_idx, best_conf = 0, 0.0
    for i in range(detections):
        conf = float(r.boxes.conf[i])
        if conf > best_conf:
            best_conf, best_idx = conf, i

    cls_id = int(r.boxes.cls[best_idx])
    final_conf = float(r.boxes.conf[best_idx])
    bbox = r.boxes.xyxy[best_idx].tolist()
    class_name = model.names[cls_id]

    # ==========================================
    # 4. FIX FILENAMES FOR THE UI
    # ==========================================
    save_dir = Path(r.save_dir)
    yolo_output = save_dir / Path(masked_path).name
    annotated_path = save_dir / Path(image_path).name

    try:
        # shutil.move is much safer on Windows than .rename()
        if yolo_output.exists():
            shutil.move(str(yolo_output), str(annotated_path))
    except Exception as e:
        print("Rename error:", e)
        annotated_path = yolo_output  # Fallback to masked name if move fails

    # Force forward slashes so the web browser can render the image
    final_ui_path = str(annotated_path).replace("\\", "/")
    print("ANNOTATED PATH:", final_ui_path)

    return {
        "issue": class_name,
        "confidence": final_conf,
        "bbox": bbox,
        "area": (bbox[2] - bbox[0]) * (bbox[3] - bbox[1]),
        "detections": detections,
        "annotated_image": final_ui_path,
    }
