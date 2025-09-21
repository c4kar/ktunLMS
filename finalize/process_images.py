import json
import base64
import os
import shutil
import argparse

def get_folder_name_from_md(file_path):
    """
    Reads the first line of a file and creates a sanitized folder name from it.

    Args:
        file_path (str): The path to the markdown file.

    Returns:
        str: A sanitized string suitable for a folder name.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            first_line = f.readline()
        
        if not first_line:
            return "default_folder"

        # Remove leading '#' and surrounding whitespace
        folder_name = first_line.strip().lstrip('# ').strip()
        
        # Replace characters invalid for folder names on Windows
        # Invalid chars: < > : " / \ | ? *
        # Also replace the en-dash with a standard hyphen
        folder_name = folder_name.replace('–', '-')
        invalid_chars = '<>:"/\|?*'
        for char in invalid_chars:
            folder_name = folder_name.replace(char, '')
            
        # Replace multiple spaces with a single space and ensure it's not empty
        folder_name = " ".join(folder_name.split())

        return folder_name if folder_name else "default_folder"

    except FileNotFoundError:
        print(f"Warning: MD file '{file_path}' not found. Using default folder name.")
        return "default_folder"
    except Exception as e:
        print(f"An error occurred while reading '{file_path}': {e}. Using default folder name.")
        return "default_folder"

def extract_base64_from_json(json_file_path):
    """
    Extracts base64 encoded image data from a JSON file.

    Args:
        json_file_path (str): The path to the input JSON file.
    
    Returns:
        list: A list of base64 encoded strings, or None if an error occurs.
    """
    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        base64_codes = []
        # The top-level structure is a list
        for item in data:
            if 'pages' in item:
                for page in item['pages']:
                    if 'images' in page:
                        for image in page['images']:
                            if 'image_base64' in image:
                                # The format is "data:image/jpeg;base64,..."
                                # We want the part after the comma.
                                parts = image['image_base64'].split(',', 1)
                                if len(parts) == 2:
                                    base64_codes.append(parts[1])
        
        print(f"Successfully extracted {len(base64_codes)} base64 codes from {json_file_path}")
        return base64_codes

    except FileNotFoundError:
        print(f"Error: The file {json_file_path} was not found.")
        return None
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {json_file_path}.")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

def convert_base64_to_images(base64_codes, image_dir):
    """
    Decodes a list of base64 strings and saves them as image files.
    
    Args:
        base64_codes (list): A list of base64 encoded strings.
        image_dir (str): The directory to save the images in.
    """
    # Create images directory if it doesn't exist
    if not os.path.exists(image_dir):
        os.makedirs(image_dir)
    
    # Process each base64 string
    for index, base64_string in enumerate(base64_codes):
        # Skip empty strings
        if not base64_string:
            continue
            
        try:
            # Decode base64 string
            image_data = base64.b64decode(base64_string)
            
            # Create filename
            filename = os.path.join(image_dir, f'img-{index}.jpeg')
            
            # Write image file
            with open(filename, 'wb') as image_file:
                image_file.write(image_data)
            
            print(f"Created {filename}")
            
        except Exception as e:
            print(f"Error processing item {index}: {str(e)}")
    
    print(f"Processed {len(base64_codes)} base64 images")

def copy_file_to_dir(source_file, dest_dir):
    """
    Copies a file into a directory.

    Args:
        source_file (str): The path to the file to copy.
        dest_dir (str): The path to the destination directory.
    """
    if not os.path.exists(source_file):
        print(f"Error: Source file '{source_file}' not found. Cannot copy.")
        return

    if not os.path.isdir(dest_dir):
        print(f"Error: Destination '{dest_dir}' is not a valid directory. Cannot copy.")
        return

    try:
        shutil.copy(source_file, dest_dir)
        print(f"Successfully copied '{source_file}' to '{dest_dir}'.")
    except Exception as e:
        print(f"An error occurred while copying the file: {e}")

def rename_md_in_folder(folder_path, original_md_filename):
    """
    Renames a markdown file inside a folder to match the folder's name.

    Args:
        folder_path (str): The path to the folder containing the md file.
        original_md_filename (str): The original name of the md file.
    """
    try:
        original_file_path = os.path.join(folder_path, original_md_filename)
        
        if not os.path.exists(original_file_path):
            print(f"Warning: File '{original_file_path}' not found. Cannot rename.")
            return

        # New name is the folder's name with .md extension
        new_filename = os.path.basename(folder_path) + '.md'
        new_file_path = os.path.join(folder_path, new_filename)

        # Check if a file with the new name already exists
        if os.path.exists(new_file_path):
            print(f"Warning: A file named '{new_filename}' already exists. Skipping rename.")
            return

        os.rename(original_file_path, new_file_path)
        print(f"Successfully renamed '{original_file_path}' to '{new_file_path}'.")

    except Exception as e:
        print(f"An error occurred during renaming: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process JSON and Markdown files to create a structured folder with images.")
    parser.add_argument("source_directory", help="The path to the directory containing data.json and md.md.")
    args = parser.parse_args()

    source_dir = args.source_directory
    
    # Define file paths based on the source directory
    json_file = os.path.join(source_dir, 'data.json')
    md_file = os.path.join(source_dir, 'md.md')
    
    if not os.path.exists(json_file) or not os.path.exists(md_file):
        print(f"Error: 'data.json' or 'md.md' not found in the specified directory: {source_dir}")
    else:
        # Step 1: Determine the folder name from the markdown file's first line
        output_folder_name = get_folder_name_from_md(md_file)
        output_folder_path = os.path.join(source_dir, output_folder_name)
        
        # Step 2: Extract base64 codes from the JSON file
        extracted_codes = extract_base64_from_json(json_file)
        
        # Step 3: If extraction was successful, process files
        if extracted_codes:
            convert_base64_to_images(extracted_codes, output_folder_path)
            copy_file_to_dir(md_file, output_folder_path)
            
            # Step 4: Rename the copied markdown file to match the folder name
            rename_md_in_folder(output_folder_path, os.path.basename(md_file))
        else:
            print("Could not proceed with image conversion due to an error during extraction.")