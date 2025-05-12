import time

def measure_input_duration(start_time: float) -> float:
    """입력 시작 시각(start_time)부터 현재 시각까지 걸린 시간을 초 단위로 반환."""
    end_time = time.time()
    return round(end_time - start_time, 2)
