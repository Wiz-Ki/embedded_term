import sounddevice as sd
import numpy as np
import wave
import os
import time
from faster_whisper import WhisperModel

# 설정
SAMPLE_RATE = 16000
CHANNELS = 1
CHUNK_SIZE = 1024
SILENCE_THRESHOLD = 0.03  # RMS 값 기준 무음 임계값 (환경에 따라 조정 필요)
SILENCE_DURATION = 2  # 무음 감지 시간 (초)
OUTPUT_DIR = "korean"
OUTPUT_FILENAME = os.path.join(OUTPUT_DIR, "command_voice.wav")

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)


def calculate_rms(audio_chunk):
    """오디오 청크의 RMS(Root Mean Square) 값 계산"""
    return np.sqrt(np.mean(np.square(audio_chunk)))


def is_silent(audio_chunk, threshold):
    """RMS 값을 기준으로 무음 여부 판단"""
    rms = calculate_rms(audio_chunk)
    return rms < threshold


def transcribe_audio(filename, model_size="small"):
    """WhisperModel을 사용하여 음성을 텍스트로 변환"""
    print(f"음성을 텍스트로 변환중...")
    model = WhisperModel(model_size, device="cpu", compute_type="int8")

    segments, info = model.transcribe(
        filename,
        beam_size=5,
        vad_filter=True,
        vad_parameters=dict(min_silence_duration_ms=500),
        language="ko"
    )

    print("감지된 언어: '%s' (확률: %f)" % (info.language, info.language_probability))

    result = []
    for segment in segments:
        result.append(segment.text)
        print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))

    return "".join(result)


def record_audio():
    """향상된 무음 감지 기능을 포함한 음성 녹음"""
    print("녹음을 시작합니다. 2초 동안 음성이 감지되지 않으면 자동으로 저장됩니다.")

    audio_frames = []
    silence_frames = 0
    is_recording = False
    voice_detected = False
    frames_to_keep = int(0.5 * SAMPLE_RATE / CHUNK_SIZE)  # 0.5초 분량의 프레임 보관
    initial_frames = []
    total_silence_frames = int(SILENCE_DURATION * SAMPLE_RATE / CHUNK_SIZE)

    # 음성 감지를 위한 초기 RMS 값들을 저장할 버퍼
    rms_buffer = []
    calibration_time = 1  # 1초 동안 주변 소음 레벨 측정
    calibration_frames = int(calibration_time * SAMPLE_RATE / CHUNK_SIZE)

    def audio_callback(indata, frames, time, status):
        nonlocal silence_frames, is_recording, voice_detected, rms_buffer
        if status:
            print(f"상태: {status}")

        current_rms = calculate_rms(indata)

        # 보정 단계
        if len(rms_buffer) < calibration_frames:
            rms_buffer.append(current_rms)
            initial_frames.append(indata.copy())
            return
        elif len(rms_buffer) == calibration_frames and not voice_detected:
            # 주변 소음 레벨의 평균과 표준편차 계산
            mean_rms = np.mean(rms_buffer)
            std_rms = np.std(rms_buffer)
            # 동적 임계값 설정 (평균 + 2 * 표준편차)
            dynamic_threshold = mean_rms + 2 * std_rms
            global SILENCE_THRESHOLD
            SILENCE_THRESHOLD = max(dynamic_threshold, SILENCE_THRESHOLD)
            print(f"보정된 무음 임계값: {SILENCE_THRESHOLD}")

        # 음성 감지 로직
        if not is_silent(indata, SILENCE_THRESHOLD):
            silence_frames = 0
            if not is_recording:
                is_recording = True
                voice_detected = True
                print("음성이 감지되었습니다.")
                # 이전 0.5초의 오디오도 포함
                audio_frames.extend(initial_frames[-frames_to_keep:])
        else:
            if is_recording:
                silence_frames += 1

        if is_recording:
            audio_frames.append(indata.copy())

        # 최근 프레임들 보관
        initial_frames.append(indata.copy())
        if len(initial_frames) > frames_to_keep:
            initial_frames.pop(0)

    # 스트림 설정 및 시작
    with sd.InputStream(samplerate=SAMPLE_RATE,
                        channels=CHANNELS,
                        callback=audio_callback,
                        blocksize=CHUNK_SIZE,
                        dtype=np.float32):

        print("음성을 감지하는 중...")

        try:
            while True:
                sd.sleep(100)

                # 녹음이 시작되었고 무음이 SILENCE_DURATION초 이상 지속되면 종료
                if is_recording and silence_frames >= total_silence_frames:
                    if voice_detected:  # 실제 음성이 감지된 경우에만 종료
                        print("무음이 감지되어 녹음을 종료합니다.")
                        break

        except KeyboardInterrupt:
            print("\n녹음이 중단되었습니다.")
            return None

    if not audio_frames or not voice_detected:
        print("녹음된 음성이 없습니다.")
        return None

    # 녹음된 오디오를 WAV 파일로 저장
    audio_data = np.concatenate(audio_frames, axis=0)
    with wave.open(OUTPUT_FILENAME, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(2)
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes((audio_data * 32767).astype(np.int16).tobytes())

    print(f"녹음이 저장되었습니다: {OUTPUT_FILENAME}")
    return OUTPUT_FILENAME


def voice_record_and_transcribe():
    """음성 녹음 및 STT 처리를 수행하는 메인 함수"""
    try:
        # 음성 녹음
        audio_file = record_audio()
        if audio_file:
            # STT 처리
            transcribed_text = transcribe_audio(audio_file)
            return transcribed_text
        return None

    except KeyboardInterrupt:
        print("\n녹음이 중단되었습니다.")
        return None
    except Exception as e:
        print(f"오류가 발생했습니다: {str(e)}")
        return None


if __name__ == "__main__":
    result = voice_record_and_transcribe()
    if result:
        print("\n변환된 텍스트:", result)