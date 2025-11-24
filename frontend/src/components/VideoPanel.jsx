import { useEffect, useRef, useState } from "react";

export default function VideoPanel({ videoUrl, onPlayDefault, botText, onStartRecording }) {
  // videoUrl: may be null or a URL like "/static/videos/VID001.mp4"
  // onPlayDefault: optional callback when launch/ default video is (re)started
  const defaultSrc = "/launch/Default_Launch.mp4";
  const videoRef = useRef(null);
  const [currentSrc, setCurrentSrc] = useState(defaultSrc);
  const [isDefault, setIsDefault] = useState(true);

  // When frontend receives a new video_url from backend, switch
  useEffect(() => {
    if (videoUrl) {
      // play the incoming video (non-looped)
      setCurrentSrc(videoUrl);
      setIsDefault(false);
      // ensure we play from start
      const v = videoRef.current;
      if (v) {
        v.loop = false;
        v.muted = false; // allow sound for content videos
        v.currentTime = 0;
        v.play().catch(() => {});
      }
    }
  }, [videoUrl]);

  // when the video ends and it was not the default, revert to default
  const handleEnded = () => {
    if (!isDefault) {
      setCurrentSrc(defaultSrc);
      setIsDefault(true);
      // default should be looped and muted
      const v = videoRef.current;
      if (v) {
        v.loop = true;
        v.muted = true;
        v.currentTime = 0;
        v.play().catch(() => {});
      }
      if (onPlayDefault) onPlayDefault();
    } else {
      // default ended (if loop=false) — we'll keep default looping so usually not here
    }
  };

  // ensure default autostarts
  useEffect(() => {
    const v = videoRef.current;
    if (v) {
      v.loop = true;
      v.muted = true;
      v.play().catch(() => {});
    }
  }, []);

  return (
    <div className="video-panel">
      <video
        ref={videoRef}
        src={currentSrc}
        className="bg-video"
        playsInline
        onEnded={handleEnded}
      />

      {/* Layer: launch button / record mic on top of the video */}
      <div className="video-overlay">
        <button className="overlay-mic" onClick={onStartRecording}>
          🎤 Tap to Speak
        </button>
      </div>

      {/* Subtitles / always show bot text */}
      <div className="subtitles">
        {botText || "Ask me something…"}
      </div>
    </div>
  );
}
