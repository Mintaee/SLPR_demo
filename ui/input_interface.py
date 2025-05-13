import time
import threading
import gradio as gr

start_time = None
running = False

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

def end_timer(text, history):
    global start_time, running
    running = False

    if start_time is None:
        return history, "", "⚠ 먼저 입력창을 클릭해 입력을 시작하세요."

    elapsed = time.time() - start_time
    new_entry = f"**⏱ {elapsed:.2f}초** — {text}"
    history.append(new_entry)
    combined_output = "\n\n".join(history)

    return history, "", combined_output  # (상태, 실시간 타이머 초기화, 전체 결과 출력)

def build_interface():
    with gr.Blocks() as demo:
        gr.Markdown("### 🧪 SLPR Demo: 입력 시간 측정기")

        # 상태: 누적 입력 기록 리스트
        history_state = gr.State([])

        with gr.Row():
            txt_input = gr.Textbox(
                placeholder="텍스트를 입력하고 Enter 키를 누르세요",
                show_label=False,
                lines=1,
                elem_id="input-box"
            )
            btn_submit = gr.Button("▶")

        live_timer = gr.Markdown(value="")     # 실시간 타이머 출력
        output_log = gr.Markdown(value="")     # 누적 출력 결과

        # 타이머 시작
        txt_input.focus(fn=start_timer, outputs=live_timer)

        # 실시간 타이머 업데이트
        txt_input.change(fn=update_timer, outputs=live_timer)

        # 제출 시: 로그 누적 + 타이머 리셋 + 결과 출력
        txt_input.submit(
            fn=end_timer,
            inputs=[txt_input, history_state],
            outputs=[history_state, live_timer, output_log]
        )
        btn_submit.click(
            fn=end_timer,
            inputs=[txt_input, history_state],
            outputs=[history_state, live_timer, output_log]
        )

    return demo
