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
        TTS("null")
        while True:
            q.put((TTS(qtext.get())))


#tts모델의 초기 세팅은 여기에 넣어야 함
#"""<here>"""과 """</here>"""사이에 코드를 작성
"""<here>"""
import numpy as np
import soundfile as sf
from pydub import AudioSegment
from pydub.silence import detect_nonsilent


from pydub import AudioSegment
import numpy as np

def trim_silence_from_audio(audio, sr, silence_thresh=-40, min_silence_len=200, padding_ms=50):
    # float32 → int16 변환
    if audio.dtype != np.int16:
        audio_int16 = (audio * 32767).astype(np.int16)
    else:
        audio_int16 = audio

    # AudioSegment 변환
    if audio_int16.ndim == 1:
        audio_segment = AudioSegment(
            audio_int16.tobytes(),
            frame_rate=sr,
            sample_width=2,
            channels=1
        )
    else:
        audio_segment = AudioSegment(
            audio_int16.tobytes(),
            frame_rate=sr,
            sample_width=2,
            channels=audio_int16.shape[1]
        )

    nonsilence_ranges = detect_nonsilent(
        audio_segment,
        min_silence_len=min_silence_len,
        silence_thresh=silence_thresh
    )
    if len(nonsilence_ranges) == 0:
        return audio
    start_trim = max(0, nonsilence_ranges[0][0] - padding_ms)
    end_trim = min(len(audio_segment), nonsilence_ranges[-1][1] + padding_ms)
    trimmed = audio_segment[start_trim:end_trim]
    y = np.array(trimmed.get_array_of_samples())
    if trimmed.channels == 2:
        y = y.reshape((-1, 2))
    y = y.astype(np.float32) / 32767
    return y

from kokoro import KPipeline
import soundfile as sf
import torch
pipeline = KPipeline(lang_code='a')
"""</here>"""
    
def TTS(text): #실제 tts 코드 작성하면 됨
    wav = text
    print(f"[TTS] {text} << writing")
    try:
        #"""<here>"""과 """</here>"""사이에 코드를 작성
        """<here>"""
        text = text
        generator = pipeline(text, voice='af_heart')
        for i, (gs, ps, audio) in enumerate(generator):
            #print(i, gs, ps)
            #display(Audio(data=audio, rate=24000, autoplay=i==0)) 
            if hasattr(audio, "numpy"):
                audio = audio.numpy()
            else:
                audio = np.array(audio)
            audio = trim_silence_from_audio(audio, 24000)
            sf.write(f'cache/{text}.wav', audio, 24000)
        """</here>"""
        print(f"[TTS] {text} >> done! :)")
    except:
        print(f"[TTS] {text} >> errer! :(")
    return text