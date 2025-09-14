import runpod
import os
from tts import TTS  # adjust depending on chatterbox TTS import
import tempfile

# Load model once
model = TTS("tts_models/en/ljspeech/tacotron2-DDC")

def handler(event):
    text = event.get("input", {}).get("text", "Hello from Chatterbox TTS")

    # Generate audio
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as fp:
        model.tts_to_file(text=text, file_path=fp.name)
        output_file = fp.name

    # Return file path OR base64 encoded audio
    with open(output_file, "rb") as f:
        audio_bytes = f.read()

    # Base64 encode to send over JSON
    import base64
    audio_b64 = base64.b64encode(audio_bytes).decode("utf-8")

    return {
        "text": text,
        "audio_base64": audio_b64
    }

runpod.serverless.start({"handler": handler})
