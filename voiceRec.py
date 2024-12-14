import os
import time
import wave
import speech_recognition as sr

# 설정
SILENCE_THRESHOLD = 2  # 무음 시간 (초)
OUTPUT_DIR = "korean"

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

def save_audio(audio_data, output_filename):
    with open(output_filename, "wb") as f:
        f.write(audio_data.get_wav_data())

def main():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    print("녹음을 시작합니다. 아무 말도 하지 않으면 자동으로 저장됩니다.")

    recording = False
    start_time = None
    audio_data = None

    try:
        with mic as source:
            recognizer.adjust_for_ambient_noise(source)

            while True:
                print("음성을 감지 중...")
                try:
                    # 음성을 감지하여 녹음 시작
                    audio_data = recognizer.listen(source, timeout=SILENCE_THRESHOLD, phrase_time_limit=10)
                    print("음성을 감지했습니다.")
                    recording = True
                    start_time = time.time()

                except sr.WaitTimeoutError:
                    if recording:
                        print("무음이 감지되어 녹음을 종료합니다.")
                        break

    except KeyboardInterrupt:
        print("녹음을 중단합니다.")

    # 파일 저장
    if recording and audio_data:
        #timestamp = time.strftime("%Y%m%d-%H%M%S")
        #filename = os.path.join(OUTPUT_DIR, f"recording_{timestamp}.wav")
        filename = os.path.join(OUTPUT_DIR, f"command_voice.wav")
        save_audio(audio_data, filename)
        print(f"녹음이 저장되었습니다: {filename}")
    else:
        print("녹음된 내용이 없어 저장하지 않습니다.")

if __name__ == "__main__":
    main()
