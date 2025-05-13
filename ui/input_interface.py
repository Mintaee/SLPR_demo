import time
import gradio as gr

def start_timer():
    start_time = time.time()
    return start_time, f"⏳ 진행 중: 0.00초"

def update_timer(start_time):
    while True:
        elapsed = time.time() - start_time
        yield f"⏳ 진행 중: {elapsed:.2f}초"
        time.sleep(0.1)

def end_timer(text, start_time):
    if start_time is None:
        return "", "", "⚠ 먼저 입력창을 클릭해 입력을 시작하세요."
    
    elapsed = time.time() - start_time
    return "", f"**⏱ 소요 시간:** {elapsed:.2f}초", f"**📝 입력한 내용:** {text}"

def build_interface():
    with gr.Blocks() as demo:
        gr.Markdown("### 🧪 SLPR Demo: 입력 시간 측정기")

        start_state = gr.State(None)

        with gr.Row():
            txt_input = gr.Textbox(
                placeholder="텍스트를 입력하고 Enter 키를 누르세요",
                show_label=False,
                lines=1
            )
            btn_submit = gr.Button("▶")

        live_timer = gr.Textbox(label="", interactive=False)
        final_timer = gr.Markdown()
        output_text = gr.Markdown()

        # 입력창 클릭 시 타이머 시작
        txt_input.focus(fn=start_timer, outputs=[start_state, live_timer])

        # 실시간 타이머 갱신 (Live)
        with gr.Live() as live:
            live.stream(fn=update_timer, inputs=start_state, outputs=live_timer)

        # 제출 시 타이머 종료
        txt_input.submit(fn=end_timer, inputs=[txt_input, start_state], outputs=[live_timer, final_timer, output_text])
        btn_submit.click(fn=end_timer, inputs=[txt_input, start_state], outputs=[live_timer, final_timer, output_text])

    return demo
