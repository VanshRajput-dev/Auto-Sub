if (!document.getElementById("autosub-overlay")) {
    const overlay = document.createElement("div");
    overlay.id = "autosub-overlay";
    overlay.style.position = "fixed";
    overlay.style.bottom = "10%";
    overlay.style.left = "50%";
    overlay.style.transform = "translateX(-50%)";
    overlay.style.backgroundColor = "rgba(0, 0, 0, 0.6)";
    overlay.style.color = "white";
    overlay.style.fontSize = "20px";
    overlay.style.padding = "10px 20px";
    overlay.style.borderRadius = "10px";
    overlay.style.zIndex = "9999";
    overlay.innerText = "Subtitles will appear here...";
    document.body.appendChild(overlay);
  } else {
    // Toggle overlay off if it already exists
    document.getElementById("autosub-overlay").remove();
  }
  