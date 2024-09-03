import time
import zipfile
import os

# Path to the zip file
zip_file_path = 'Archive (2).zip'
extracted_dir = 'path_to_extract_directory'

# Extract the zip file
with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
    zip_ref.extractall(extracted_dir)

# Initialize the result list
result = []

# Traverse the extracted directory
for root, dirs, files in os.walk(extracted_dir):
    for file in files:
        if file.endswith('.txt'):
            file_path = os.path.join(root, file)
            with open(file_path, 'r', encoding='utf-8') as f:
                for line_number, line_content in enumerate(f, start=1):
                    stripped_content = line_content.strip()
                    # Only add non-empty lines and lines with non-whitespace content
                    if stripped_content:
                        result.append({
                            'file_name': file,
                            'line_number': line_number,
                            'line_content': stripped_content
                        })

if __name__ == '__main__':
    # Get the substring from the user
    substring = input("Enter the substring to search for: ")

    # Start timing the search
    start_time = time.time()

    # Filter results to find lines containing the substring
    filtered_results = [entry for entry in result if substring in entry['line_content']]

    # End timing the search
    end_time = time.time()
    elapsed_time = end_time - start_time

    # Print filtered results
    for entry in filtered_results:
        print(entry)

    print(f"Search runtime: {elapsed_time:.2f} seconds")
