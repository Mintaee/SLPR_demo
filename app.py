# app.py

from ui.input_interface import build_interface
import threading
from tts.tts import run

import os
import signal

#ctrl + c 를 눌렀을때에 프로그램을 강제 종료 시켜버림
def signal_handler(sig, frame):
    print("Force killing everything.")
    os._exit(1)  # 즉시 프로세스 종료 (스레드 포함)

signal.signal(signal.SIGINT, signal_handler)
#tts모델을 쓰레드에 미리 올려둠
t = run()
t.start()

#화면 출력
if __name__ == "__main__":
    demo = build_interface()
    demo.launch()
