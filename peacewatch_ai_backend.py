from fastapi import FastAPI, File, UploadFile, Form, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from ultralytics import YOLO
import whisper
import os
import tempfile
from datetime import datetime
import logging
from openai import OpenAI
import uuid
import cv2

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="public")

# Load models
vision_model = YOLO("yolov8n.pt")
speech_model = whisper.load_model("base")
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

os.makedirs("static/frames", exist_ok=True)

@app.get("/", response_class=HTMLResponse)
def serve_frontend(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/api")
def read_root():
    return {"message": "PeaceWatch AI Backend is running"}

def extract_frames(video_path, start_time="00:00", interval=1.0, max_frames=20):
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)

    # Convert start_time (mm:ss) into seconds
    try:
        minutes, seconds = map(int, start_time.split(":"))
        start_seconds = minutes * 60 + seconds
    except:
        start_seconds = 0

    cap.set(cv2.CAP_PROP_POS_MSEC, start_seconds * 1000)
    frame_gap = int(fps * interval)
    current = 0
    extracted = []

    while cap.isOpened() and len(extracted) < max_frames:
        ret, frame = cap.read()
        if not ret:
            break
        if current % frame_gap == 0:
            uid = str(uuid.uuid4())
            filename = f"static/frames/{uid}.jpg"
            cv2.imwrite(filename, frame)
            extracted.append({
                "url": f"/static/frames/{uid}.jpg",
                "index": current
            })
        current += 1
    cap.release()
    return extracted

@app.post("/analyze")
async def analyze(file: UploadFile = File(...), description: str = Form(...), start_time: str = Form("00:00")):
    suffix = os.path.splitext(file.filename)[1]
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp:
        temp.write(await file.read())
        temp_path = temp.name

    result_summary = {
        "description": description,
        "timestamp": datetime.utcnow().isoformat()
    }

    try:
        if suffix.lower() in [".jpg", ".jpeg", ".png"]:
            result = vision_model(temp_path)[0]
            labels = result.names
            detected = [labels[int(cls)] for cls in result.boxes.cls] if result.boxes else []
            result_summary["image_detections"] = detected

        elif suffix.lower() in [".mp4", ".mov", ".avi"]:
            frames = extract_frames(temp_path, start_time=start_time, interval=0.5, max_frames=10)
            all_labels, frame_data = [], []
            for f in frames:
                result = vision_model(f["url"].lstrip("/"))[0]
                labels = result.names
                detections = [labels[int(cls)] for cls in result.boxes.cls] if result.boxes else []
                all_labels.extend(detections)
                frame_data.append({**f, "detections": detections})
            result_summary["video_detections"] = list(set(all_labels))
            result_summary["detected_frames"] = frame_data

        elif suffix.lower() in [".mp3", ".wav", ".m4a"]:
            transcription = speech_model.transcribe(temp_path)
            result_summary["audio_transcription"] = transcription['text']

        # GPT Summary
        summary_prompt = f"""You are an AI assistant summarizing conflict reports.
Description: {description}
Detections: {result_summary.get('image_detections') or result_summary.get('video_detections')}
Transcription: {result_summary.get('audio_transcription', '')}"""

        summary = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Summarize incidents clearly."},
                {"role": "user", "content": summary_prompt}
            ]
        ).choices[0].message.content.strip()
        result_summary["gpt_summary"] = summary

        # GPT Guidance
        guidance_prompt = f"""Offer advice to a civilian reporting this incident:\n{summary_prompt}\nSummary: {summary}"""

        guidance = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You give safe and wise advice to citizens."},
                {"role": "user", "content": guidance_prompt}
            ]
        ).choices[0].message.content.strip()
        result_summary["user_guidance"] = guidance

    except Exception as e:
        logger.error(f"Analysis error: {e}")
        return JSONResponse({"error": str(e)}, status_code=500)
    finally:
        os.remove(temp_path)

    return result_summary
