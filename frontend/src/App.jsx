import { useEffect, useRef, useState } from "react";
import VoiceRecorder from "./components/VoiceRecorder";
import VideoPanel from "./components/VideoPanel";
import { sendVoice } from "./api/voiceChat";

export default function App() {
  const [botText, setBotText] = useState("TechiGenie is listening…");
  const [videoUrl, setVideoUrl] = useState(null);
  const [isSpeaking, setIsSpeaking] = useState(false);

  const recorderRef = useRef(null);

  function triggerRecording() {
    console.log("▶ Triggering actual recorder…");
    if (recorderRef.current) {
      recorderRef.current();
    }
  }

  function handleDefaultVideo() {
    console.log("🔄 Default video resumed");
    setVideoUrl(null);  // ensures fallback stays stable
  }

  async function handleRecorded(blob) {
    setBotText("Processing…");

    const res = await sendVoice(blob);
    setBotText(res.answer || "");

    setVideoUrl(res.video_url || null);

    if (res.audio_url) {
      const audio = new Audio(res.audio_url);
      setIsSpeaking(true);
      audio.onended = () => setIsSpeaking(false);
      audio.play();
    }
  }

  return (
    <div className="app-root">
      <VideoPanel
        videoUrl={videoUrl}
        botText={botText}
        onStartRecording={triggerRecording}
        onPlayDefault={handleDefaultVideo}   // ✔ NOW IT WORKS
      />

      <VoiceRecorder
        onRecorded={handleRecorded}
        registerStart={(fn) => (recorderRef.current = fn)}
      />

      <footer className="footer">
        Technovate • TechiGenie Demo
      </footer>
    </div>
  );
}
