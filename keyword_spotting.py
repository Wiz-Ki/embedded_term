import openwakeword
from openwakeword.model import Model
openwakeword.download_default_models()

import sounddevice as sd
import numpy as np
import time
from playsound import playsound
import threading
import subprocess



class WakeWordDetector:
    def __init__(self, detection_threshold=0.5):
        #pretrain된 wakeup call 모델 사용
        self.model = Model(wakeword_models=["hai_raje-beri.onnx"],
                           inference_framework = "onnx"  # 여기를 수정
        )
        self.detection_threshold = detection_threshold
        self.is_running = True
        self.alert_sound = "mixkit-correct-answer-tone-2870.wav"
        self.detected_command = None

    def process_audio(self, indata, frames, time, status):
        audio_data = indata.flatten().astype(np.float32)
        predictions = self.model.predict(audio_data)

        if predictions[0] > self.detection_threshold:
            threading.Thread(target=self.play_alert).start()
            self.is_running = False
            # 감지된 명령어에 따라 다른 값을 설정
            # 예시로 첫번째 웨이크워드를 감지하면 'command1' 반환
            self.detected_command = True

    def play_alert(self):
        try:
            playsound(self.alert_sound)
        except Exception as e:
            print(f"알림음 재생 에러: {e}")

    def start(self):
        try:
            with sd.InputStream(callback=self.process_audio,
                                channels=1,
                                samplerate=16000,
                                blocksize=480):
                print("웨이크워드 감지 시작...")
                while self.is_running:
                    time.sleep(0.1)
                print("웨이크워드 감지!")
                return self.detected_command
        except Exception as e:
            print(f"오디오 스트림 처리 에러: {e}")
            return None



def start_wake_word_detection():
    sd.default.device = (1, None)
    detector = WakeWordDetector(detection_threshold=0.5)
    return detector.start()


Detect_command = start_wake_word_detection()
print(Detect_command)