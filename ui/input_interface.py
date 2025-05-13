import time
import threading
import gradio as gr

start_time = None
running = False
live_timer_text = ""

def start_timer():
    global start_time, running
    start_time = time.time()
    running = True
    return gr.update(value="⏳ 진행 중: 0.00초")

def update_timer():
    global start_time, running
    while running:
        elapsed = time.time() - start_time
        time.sleep(0.1)
        yield f"⏳ 진행 중: {elapsed:.2f}초"

def end_timer(text):
    global start_time, running
    running = False
    if start_time is None:
        return "", "", "⚠ 먼저 입력창을 클릭해 입력을 시작하세요."

    elapsed = time.time() - start_time
    return "", f"**⏱ 소요 시간:** {elapsed:.2f}초", f"**📝 입력한 내용:** {text}"

def build_interface():
    with gr.Blocks() as demo:
        gr.Markdown("### 🧪 SLPR Demo: 입력 시간 측정기")

        with gr.Row():
            txt_input = gr.Textbox(
                placeholder="텍스트를 입력하고 Enter 키를 누르세요",
                show_label=False,
                lines=1,
                elem_id="input-box"
            )
            btn_submit = gr.Button("▶")

        live_timer = gr.Markdown(value="")
        output_time = gr.Markdown()
        output_text = gr.Markdown()

        # 타이머 시작
        txt_input.focus(start_timer, outputs=live_timer)
        # 실시간 타이머 업데이트
        txt_input.change(update_timer, outputs=live_timer)
        # 입력 제출
        txt_input.submit(end_timer, inputs=txt_input, outputs=[live_timer, output_time, output_text])
        btn_submit.click(end_timer, inputs=txt_input, outputs=[live_timer, output_time, output_text])

    return demo
