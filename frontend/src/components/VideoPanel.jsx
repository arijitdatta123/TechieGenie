import { useEffect, useRef, useState } from "react";

export default function VideoPanel({ videoUrl, onPlayDefault, botText, onStartRecording, isProcessing }) {
  // videoUrl: may be null or a URL like "/static/videos/VID001.mp4"
  // onPlayDefault: optional callback when launch/ default video is (re)started
  const defaultSrc = "/launch/RoboFace.mp4";
  const videoRef = useRef(null);
  const [currentSrc, setCurrentSrc] = useState(defaultSrc);
  const [isDefault, setIsDefault] = useState(true);

  // When frontend receives a new video_url from backend, switch
  // Step 1: When a new backend video arrives, update currentSrc
  useEffect(() => {
    if (videoUrl) {
      setCurrentSrc(videoUrl);
      setIsDefault(false);
    }
  }, [videoUrl]);

  // Step 2: Play the video whenever currentSrc or isDefault changes
  useEffect(() => {
    const v = videoRef.current;
    if (!v) return;

    if (isDefault) {
      v.loop = true;
      v.muted = true;
    } else {
      v.loop = false;
      v.muted = false;
    }

    v.currentTime = 0;
    v.play().catch(() => {});
  }, [currentSrc, isDefault]);


  // when the video ends and it was not the default, revert to default
  const handleEnded = () => {
    if (!isDefault) {
      // non-default video finished → go back to default
      setCurrentSrc(defaultSrc);
      setIsDefault(true);

      if (onPlayDefault) onPlayDefault();
    }
    // if default video ends, do nothing (looping will handle)
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
      {/* <div className="video-overlay">
        <button className="overlay-mic" onClick={onStartRecording}>
          🎤 Tap to Speak
        </button>
      </div> */}
      <div className="video-overlay">
        {isDefault && !isProcessing && (   // hide button while processing
          <button className="overlay-mic" onClick={onStartRecording}>
            🎤 Tap to Speak
          </button>
        )}
      </div>


      {/* Subtitles / always show bot text */}
      <div className="subtitles">
        {botText || "Ask me something…"}
      </div>
    </div>
  );
}
