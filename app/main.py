from fastapi import FastAPI, File, UploadFile
from fastapi.staticfiles import StaticFiles
from PIL import Image, ImageDraw
import io
import uuid
from pathlib import Path
from app.inference import run_inference

app = FastAPI()

# Mount static directory for serving images
app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.post("/detect/")
async def detect(file: UploadFile = File(...)):
    # Load the uploaded image
    image = Image.open(io.BytesIO(await file.read())).convert("RGB")

    # Run inference using ONNX model
    detections = run_inference(image)

    # Draw bounding boxes on the image
    draw = ImageDraw.Draw(image)
    for detection in detections:
        x1, y1, x2, y2 = detection["x1"], detection["y1"], detection["x2"], detection["y2"]
        confidence, class_id = detection["confidence"], detection["class"]

        # Draw bounding box
        draw.rectangle([x1, y1, x2, y2], outline="red", width=3)
        # Add class label and confidence score
        draw.text((x1, y1 - 10), f"Class {class_id}: {confidence:.2f}", fill="red")

    # Save the image with a unique filename
    output_dir = Path("app/static/output")
    output_dir.mkdir(parents=True, exist_ok=True)
    unique_filename = f"{uuid.uuid4().hex}.jpg"
    output_image_path = output_dir / unique_filename
    image.save(output_image_path)

    # Return JSON response with detections and image URL
    return {
        "detections": detections,
        "image_url": f"/static/output/{unique_filename}"
    }
