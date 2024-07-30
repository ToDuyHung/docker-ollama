FROM pytorch/pytorch:1.13.1-cuda11.6-cudnn8-runtime

WORKDIR /app

RUN curl -fsSL https://ollama.com/install.sh | sh
