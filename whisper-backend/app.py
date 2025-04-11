from flask import Flask, request, jsonify
import whisper
import os
import tempfile

app = Flask(__name__)
model = whisper.load_model("base")

@app.route('/transcribe', methods=['POST'])
def transcribe():
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file provided'}), 400

    audio_file = request.files['audio']

    # Save to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        audio_path = tmp.name
        audio_file.save(audio_path)

    # Transcribe using Whisper
    result = model.transcribe(audio_path)
    os.remove(audio_path)  # Clean up temp file

    return jsonify({'transcription': result['text']})

if __name__ == '__main__':
    app.run(debug=True)
