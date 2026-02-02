# modules/audio/audio_listener.py

import sounddevice as sd
import numpy as np
import whisper
import queue
import threading
from modules.core.working_memory_queue import WorkingMemoryQueue

class AudioListener:
    def __init__(self, model_size="base", memory=None):
        self.model = whisper.load_model(model_size)
        self.samplerate = 16000
        self.chunk_duration = 3  # Reduced for responsiveness
        self.memory = memory or WorkingMemoryQueue()
        self.q = queue.Queue()
        self.stream = None
        self._running = False
        self.energy_threshold = 10  # Adjusted back to 10 for noise filtering

    def _callback(self, indata, frames, time, status):
        if self._running:
            energy = np.linalg.norm(indata) * 10
            print(f"[AudioListener] Energy: {energy:.2f}")
            if energy > self.energy_threshold:
                self.q.put(indata.copy())
            else:
                print(f"[AudioListener] Skipping low-energy audio chunk (threshold: {self.energy_threshold})")

    def listen_generator(self):
        self._running = True
        self.stream = sd.InputStream(
            channels=1,
            samplerate=self.samplerate,
            callback=self._callback
        )
        self.stream.start()
        print("[🎤] Listening for audio input... (3 sec chunks)")
        try:
            while self._running:
                audio_frames = []
                for _ in range(0, int(self.samplerate * self.chunk_duration / 1024)):
                    try:
                        audio_chunk = self.q.get(timeout=1.0)
                        audio_frames.append(audio_chunk)
                    except queue.Empty:
                        print("[AudioListener] No audio data received, skipping chunk")
                        continue

                if not audio_frames:
                    print("[AudioListener] No valid audio frames, skipping transcription")
                    continue

                audio_data = np.concatenate(audio_frames, axis=0).flatten()
                audio_np = np.array(audio_data, dtype=np.float32)

                print("[🧠] Transcribing...")
                result = self.model.transcribe(audio_np, fp16=False, language='en')
                text = result["text"].strip()
                if not text:
                    print("[AudioListener] Empty transcription, skipping")
                    continue

                print(f"[🗣️] Heard: {text}")
                self.memory.store({"source": "microphone", "text": text})
                yield text
        finally:
            self.stop_listening()

    def stop_listening(self):
        self._running = False
        if self.stream:
            self.stream.stop()
            self.stream.close()
        print("[🔇] AudioListener stopped.")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.stop_listening()