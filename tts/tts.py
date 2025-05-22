import threading #비동기 모듈
import queue

q = queue.Queue()
textq = queue.Queue()

def getQ()-> str:
    a = q.get()
    b = textq.get()
    #print(f"[TTS] what {b}")
    while a != b:
        q.put(a)
        a = q.get()
    if a == None:
        print("[TTS] None")
    else:
        print(f"[TTS] {a} get")
    return a


class tts(threading.Thread):
    def __init__(self, text, name=None):
        super().__init__(name=name)
        self.text = text.strip()

    def run(self):
        textq.put(self.text)
        q.put(TTS(self.text))
      

#tts모델의 초기 세팅은 여기에 넣어야 함
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
    """<here>"""
    try:
        # 음성으로 생성하고자 하는 텍스트
        prompt = text
        # 음성의 style을 지정하는 prompt
        description = "A female speaker delivers a slightly expressive and animated speech with a moderate speed and pitch The recording is of very high quality, with the speaker's voice sounding clear and very close up."

        input_ids = tokenizer(description, return_tensors="pt").input_ids.to(device)
        prompt_input_ids = tokenizer(prompt, return_tensors="pt").input_ids.to(device)

        generation = model.generate(input_ids=input_ids, prompt_input_ids=prompt_input_ids) # 음성 생성
        audio_arr = generation.cpu().numpy().squeeze()
        sf.write(f"cache/{text}.wav", audio_arr, model.config.sampling_rate) # 생성된 음성을 .wav파일로 저장
    except:
        print(f"[TTS] {text} >> errer! :(")
    """</here>"""
    print(f"[TTS] {text} >> done! :)")
    return text