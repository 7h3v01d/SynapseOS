# 🧠 SynapseOS v2.3 (Archived)

**An experimental cognitive operating system for real-time, voice-driven intelligent agents.**

SynapseOS is a modular AI runtime that models *how cognition flows*, not just how prompts are answered.

This project is currently **on ice**, preserved as a snapshot of an ambitious learning phase — big ideas, real wiring, and a strong architectural core.

---

⚠️ **LICENSE & USAGE NOTICE — READ FIRST**

This repository is **source-available for private technical evaluation and testing only**.

- ❌ No commercial use  
- ❌ No production use  
- ❌ No academic, institutional, or government use  
- ❌ No research, benchmarking, or publication  
- ❌ No redistribution, sublicensing, or derivative works  
- ❌ No independent development based on this code  

All rights remain exclusively with the author.  
Use of this software constitutes acceptance of the terms defined in **LICENSE.txt**.

---

## 🚀 What is SynapseOS?

SynapseOS is an attempt to build an **AI operating system**, not an app.

Instead of a monolithic loop, it models intelligence as a **pipeline of cooperating cognitive modules**:
- perception
- memory
- intent evaluation
- speech planning
- action emission

All connected through an internal message bus.

Think: *a nervous system*, not a chatbot.

---

## 🧬 Core ideas

- 🧠 **Human-inspired cognition**
  - Working memory with decay and recall
  - Goal evaluation using context + sentiment
  - Intent-driven response generation

- 🎤 **Real-time voice input**
  - Live microphone capture
  - Energy-based audio gating
  - Whisper-powered speech-to-text

- 🧠 **Hybrid reasoning**
  - Rule-based intent detection for known commands
  - NLP model fallback for ambiguous input
  - Confidence thresholds and safety fallbacks

- 🗣️ **Speech planning pipeline**
  - Intent → linguistic template → contextual refinement
  - Modular speech synthesis stage (stubbed for now)

- 🔁 **Event-driven architecture**
  - All modules communicate via an internal relay bus
  - Loose coupling between perception, reasoning, and output

---

## 🖥️ Live system dashboard

SynapseOS includes a **Rich-powered TUI dashboard** showing:

- current pipeline state (Input → Tokens → Intent → Response)
- color-coded cognitive stages
- scrollback log
- CPU + RAM usage
- live audio activity meter
- pause / resume controls with desktop notifications

This was designed as a *debuggable mind*, not a black box.

---

## 🧠 Architecture overview

High-level cognitive flow:
```text
Audio Input
↓
Voice Segmentation
↓
Lexical Recognition
↓
Working Memory
↓
Goal Evaluation
↓
Speech Planning
↓
Vocalization Output
```

Each stage is implemented as an independent module registered on a central relay bus.

---

## 🗂️ Project structure

```text
synapseos/
├── main.py # Core execution loop + live dashboard
├── config.py # Environment configuration
├── relay/
│ └── synapse_bus.py # Internal message bus
├── modules/
│ ├── audio/ # Microphone + STT pipeline
│ ├── core/ # Memory + goal evaluation
│ └── speech/ # Speech planning + emission
├── test_synapseos.py # End-to-end pipeline test
└── utils.py
```

---

## ▶️ Running it (experimental)

Requirements include:
- Python 3.x
- `whisper`, `transformers`, `torch`
- `sounddevice`, `numpy`, `rich`, `psutil`

Run:
```bash
python main.py
```
>⚠️ This is a live audio system. Expect experimental behavior.

### 🧪 What this project is not

- Not production-ready
- Not safety-hardened
- Not optimized for performance
- Not a finished assistant

This repo exists as:

- a learning artifact
- an architectural prototype
- a record of how the ideas evolved

### 💡 Why it’s archived
This project reached the point where:

- governance mattered
- autonomy needed constraints
- safety contracts were required
- determinism became important

Rather than patching endlessly, it was paused — and its ideas later informed more structured systems.

### 🧭 If revisited someday…
Potential next steps would include:

- persistent memory (SQLite / vector store)
- async task scheduling
- formal autonomy & safety contracts
- real TTS backend
- plugin-based module loading
- deterministic testing harness

## 🏷️ Status
Archived — but foundational.

This project represents a key stepping stone toward larger, more disciplined AI system design.

## Contribution Policy

Feedback, bug reports, and suggestions are welcome.

You may submit:

- Issues
- Design feedback
- Pull requests for review

However:

- Contributions do not grant any license or ownership rights
- The author retains full discretion over acceptance and future use
- Contributors receive no rights to reuse, redistribute, or derive from this code

---

## License
This project is not open-source.

It is licensed under a private evaluation-only license.
See LICENSE.txt for full terms.
