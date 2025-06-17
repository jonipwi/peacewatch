import os
import pytesseract
from PIL import Image
from flask import Flask, render_template
from transformers import pipeline
import openai
import json
import shutil
from datetime import datetime

# ---- Configurations ---- #
SCREENSHOT_FOLDER = "./proof-of-threat"
LOG_FILE = "./logs/result_log.json"
TEXT_LOG_FILE = "./logs/text.log"
OUTPUT_IMAGE_FOLDER = "./static/images"
os.makedirs(OUTPUT_IMAGE_FOLDER, exist_ok=True)
os.makedirs("logs", exist_ok=True)

# OpenAI API key (ensure it's set in your environment)
openai.api_key = os.getenv("OPENAI_API_KEY")

# ---- Initialize AI Models ---- #
print("Loading HuggingFace toxicity model...")
threat_detector = pipeline("text-classification", model="unitary/toxic-bert")
print("Model loaded.")

results = []
with open(TEXT_LOG_FILE, "w", encoding="utf-8") as textlog:
    for file in os.listdir(SCREENSHOT_FOLDER):
        if file.lower().endswith((".png", ".jpg", ".jpeg")):
            img_path = os.path.join(SCREENSHOT_FOLDER, file)
            print(f"\n🔍 Reading image: {file}")

            text = pytesseract.image_to_string(Image.open(img_path), lang='ind').strip()
            print("📜 Extracted Text:", text)

            textlog.write(f"--- {file} ---\n{text}\n\n")

            if not text:
                print("❌ No text found, skipping.")
                continue

            analysis = threat_detector(text)
            print(f"🔍 Full toxicity result: {analysis}")

            # Lowered threshold to 0.5
            toxic = [res for res in analysis if "toxic" in res['label'].lower() and res['score'] > 0.5]

            # Manual keyword match for Bahasa threats
            threat_keywords = ["lempar", "serang", "ancam", "siksa", "bakar", "aniaya"]
            keyword_matched = any(word in text.lower() for word in threat_keywords)

            # GPT threat detection
            try:
                threat_check_response = openai.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": "You are a forensic linguist and threat analyst."},
                        {"role": "user", "content": f"""
Does this text contain a direct or indirect threat, such as suggesting violence (e.g. throwing objects) or blaming the victim for potential harm?

Text:
{text}

Answer YES or NO, and explain briefly if YES.
"""}
                    ]
                )
                gpt_threat_check = threat_check_response.choices[0].message.content.strip()
            except Exception as e:
                gpt_threat_check = f"GPT Error: {e}"

            should_flag = toxic or keyword_matched or "YES" in gpt_threat_check.upper()

            if should_flag:
                print("⚠️ Threat Detected!")
                shutil.copy(img_path, os.path.join(OUTPUT_IMAGE_FOLDER, file))

                try:
                    # Emotional impact analysis
                    emotion_response = openai.chat.completions.create(
                        model="gpt-4o",
                        messages=[
                            {"role": "system", "content": "You are a trauma psychologist and community harm analyst."},
                            {"role": "user", "content": f"""
A group chat message is potentially causing mental harm to a woman (my wife), who has been falsely accused.

Important context:
- Our dog is not wild and never bites.
- When the dog goes out to defecate, we always bring a plastic bag to clean up.
- Due to harassment and threats, the dog hasn’t gone outside for over two years.
- My wife is deeply affected mentally after being forced to defend herself in the community WhatsApp group.
- The community chat wrongly accuses her of negligence and implies she or our dog is a public threat.

Now, here is the chat text:
{text}

Does this message contribute to mental distress or social discrimination? Provide a short explanation and recommended psychological or community action.
"""}
                        ]
                    )
                    emotional_impact = emotion_response.choices[0].message.content

                    victim_response = openai.chat.completions.create(
                        model="gpt-4o",
                        messages=[
                            {"role": "system", "content": "You are a community conflict analyzer. Identify any person or group that may feel harmed by the message."},
                            {"role": "user", "content": text}
                        ]
                    )
                    victim_detected = victim_response.choices[0].message.content

                    legal_response = openai.chat.completions.create(
                        model="gpt-4o",
                        messages=[
                            {"role": "system", "content": "You are a legal assistant generating incident reports in Indonesian context."},
                            {"role": "user", "content": f"""
Based on the following chat message and the following facts:

1. The family has been accused of letting their dog roam, poop indiscriminately, or cause fear — all of which are false.
2. The dog is under control, and the family always cleans up after it.
3. Due to threats and discrimination, the dog has been confined indoors for two years.
4. The woman in the family has suffered mental distress from being verbally attacked and defending herself in the group.
5. This group chat acts as a social tribunal without evidence, encouraging hostile behavior.

Chat message:
{text}

Please generate a short legal-style summary: who is responsible for any verbal harassment, who are the victims, and what laws or moral boundaries may have been violated.
"""}
                        ]
                    )
                    legal_summary = legal_response.choices[0].message.content

                except Exception as e:
                    emotional_impact = f"OpenAI Error: {e}"
                    victim_detected = "OpenAI Error"
                    legal_summary = "OpenAI Error"

                result = {
                    "filename": file,
                    "timestamp": datetime.now().isoformat(),
                    "text": text,
                    "score": round(toxic[0]['score'], 2) if toxic else 0,
                    "label": toxic[0]['label'] if toxic else "manual_detected",
                    "keyword_matched": keyword_matched,
                    "gpt_threat": gpt_threat_check,
                    "emotional_impact": emotional_impact,
                    "victim": victim_detected,
                    "legal_summary": legal_summary
                }
                results.append(result)
            else:
                print("✅ Message seems safe.")

# Save logs
with open(LOG_FILE, "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"\n📝 Log saved to {LOG_FILE}")
    print(f"📂 OCR text saved to {TEXT_LOG_FILE}")

# ---- Flask Server ---- #
app = Flask(__name__)

@app.route("/")
def index():
    try:
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            logs = json.load(f)
    except:
        logs = []
    return render_template("result.html", logs=logs)

if __name__ == "__main__":
    print("\n🌐 Starting local web server at http://localhost:5000")
    app.run(debug=True)
