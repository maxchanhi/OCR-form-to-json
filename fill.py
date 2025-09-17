import ollama
import os
import time
import json

def main():
    """
    Scans a folder for images of visa forms, performs OCR, and fills in a
    pre-defined JSON template with the extracted information using an Ollama model.
    """
    start_time = time.time()
    
    # --- Configuration ---
    img_folder = "img"
    json_template_path = "json_template/artist_visa_template.json"
    output_folder = "result"
    model_name = "qwen2.5vl" # Or "llava", "moondream", etc.

    # --- Pre-run Checks ---
    os.makedirs(output_folder, exist_ok=True)
    # Check for image folder
    if not os.path.isdir(img_folder):
        print(f"Error: Image folder not found or is not a directory: {img_folder}")
        return
        
    # Check for and read the JSON template file
    try:
        with open(json_template_path, 'r') as f:
            json_template_str = f.read()
        print(f"Successfully loaded JSON template from: {json_template_path}")
    except FileNotFoundError:
        print(f"Error: JSON template file not found at: {json_template_path}")
        return
    except Exception as e:
        print(f"Error reading JSON template file: {e}")
        return

    # Find images in the folder
    image_files = [f for f in os.listdir(img_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    if not image_files:
        print(f"No images found in {img_folder}")
        return

    # --- Main Processing Loop ---
    for image_file in image_files:
        image_path = os.path.join(img_folder, image_file)
        print(f"\nProcessing {image_path}...")
        
        # Construct the detailed prompt for the model
        prompt_content = f"""
        [TASK]
        You are an expert data extraction assistant. Your task is to analyze the provided image of a Hong Kong visa application form and accurately fill in the JSON template below with the information you find.

        [INSTRUCTIONS]
        1.  Carefully read all text in the image.
        2.  Populate the values in the JSON template using only the information from the image.
        3.  Do NOT change any keys or the structure of the JSON template.
        4.  If a specific piece of information cannot be found on the form, use `null` as the value for that field.
        5.  Ensure your final output is ONLY the completed JSON object. Do not include any explanatory text, markdown formatting, or anything else before or after the JSON.

        [JSON TEMPLATE TO FILL]
        {json_template_str}
        """

        try:
            response = ollama.chat(
                model=model_name,
                messages=[
                    {
                        "role": "user",
                        "content": prompt_content,
                        "images": [image_path]
                    }
                ],
                format="json"  # Enforce JSON output mode
            )
            
            print(f"--- Extracted Data for {image_file} ---")
            
            response_content = response['message']['content']
            
            try:
                # Parse the JSON string from the model into a Python dictionary
                json_data = json.loads(response_content)
                
                # Pretty-print the structured JSON data
                print(json.dumps(json_data, indent=4))

                # Save the JSON data to a file
                output_filename = os.path.splitext(image_file)[0] + ".json"
                output_path = os.path.join(output_folder, output_filename)
                with open(output_path, 'w') as f:
                    json.dump(json_data, f, indent=4)
                print(f"Successfully saved extracted data to: {output_path}")
                
            except json.JSONDecodeError:
                print("Error: Model did not return a valid JSON object.")
                print("--- Raw Model Output ---")
                print(response_content)

            print("--------------------------------------\n")

        except Exception as e:
            print(f"An error occurred while processing {image_file} with the model: {e}")

    # --- Final Summary ---
    end_time = time.time()
    print(f"Finished processing {len(image_files)} image(s).")
    print(f"Total runtime: {end_time - start_time:.2f} seconds")


if __name__ == "__main__":
    main()
