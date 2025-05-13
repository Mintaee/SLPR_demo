# ui/input_interface.py

import time
import gradio as gr

start_time = None  # 입력 시작 시간 저장용

def on_input_focus():
    global start_time
    start_time = time.time()
    return gr.update(), gr.update()

def on_submit(text):
    global start_time
    if start_time is None:
        return "", "⚠ 먼저 입력창을 클릭해 입력을 시작하세요."

    elapsed = time.time() - start_time
    return f"**📝 입력한 내용:** {text}", f"**⏱ 소요 시간:** {elapsed:.2f}초"

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

        output_text = gr.Markdown()
        output_time = gr.Markdown()

        # 이벤트 연결
        txt_input.focus(on_input_focus, outputs=[output_text, output_time])
        txt_input.submit(on_submit, inputs=txt_input, outputs=[output_text, output_time])
        btn_submit.click(on_submit, inputs=txt_input, outputs=[output_text, output_time])

    return demo
