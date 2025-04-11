chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === "show_transcript") {
      const div = document.createElement("div");
      div.style.position = "fixed";
      div.style.bottom = "10px";
      div.style.left = "10px";
      div.style.padding = "10px";
      div.style.backgroundColor = "rgba(0,0,0,0.7)";
      div.style.color = "white";
      div.style.fontSize = "16px";
      div.style.zIndex = 9999;
      div.innerText = request.text;
      document.body.appendChild(div);
  
      setTimeout(() => div.remove(), 8000);
    }
  });
  