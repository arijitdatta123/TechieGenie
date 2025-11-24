import { useEffect, useState } from "react";

export default function VoiceRecorder({ onRecorded, registerStart }) {
  const [isRecording, setIsRecording] = useState(false);

  async function startRecording() {
    console.log("🎙️ REAL recording started");
    try {
      setIsRecording(true);
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const mediaRecorder = new MediaRecorder(stream);
      let chunks = [];

      mediaRecorder.ondataavailable = (e) => chunks.push(e.data);

      mediaRecorder.onstop = () => {
        const blob = new Blob(chunks, { type: "audio/webm" });
        onRecorded(blob);
        setIsRecording(false);
      };

      mediaRecorder.start();
      setTimeout(() => mediaRecorder.stop(), 5000);
    } catch (err) {
      console.error("Mic error:", err);
      setIsRecording(false);
    }
  }

  // Allow parent to trigger microphone
  useEffect(() => {
    if (registerStart) registerStart(startRecording);
  }, []);

  return (
    <button
      className={`mic-btn ${isRecording ? "recording" : ""}`}
      onClick={startRecording}
    >
      🎤 Tap to Speak
    </button>
  );
}
