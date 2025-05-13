import time
import threading
import gradio as gr

start_time = None
running = False
current_timer_value = ""
timer_component = None

def start_timer():
    global start_time, running
    start_time = time.time()
    running = True

    # 타이머 쓰레드 시작
    def update_loop():
        global current_timer_value
        while running:
            elapsed = time.time() - start_time
            current_timer_value = f"⏳ 진행 중: {elapsed:.2f}초"
            if timer_component:
                timer_component.update(value=current_timer_value)
            time.sleep(0.1)

    threading.Thread(target=update_loop, daemon=True).start()
    return gr.update()

def end_timer(text):
    global start_time, running
    running = False
    if start_time is None:
        return "", "", "⚠ 먼저 입력창을 클릭해 입력을 시작하세요."

    elapsed = time.time() - start_time
    return "", f"**⏱ 소요 시간:** {elapsed:.2f}초", f"**📝 입력한 내용:** {text}"

def build_interface():
    global timer_component

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

        timer_component = gr.Markdown(value="")
        output_time = gr.Markdown()
        output_text = gr.Markdown()

        # 입력창 클릭 시 타이머 시작
        txt_input.focus(start_timer, outputs=timer_component)

        # 입력 종료 시 결과 출력
        txt_input.submit(end_timer, inputs=txt_input, outputs=[timer_component, output_time, output_text])
        btn_submit.click(end_timer, inputs=txt_input, outputs=[timer_component, output_time, output_text])

    return demo
