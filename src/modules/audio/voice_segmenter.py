# modules/audio/voice_segmenter.py

class VoiceSegmenter:
    def process(self, utterance: str):
        """
        Segments an utterance into tokens, skipping empty or whitespace-only inputs.
        """
        print("[VoiceSegmenter] Segmenting utterance...")
        if not utterance.strip():
            print("[VoiceSegmenter] Skipping empty or whitespace-only utterance")
            return []
        return utterance.strip().split()  # Simple whitespace split for tokens