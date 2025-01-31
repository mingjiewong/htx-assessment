import os
import requests
import argparse
import csv
import sys

def transcribe_file(file_path, api_url):
    """
    Sends an audio file to the speech recognition API and returns the response.

    Args:
        file_path (str): Path to the audio file.
        api_url (str): URL of the speech recognition API endpoint.

    Returns:
        dict or None: JSON response from the API if successful; otherwise, None.
    """
    try:
        with open(file_path, 'rb') as f:
            files = {'file': f}
            response = requests.post(api_url, files=files)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to transcribe {file_path}: {response.text}")
            return None
    except Exception as e:
        print(f"Error while transcribing {file_path}: {e}")
        return None

def update_csv(csv_path, filename, generated_text, duration):
    """
    Updates the CSV file by adding or updating the 'generated_text' column for the corresponding row.

    Args:
        csv_path (str): Path to the CSV file.
        filename (str): Name of the audio file.
        generated_text (str): Transcribed text from the API.
    """
    # Check if the CSV file exists
    if not os.path.isfile(csv_path):
        print(f"The CSV file {csv_path} does not exist. Creating a new one with headers.")
        # Define CSV headers including new columns
        headers = ['filename', 'text', 'up_votes', 'down_votes', 'age', 'gender', 'accent', 'duration', 'generated_text']
        rows = []
    else:
        # Open the existing CSV file for reading
        with open(csv_path, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            headers = reader.fieldnames
            rows = list(reader)

    # If 'generated_text' column doesn't exist, add it to headers
    if 'generated_text' not in headers:
        headers.append('generated_text')
        print("Added 'generated_text' column to the CSV headers.")

    # Flag to determine if the filename exists in the CSV
    found = False

    # Iterate through each row to find the matching filename
    for row in rows:
        if row['filename'] == filename:
            # Update 'generated_text' for the matching filename
            row['generated_text'] = generated_text
            # Update 'duration' for the matching filename
            row['duration'] = duration
            found = True
            print(f"Updated 'generated_text' and 'duration' for {filename}.")
            break # Exit loop after finding the matching row

    # If the filename was not found in the CSV, append a new row
    if not found:
        print(f"Filename {filename} not found in CSV. Adding a new row.")
        # Initialize all other columns as empty or default values if necessary
        new_row = {header: '' for header in headers}
        new_row['filename'] = filename
        new_row['generated_text'] = generated_text
        new_row['duration'] = duration
        rows.append(new_row)

    # Write the updated rows back to the CSV file
    with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers)
        writer.writeheader() # Write headers to CSV
        writer.writerows(rows) # Write all rows to CSV

    print(f"CSV '{csv_path}' updated successfully.\n")

def main():
    parser = argparse.ArgumentParser(description="Transcribe all audio files in a specified directory.")
    
    # Required argument: Path to the directory containing audio files
    parser.add_argument(
        '--data-dir',
        type=str,
        required=True,
        help='Path to the directory containing audio files.'
    )

    # Required argument: Path to the CSV file to update
    parser.add_argument(
        '--csv-file',
        type=str,
        required=True,
        help='Path to the CSV file containing audio files metadata.'
    )

    # Optional argument: URL of the speech recognition API endpoint
    parser.add_argument(
        '--api-url',
        type=str,
        default="http://localhost:8001/asr",
        help='URL of the speech recognition API endpoint.'
    )
    args = parser.parse_args()

    # Convert provided paths to absolute paths for consistency
    data_dir = os.path.abspath(args.data_dir)
    csv_path = os.path.abspath(args.csv_file)
    api_url = args.api_url

    # Verify if the specified CSV file exists
    if not os.path.isfile(csv_path):
        print(f"The file {csv_path} does not exist.")
        sys.exit(1)

    # Verify if the specified directory exists
    if not os.path.isdir(data_dir):
        print(f"The directory {data_dir} does not exist.")
        sys.exit(1)

    # Traverse through all audio files in the specified directory
    for root, _, files in os.walk(data_dir):
        for file in files:
            # Process only .mp3 files
            if file.lower().endswith('.mp3'):
                # Construct the full path of the audio file
                file_path = os.path.join(root, file)
                print(f"Transcribing {file_path}...")
                # Transcribe the audio file using the API
                result = transcribe_file(file_path, api_url)
                if result:
                    # Extract transcription and duration from the API response
                    generated_text = result.get('transcription', '').strip()
                    duration = result.get('duration', 0)  # Optional: If you want to use duration

                    # Extract the filename relative to data_dir (e.g., 'cv-valid-dev/sample-000000.mp3')
                    relative_path = root.split("/")[-1] + "/" + file
                    print(f"Transcription: {generated_text}, Duration: {duration}")

                    # Update the CSV file with the transcription and duration
                    update_csv(csv_path, relative_path, generated_text, duration)

                    # Delete the audio file after successful transcription
                    try:
                        os.remove(file_path)
                        print(f"Deleted {file_path}\n")
                    except Exception as e:
                        print(f"Failed to delete {file_path}: {e}\n")
                else:
                    # If transcription failed, skip deleting the file
                    print(f"Skipping deletion for {file_path} due to transcription failure.\n")

if __name__ == "__main__":
    main()