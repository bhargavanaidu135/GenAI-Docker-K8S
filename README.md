# Deploying a Local LLM powered- Dockerfile & k8S YAML generator with FLASK api & webUI 

This project is aimed to generate docker and k8s dynamic config files locally by setting up local LLMs with to keep the organization's privacy and security.

## Table of Contents:

1. [Setup a Virtual Machine (VM) for running LLM](#setup-a-VM-based-on-LLM)
2. [Install required dependencies](#install-required-dependencies)
3. [Create Flask REST API and webUI](#create-flask-rest-api--webui-for-user-interaction)
4. [Run the flask app and access webUI via browser](#run-the-flask-app--access-webui-via-browser)

   Must allow the port that you exposed the app on.(eg: 5000

Pre-Requisites:
- A Virtual Machine (Required based on model you use for running)
- knowledge of html and Python Flask REST API
-  
STEP1:
## Setup a VM based on LLM

Get the VM which is suitable for your LLM that you are planning to run. Must choose the RAM and CPU or GPU purpose computation to see the significant performance while running the model.

STEP2: 
## Install required dependencies

Ollama environment:
```
curl -fsSL https://ollama.ai/install.sh | sh
ollama pull llama3
ollama run llama3

# Ensure the ollama is running (exposed ollama API)
curl http://localhost:11434 
```
Python Setup:

```
python -m venv <EnvName>
source <EnvName>/bin/activate  # (Linux/macOS)
pip3 install ollama
```

STEP3: 
## Create Flask REST API and webUI for User Interaction

Goto 'FlaskAPI-webUI-LLM' folder --> you would see the files LLM_WebUI_k8sDockerGen.py, requirements.txt, templates/index.html that contains the code for making flaskAPI and webUI for seamless user interactions.

STEP4: 
## Run the Flask App and Access webUI via browser

```
python3 flaskapi-webui.py
```
Access the app via ```<YourVM_IP_address>:<port>```

![webUI-flask](https://github.com/user-attachments/assets/1f6a9baf-c005-4c7d-a0a1-39a2c1c8b72f)


