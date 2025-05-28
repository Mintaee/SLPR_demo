import time
import threading
import gradio as gr
from tts.tts import tts
from tts.tts import getQ

start_time = None #해당 토큰을 처리할 때의 시간 (종료시간 - 시작시간)을 이용하여 걸린 시간을 측정한다.
running = False #타이핑 하고 있는 중이면 running이 true가 된다.

textArr = []#현제 입력하고 있는 text
TTSTokkenI = 0#입력된 가장 끝의 토큰 수

def reset_inputs():
    return ""  # txt_input의 값을 빈 문자열로

#타이머를 초기화 하는 코드
def start_timer():
    global start_time, running
    global textArr
    global TTSTokkenI

    start_time = time.time()
    running = True
    return gr.update(value="⏳ 진행 중: 0.00초")

#타이머
def update_timer():
    global start_time, running

    while running:
        elapsed = time.time() - start_time
        time.sleep(0.1)
        yield f"⏳ 진행 중: {elapsed:.2f}초"

#text를 입력을 받기전에 전역변수들을 초기화 시켜줌
def set_text2TTS():
    textArr = []
    TTSTokkenI = 0

def update_text2TTS(numText,text,history):#실시간으로 input을 할때에 실행된는 함수 numText(끊어서 쓰는 숫자 input)
    global textArr
    global TTSTokkenI
    num = 1 #tts에 넣을 토큰 수

    #print(numText,text,TTSTokkenI)
    try:
        num = int(numText)
    except:
        #print("is not num")
        #만약에 숫자가 입렵 받지 않거나, 아무것도 입력하지 않는 경우 자동으로 1로 바꾼다.
        num = 1
    try: #토큰을 자르는 코드
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

#마지막에 enter를 누르고 난 후 num만큼의 토큰을 자르고 남은 토큰들을 모두 모아 tts 모델에 넣어줌
def end_text2TTS(text):
    global textArr

    AllTextArr = text.split(" ")
    lastText = "" #마지막 토큰들
    for j in range(len(AllTextArr)-len(textArr)):
        lastText = AllTextArr[-j-1] + " " +lastText
    run_tts_background(lastText)

#text를 스페이스를 기준으로 토크나이즈 한 후, list로 변환 해줌
def run_tts_tokkenize(text):
    textArr = text.split(" ")
    return textArr[:-2]#[-1]은 현제 입력하고 있는 곳이며, [-2]는 혹시 모를 backspace입력에 대비하여 여유를 남김

#text를 tts모델에 넣어줌, 가장 먼저 넣은 토큰이 가장 먼저 나오는 queue의 형태이며 getQ()를 통해 가져올 수 있다.
def run_tts_background(text):
    t = tts(text)
    t.start()
    t.join()

#해당 토큰이 처리가 끝나면, 그때 걸린 시간과, tts로 변환된 text를 화면에 표기해준다.
def end_timer(text, history):#history는 list(str)형태로, 전의 출력을 기록하고 있다.history에 이번에 적어야할 text를 뒤에 붙어간다.
    global start_time, running
    running = False

    if start_time is None:
        return history, "", "⚠ 먼저 입력창을 클릭해 입력을 시작하세요.", gr.update(value="")
    
    global textArr
    
    #t = tts(text)
    #t.start()
    #t.join()#쓰레드가 끝날때 까지 기다리는 코드임

    #text 업데이트
    elapsed = time.time() - start_time
    new_entry = f"**⏱ {elapsed:.2f}초** — {text}"
    history.append(new_entry)
    combined_output = "\n\n".join(history)

    # 타이머 초기화
    start_time = time.time()
    running = True

    return history, "⏳ 진행 중: 0.00초", combined_output, gr.update(value="")

#text를 치지 않고 있을 때의 타이머 중단
def stop_timer():
    global running
    running = False
    return gr.update(value="⏹ 타이머 중단됨")

#오디오 파일을 가져올 때에 타이머를 초기화 해줘야함
def getAudio(text,history):
    #오디오 파일 가져오기
    a = getQ()
    '''
    while a == None:
        a = getQ()
    '''
    #타이머 초기화
    x,y,z,w = end_timer(a, history)
    return f"cache/{a}.wav",x,z

#main 함수
def build_interface():
    with gr.Blocks() as demo:
        #text
        gr.Markdown("### 🧪 SLPR Demo: 입력 시간 측정기")

        history_state = gr.State([])
        #inputField들
        with gr.Row():
            # 문자열을 입력하는 곳
            txt_input = gr.Textbox(
                placeholder="텍스트를 입력하고 Enter 키를 누르세요",
                show_label=False,
                lines=1,
                every=0.1,
                elem_id="input-box",
            )
            btn_submit = gr.Button("▶")
            #숫자를 입력하는 곳 입력한 숫자 만큼의 토큰으로 잘려나감
            num_input = gr.Textbox(
                placeholder="숫자를 입력하세요",
                label="숫자",
                type="text"
            )
        #실시간 작성하고 있는 타이머
        live_timer = gr.Markdown(value="")
        #화면에 몇초 걸렸는지, 그리고 어떤 문자가 tts로 변화 되는지 보여주는 text
        output_log = gr.Markdown(value="")

        #오디오 출력
        output_audio = gr.Audio(label="음성 출력", type="filepath", autoplay=True)
        #소리 재생이 멈추면 그 다음의 wav파일을 찾음
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

        
        # 입력 제출: Enter키를 눌렀을때에 마지막으로 남은 토큰을 tts모델에 넣어줌
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
