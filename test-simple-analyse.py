import pytesseract
from PIL import Image
import os
from transformers import pipeline
import torch

# ---- Config ----
image_path = './proof-of-threat/WhatsApp Image 2025-06-17 at 10.10.30_9dca3e5b.jpg'

# ---- Step 1: OCR - Extract Text from Image ----
print("🔍 Reading image:", image_path)
img = Image.open(image_path)
extracted_text = pytesseract.image_to_string(img, lang='ind')  # uses Indonesian OCR
print("\n📜 Extracted Text:\n", extracted_text)

# ---- Step 2: Basic Classification (Optional with AI) ----
# We'll just check for polite/aggressive tones using simple word flags

polite_keywords = [
    "terima kasih", "maaf", "tolong", "mohon", "dengan hormat",
    "sopan", "diskusi", "damai", "legowo", "baik hati"
]

aggressive_keywords = [
    "bodoh", "anjing", "mati", "bunuh", "kotor", "pengacau", "sialan", "brengsek", "kampret", "brengsek"
]

def classify_text(text):
    text_lower = text.lower()
    polite = any(word in text_lower for word in polite_keywords)
    aggressive = any(word in text_lower for word in aggressive_keywords)

    if aggressive:
        return "⚠️ Possibly Threatening or Aggressive"
    elif polite:
        return "✅ Polite / Community-oriented Message"
    else:
        return "ℹ️ Neutral / Unknown Tone"

classification = classify_text(extracted_text)

# ---- Step 3: Display Result ----
print("\n🧠 AI Interpretation:", classification)
