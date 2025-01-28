# HTX Assessment

This repository contains the codebase for the HTX assessment. 

## Table of Contents

## Full Directory Structure

## Pre-requisites

The following instructions are designed for use with Python 3.10.

Before starting, ensure that the necessary environment variables are properly configured. This is neccessary for (1) [Speech Recognition](#speech-recognition), (2) [Elasticsearch Cluster](#elasticsearch-cluster) and (3)[UI In Elasticsearch](#ui-in-elasticsearch).

1. Set up the following environment variables in a `.env` file located at the root of the repository:
```bash
# ============================
# Speech Recognition Configuration
# ============================

## Debugging
DEBUG=False

## Pre-trained model for speech recognition tasks
MODEL_NAME=facebook/wav2vec2-large-960h

## Logging
LOG_FILE=logs/app.log

# ============================
# Application Layer Configuration
# ============================

## Port number on which the speech recognition API will run
APP_PORT=8001

## Service Name identifier for the speech recognition API application
APP_NAME=asr-api

# ============================
# Elasticsearch Configuration
# ============================

## URL of the Elasticsearch host
ES_HOST=http://localhost:9200

## Name of the Elasticsearch index for storing transcriptions
INDEX_NAME=cv-transcriptions

## Relative path to the CSV file containing transcription data
CSV_FILE_PATH=../asr/data/cv-valid-dev.csv
```

2. Load the environment variables into your current terminal session.
```bash
# Use allexport to export the environment variables
set -a
source .env
set +a

# To check the allexport status
# set -o | grep allexport
```

3. Verify that the environment variables have been loaded correctly.
```bash
printenv | grep -E 'DEBUG|MODEL_NAME|LOG_FILE|APP_PORT|APP_NAME|ES_HOST|INDEX_NAME|CSV_FILE_PATH'

# Expected Output
# DEBUG=False
# MODEL_NAME=facebook/wav2vec2-large-960h
# LOG_FILE=logs/app.log
# APP_PORT=8001
# APP_NAME=asr-api
# ES_HOST=http://localhost:9200
# INDEX_NAME=cv-transcriptions
# CSV_FILE_PATH=../asr/data/cv-valid-dev.csv
```

## Speech Recognition

### Project Directory Structure

The files and directories which might be relevant to this section of the project are as follows:
```
htx-assessment/
│
├── asr/
│   ├── cv-decode.py
│   ├── Dockerfile
│   ├── requirements-cvdecode.txt
│   ├── requirements.txt
│   ├── src/
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── asr_api.py
│   │   │   ├── constants.py
│   │   │   ├── dependencies.py
│   │   │   ├── exceptions.py
│   │   │   ├── logging_config.py
│   │   │   ├── middleware.py
│   │   │   ├── routes.py
│   │   │   └── schemas.py
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   └── factory.py
│   │   ├── speech_recognition/
│   │   │   ├── __init__.py
│   │   │   ├── asr_logic.py
│   │   │   └── model.py
│   │   └── __init__.py
│   └── data/
│       ├── cv-valid-dev/
│       │    ├── .placeholder
│       │    └── ...
│       └── cv-valid-dev.csv
│
├── .env
├── .gitignore
└── README.md
```

### Overview

The following instructions is to (1) set up the speech recognition tool using Facebook's [wave2vec2](https://huggingface.co/facebook/wav2vec2-large-960h), serve the tool via an API using FastAPI, package the API as a Docker image locally and (2) apply transcription on a set of mp3 files from the [Common Voice](https://www.kaggle.com/datasets/mozillaorg/common-voice) dataset.

**Note**: _Although this setup assumes the use of Podman, Docker can be used interchangeably here due to Podman's Docker-compatible CLI. However, Podman is recommended as it is free for commercial use and operates without a central daemon. This daemonless architecture enhances security and supports rootless container management. Please note that due to time constraints, the following instructions have not been tested with Docker, but testing and validation are planned in the future._

### Containerisation

1. Navigate to `asr` directory (from the root of the repository).
```bash
cd asr
```

2. Build the Docker image.
```bash
podman build -t ${APP_NAME} .
```

3. List your Podman images to confirm the build was successful.
```bash
podman images
```

4. Run the Docker container.
```bash
podman run -d --name ${APP_NAME} -p ${APP_PORT}:${APP_PORT} ${APP_NAME}
```

5. To verify the health of the application, run the following `curl` command:
    ```bash
    curl -X GET "http://localhost:8001/ping"
    ```

    Upon successful execution, a string response similar to the following should be received:
    ```bash
    "pong"
    ```

6. To test the application locally, run the following `curl` command:
    ```bash
    curl -F 'file=@data/path/to/sample.mp3' "http://localhost:8001/asr"
    ```

    Upon successful execution, a JSON response similar to the following should be received:
    ```json
    {
        "request_id": "unique-request-id",
        "transcription": "TRANSCRIBED-TEXT",
        "duration": "4.464"
    }
    ```

    The `transcription` field will contain the transcribed text from the audio file, and the `duration` field will contain the duration of the audio file in seconds. The `request_id` field will contain a unique identifier for the request, used for tracing and debugging purposes.

### Running the Model on Common Voice Locally

1. Download the [Common Voice](https://www.kaggle.com/datasets/mozillaorg/common-voice) dataset from [here](https://www.dropbox.com/scl/fi/i9yvfqpf7p8uye5o8k1sj/common_voice.zip?rlkey=lz3dtjuhekc3xw4jnoeoqy5yu&dl=0) and extract the contents from `cv-valid-dev` directory and `cv-valid-dev.csv` file to `data` directory.

2. Create and activate a virtual environment from the `asr` directory.
```bash
python3.10 -m venv venv
source venv/bin/activate
``` 

3. Install the required dependencies.
```bash
pip install -r requirements-cvdecode.txt
```

4. Make sure the Docker container for the speech recognition API is running. If not, follow the steps in the [Containerisation](#containerisation) section. 

5. Run the `cv-decode.py` script to transcribe each audio file from the `data/cv-valid-dev` directory and upload its transcribed words and duration into the `data/cv-valid-dev.csv` file.
```bash
python cv-decode.py --data-dir ./data/cv-valid-dev --csv-file ./data/cv-valid-dev.csv  --api-url http://localhost:8001/asr
```

6. [Optional] Verify the transcriptions.
```bash
head -n 5 ./data/cv-valid-dev.csv
```

7. [Optional] Deactivate the virtual environment.
```bash
deactivate
```

## Elasticsearch Cluster

### Project Directory Structure

The files and directories which might be relevant to this section of the project are as follows:
```
htx-assessment/
│
├── asr/
│   └── data/
│       └── cv-valid-dev.csv
│
├── elastic-backend/
│   ├── cv-index.py
│   ├── docker-compose.yaml
│   ├── logging_config.py
│   └── requirements.txt
│
├── .env
├── .gitignore
└── README.md
```

### Overview

The following instructions are to (1) set up an Elasticsearch cluster, (2) create an index in the cluster, and (3) index the transcriptions from the Common Voice dataset into the Elasticsearch cluster.

**Note**: _While these instructions are designed for use with Podman, Podman commands and Podman-Compose are assumed throughout, Docker can generally be used as a substitute due to Podman's compatibility as a drop-in replacement for Docker in most standard container operations (and in this context). However, please be aware that due to limited time, these instructions have not been specifically tested with Docker. Users may need to adjust certain commands or configurations to ensure compatibility._

### Setting Up the Elasticsearch Cluster

1. Navigate to `elastic-backend` directory (from the root of the repository).
```bash
cd elastic-backend
```

2. Create and activate a virtual environment from the `elastic-backend` directory.
```bash
python3.10 -m venv venv-es
source venv-es/bin/activate
``` 

3. Install the required dependencies.
```bash
pip install -r requirements.txt
```

4. Start Elasticsearch Cluster.
```bash
podman-compose up -d
```

5. To verify the health of the Elasticsearch cluster, run the following `curl` command:
```bash
curl -X GET "http://localhost:9200/_cluster/health?pretty"
```

6. Create the `cv-transcriptions` index in the Elasticsearch cluster and index the speech recongition data.
```bash
python cv-index.py
```

7. [Optional] To verify that the `cv-transcriptions` index and its data is successfully set up in the Elasticsearch cluster, run the following `curl` command:
```bash
curl -X GET "http://localhost:9200/cv-transcriptions/_search?pretty&q=*:*"
```

8. [Optional] Deactivate the virtual environment.
```bash
deactivate
```

## UI in Elasticsearch

### Setting Up the UI for  Cluster

1. Navigate to `search-ui` directory (from the root of the repository).
```bash
mkdir search-ui
cd search-ui
```

2. Initialize a new React project.
```bash
npm init -y
```

3. Install the required dependencies.
```bash
npm install react@18 react-dom@18 @testing-library/react @testing-library/jest-dom @testing-library/user-event web-vitals
```

4. Install the `react-scripts` package.
```bash
npm install react-scripts
```