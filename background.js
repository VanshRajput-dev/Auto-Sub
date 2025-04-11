let audioStream = null;

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === "start_capture") {
    console.log("Starting audio capture...");

    chrome.tabCapture.capture({ audio: true, video: false }, (stream) => {
      if (!stream) {
        console.error("Failed to capture audio:", chrome.runtime.lastError);
        return;
      }

      audioStream = stream;
      console.log("Audio stream captured!");

      // You could process this stream here or send it to a recorder function
      startStreamingAudioToBackend(audioStream);
    });
  }
});

function startStreamingAudioToBackend(stream) {
  const mediaRecorder = new MediaRecorder(stream, { mimeType: "audio/webm" });

  mediaRecorder.ondataavailable = async (event) => {
    if (event.data.size > 0) {
      console.log("Sending audio chunk to backend...");

      const blob = event.data;
      const formData = new FormData();
      formData.append("audio", blob, "chunk.webm");

      try {
        const response = await fetch("http://localhost:5000/transcribe", {
          method: "POST",
          body: formData,
        });

        const data = await response.json();
        const transcript = data.transcript;
        console.log("Transcript:", transcript);

        // Send this to content script to show on screen
        chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
          chrome.tabs.sendMessage(tabs[0].id, {
            action: "show_transcript",
            text: transcript,
          });
        });
      } catch (err) {
        console.error("Error sending audio to backend:", err);
      }
    }
  };

  mediaRecorder.start(5000); // capture in 5-second chunks
}
