# Docker - Ollama

Simple boilerplate for using Ollama with Docker


## 1. Prerequisite

- Ensure your GPU has at least 7GB of memory for using gpu option, otherwise you can use the cpu option

- Install the necessary NVIDIA drivers and CUDA toolkit


## 2. Requirements

- ollama-python
- ollama


## 3. Pull LLM weights

There are some examples:

- ollama pull llama3

- ollama pull llama3.1

- ollama pull gemma2

## 4. Build Ollama image

    docker build -t ollama . 
    
    (or use Dockerfile-cpu for the cpu option)

## 5. Copy the weight of models into your path

    cp -r /usr/share/ollama/.ollama/models ./ollama_models

## 6. Build client host for using Ollama Client/AsyncClient

    docker build -t ollama . 
    
    (or use docker-compose-cpu.yaml for the cpu option)

## Citation

If you find *Ollama* useful in your research, please consider to cite the following repo:

```

https://github.com/ollama/ollama

```
