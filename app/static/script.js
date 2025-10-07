const recordBtn = document.getElementById("recordBtn");
const statusEl = document.getElementById("status");
const resultText = document.getElementById("resultText");

let mediaRecorder;
let audioChunks = [];
let isRecording = false;

recordBtn.addEventListener("click", async () => {
  if (!isRecording) {
    // Start recording
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    mediaRecorder = new MediaRecorder(stream);

    audioChunks = [];
    mediaRecorder.ondataavailable = (event) => {
      audioChunks.push(event.data);
    };

    mediaRecorder.onstop = async () => {
      // Convert to blob and send to backend
      const audioBlob = new Blob(audioChunks, { type: "audio/webm" });
      const formData = new FormData();
      formData.append("audio", audioBlob, "recording.webm");

      statusEl.textContent = "Uploading and transcribing...";
      recordBtn.disabled = true;

      try {
        const response = await fetch("/api/transcribe", {
          method: "POST",
          body: formData,
        });

        const data = await response.json();

        if (data.text) {
          resultText.value = data.text;
          statusEl.textContent = "✅ Transcription complete!";
        } else {
          resultText.value = "";
          statusEl.textContent = "⚠️ Error: " + (data.error || "Unknown error");
        }
      } catch (error) {
        statusEl.textContent = "⚠️ Failed to send audio.";
      }

      recordBtn.disabled = false;
    };

    mediaRecorder.start();
    isRecording = true;
    recordBtn.textContent = "Stop Recording";
    statusEl.textContent = "🎙️ Recording... (max 1 minute)";

    // Auto-stop after 1 minute
    setTimeout(() => {
      if (isRecording) {
        mediaRecorder.stop();
        isRecording = false;
        recordBtn.textContent = "Start Recording";
      }
    }, 60000);
  } else {
    // Stop recording manually
    mediaRecorder.stop();
    isRecording = false;
    recordBtn.textContent = "Start Recording";
    statusEl.textContent = "Processing...";
  }
});
