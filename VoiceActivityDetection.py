import sounddevice as sd
import numpy as np


class VoiceDectation():

    def __init__(self):
        # 샘플링 레이트와 설정
        self.SAMPLE_RATE = 16000  # 16kHz
        self.THRESHOLD = 0.02  # 음성 에너지 임계값
        self.SILENCE_DURATION = 1.0  # 말이 멈췄다고 간주하는 침묵 시간(초)
        self.silence_start = None
        self.recording = True

        #start_dection()메소드 실행
        self.start_detection()

    def audio_callback(self, indata, frames, time, status):
        if not self.recording:  # recording이 False면 바로 리턴
            return

        # 에너지 계산 (RMS)
        volume_norm = np.linalg.norm(indata) / frames
        print(f"Current Volume: {volume_norm:.4f}")  # 볼륨 확인

        if volume_norm > self.THRESHOLD:
            self.silence_start = None
            print("음성 감지 중...")
        else:
            if self.silence_start is None:
                self.silence_start = time.currentTime
            elif time.currentTime - self.silence_start >= self.SILENCE_DURATION:
                print("말이 끝났습니다.")
                self.recording = False  # 녹음을 중단하도록 플래그 설정
                return  # 메시지 출력 후 바로 리턴

    def start_detection(self):
        # 전역 변수 초기화
        self.silence_start = None
        self.recording = True

        print("음성을 입력하세요...")

        # `sounddevice` 스트림 열기
        with sd.InputStream(callback=self.audio_callback, channels=1, samplerate=self.SAMPLE_RATE):
            while self.recording:
                sd.sleep(100)  # 100ms 대기 (비동기 처리)

        print("녹음이 종료되었습니다.")


if __name__ == "__main__":
    VoiceDectation()