from flask import Flask, request, jsonify
import whisper
import os
import tempfile
import subprocess
import base64

app = Flask(__name__)
model = whisper.load_model("base")

@app.route('/')
def home():
    return jsonify({"message": "Whisper backend is running!"})

@app.route('/transcribe', methods=['POST'])
def transcribe():
    if 'audio' not in request.files:
        print("No 'audio' file part in request")
        return jsonify({'error': 'No audio file provided'}), 400

    file = request.files['audio']
    print("File received:", file)
    print("Filename:", file.filename)
    print("Content-Type:", file.content_type)
    print("Content-Length:", request.content_length)

    if file.filename == '':
        print("Empty filename in request")
        return jsonify({'error': 'Empty filename'}), 400

    # Skip WebM and go directly to WAV to avoid WebM parsing issues
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_wav:
        wav_path = tmp_wav.name
    
    try:
        # Save file content to a temporary raw file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".raw") as tmp_raw:
            raw_path = tmp_raw.name
            file.save(raw_path)
            print(f"Saved incoming audio to raw file: {raw_path}")
            
        size = os.path.getsize(raw_path)
        print(f"Saved raw file size: {size} bytes")
        if size < 10:  # Even tiny audio files should be bigger than this
            print("File is too small — upload likely failed")
            os.remove(raw_path)
            return jsonify({'error': 'Uploaded file is too small'}), 400
            
        # Use FFmpeg to directly process the raw audio data
        # This bypasses container format issues
        print("Attempting direct raw PCM conversion...")
        result = subprocess.run([
            "ffmpeg", "-y", "-f", "data", "-i", raw_path, 
            "-ar", "16000", "-ac", "1", "-c:a", "pcm_s16le", wav_path
        ], capture_output=True, text=True)
        
        if result.returncode != 0:
            print("Raw conversion failed, trying with opus codec...")
            # Try to interpret as raw opus data
            result = subprocess.run([
                "ffmpeg", "-y", "-f", "opus", "-i", raw_path,
                "-ar", "16000", "-ac", "1", wav_path
            ], capture_output=True, text=True)
            
            if result.returncode != 0:
                # Let's inspect the first few bytes of the file to determine what we're dealing with
                with open(raw_path, 'rb') as f:
                    header = f.read(16)
                print(f"File header (hex): {header.hex()}")
                
                # Try one more approach - assume it's raw PCM data
                result = subprocess.run([
                    "ffmpeg", "-y", "-f", "s16le", "-ar", "48000", "-ac", "1", 
                    "-i", raw_path, "-ar", "16000", wav_path
                ], capture_output=True, text=True)
                
                if result.returncode != 0:
                    print("FFmpeg stderr:", result.stderr)
                    print("FFmpeg stdout:", result.stdout)
                    os.remove(raw_path)
                    return jsonify({
                        'error': 'All conversion methods failed', 
                        'ffmpeg_output': result.stderr
                    }), 500

        print(f"Converted to WAV: {wav_path}")
        os.remove(raw_path)
        
    except Exception as e:
        print("Conversion exception:", e)
        if os.path.exists(raw_path):
            os.remove(raw_path)
        return jsonify({'error': f'Conversion exception: {str(e)}'}), 500

    try:
        if not os.path.exists(wav_path) or os.path.getsize(wav_path) == 0:
            print("WAV file is missing or empty")
            return jsonify({'error': 'WAV conversion produced an empty file'}), 500
            
        print("Running transcription...")
        result = model.transcribe(wav_path)
        transcription = result.get('text', '').strip()
        print("Transcription successful:", transcription)
    except Exception as e:
        print("Whisper transcription failed:", e)
        return jsonify({'error': f'Transcription failed: {str(e)}'}), 500
    finally:
        if os.path.exists(wav_path):
            os.remove(wav_path)

    return jsonify({'transcription': transcription})

# Add support for possible base64 encoded audio
@app.route('/transcribe/base64', methods=['POST'])
def transcribe_base64():
    try:
        data = request.get_json()
        if not data or 'audio' not in data:
            return jsonify({'error': 'No audio data provided'}), 400
            
        # Decode base64 audio
        audio_data = base64.b64decode(data['audio'])
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_wav:
            wav_path = tmp_wav.name
            
        with tempfile.NamedTemporaryFile(delete=False, suffix=".raw") as tmp_raw:
            raw_path = tmp_raw.name
            with open(raw_path, 'wb') as f:
                f.write(audio_data)
                
        # Convert raw data to WAV using FFmpeg
        result = subprocess.run([
            "ffmpeg", "-y", "-f", "s16le", "-ar", "48000", "-ac", "1", 
            "-i", raw_path, "-ar", "16000", wav_path
        ], capture_output=True, text=True)
        
        if result.returncode != 0:
            os.remove(raw_path)
            os.remove(wav_path)
            return jsonify({'error': 'Audio conversion failed'}), 500
            
        # Transcribe the WAV file
        result = model.transcribe(wav_path)
        transcription = result.get('text', '').strip()
        
        os.remove(raw_path)
        os.remove(wav_path)
        
        return jsonify({'transcription': transcription})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Add CORS support for web clients
@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    response.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
    return response

@app.route('/transcribe', methods=['OPTIONS'])
@app.route('/transcribe/base64', methods=['OPTIONS'])
def options():
    return '', 204

if __name__ == '__main__':
    app.run(debug=True)