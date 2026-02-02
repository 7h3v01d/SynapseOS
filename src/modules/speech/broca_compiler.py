# modules/speech/broca_compiler.py

import random
from modules.core.working_memory_queue import WorkingMemoryQueue

class BrocaCompiler:
    def __init__(self, memory=None):
        self.memory = memory or WorkingMemoryQueue()
        self.templates = {
            "greeting": ["Hello! What's up?", "Hi there!", "Hey, nice to hear from you!"],
            "ask_status": ["I'm doing great, thanks for asking!", "All good here!", "I'm SynapseOS, running smoothly!"],
            "get_weather": ["I can check the weather for you! What's your location?", "Weather info coming up!"],
            "query_identity": ["I'm SynapseOS, your friendly AI!", "That's me, SynapseOS!"],
            "gratitude": ["You're welcome!", "Glad I could help!"],
            "command_action": ["Alright, performing the action!", "Got it, acting on your command!"],
            "start_call": ["Starting the call now!", "Let's get that call going!"],
            "stop_action": ["Okay, stopping now!", "Got it, halting the action!"],
            "offer_support": ["I'm here for you! What's on your mind?", "Sorry to hear that, want to talk?"],
            "unknown": ["Can you clarify that?", "Hmm, let's dive deeper."]
        }

    def synthesize(self, intent: dict) -> str:
        intent_type = intent.get("intent", "unknown")
        responses = self.templates.get(intent_type, self.templates["unknown"])
        response = random.choice(responses)

        recent_context = self.memory.recall_last(3)
        for item in recent_context:
            if "text" in item and "how" in item["text"].lower():
                response += " You asked about status earlier, right?"
                break
        return response