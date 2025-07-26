FROM python:3.12-slim

# Install system-level dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    bash \
    libportaudio2 \
    libportaudiocpp0 \
    portaudio19-dev \
    ffmpeg \
    libsndfile1 \
    git \
    curl \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Working directory (this will be overridden by your volume mount)
WORKDIR /app

# Copy requirements
COPY requirements.txt /tmp/requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip setuptools wheel \
 && pip install --prefer-binary numpy \
 && pip install --no-cache-dir -r /tmp/requirements.txt

# Watchdog for autoreload
# RUN pip install watchdog

EXPOSE 7860

# Copy entrypoint to a safe location not overridden by volumes
COPY entrypoint.sh /opt/entrypoint.sh
RUN chmod +x /opt/entrypoint.sh

ENTRYPOINT ["/opt/entrypoint.sh"]
