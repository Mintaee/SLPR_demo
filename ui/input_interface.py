import time
import threading
import gradio as gr
from tts.tts import tts
from tts.tts import getQ

start_time = None
running = False

textArr = []#현제 입력하고 있는 text
TTSTokkenI = 0#입력된 가장 끝의 토큰 수

def reset_inputs():
    return ""  # txt_input의 값을 빈 문자열로

def start_timer():
    global start_time, running
    global textArr
    global TTSTokkenI

    start_time = time.time()
    running = True
    return gr.update(value="⏳ 진행 중: 0.00초")

def update_timer():
    global start_time, running

    while running:
        elapsed = time.time() - start_time
        time.sleep(0.1)
        yield f"⏳ 진행 중: {elapsed:.2f}초"

def set_text2TTS():
    textArr = []
    TTSTokkenI = 0

def update_text2TTS(numText,text,history):#실시간으로 input을 할때에 실행된는 함수 numText(끊어서 쓰는 숫자 input)
    global textArr
    global TTSTokkenI
    num = 1

    #print(numText,text,TTSTokkenI)
    try:
        num = int(numText)
    except:
        #print("is not num")
        num = 1
    try:
        if(textArr != run_tts_tokkenize(text)):
            TTSTokkenI += 1
        textArr = run_tts_tokkenize(text)
        if(TTSTokkenI == num):
            TTSTokkenI = 0
            textToTTS = ""#tts에 넣을 토큰
            for j in range(num):
                #print(j-num, textArr)
                textToTTS = textToTTS + " "+textArr[j-num] #tts에 넣을 num만큼의 토큰
            threading.Thread(target=run_tts_background, args=(textToTTS,), daemon=True).start()
    except:
        textArr = []
        TTSTokkenI = 0


def end_text2TTS(text):
    global textArr

    AllTextArr = text.split(" ")
    lastText = ""
    for j in range(len(AllTextArr)-len(textArr)):
        lastText = AllTextArr[-j-1] + " " +lastText
    run_tts_background(lastText)

def run_tts_tokkenize(text):
    textArr = text.split(" ")
    return textArr[:-2]
def run_tts_background(text):
    t = tts(text)
    t.start()
    t.join()
    
def end_timer(text, history):
    global start_time, running
    running = False

    if start_time is None:
        return history, "", "⚠ 먼저 입력창을 클릭해 입력을 시작하세요.", gr.update(value="")
    
    global textArr
    
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

def getAudio(text,history):
    a = getQ()
    '''
    while a == None:
        a = getQ()
    '''
    x,y,z,w = end_timer(a, history)
    return f"cache/{a}.wav",x,z
def build_interface():
    with gr.Blocks() as demo:
        gr.Markdown("### 🧪 SLPR Demo: 입력 시간 측정기")

        history_state = gr.State([])

        with gr.Row():
            txt_input = gr.Textbox(
                placeholder="텍스트를 입력하고 Enter 키를 누르세요",
                show_label=False,
                lines=1,
                every=0.1,
                elem_id="input-box",
            )
            btn_submit = gr.Button("▶")
            num_input = gr.Textbox(
                placeholder="숫자를 입력하세요",
                label="숫자",
                type="text"
            )

        live_timer = gr.Markdown(value="")
        output_log = gr.Markdown(value="")

        #오디오 출력
        output_audio = gr.Audio(label="음성 출력", type="filepath", autoplay=True)
        output_audio.stop(
            fn=getAudio,
            inputs=[txt_input, history_state],
            outputs=[output_audio,history_state, output_log]            
        )
        # 타이머 시작
        txt_input.focus(fn=start_timer, outputs=live_timer)
        txt_input.focus(fn=set_text2TTS)
        txt_input.focus(fn=reset_inputs,outputs=txt_input)
        txt_input.focus(
            fn=getAudio,
            inputs=[txt_input, history_state],
            outputs=[output_audio,history_state, output_log]            
        )

        # 실시간 타이머 업데이트
        txt_input.change(fn=update_timer,
                          outputs=live_timer,
                        )
        txt_input.change(fn=update_text2TTS,
                    inputs=[num_input,txt_input,history_state]
                )
        

        # 포커스 해제 시 타이머 정지
        txt_input.blur(fn=stop_timer, outputs=live_timer)

        
        # 입력 제출: 결과 누적 + 타이머 리셋 + 입력창 초기화
        '''
        txt_input.submit(
            fn=end_timer,
            inputs=[txt_input, history_state],
            outputs=[history_state, live_timer, output_log, txt_input]
        )
        '''
        txt_input.submit(
            fn=end_text2TTS,
            inputs=[txt_input]
        )
        
        '''
        btn_submit.click(
            fn=end_timer,
            inputs=[txt_input],
            outputs=[history_state, live_timer, output_log, txt_input]
        )
        '''
        
        

    return demo
