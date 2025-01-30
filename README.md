# HTX Assessment

This repository contains the codebase for the HTX assessment. 

## Table of Contents

- [Full Directory Structure](#full-directory-structure)
- [Pre-requisites](#pre-requisites)
- [Speech Recognition](#speech-recognition)
  - [Relevant Directories and Files](#relevant-directories-and-files)
  - [Overview](#overview)
  - [Containerisation](#containerisation)
  - [Running the Model on Common Voice Locally](#running-the-model-on-common-voice-locally)
- [Elasticsearch](#elasticsearch)
  - [Relevant Directories and Files](#relevant-directories-and-files-1)
  - [Overview](#overview-1)
  - [Setting Up the Elasticsearch Cluster and UI](#setting-up-the-elasticsearch-cluster-and-ui)

## Full Directory Structure

The full directory structure of the repository is as follows:
```
htx-assessment/
├── asr/                               # Automated Speech Recognition module
│   ├── cv-decode.py                   # Script to decode audio files and generate transcriptions
│   ├── Dockerfile                     # Docker configuration for the ASR module
│   ├── requirements-cvdecode.txt      # Python dependencies for cv-decode.py
│   ├── requirements.txt               # General Python dependencies for the ASR module
│   ├── src/                           # Source code for the ASR module
│   │   ├── api/                       # API-related code for the ASR service
│   │   │   ├── __init__.py            # Initializes the API package
│   │   │   ├── asr_api.py             # Defines API endpoints for speech recognition
│   │   │   ├── constants.py           # Constants used in the API
│   │   │   ├── dependencies.py        # Dependency injections for the API
│   │   │   ├── exceptions.py          # Custom exception handlers for the API
│   │   │   ├── logging_config.py      # Configures logging for the API
│   │   │   ├── middleware.py          # Middleware for request processing
│   │   │   ├── routes.py              # Defines API routes
│   │   │   └── schemas.py             # Data schemas for request and response validation
│   │   ├── core/                      # Core functionalities and configurations
│   │   │   ├── config.py              # Configuration settings for the ASR module
│   │   │   └── factory.py             # Factory patterns for creating instances
│   │   ├── speech_recognition/        # Speech recognition logic and models
│   │   │   ├── __init__.py            # Initializes the speech_recognition package
│   │   │   ├── asr_logic.py           # Core logic for speech recognition
│   │   │   └── model.py               # Speech recognition models and utilities
│   │   └── __init__.py                # Initializes the src package
│   └── data/                          # Data files used by the ASR module
│       ├── cv-valid-dev/              # Directory for Common Voice validation dataset
│       │    ├── .placeholder          # Placeholder file to ensure directory is tracked
│       │    └── ...                   # Additional data files
│       └── cv-valid-dev.csv           # CSV file containing metadata for Common Voice validation dataset
├── elastic-backend/                   # Backend services for Elasticsearch integration
│   ├── cv-index.py                    # Script to index data into Elasticsearch
│   ├── docker-compose.yaml            # Docker Compose configuration for Elasticsearch services
│   ├── logging_config.py              # Logging configuration for Elasticsearch backend
│   └── requirements.txt               # Python dependencies for Elasticsearch backend
├── search-ui/                         # Frontend application for search interface
│   ├── public/                        # Static assets (HTML, images, etc.)
│   │   └── ...
│   ├── src/                           # Source code for the React application
│   │   ├── App.js                     # Main React component
│   │   ├── index.js                   # Entry point for React application
│   │   └── ...
│   ├── Dockerfile                     # Dockerfile for building the search-ui container
│   ├── package.json                   # Yarn package configuration and dependencies
│   ├── yarn.lock                      # Yarn lock file for dependency versioning
│   └── ...
├── .gitignore                         # Specifies intentionally untracked files to ignore
└── README.md                          # Project documentation and instructions
```

## Pre-requisites

The following instructions are designed for use with Python 3.10.

Before starting, ensure that the necessary environment variables are properly configured. This is neccessary for (1) [Speech Recognition](#speech-recognition), (2) [Elasticsearch Cluster](#elasticsearch-cluster) and (3) [UI In Elasticsearch](#ui-in-elasticsearch).

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

## The base URL of the Elasticsearch cluster that the search-ui application (as a frontend container) connects to.
### Ensure that this matches the hostname of the Elasticsearch service in Docker Compose (if used).
REACT_APP_ELASTICSEARCH_HOST=http://elasticsearch-node1:9200
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
printenv | grep -E 'DEBUG|MODEL_NAME|LOG_FILE|APP_PORT|APP_NAME|ES_HOST|INDEX_NAME|CSV_FILE_PATH|REACT_APP_ELASTICSEARCH_HOST'

# Expected Output
# DEBUG=False
# MODEL_NAME=facebook/wav2vec2-large-960h
# LOG_FILE=logs/app.log
# APP_PORT=8001
# APP_NAME=asr-api
# ES_HOST=http://localhost:9200
# INDEX_NAME=cv-transcriptions
# CSV_FILE_PATH=../asr/data/cv-valid-dev.csv
# REACT_APP_ELASTICSEARCH_HOST=http://elasticsearch-node1:9200
```

## Speech Recognition

### Relevant Directories and Files

The directories and their files, relevant to this section, are as follows:
```
htx-assessment/
├── asr/                               # Automated Speech Recognition module
│   ├── cv-decode.py                   # Script to decode audio files and generate transcriptions
│   ├── Dockerfile                     # Docker configuration for the ASR module
│   ├── requirements-cvdecode.txt      # Python dependencies for cv-decode.py
│   ├── requirements.txt               # General Python dependencies for the ASR module
│   ├── src/                           # Source code for the ASR module
│   │   ├── api/                       # API-related code for the ASR service
│   │   │   ├── __init__.py            # Initializes the API package
│   │   │   ├── asr_api.py             # Defines API endpoints for speech recognition
│   │   │   ├── constants.py           # Constants used in the API
│   │   │   ├── dependencies.py        # Dependency injections for the API
│   │   │   ├── exceptions.py          # Custom exception handlers for the API
│   │   │   ├── logging_config.py      # Configures logging for the API
│   │   │   ├── middleware.py          # Middleware for request processing
│   │   │   ├── routes.py              # Defines API routes
│   │   │   └── schemas.py             # Data schemas for request and response validation
│   │   ├── core/                      # Core functionalities and configurations
│   │   │   ├── config.py              # Configuration settings for the ASR module
│   │   │   └── factory.py             # Factory patterns for creating instances
│   │   ├── speech_recognition/        # Speech recognition logic and models
│   │   │   ├── __init__.py            # Initializes the speech_recognition package
│   │   │   ├── asr_logic.py           # Core logic for speech recognition
│   │   │   └── model.py               # Speech recognition models and utilities
│   │   └── __init__.py                # Initializes the src package
│   └── data/                          # Data files used by the ASR module
│       ├── cv-valid-dev/              # Directory for Common Voice validation dataset
│       │    ├── .placeholder          # Placeholder file to ensure directory is tracked
│       │    └── ...
│       └── cv-valid-dev.csv           # CSV file containing metadata for Common Voice validation dataset
├── .env                               # Environment variables for the project
├── .gitignore                         # Specifies intentionally untracked files to ignore
└── README.md                          # Project documentation and instructions
```

### Overview

The following instructions are to:
1. Set up the speech recognition tool using Facebook's [wave2vec2](https://huggingface.co/facebook/wav2vec2-large-960h), serve the tool via an API using FastAPI and package the API as a Docker image locally, and
2. Apply transcription on a set of mp3 files from the [Common Voice](https://www.kaggle.com/datasets/mozillaorg/common-voice) dataset.

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

## Elasticsearch

### Relevant Directories and Files

The directories and their files, relevant to this section, are as follows:
```
htx-assessment/
├── asr/                       # Automated Speech Recognition module
│   └── data/
│       └── cv-valid-dev.csv   # CSV file containing valid development data
├── elastic-backend/           # Backend services for Elasticsearch integration
│   ├── cv-index.py            # Script to index data into Elasticsearch
│   ├── docker-compose.yaml    # Docker Compose configuration for Elasticsearch services
│   ├── logging_config.py      # Logging configuration for Elasticsearch backend
│   └── requirements.txt       # Python dependencies for Elasticsearch backend
├── search-ui/                 # Frontend application for search interface
│   ├── public/                # Static assets (HTML, images, etc.)
│   │   └── ...
│   ├── src/                   # Source code for the React application
│   │   ├── App.js             # Main React component
│   │   ├── index.js           # Entry point for React application
│   │   └── ...
│   ├── Dockerfile             # Dockerfile for building the search-ui container
│   ├── package.json           # Yarn package configuration and dependencies
│   ├── yarn.lock              # Yarn lock file for dependency versioning
│   └── ...
├── .env                       # Environment variables for the project
├── .gitignore                 # Specifies intentionally untracked files to ignore
└── README.md                  # Project documentation and instructions
```

### Overview

The following instructions are to: 
1. Set up an Elasticsearch cluster,
2. Create an index in the cluster, 
3. Create a search UI to query the index from the cluster, and 
4. Index the transcriptions from the Common Voice dataset into the cluster.

**Note**: _While these instructions are designed for use with Podman, Podman commands and Podman-Compose are assumed throughout, Docker can generally be used as a substitute due to Podman's compatibility as a drop-in replacement for Docker in most standard container operations (and in this context). However, please be aware that due to limited time, these instructions have not been specifically tested with Docker. Users may need to adjust certain commands or configurations to ensure compatibility._

### Setting Up the Elasticsearch Cluster and UI

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
podman-compose up -d --build
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

8. [Optional] Shut down the Elasticsearch cluster.
```bash
podman-compose down
```

9. [Optional] Deactivate the virtual environment.
```bash
deactivate
```
