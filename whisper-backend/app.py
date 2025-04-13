from flask import Flask, request, jsonify
import whisper
import os
import tempfile
import subprocess

app = Flask(__name__)
model = whisper.load_model("base")

@app.route('/')
def home():
    return jsonify({"message": "Whisper backend is running!"})

@app.route('/transcribe', methods=['POST'])
def transcribe():
    if 'audio' not in request.files:
        print("No audio part in request")
        return jsonify({'error': 'No audio file provided'}), 400

    # Save the incoming .webm file
    webm_file = request.files['audio']
    with tempfile.NamedTemporaryFile(delete=False, suffix=".webm") as tmp_webm:
        webm_path = tmp_webm.name
        webm_file.save(w   ebm_path)
        print(f"Saved incoming audio to: {webm_path}")

    # Convert .webm to .wav using FFmpeg
    wav_path = webm_path.replace(".webm", ".wav")
    try:
        subprocess.run([
            "ffmpeg", "-y", "-i", webm_path, wav_path
        ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"Converted to WAV: {wav_path}")
    except subprocess.CalledProcessError as e:
        print("FFmpeg conversion failed:", e)
        os.remove(webm_path)
        return jsonify({'error': 'FFmpeg conversion failed'}), 500

    # Transcribe with Whisper
    try:
        print("Running transcription...")
        result = model.transcribe(wav_path)
        transcription = result.get('text', '').strip()
        print("Transcription successful:", transcription)
    except Exception as e:
        print("Whisper transcription failed:", e)
        return jsonify({'error': f'Transcription failed: {str(e)}'}), 500
    finally:
        # Clean up temporary files
        if os.path.exists(webm_path):
            os.remove(webm_path)
        if os.path.exists(wav_path):
            os.remove(wav_path)

    return jsonify({'transcription': transcription})

if __name__ == '__main__':
    app.run(debug=True)
