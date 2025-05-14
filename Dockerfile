# Dockerfile
FROM python:3.8-slim
LABEL authors="ki"

# 시스템 패키지 설치
RUN apt-get update && \
    apt-get install -y \
    portaudio19-dev \
    libsndfile1 \
    gcc \
    python3-dev \
    libasound2-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 오디오 그룹 및 사용자 설정
RUN groupadd -r audio || true
RUN useradd -r -g audio audiouser || true

# 작업 디렉터리 설정
WORKDIR /app

# 필요한 라이브러리 설치 (순서 중요)
COPY requirements.txt /app/

# PyAudio와 Sounddevice를 먼저 설치
RUN pip install --no-cache-dir PyAudio sounddevice

# 나머지 패키지 설치
RUN pip install --no-cache-dir -r requirements.txt

# 어플리케이션 코드 복사
COPY . /app

# 음성 파일 저장 디렉토리 생성 및 권한 설정
RUN mkdir -p korean && \
    chown -R audiouser:audio /app

# audiouser로 전환
USER audiouser

# 컨테이너 실행시 자동으로 실행될 명령어
ENTRYPOINT ["python", "main.py"]