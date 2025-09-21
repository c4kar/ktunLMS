import base64
import os

def convert_base64_to_images():
    # Check if base64_codes.txt exists
    if not os.path.exists('base64_codes.txt'):
        print("Error: base64_codes.txt not found!")
        return
    
    # Create images directory if it doesn't exist
    if not os.path.exists('images'):
        os.makedirs('images')
    
    # Read base64 codes from file
    with open('base64_codes.txt', 'r', encoding='utf-8') as file:
        lines = file.readlines()
    
    # Process each base64 line
    for index, line in enumerate(lines):
        # Strip any whitespace/newlines
        base64_string = line.strip()
        
        # Skip empty lines
        if not base64_string:
            continue
            
        try:
            # Decode base64 string
            image_data = base64.b64decode(base64_string)
            
            # Create filename
            filename = f'images/img-{index}.jpeg'
            
            # Write image file
            with open(filename, 'wb') as image_file:
                image_file.write(image_data)
            
            print(f"Created {filename}")
            
        except Exception as e:
            print(f"Error processing line {index}: {str(e)}")
    
    print(f"Processed {len([l for l in lines if l.strip()])} base64 images")

if __name__ == "__main__":
    convert_base64_to_images()