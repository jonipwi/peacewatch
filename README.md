# peacewatch
🕊️ PeaceWatch AI is a community-focused conflict monitoring tool using AI to analyze images, videos, and audio for violence, abuse, and public threats — providing summaries, guidance, and frame evidence for victims and authorities.

# 🕊️ PeaceWatch AI - Community Conflict Monitoring

PeaceWatch AI helps communities detect, report, and respond to acts of violence, intimidation, and abuse using artificial intelligence.

It analyzes **uploaded images, videos, or audio** using:
- 🧠 GPT-4 for summaries and guidance
- 🧍 YOLOv8 for person and object detection
- 🔊 Whisper for audio transcription
- 🎞️ Frame extraction from videos
- 📦 JSON reporting for law enforcement or NGOs

---

## ✨ Features

- 🖼️ Detect people and suspicious objects from image or video
- 🔊 Transcribe and analyze spoken threats from audio files
- 🧠 Summarize incident with GPT-4
- 🛟 Give clear, peaceful, victim-focused guidance
- 🎞️ Generate preview frames with detection badges
- 📄 Return complete JSON with detections, summaries, frames

---

## 📸 Example Use Cases

- **A woman uploads a video of someone throwing stones at her and her dog.**
- PeaceWatch detects the person, analyzes the video, transcribes shouting, and provides:
  - A clear AI-written summary of the event
  - Guidance on what to do next (legal, safety, emotional)
  - Visual frame snapshots with detection overlay
  - Downloadable evidence for law enforcement or NGOs

---

## 🔧 Installation

### Requirements

- Python 3.10+
- Node.js (optional, for frontend enhancements)
- `ffmpeg` (required for Whisper/audio transcription)

### Backend Setup

```bash
git clone https://github.com/your-username/peacewatch-ai.git
cd peacewatch-ai

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt

--
# Create a .env file:
env
OPENAI_API_KEY=your_openai_key_here

# Then start the backend:
bash
uvicorn main:app --reload

# Frontend
Open your browser at http://127.0.0.1:8000
