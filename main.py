from flask import Flask, request, jsonify
import whisper
import tempfile
import os
import subprocess
from pytube import YouTube

app = Flask(__name__)
model = whisper.load_model("base")

@app.route('/')
def home():
    return "YouTube to Text API is running."

@app.route('/transcribe', methods=['POST'])
def transcribe():
    data = request.get_json()
    video_url = data.get("url")
    
    if not video_url:
        return jsonify({"error": "يرجى إرسال رابط الفيديو"}), 400

    try:
        yt = YouTube(video_url)
        stream = yt.streams.filter(only_audio=True).first()

        temp_dir = tempfile.mkdtemp()
        audio_path = os.path.join(temp_dir, "audio.mp4")
        stream.download(output_path=temp_dir, filename="audio.mp4")

        result = model.transcribe(audio_path, language='ar')
        text = result['text']

        return jsonify({"text": text})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
