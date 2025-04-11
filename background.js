let audioStream = null;
let mediaRecorder = null;

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === "start_capture") {
    console.log("✅ Start capture message received!");

    chrome.tabCapture.capture({ audio: true, video: false }, (stream) => {
      if (!stream) {
        console.error("❌ Failed to capture audio:", chrome.runtime.lastError);
        return;
      }

      audioStream = stream;
      console.log("🎙️ Audio stream captured!");

      startStreamingAudioToBackend(audioStream);
    });
  }

  if (request.action === "stop_capture") {
    console.log("🛑 Stop capture message received!");

    if (mediaRecorder && mediaRecorder.state !== "inactive") {
      mediaRecorder.stop();
      console.log("📴 MediaRecorder stopped.");
    }

    if (audioStream) {
      const tracks = audioStream.getTracks();
      tracks.forEach(track => track.stop());
      console.log("🔇 Audio stream tracks stopped.");
    }

    audioStream = null;
    mediaRecorder = null;
  }
});

function startStreamingAudioToBackend(stream) {
  mediaRecorder = new MediaRecorder(stream, { mimeType: "audio/webm" });

  mediaRecorder.ondataavailable = async (event) => {
    if (event.data.size > 0) {
      console.log("📤 Sending audio chunk to backend...");

      const blob = event.data;
      const formData = new FormData();
      formData.append("audio", blob, "chunk.webm");

      try {
        const response = await fetch("http://localhost:5000/transcribe", {
          method: "POST",
          body: formData,
        });

        const data = await response.json();

        if (data.transcription) {
          const transcript = data.transcription;
          console.log("📄 Transcript:", transcript);

          chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
            if (tabs && tabs.length > 0) {
              chrome.tabs.sendMessage(tabs[0].id, {
                action: "show_transcript",
                text: transcript,
              });
            } else {
              console.warn("⚠️ No active tab found to send transcript.");
            }
          });
        } else {
          console.error("❌ No transcription returned from backend:", data);
        }
      } catch (err) {
        console.error("❌ Error sending audio to backend:", err);
      }
    }
  };

  mediaRecorder.start(5000); // capture in 5-second chunks
}
