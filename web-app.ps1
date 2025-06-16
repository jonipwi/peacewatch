#python.exe -m pip install --upgrade pip
#pip install --upgrade pip

#choco install ffmpeg-full

py -3.10 -m venv venv
.\venv\Scripts\activate

#pip install jinja2 python-multipart
#pip install openai-whisper
#pip install ultralytics
#pip install fastapi uvicorn python-multipart ffmpeg-python openai

uvicorn peacewatch_ai_backend:app --reload