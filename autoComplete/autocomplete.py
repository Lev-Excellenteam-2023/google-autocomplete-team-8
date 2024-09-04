import time
import zipfile
import os
import re

def extract_zip_file(zip_file_path, extracted_dir):
    """Extracts all contents of the specified zip file into the provided directory, with error handling."""
    try:
        # Ensure the zip file exists
        if not os.path.exists(zip_file_path):
            raise FileNotFoundError(f"The zip file '{zip_file_path}' does not exist.")

        # Ensure the extraction directory exists, create if it doesn't
        if not os.path.exists(extracted_dir):
            os.makedirs(extracted_dir)

        # Attempt to extract the zip file
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            zip_ref.extractall(extracted_dir)
        print(f"Successfully extracted '{zip_file_path}' to '{extracted_dir}'.")

    except FileNotFoundError as fnf_error:
        print(fnf_error)
    except zipfile.BadZipFile:
        print(f"Error: The file '{zip_file_path}' is not a valid zip file.")
    except PermissionError:
        print(f"Error: Permission denied while trying to extract '{zip_file_path}'.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def clean_line(line):
    """Cleans a line by removing non-letter characters, 
    converting to lowercase, and normalizing white spaces."""

    # Remove anything that is not a letter or white space
    cleaned_line = re.sub(r'[^a-zA-Z\s]', '', line)

    # Convert to lowercase
    cleaned_line = cleaned_line.lower()

    # Normalize white spaces (remove consecutive white spaces)
    cleaned_line = re.sub(r'\s+', ' ', cleaned_line).strip()

    return cleaned_line

def initialize_data(extracted_dir):
    """Initializes a list with each line from the extracted
    .txt files, including file name, line number, original content, and cleaned content."""

    print("Initializing system data and components")

    data = []
    for root, dirs, files in os.walk(extracted_dir):
        for file in files:
            if file.endswith('.txt'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    for line_number, line_content in enumerate(f, start=1):
                        cleaned_content = clean_line(line_content)
                        # Only add lines containing letters (ignoring empty or whitespace-only lines)
                        if re.search(r'[a-zA-Z]', cleaned_content):
                            data.append({
                                'file_name': file,
                                'line_number': line_number,
                                'original_line': line_content.strip(),
                                'cleaned_line': cleaned_content
                            })
    return data

if __name__ == '__main__':
    zip_file_path = 'Archive (2).zip'
    extracted_dir = 'path_to_extract_directory'

    # Step 1: Extract the zip file
    extract_zip_file(zip_file_path, extracted_dir)

    # Step 2: Initialize the data
    data = initialize_data(extracted_dir)

    print("System is online!")

    # Get the substring from the user
    substring = input("Enter the substring to search for: ").lower()

    # Start timing the search
    start_time = time.time()

    # Filter results to find lines containing the substring in the cleaned content
    filtered_results = [entry for entry in data if substring in entry['cleaned_line']]

    # End timing the search
    end_time = time.time()
    elapsed_time = end_time - start_time

    # Print the original lines from filtered results
    for entry in filtered_results:
        print(entry)

    print(f"Search runtime: {elapsed_time:.2f} seconds")
