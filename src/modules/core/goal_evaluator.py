# modules/core/goal_evaluator.py

from transformers import pipeline
from modules.core.working_memory_queue import WorkingMemoryQueue

class GoalEvaluator:
    def __init__(self, memory=None):
        self.memory = memory or WorkingMemoryQueue()
        self.nlp = pipeline("text-classification", model="distilbert-base-uncased-finetuned-sst-2-english")
        self.intent_map = {
            "POSITIVE": "greeting",
            "NEGATIVE": "offer_support",
        }
        self.fallback_intent = {"intent": "unknown", "confidence": 0.3}

    def evaluate(self, lexemes):
        """
        Determines user intent based on current input and recent memory context using a pre-trained NLP model.
        """
        print("[🧠] Evaluating intent based on input and context...")
        current_input = " ".join(lexemes).lower()
        recent_context = self.memory.recall_last(5)
        context_text = " ".join([item.get("text", "") for item in recent_context]).lower()
        combined_input = f"{context_text} {current_input}".strip()

        if not combined_input or len(lexemes) < 2 and "day" in current_input:
            print("[GoalEvaluator] Ambiguous or short input, using fallback intent")
            return self.fallback_intent

        try:
            # Rule-based checks (prioritized over NLP model)
            if "weather" in current_input:
                return {"intent": "get_weather", "confidence": 0.9}
            if "name" in current_input:
                return {"intent": "query_identity", "confidence": 0.9}
            if any("thank" in word for word in lexemes):
                return {"intent": "gratitude", "confidence": 0.9}
            if "wave" in current_input or "move" in current_input or "save" in current_input:
                return {"intent": "command_action", "confidence": 0.9}
            if "start" in current_input and ("call" in current_input or "course" in current_input):
                return {"intent": "start_call", "confidence": 0.9}
            if "how" in current_input and "you" in current_input:
                return {"intent": "ask_status", "confidence": 0.9}
            if "stop" in current_input:
                return {"intent": "stop_action", "confidence": 0.9}
            if "sad" in current_input or "unhappy" in current_input:
                return {"intent": "offer_support", "confidence": 0.9}

            # NLP model for remaining cases
            result = self.nlp(combined_input, truncation=True, max_length=512)
            label = result[0]["label"]
            confidence = result[0]["score"]
            intent = self.intent_map.get(label, "unknown")

            if confidence < 0.5:
                print("[GoalEvaluator] Low confidence score, using fallback intent")
                return self.fallback_intent

            return {"intent": intent, "confidence": confidence}
        except Exception as e:
            print(f"[GoalEvaluator] NLP model error: {e}")
            return self.fallback_intent