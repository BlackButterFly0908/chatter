import runpod
import os
import tempfile
import torchaudio as ta
import base64
from chatterbox.tts import ChatterboxTTS

# Load model once at startup
print("Loading Chatterbox TTS model...")
try:
    # Try CUDA first, fallback to CPU if not available
    device = "cuda" if os.environ.get("CUDA_VISIBLE_DEVICES") else "cpu"
    model = ChatterboxTTS.from_pretrained(device=device)
    print(f"Model loaded successfully on {device}!")
except Exception as e:
    print(f"Failed to load model on CUDA, trying CPU: {e}")
    model = ChatterboxTTS.from_pretrained(device="cpu")
    print("Model loaded successfully on CPU!")

def handler(event):
    try:
        # Get input parameters
        input_data = event.get("input", {})
        text = input_data.get("text", "Hello from Chatterbox TTS")
        audio_prompt_path = input_data.get("audio_prompt_path", None)
        
        print(f"Generating audio for text: {text}")
        
        # Generate audio with optional voice cloning
        if audio_prompt_path:
            wav = model.generate(text, audio_prompt_path=audio_prompt_path)
        else:
            wav = model.generate(text)
        
        # Save to temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as fp:
            ta.save(fp.name, wav, model.sr)
            output_file = fp.name

        # Read and encode audio file
        with open(output_file, "rb") as f:
            audio_bytes = f.read()

        # Clean up temporary file
        os.unlink(output_file)

        # Base64 encode to send over JSON
        audio_b64 = base64.b64encode(audio_bytes).decode("utf-8")

        return {
            "text": text,
            "audio_base64": audio_b64,
            "sample_rate": model.sr,
            "success": True
        }
        
    except Exception as e:
        print(f"Error in handler: {str(e)}")
        import traceback
        traceback.print_exc()
        return {
            "error": str(e),
            "success": False
        }

runpod.serverless.start({"handler": handler})
