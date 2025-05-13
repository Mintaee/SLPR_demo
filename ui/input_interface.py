# ui/input_interface.py

import time
import gradio as gr

start_time = None  # 전역변수로 입력 시작 시간 기록

def start_timer():
    global start_time
    start_time = time.time()
    return "입력을 시작하세요."

def end_timer(text):
    global start_time
    if start_time is None:
        return "먼저 시작 버튼을 누르세요.", None
    elapsed = time.time() - start_time
    return f"입력된 텍스트: {text}", f"소요 시간: {elapsed:.2f}초"

def build_interface():
    with gr.Blocks() as demo:
        gr.Markdown("### ⌛ SLPR Demo: 입력 시간 측정기")

        btn_start = gr.Button("입력 시작")
        txt_input = gr.Textbox(placeholder="여기에 텍스트 입력", lines=2)
        btn_submit = gr.Button("엔터 (입력 완료)")

        output_text = gr.Textbox(label="입력 내용")
        output_time = gr.Textbox(label="소요 시간")

        # 버튼 이벤트 연결
        btn_start.click(fn=start_timer, outputs=output_text)
        btn_submit.click(fn=end_timer, inputs=txt_input, outputs=[output_text, output_time])

    return demo
