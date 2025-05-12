from logic.input_timer import measure_input_duration
import time

start = time.time()
input("타이핑 시작 → Enter 키로 제출: ")
duration = measure_input_duration(start)

print(f"입력에 걸린 시간: {duration}초")
