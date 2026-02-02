# test_synapseos.py

import time
from modules.audio.audio_listener import AudioListener
from modules.core.goal_evaluator import GoalEvaluator
from modules.speech.broca_compiler import BrocaCompiler
from modules.core.working_memory_queue import WorkingMemoryQueue

def test_pipeline():
    memory = WorkingMemoryQueue()
    listener = AudioListener(memory=memory)
    evaluator = GoalEvaluator(memory=memory)
    compiler = BrocaCompiler(memory=memory)

    print("Starting test. Speak the following phrases (5s each):")
    test_phrases = [
        "Hello, what's the weather?",
        "How are you?",
        "Wave your hand.",
        "Let's start the call.",
        "I'm sad.",
        "Let's stop.",
        "(stay silent)",
        "Hello, I'm sad.",
        "Let's start the course."
    ]
    print("Phrases to test:", test_phrases)

    with listener:
        for phrase in test_phrases:
            print(f"\nPlease say: '{phrase}'")
            time.sleep(5)  # Give 5 seconds to speak
            for text in listener.listen_generator():
                if text:
                    print(f"[Input] {text}")
                    lexemes = text.lower().split()
                    print(f"[Lexemes] {lexemes}")
                    intent = evaluator.evaluate(lexemes)
                    print(f"[Intent] {intent}")
                    response = compiler.synthesize(intent)
                    print(f"[Response] {response}")
                    memory.store({"text": text, "intent": intent})
                break  # Process one input per phrase

if __name__ == "__main__":
    test_pipeline()