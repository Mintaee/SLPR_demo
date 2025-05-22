import time
import threading
import gradio as gr
from tts.tts import tts
from tts.tts import getQ

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
        
def run_tts_background(text):
    t = tts(text)
    t.start()
    t.join()
    
def end_timer(text, history):
    global start_time, running
    running = False

    if start_time is None:
        return history, "", "⚠ 먼저 입력창을 클릭해 입력을 시작하세요.", gr.update(value="")
    
    
    #tts 변환
    threading.Thread(target=run_tts_background, args=(text,), daemon=True).start()
    #t = tts(text)
    #t.start()
    #t.join()#쓰레드가 끝날때 까지 기다리는 코드임

    elapsed = time.time() - start_time
    new_entry = f"**⏱ {elapsed:.2f}초** — {text}"
    history.append(new_entry)
    combined_output = "\n\n".join(history)

    # 타이머 초기화
    start_time = time.time()
    running = True

    return history, "⏳ 진행 중: 0.00초", combined_output, gr.update(value="")

def stop_timer():
    global running
    running = False
    return gr.update(value="⏹ 타이머 중단됨")

def build_interface():
    with gr.Blocks() as demo:
        gr.Markdown("### 🧪 SLPR Demo: 입력 시간 측정기")

        history_state = gr.State([])

        with gr.Row():
            txt_input = gr.Textbox(
                placeholder="텍스트를 입력하고 Enter 키를 누르세요",
                show_label=False,
                lines=1,
                elem_id="input-box"
            )
            btn_submit = gr.Button("▶")
            num_input = gr.Textbox(
                placeholder="숫자를 입력하세요",
                label="숫자",
                type="text"
            )

        live_timer = gr.Markdown(value="")
        output_log = gr.Markdown(value="")

        # 타이머 시작
        txt_input.focus(fn=start_timer, outputs=live_timer)

        # 실시간 타이머 업데이트
        txt_input.change(fn=update_timer, outputs=live_timer)

        # 포커스 해제 시 타이머 정지
        txt_input.blur(fn=stop_timer, outputs=live_timer)

        #오디오 출력
        output_audio = gr.Audio(label="음성 출력", type="filepath", autoplay=True)

        
        # 입력 제출: 결과 누적 + 타이머 리셋 + 입력창 초기화
        txt_input.submit(
            fn=end_timer,
            inputs=[txt_input, history_state],
            outputs=[history_state, live_timer, output_log, txt_input]
        )

        btn_submit.click(
            fn=end_timer,
            inputs=[txt_input, history_state],
            outputs=[history_state, live_timer, output_log, txt_input]
        )
        
        

    return demo
