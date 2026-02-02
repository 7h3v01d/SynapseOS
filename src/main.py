# SynapseOS v2.3 - Core Execution Entry
# Author: Leon Priest
# Date: 2025-06-30

from relay.synapse_bus import SynapseRelay
from modules.audio.voice_segmenter import VoiceSegmenter
from modules.audio.lexical_recognizer import LexicalRecognizer
from modules.speech.broca_compiler import BrocaCompiler
from modules.speech.vocalization_emitter import VocalizationEmitter
from modules.core.working_memory_queue import WorkingMemoryQueue
from modules.core.goal_evaluator import GoalEvaluator
from modules.audio.audio_listener import AudioListener

from rich.live import Live
from rich.table import Table
from rich.console import Console
from rich.panel import Panel
from rich.layout import Layout
from rich.align import Align
from datetime import datetime
import threading
import logging
import psutil
import numpy as np
import sounddevice as sd
import time
import keyboard
from plyer import notification

# Setup logging to file
logging.basicConfig(filename="log.txt", level=logging.DEBUG, format="%(asctime)s - %(message)s")

# Console for pretty printing
console = Console()

# Initialize Core Relay Bus
bus = SynapseRelay()

# Load Cognitive Modules
memory = WorkingMemoryQueue()
goals = GoalEvaluator()
segmenter = VoiceSegmenter()
recognizer = LexicalRecognizer()
planner = BrocaCompiler()
emitter = VocalizationEmitter()

# Register modules to the message bus
bus.register("segmenter", segmenter)
bus.register("recognizer", recognizer)
bus.register("memory", memory)
bus.register("goals", goals)
bus.register("planner", planner)
bus.register("emitter", emitter)

# Setup AudioListener
listener = AudioListener(model_size="base", memory=memory)

# State
latest_updates = {
    "Input": "",
    "Tokens": "",
    "Lexemes": "",
    "Intent": "",
    "Response": ""
}
log_history = []
paused_flag = {"value": False}
waveform_value = 0

# Colors per step
color_map = {
    "Input": "cyan",
    "Tokens": "green",
    "Lexemes": "blue",
    "Intent": "yellow",
    "Response": "magenta",
    "System": "bright_black"
}

def create_status_table():
    table = Table(show_header=True, header_style="bold white")
    table.add_column("Timestamp", width=20)
    table.add_column("Step", width=12)
    table.add_column("Content", overflow="fold")
    for key, value in latest_updates.items():
        color = color_map.get(key, "white")
        content = value if value else "[dim]waiting...[/dim]"
        table.add_row(datetime.now().strftime("%H:%M:%S"), f"[{color}]{key}[/{color}]", content)
    return table

def create_log_history_table():
    table = Table(show_header=True, header_style="dim")
    table.add_column("Time", width=8)
    table.add_column("Tag", width=10)
    table.add_column("Message", overflow="fold")
    for t, tag, msg in reversed(log_history[-20:]):
        color = color_map.get(tag, "white")
        table.add_row(t.strftime("%H:%M:%S"), f"[{color}]{tag}[/{color}]", msg)
    return table

def get_system_stats():
    cpu = psutil.cpu_percent()
    mem = psutil.virtual_memory()
    return f"CPU: {cpu}% | RAM: {mem.percent}%"

def audio_meter_callback(indata, frames, time_info, status):
    global waveform_value
    volume_norm = np.linalg.norm(indata) * 10
    waveform_value = min(100, int(volume_norm))

def start_audio_meter():
    stream = sd.InputStream(callback=audio_meter_callback)
    stream.start()
    return stream

def create_waveform_panel():
    filled = int((waveform_value / 100) * 40)
    bar = "█" * filled + " " * (40 - filled)
    return Panel(
        f"[red]{bar}[/red] {waveform_value}%",
        title="Audio Activity",
        border_style="cyan"
    )

def build_layout():
    layout = Layout()
    layout.split_column(
        Layout(name="main", ratio=3),
        Layout(name="log", ratio=2),
        Layout(name="bottom", ratio=1)
    )
    layout["bottom"].split_row(
        Layout(name="stats"),
        Layout(name="waveform")
    )

    status = "⏸ Paused" if paused_flag["value"] else "▶️ Listening"
    status_color = "red" if paused_flag["value"] else "green"

    layout["main"].update(Panel(create_status_table(), title=f"[{status_color}]{status}[/{status_color}]", border_style="white"))
    layout["log"].update(Panel(create_log_history_table(), title="Scrollback Log", border_style="dim"))
    layout["stats"].update(Panel(get_system_stats(), title="System Stats", border_style="bright_black"))
    layout["waveform"].update(create_waveform_panel())
    return layout

def log_and_display(tag, message):
    latest_updates[tag] = message
    log_history.append((datetime.now(), tag, message))
    if len(log_history) > 100:
        log_history.pop(0)
    logging.info(f"[{tag}] {message}")

def process_transcribed_text(text: str):
    log_and_display("Input", text)
    tokens = bus.send("segmenter", "process", text)
    log_and_display("Tokens", str(tokens))

    lexemes = bus.send("recognizer", "recognize", tokens)
    log_and_display("Lexemes", str(lexemes))

    bus.send("memory", "store", lexemes)

    intent = bus.send("goals", "evaluate", lexemes)
    log_and_display("Intent", str(intent))

    response = bus.send("planner", "synthesize", intent)
    log_and_display("Response", response)

    bus.send("emitter", "speak", response)

def monitor_keyboard():
    last_state = False
    while True:
        current_state = keyboard.is_pressed('p')
        if current_state and not last_state:
            paused_flag["value"] = not paused_flag["value"]
            state = "PAUSED" if paused_flag["value"] else "RESUMED"
            log_and_display("System", f"Audio {state}")
            notification.notify(
                title="SynapseOS",
                message=f"Audio {state}",
                app_name="SynapseOS",
                timeout=2
            )
            bus.send("emitter", "speak", f"Audio {state.lower()}")
        last_state = current_state
        time.sleep(0.1)

threading.Thread(target=monitor_keyboard, daemon=True).start()

def run_audio_loop():
    console.print("\n🎤 [bold green]SynapseOS is listening for real-time speech...[/bold green]\n")
    meter_stream = start_audio_meter()

    with Live(build_layout(), refresh_per_second=4, console=console, screen=True) as live:
        with listener:
            for transcript in listener.listen_generator():
                if not paused_flag["value"]:
                    process_transcribed_text(transcript)
                live.update(build_layout())

if __name__ == "__main__":
    run_audio_loop()
