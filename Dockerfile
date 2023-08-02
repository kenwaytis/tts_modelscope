FROM paidax/dev-containers:modelscope-v0.8

RUN pip install --no-cache-dir \
    loguru  \
    fastapi \
    uvicorn \
    pydantic==1.10.8  && \
    rm -rf /root/.cache/pip/* && \
    mkdir -p /home/tts

WORKDIR /home/tts
COPY . .

RUN python /home/tts/download_file.py
