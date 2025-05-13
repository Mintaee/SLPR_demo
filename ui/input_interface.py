import time
import threading
import gradio as gr

start_time = None
timer_thread = None
running = False

def start_timer():
    global start_time, running, timer_thread

    # 타이머 리셋
    start_time = time.time()
    running = True

    # 별도 쓰레드에서 타이머 업데이트
    def run_timer():
        while running:
            elapsed = time.time() - start_time
            timer_textbox.update(value=f"⏳ 진행 중: {elapsed:.2f}초")
            time.sleep(0.1)

    timer_thread = threading.Thread(target=run_timer, daemon=True)
    timer_thread.start()
    return gr.update()

def stop_timer_and_submit(text):
    global running, start_time
    running = False
    if start_time is None:
        return "", "", "⚠ 먼저 입력창을 클릭해 입력을 시작하세요."

    elapsed = time.time() - start_time
    return "", f"**⏱ 소요 시간:** {elapsed:.2f}초", f"**📝 입력한 내용:** {text}"

# 컴포넌트 선언을 함수 밖에서 해야 update() 접근 가능
with gr.Blocks() as demo:
    gr.Markdown("### ⌛ SLPR Demo: 입력 시간 측정기")

    with gr.Row():
        txt_input = gr.Textbox(
            placeholder="텍스트를 입력하고 Enter 키를 누르세요",
            show_label=False,
            lines=1,
        )
        btn_submit = gr.Button("▶")

    timer_textbox = gr.Textbox(label="", interactive=False)
    final_time = gr.Markdown()
    output_text = gr.Markdown()

    # 타이머 시작
    txt_input.focus(fn=start_timer, outputs=timer_textbox)

    # 제출 시
    txt_input.submit(fn=stop_timer_and_submit, inputs=txt_input, outputs=[timer_textbox, final_time, output_text])
    btn_submit.click(fn=stop_timer_and_submit, inputs=txt_input, outputs=[timer_textbox, final_time, output_text])
