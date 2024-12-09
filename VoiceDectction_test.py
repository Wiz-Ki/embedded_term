import sounddevice as sd
import numpy as np

# 샘플링 레이트와 설정
SAMPLE_RATE = 16000  # 16kHz
THRESHOLD = 0.02  # 음성 에너지 임계값
SILENCE_DURATION = 1.0  # 말이 멈췄다고 간주하는 침묵 시간(초)


def audio_callback(indata, frames, time, status):
    global silence_start, recording

    # 에너지 계산 (RMS)
    volume_norm = np.linalg.norm(indata) / frames
    print(f"Current Volume: {volume_norm:.4f}")  # 볼륨 확인

    if volume_norm > THRESHOLD:
        silence_start = None
        print("음성 감지 중...")
    else:
        if silence_start is None:
            silence_start = time.currentTime
        elif time.currentTime - silence_start >= SILENCE_DURATION:
            print("말이 끝났습니다.")
            recording = False  # 녹음을 중단하도록 플래그 설정


# 전역 변수 초기화
silence_start = None
recording = True

print("음성을 입력하세요...")

# `sounddevice` 스트림 열기
with sd.InputStream(callback=audio_callback, channels=1, samplerate=SAMPLE_RATE):
    while recording:
        sd.sleep(100)  # 100ms 대기 (비동기 처리)

print("녹음이 종료되었습니다.")