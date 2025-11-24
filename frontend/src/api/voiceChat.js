export async function sendVoice(blob) {
  const formData = new FormData();
  formData.append("file", blob, "audio.webm");

  const API_BASE = "http://127.0.0.1:8000";

  const res = await fetch(`${API_BASE}/chat/voice`, {
    method: "POST",
    body: formData
  });

  if (!res.ok) {
    throw new Error("API error");
  }

  const data = await res.json();

  // FIX: convert relative → absolute
  if (data.audio_url && !data.audio_url.startsWith("http")) {
    data.audio_url = `${API_BASE}${data.audio_url}`;
  }

  if (data.video_url && !data.video_url.startsWith("http")) {
    data.video_url = `${API_BASE}${data.video_url}`;
  }

  return data;
}
