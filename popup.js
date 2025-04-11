document.getElementById("toggleSubs").addEventListener("click", () => {
    chrome.runtime.sendMessage({ action: "start_capture" });
  });
  