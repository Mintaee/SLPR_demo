import threading #비동기 모듈
import queue

q = queue.Queue()#tts 결과물
qtext  = queue.Queue()#tts에 넣을 text

#tts가 만든 결과물을 가져오는 함수, queue형태로 가장 오래된 결과부터 가져옴
def getQ()-> str:
    a = q.get()
    if a == None:
        print("[TTS] None")
    else:
        print(f"[TTS] {a} get")
    return a

#tts에 넣을 text를 받아오는 쓰레드
class tts(threading.Thread):
    def __init__(self, text, name=None):
        super().__init__(name=name)
        self.text = text.strip()#입력 들어올 text를 해당 쓰레드의 이름으로 명명한다.

    def run(self):
        qtext.put(self.text)
      
#tts모델을 background에 항상 실행 시키고 있는 쓰레드
class run(threading.Thread):
    def __init__(self, name=None):
        super().__init__(name=name)

    def run(self):
        while True:
            q.put((TTS(qtext.get())))


#tts모델의 초기 세팅은 여기에 넣어야 함
#"""<here>"""과 """</here>"""사이에 코드를 작성
"""<here>"""
import torch
from parler_tts import ParlerTTSForConditionalGeneration
from transformers import AutoTokenizer
import soundfile as sf

# ParlerTTS 모델 선언
device = "cuda:0" if torch.cuda.is_available() else "cpu"
model = ParlerTTSForConditionalGeneration.from_pretrained("parler-tts/parler-tts-mini-v1").to(device)
tokenizer = AutoTokenizer.from_pretrained("parler-tts/parler-tts-mini-v1")
"""</here>"""
    
def TTS(text): #실제 tts 코드 작성하면 됨
    wav = text
    print(f"[TTS] {text} << writing")
    try:
        #"""<here>"""과 """</here>"""사이에 코드를 작성
        """<here>"""
        # 음성으로 생성하고자 하는 텍스트
        prompt = text
        # 음성의 style을 지정하는 prompt
        description = "A female speaker delivers a slightly expressive and animated speech with a moderate speed and pitch The recording is of very high quality, with the speaker's voice sounding clear and very close up."

        input_ids = tokenizer(description, return_tensors="pt").input_ids.to(device)
        prompt_input_ids = tokenizer(prompt, return_tensors="pt").input_ids.to(device)

        generation = model.generate(input_ids=input_ids, prompt_input_ids=prompt_input_ids) # 음성 생성
        audio_arr = generation.cpu().numpy().squeeze()
        sf.write(f"cache/{text}.wav", audio_arr, model.config.sampling_rate) # 생성된 음성을 .wav파일로 저장
        """</here>"""
    except:
        print(f"[TTS] {text} >> errer! :(")

    print(f"[TTS] {text} >> done! :)")
    return text