# HTX Assessment

This repository contains the codebase for the HTX assessment. 

The url for the deployed application is [https://htx.euthyphro.io](https://htx.euthyphro.io).

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
- [AWS Deployment](#aws-deployment)
  - [Overview](#overview-2)
  - [DNS Configuration for Custom Domain with CloudFlare](#dns-configuration-for-custom-domain-with-cloudflare)
    - [ACM Validation DNS Records](#acm-validation-dns-records)
    - [DNS Records for ALB](#dns-records-for-alb)
  - [Setting Up the Infrastructure](#setting-up-the-infrastructure)
  - [Manual Configuration](#manual-configuration)
- [Future Improvements](#future-improvements)

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
│   ├── docker-compose.podman.yaml     # Podman Compose configuration for Elasticsearch services
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
├── terraform/                         # Infrastructure as Code for AWS deployment
│   ├── instances.tf                   # Configuration for EC2 instances
│   ├── load_balancer.tf               # Configuration for ALB
│   ├── main.tf                        # Main Terraform configuration file
│   ├── networking.tf                  # Configuration for VPC, Subnets and Security Groups
│   ├── providers.tf                   # Configuration for Terraform providers
│   ├── security_groups.tf             # Configuration for Security Groups
│   ├── variables.tf                   # Configuration for Terraform variables
│   └── volumes.tf                     # Configuration for EBS volumes
├── .gitignore                         # Specifies intentionally untracked files to ignore
└── README.md                          # Project documentation and instructions
```

## Pre-requisites

The following instructions are designed for use with Python 3.10.

Before starting, ensure that the necessary environment variables are properly configured. This is neccessary for (1) [Speech Recognition](#speech-recognition), (2) [Elasticsearch](#elasticsearch) and (3) [AWS Deployment](#aws-deployment).

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

# ============================
# Public Cloud Deployment Configuration
# ============================

## AWS Access Key ID
AWS_ACCESS_KEY_ID=aws-access-key-id             # Replace with your AWS Access Key ID

## AWS Secret Access Key
AWS_SECRET_ACCESS_KEY=aws-secret-access-key     # Replace with your AWS Secret Access Key

## AWS Region
AWS_REGION=aws-region                           # Replace with your AWS Region

## Certificate ARN for HTTPS
CERTIFICATE_ARN=certificate-arn                 # Replace with your SSL Certificate ARN

## EC2 SSH Key Pair Name
EC2_SSH_KEY_NAME=ec2-ssh-key-name               # Replace with your EC2 SSH Key Pair Name (i.e., name of the key pair in AWS EC2)

## Hostname for the search-ui application
HOSTNAME=hostname                               # Replace with the hostname for the search-ui application

## My IP Address for SSH access to the EC2 instance
PERSONAL_IP=person-ip-address                   # Replace with your IP Address
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
printenv | grep -E 'DEBUG|MODEL_NAME|LOG_FILE|APP_PORT|APP_NAME|ES_HOST|INDEX_NAME|CSV_FILE_PATH|REACT_APP_ELASTICSEARCH_HOST|AWS_ACCESS_KEY_ID|AWS_SECRET_ACCESS_KEY|AWS_REGION|CERTIFICATE_ARN|EC2_SSH_KEY_NAME|HOSTNAME|PERSONAL_IP'

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
# AWS_ACCESS_KEY_ID=aws-access-key-id
# AWS_SECRET_ACCESS_KEY=aws-secret-access-key
# AWS_REGION=aws-region
# CERTIFICATE_ARN=certificate-arn
# EC2_SSH_KEY_NAME=ec2-ssh-key-name
# HOSTNAME=hostname
# PERSONAL_IP=person-ip-address
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
├── asr/                               # Automated Speech Recognition module
│   └── data/
│       └── cv-valid-dev.csv           # CSV file containing valid development data
├── elastic-backend/                   # Backend services for Elasticsearch integration
│   ├── cv-index.py                    # Script to index data into Elasticsearch
│   ├── docker-compose.podman.yaml     # Podman Compose configuration for Elasticsearch services
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
├── .env                               # Environment variables for the project
├── .gitignore                         # Specifies intentionally untracked files to ignore
└── README.md                          # Project documentation and instructions
```

### Overview

The following instructions are to: 
1. Set up an Elasticsearch cluster,
2. Create an index in the cluster, 
3. Create a search UI to query the index from the cluster, and 
4. Index the transcriptions from the Common Voice dataset into the cluster.

**Note**: _While these instructions are designed for use with Podman, Podman commands and Podman-Compose are assumed throughout, Docker can generally be used as a substitute due to Podman's compatibility as a drop-in replacement for Docker in most standard container operations (and in this context). However, please be aware that due to limited time, these instructions have not been specifically tested with Docker. Users may need to adjust certain commands or configurations to ensure compatibility._

**Further Notes**: _There are 2 docker-compose files in the `elastic-backend` directory: `docker-compose.yaml` and `docker-compose.podman.yaml`. The file `docker-compose.podman.yaml` is specifically for Podman, while `docker-compose.yaml` is used for Docker._ 

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
podman-compose -f docker-compose.podman.yaml up -d --build
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

## AWS Deployment

### Overview

The following instructions use the Terraform scripts in the `terraform` directory to:
1. Set up a VPC, Subnets and Security Groups, 
2. Deploy the search UI application to EC2 instances in AWS,
2. Set up a Bastion host for SSH access to the EC2 instances, and
3. Set up an Application Load Balancer (ALB).

**Note**: _Requires an AWS account with the necessary permissions to create and manage resources. Proceed to guide [here](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html) on how to create an AWS Access Key ID and Secret Access Key to gain that necessary permissions._

**Further Notes**:
- _The following instructions assume the use of Terraform 1.9.8._
- _The deployment requires a valid SSL certificate ARN, an EC2 SSH Key Pair Name and a custom domain._
- _A valid SSL certificate ARN can be obtained from the AWS Certificate Manager or another certificate provider (e.g., CloudFlare etc.) Instructions [here](https://docs.aws.amazon.com/apigateway/latest/developerguide/how-to-specify-certificate-for-custom-domain-name.html)._
- _A valid EC2 SSH Key Pair Name can be created in the AWS EC2 console. Instructions [here](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/create-key-pairs.html). The `.pem` file should be stored in the root of the repository._
- _The custom domain should be set up in Route 53 or another DNS provider (e.g., CloudFlare etc.). Instructions [here](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/domain-register.html)._

### DNS Configuration for Custom Domain with CloudFlare

These instructions are for users who use popular non-AWS DNS providers, such as Cloudflare.

#### ACM Validation DNS Records

If you are using the AWS Certificate Manager (ACM) to obtain an SSL certificate for your custom domain, you will need to validate the certificate. After obtaining the certificate, ACM will provide you with one or more CNAME records for each domain/subdomain you requested to add to your DNS provider. Each of these records is used to validate that you own the domain/subdomain. 

You can validate the certificate by adding each CNAME validation record provided by ACM in CloudFlare (`_your-acm-id` is from its CNAME name and `_your-acm-validation-code.your-acm-region.acm.aws` is from its CNAME value):

|**Type**| **Name**        | **Target**                                              | **Proxy Status**     |
|--------|-----------------|---------------------------------------------------------|----------------------|
|CNAME   | _your-acm-id    | _your-acm-validation-code.your-acm-region.acm.aws       | DNS Only             |

#### DNS Records for ALB

If CloudFlare is your primary DNS provider, all DNS queries for your custom domain are handled by CloudFlare's nameservers. In this case, the following DNS records should be manually set up for both the root domain and the subdomain (e.g., `your-domain.com` and `htx.your-domain.com` respectively etc.) after the ALB is provisioned via Terraform:

|**Type**| **Name**        | **Target**                                              | **Proxy Status**     |
|--------|-----------------|---------------------------------------------------------|----------------------|
|CNAME   | @ (root)        | your-alb-1234567890.aws-region.elb.amazonaws.com        | Proxied              |
|CNAME   | htx             | your-alb-1234567890.aws-region.elb.amazonaws.com        | Proxied              |

### Setting Up the Infrastructure

1. Navigate to the `terraform` directory.
```bash
cd terraform
```

2. Initialize the Terraform configuration.
```bash
terraform init
```

3. Check the version of Terraform and the installed providers in configuration. 
```bash
terraform version
```

4. Format the code.
```bash
terraform fmt
```

5. Plan the changes.
```bash
terraform plan -var="region=$AWS_DEFAULT_REGION" -var="certificate_arn=$CERTIFICATE_ARN" -var="ec2_ssh_key_name=$EC2_SSH_KEY_NAME" -var="hostname=$HOSTNAME" -var="personal_ip=$PERSONAL_IP"
```

6. Apply the changes.
```bash
terraform apply -auto-approve -var="region=$AWS_DEFAULT_REGION" -var="certificate_arn=$CERTIFICATE_ARN" -var="ec2_ssh_key_name=$EC2_SSH_KEY_NAME" -var="hostname=$HOSTNAME" -var="personal_ip=$PERSONAL_IP"
```

7. View the applied configuration in the Terraform state.
```bash
terraform show
```

8. List all of the items in Terraform's managed state.
```bash
terraform state list
```

9. Print the outputs in a machine-readable format.
```bash
terraform output -json
```

10. To verify the setup, open a web browser and navigate to your custom domain (e.g., `https://htx.your-domain.com`). You should see a message from the running Nginx container.

11. [Optional] SSH into the EC2 instance via Bastion host.
```bash
# Copy the SSH key to the Bastion Host (same key used for the private EC2 instance and Bastion Host)
scp -i ./path/to/key.pem ./path/to/key.pem ec2-user@ec2-XXX-XXX-XXX-XXX.aws-region.compute.amazonaws.com:/home/ec2-user/

# SSH into the Bastion Host
ssh -i "key.pem" ec2-user@ec2-XXX-XXX-XXX-XXX.aws-region.compute.amazonaws.com

# From the Bastion Host, SSH into the private EC2 instance
ssh -i "key.pem" ubuntu@XX.XX.XXX.XX
```

12. [Optional] Destroy the infrastructure.
```bash
terraform destroy -auto-approve -var="region=$AWS_DEFAULT_REGION" -var="certificate_arn=$CERTIFICATE_ARN" -var="ec2_ssh_key_name=$EC2_SSH_KEY_NAME" -var="hostname=$HOSTNAME" -var="personal_ip=$PERSONAL_IP"
```

### Manual Configuration

After the infrastructure has been set up, the following manual configurations are required for each EC2 instance:

1. SSH into an EC2 instance via Bastion host.
```bash
# Copy the SSH key to the Bastion Host (same key used for the private EC2 instance and Bastion Host)
scp -i ./path/to/key.pem ./path/to/key.pem ec2-user@ec2-XXX-XXX-XXX-XXX.aws-region.compute.amazonaws.com:/home/ec2-user/

# SSH into the Bastion Host
ssh -i "key.pem" ec2-user@ec2-XXX-XXX-XXX-XXX.aws-region.compute.amazonaws.com

# From the Bastion Host, SSH into the private EC2 instance
ssh -i "key.pem" ubuntu@XX.XX.XXX.XX
```

2. Clone the project repository.
```bash
git clone https://github.com/mingjiewong/htx-assessment.git
```

3. Shut down the running Nginx container.
```bash
# List all running containers
sudo docker ps

# Stop and remove the container
sudo docker stop XXXXXXX
sudo docker rm XXXXXXX
```

4. Navigate to the `htx-assessment/elastic-backend` directory of the project repository.
```bash
cd htx-assessment/elastic-backend
```

5. Install the required dependencies.
```bash
sudo pip3 install -r requirements.txt
```

6. Load the following environment variables for indexing the data into the Elasticsearch cluster later.
```bash
echo -e "ES_HOST=http://localhost:9200\nINDEX_NAME=cv-transcriptions\nCSV_FILE_PATH=../asr/data/cv-valid-dev.csv" > ../.env
export $(grep -v '^#' ../.env | xargs)
```

7. Increase the `max_map_count` for the Elasticsearch cluster. This is necessary because Elasticsearch needs a higher `vm.max_map_count` setting (which determines the maximum number of memory-mapped areas a process can have) than the default value (e.g., `65530`) on many Linux systems, including Ubuntu, CentOS, RHEL, and Debian.
```bash
# Check the current max_map_count
sysctl vm.max_map_count

# Increase the max_map_count
sudo sysctl -w vm.max_map_count=262144

# Persist the change
echo "vm.max_map_count=262144" | sudo tee -a /etc/sysctl.conf
```

8. Since the frontend is served over HTTPS, accessing Elasticsearch over HTTP can cause browser blocks due to Mixed Content Issues. To resolve this, set the host to a relative path `/api/` in the `App.js` file. This allows the frontend to connect to the backend API using the same domain and protocol, leveraging Nginx to proxy API requests and avoiding mixed content issues.
```bash
vim ../search-ui/src/App.js

# Change the line in App.js from:
# host: process.env.REACT_APP_ELASTICSEARCH_HOST || 'http://localhost:9200',
# to:
# host: '/api/',
```

9. Start Elasticsearch Cluster. 
```bash
sudo docker-compose up -d --build
```

10. Check the health of the Elasticsearch cluster.
```bash
curl -X GET "http://localhost:9200/_cluster/health?pretty"
```

11. Create the `cv-transcriptions` index in the Elasticsearch cluster and index the speech recongition data.
```bash
python3 cv-index.py
```

12. Update the nginx configuration in the search UI application to address the Mixed Content Issues.

    Execute the following commands in the container of the `search-ui` application.
    ```bash
    # Access shell in the container
    sudo docker exec -it search-ui sh

    # Edit the nginx configuration file
    vi /etc/nginx/conf.d/default.conf

    # Add the following location block to the nginx configuration file

    # Test the nginx configuration
    nginx -t

    # Reload the nginx configuration
    nginx -s reload
    ```

    Update the nginx configuration file to include the following location block.
    ```bash
      location /api/ {                                  
          proxy_pass http://elasticsearch-node1:9200/;
          proxy_set_header Host $host;                
          proxy_set_header X-Real-IP $remote_addr;    
                                                      
          # CORS Headers                              
          add_header 'Access-Control-Allow-Origin' '*' always;
          add_header 'Access-Control-Allow-Methods' 'GET, POST, OPTIONS' always;
          add_header 'Access-Control-Allow-Headers' 'Content-Type, Authorization' always;
                                                                                      
          # Handle preflight OPTIONS requests                                            
          if ($request_method = 'OPTIONS') {                                             
              add_header 'Access-Control-Max-Age' 1728000;                               
              add_header 'Content-Type' 'text/plain charset=UTF-8';                      
              add_header 'Content-Length' 0;                                             
              return 204;                                                       
          }                                                                              
      } 
    ```

## Future Improvements

Currently, my infrastructure utilizes two separate EC2 instances deployed across different Availability Zones (AZs). Each instance hosts an identical Elasticsearch cluster within the same target group, a strategy designed to distribute load efficiently, boost availability, and enhance fault tolerance.

This configuration operates under the assumption that the Elasticsearch index remains static, with no anticipated future updates or the necessity for synchronization between the two clusters. By allowing each cluster to function independently, I can eliminate the complexities associated with data synchronization, ensuring straightforward maintenance and operation.

However, this approach presents significant challenges if updates to the Elasticsearch index become necessary. Managing two separate clusters increases the risk of data inconsistency, especially as the dataset involves common voice data generated by automatic speech models. Given the rapid advancements and frequent updates expected in these models, adding new features or modifying existing ones could complicate the maintenance of identical clusters, undermining the benefits of our current setup.

To address these challenges, I propose transitioning to Amazon OpenSearch Service (the successor to Amazon Elasticsearch Service) on AWS. Unlike my current setup, Amazon OpenSearch Service inherently manages data replication and ensures high availability by allowing the Elasticsearch cluster to span multiple AZs. This managed service simplifies cluster management, automatically handles data replication across AZs, and maintains data accessibility even if one AZ encounters issues, thereby preserving the integrity and availability of our Elasticsearch deployment.

Furthermore, to accommodate the need for dynamic feature additions driven by continuous improvements in automatic speech models, I recommend integrating MongoDB into our data architecture. MongoDB offers a higher level of flexibility with its document-based data structure, facilitating the easy addition and modification of data fields without the need for extensive schema migrations. This adaptability is crucial for supporting the evolving requirements of speech models.

To ensure seamless synchronization between MongoDB and Elasticsearch, we can utilize tools like the MongoDB Connector for Elasticsearch. This integration ensures that search indices remain up-to-date with the primary data store, maintaining consistency across our databases. Additionally, MongoDB's native search capabilities, such as MongoDB Atlas Search, leverage Lucene—the same underlying technology as Elasticsearch—and support semantic search functionalities, enabling effective vectorization of transcripts.

In summary, while my current deployment of two separate EC2 instances across different AZs effectively enhances availability and fault tolerance for a static Elasticsearch index, the anticipated dynamic nature of our dataset requires us to think of a more flexible approach. Transitioning to Amazon OpenSearch Service can ensure a level of robustness in data replication and high availability, while integrating MongoDB can provide us the necessary flexibility to support rapid advancements and feature enhancements in our automatic speech models. Combining both of them together will allow us to leverage their strengths to ensure a scalable, reliable, and adaptable data infrastructure on AWS.