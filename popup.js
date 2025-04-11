document.getElementById("startBtn").addEventListener("click", () => {
  chrome.runtime.sendMessage({ action: "start_capture" });
});

document.getElementById("stopBtn").addEventListener("click", () => {
  chrome.runtime.sendMessage({ action: "stop_capture" });
});
