# app.py

from ui.input_interface import build_interface
import threading
from tts.tts import run

#tts모델을 쓰레드에 미리 올려둠
t = run()
t.start()

#화면 출력
if __name__ == "__main__":
    demo = build_interface()
    demo.launch()
