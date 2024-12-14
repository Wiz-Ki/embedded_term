import pyaudio
import numpy as np
from openwakeword.model import Model
import time
from playsound import playsound
import threading


class WakeWordDetector:
    def __init__(self, detection_threshold=0.5):
        # 오디오 설정
        self.CHUNK = 1280  # 공식 예제와 동일한 청크 사이즈
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 16000

        # 모델 초기화
        self.model = Model(
            #wakeword_models=["hey_jarvis"],
            wakeword_models=["hai_raje-beri.onnx"],
            inference_framework="onnx"
        )
        self.detection_threshold = detection_threshold
        self.is_running = True
        self.alert_sound = "mixkit-correct-answer-tone-2870.wav"
        self.detected_command = None

        # PyAudio 초기화
        self.audio = pyaudio.PyAudio()

    #sounddevice를 사용하여 소리 재생
    def play_alert(self):
        try:
            import sounddevice as sd
            import soundfile as sf

            # 알림음 파일 읽기
            data, samplerate = sf.read(self.alert_sound)
            sd.play(data, samplerate)
            sd.wait()  # 소리가 끝날 때까지 대기
        except Exception as e:
            print(f"알림음 재생 에러: {e}")

    def start(self):
        try:
            # 마이크 스트림 열기
            stream = self.audio.open(
                format=self.FORMAT,
                channels=self.CHANNELS,
                rate=self.RATE,
                input=True,
                frames_per_buffer=self.CHUNK
            )

            print("웨이크워드 감지 시작...")

            while self.is_running:
                try:
                    # 오디오 데이터 읽기
                    audio_data = np.frombuffer(
                        stream.read(self.CHUNK),
                        dtype=np.int16
                    )

                    # 예측
                    predictions = self.model.predict(audio_data)
                    pred_value = predictions["hai_raje-beri"]

                    # 높은 값만 출력
                    if pred_value > 0.1:  # 임계값 조정
                        print(f"Prediction value: {pred_value:.4f}")

                    # 웨이크워드 감지
                    if pred_value > self.detection_threshold:
                        print(f"Wake word detected! Confidence: {pred_value:.4f}")
                        threading.Thread(target=self.play_alert).start()
                        self.is_running = False
                        self.detected_command = True
                        break

                    time.sleep(0.01)  # CPU 부하 감소

                except Exception as e:
                    print(f"프레임 처리 중 에러: {e}")
                    continue

            print("웨이크워드 감지!")
            return self.detected_command

        except Exception as e:
            print(f"오디오 스트림 처리 에러: {e}")
            return None

        finally:
            # 스트림 정리
            stream.stop_stream()
            stream.close()
            self.audio.terminate()


def start_wake_word_detection():
    detector = WakeWordDetector(detection_threshold=0.5)
    return detector.start()


if __name__ == "__main__":
    Detect_command = start_wake_word_detection()
    print(Detect_command)