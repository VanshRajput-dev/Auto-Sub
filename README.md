# Sign Language Translator for Video Accessibility

This project provides real-time transcription of any video's audio and translates it into Indian Sign Language (ISL), which is then displayed using an AI-generated avatar. This system is designed to assist deaf individuals who prefer sign language over reading subtitles.

## Features

- Real-time audio capture from browser video using a Chrome extension
- Transcription of speech to English using OpenAI’s Whisper model
- Translation of English text into ISL gloss
- AI-based sign language avatar (under development)
- Web-based integration using a Chrome extension overlay
- Flask backend for processing audio and generating transcripts

## Technology Stack

| Component        | Technology                  |
|------------------|-----------------------------|
| Frontend         | Chrome Extension, HTML, JavaScript |
| Audio Capture    | chrome.tabCapture API       |
| Backend          | Python Flask                |
| Transcription    | OpenAI Whisper              |
| Audio Conversion | FFmpeg                      |
| Avatar Rendering | (Planned) Three.js / WebGL / Unity |
| Sign Language    | (Planned) ISL Dataset and Gloss Translation Models |

## Project Structure

 AUTO-SUB 
    ├──Whisper-backend
   │ ├── app.py # Flask server 
   ├── requirements.txt # Python dependencies 
   ├── extension/ # Chrome extension files │ 
   ├── background.js │
   ├── content.js │ 
   ├── popup.html │ 
   ├── popup.js │ 
   └── manifest.json 
   └── README.md # Project documentation

bash
Copy
Edit

## How to Run the Project on Your PC

### Prerequisites

- Python 3.8 or higher
- Node.js and npm (for Chrome extension management)
- FFmpeg (must be installed and accessible from the command line)
- Git

 
```bash
 ### Step 1: Clone the Repository 

git clone https://github.com/VanshRajput-dev/Auto-Sub.git
 
### Step 2: Set Up Python Virtual Environment

On Windows (Command Prompt):

 -> cd  whisper-backend
 venv\Scripts\activate
 

 

### Step 3: Install Required Packages
 
pip install -r requirements.txt
Make sure FFmpeg is installed by running:
ffmpeg -version

### Step 4: Run the Flask Server
Start the backend server:

python app.py
The server will run by default at http://127.0.0.1:5000.

### Step 5: Load the Chrome Extension
Open Google Chrome and go to chrome://extensions

Enable Developer Mode

Click "Load Unpacked"

Select the extension/ folder inside the cloned repository

Navigate to any video website and click the extension icon to start capturing audio

Notes
Ensure the Flask backend is running before starting the Chrome extension

Monitor the browser console for any real-time errors or logs

The AI avatar and sign language rendering features are currently under development

The project is focused on Indian Sign Language (ISL)
 

Contributing
Contributions to this project are welcome. You can help by submitting issues, improving the code, integrating ISL gloss translation, or building the avatar system. Fork the repository and open a pull request with your changes.

License
This project is licensed under the MIT License. You are free to use, modify, and distribute it under the terms of the license.

Contact