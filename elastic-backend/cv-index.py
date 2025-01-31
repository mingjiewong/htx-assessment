import os
import sys

import csv
from elasticsearch import Elasticsearch, helpers

from typing import Dict, Any, Iterator

from logging_config import logger

# Elasticsearch configuration from environment variables
ES_HOST = os.getenv("ES_HOST")
INDEX_NAME = os.getenv("INDEX_NAME")
CSV_FILE_PATH = os.getenv("CSV_FILE_PATH")

def create_index(es: Elasticsearch) -> None:
    """Create an Elasticsearch index with predefined mappings if it does not exist.

    This function checks whether the specified index exists in Elasticsearch.
    If the index does not exist, it defines the necessary mappings and creates the index.
    Proper logging is performed to indicate the success or failure of the operation.

    Args:
        es (Elasticsearch): An instance of the Elasticsearch client.

    Raises:
        SystemExit: Exits the program if index creation fails.
    """
    if not es.indices.exists(index=INDEX_NAME):
        # Define index mappings
        mappings = {
            "mappings": {
                "properties": {
                    "filename"       : {"type": "keyword"},    # Set as keyword for exact match
                    "text"           : {"type": "text"},       # Set as text for full-text search
                    "up_votes"       : {"type": "integer"},
                    "down_votes"     : {"type": "integer"},
                    "age"            : {"type": "keyword"},    # Set as keyword for aggregations and filtering
                    "gender"         : {"type": "keyword"},    # Set as keyword for aggregations and filtering
                    "accent"         : {"type": "keyword"},    # Set as keyword for aggregations and filtering
                    "duration"       : {"type": "float"},
                    "generated_text" : {"type": "text"}        # Set as text for full-text search
                }
            }
        }
        try:
            es.indices.create(index=INDEX_NAME, body=mappings)
            logger.info(f"Index '{INDEX_NAME}' created with mappings.")
        except Exception as e:
            logger.error(f"Failed to create index '{INDEX_NAME}': {e}")
            sys.exit(1)
    else:
        logger.info(f"Index '{INDEX_NAME}' already exists.")

def generate_actions(csv_file: str) -> Iterator[Dict[str, Any]]:
    """Generator that yields actions for Elasticsearch bulk API.

    Reads a CSV file and converts each row into a format suitable for bulk indexing in Elasticsearch.
    Handles data type conversions and logs warnings for invalid values.

    Args:
        csv_file (str): The path to the CSV file containing transcription data.

    Yields:
        Dict[str, Any]: A dictionary representing an action for Elasticsearch bulk indexing.
    """
    with open(csv_file, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:

            # Handle 'up_votes' conversion with error handling
            up_votes_value = row.get("up_votes", 0)
            try:
                up_votes = int(up_votes_value)
            except ValueError:
                logger.warning(f"Invalid up_votes value '{up_votes_value}' for filename '{row.get('filename')}'. Setting up_votes to 0.")
                up_votes = 0

            # Handle 'down_votes' conversion with error handling
            down_votes_value = row.get("down_votes", 0)
            try:
                down_votes = int(down_votes_value)
            except ValueError:
                logger.warning(f"Invalid down_votes value '{down_votes_value}' for filename '{row.get('filename')}'. Setting down_votes to 0.")
                down_votes = 0

            # Handle 'duration' conversion with error handling
            duration_value = row.get("duration", 0)
            try:
                duration = float(duration_value)
            except ValueError:
                logger.warning(f"Invalid duration value '{duration_value}' for filename '{row.get('filename')}'. Setting duration to 0.0.")
                duration = 0.0

            yield {
                "_index" : INDEX_NAME,
                "_id"    : row.get("filename"),  # Using filename as unique ID
                "_source": {
                    "filename"        : row.get("filename"),
                    "text"            : row.get("text"),
                    "up_votes"        : up_votes,
                    "down_votes"      : down_votes,
                    "age"             : row.get("age") or None,
                    "gender"          : row.get("gender") or None,
                    "accent"          : row.get("accent") or None,
                    "duration"        : duration,
                    "generated_text"  : row.get("generated_text")
                }
            }

def main():
    # Initialize Elasticsearch client
    es = Elasticsearch([ES_HOST])

    # Verify connection
    if not es.ping():
        logger.error(f"Cannot connect to Elasticsearch at {ES_HOST}. Ensure it's running.")
        sys.exit(1)
    logger.info(f"Connected to Elasticsearch at {ES_HOST}.")

    # Create index if it doesn't exist
    create_index(es)

    # Check if CSV file exists
    if not os.path.isfile(CSV_FILE_PATH):
        logger.error(f"CSV file {CSV_FILE_PATH} does not exist.")
        sys.exit(1)

    # Generate actions from CSV
    actions = generate_actions(CSV_FILE_PATH)

    # Bulk index data
    try:
        helpers.bulk(es, actions)
        logger.info("Indexing completed successfully.")
    except Exception as e:
        logger.error(f"Error during bulk indexing: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()