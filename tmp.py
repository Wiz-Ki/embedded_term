import sounddevice as sd
import wave
import threading
from faster_whisper import WhisperModel

# 녹음 파라미터
SAMPLE_RATE = 16000
CHANNELS = 1
OUTPUT_FILENAME = "korean/command_voice.wav"  # 녹음된 파일 경로
recording = False  # 녹음 상태 플래그
audio_frames = []  # 녹음된 데이터 저장

# 녹음 시작 함수
def start_recording():
    global recording, audio_frames
    recording = True
    audio_frames = []
    print("Recording started. Press 'e' to stop.")
    with sd.InputStream(samplerate=SAMPLE_RATE, channels=CHANNELS, dtype='int16') as stream:
        while recording:
            data, _ = stream.read(1024)
            audio_frames.append(data)

# 녹음 종료 함수
def stop_recording():
    global recording
    recording = False
    print("Recording stopped. Saving...")
    # WAV 파일 저장
    with wave.open(OUTPUT_FILENAME, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(2)  # 16비트 오디오
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes(b"".join(audio_frames))
    print(f"File saved: {OUTPUT_FILENAME}")

    # 녹음 종료 후 자동으로 STT 실행
    return transcribe_audio(OUTPUT_FILENAME)

# STT 추론 함수
# model_size="tiny", "base", "small", "medium", "large-v3"
def transcribe_audio(filename, model_size="base"):
    print(f"Transcribing {filename}...")
    model = WhisperModel(model_size, device="cpu", compute_type="int8")  # CPU에서 실행

    # Faster Whisper를 사용한 STT 실행
    segments, info = model.transcribe(
        filename,
        beam_size=5,
        vad_filter=True,
        vad_parameters=dict(min_silence_duration_ms=500),
        language="ko"
    )

    print("Detected language '%s' with probability %f" % (info.language, info.language_probability))
    
    result = []
    
    for segment in segments:
        result.append(segment.text)
        print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))
    return "".join(result)

# 녹음 제어 함수
def control_recording():
    global recording

    while True:
        command = input("Press 's' to start recording, 'e' to stop, or 'q' to quit: ").strip().lower()
        if command == "s" and not recording:
            threading.Thread(target=start_recording).start()  # 녹음을 별도 스레드에서 실행
        elif command == "e" and recording:
            return stop_recording()  # 녹음 종료 + STT 실행
        elif command == "q":
            if recording:
                return stop_recording()  # 녹음 중이라면 종료
            print("Exiting")
            break
        else:
            print("Invalid command. Use 's' to start, 'e' to stop, or 'q' to quit.")

# result = control_recording()
# print("result" , result)
