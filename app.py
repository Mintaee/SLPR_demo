# app.py

from ui.input_interface import build_interface
import threading
from tts.tts import run


t = run()
t.start()
if __name__ == "__main__":
    demo = build_interface()
    demo.launch()
