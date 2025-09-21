import json

def extract_base64_from_json(json_file_path, output_txt_file):
    """
    Extracts base64 encoded image data from a JSON file and writes it to a text file.

    Args:
        json_file_path (str): The path to the input JSON file.
        output_txt_file (str): The path to the output text file.
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

        with open(output_txt_file, 'w', encoding='utf-8') as f:
            for code in base64_codes:
                f.write(code + '\n')

        print(f"Successfully extracted {len(base64_codes)} base64 codes to {output_txt_file}")

    except FileNotFoundError:
        print(f"Error: The file {json_file_path} was not found.")
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {json_file_path}.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == '__main__':
    JSON_FILE = 'data.json'
    OUTPUT_FILE = 'base64_codes.txt'
    extract_base64_from_json(JSON_FILE, OUTPUT_FILE)
