FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git ffmpeg espeak-ng \
    && rm -rf /var/lib/apt/lists/*

# Install Chatterbox TTS
WORKDIR /app
RUN git clone https://github.com/ChatterboxAI/tts.git .
RUN pip install --no-cache-dir -r requirements.txt

# Install RunPod SDK
RUN pip install runpod

# Copy handler
COPY handler.py .

# Default command
CMD ["python", "handler.py"]
