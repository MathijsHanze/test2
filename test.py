import os
import glob
import json

def format_and_merge_presets():
    """
    Finds all loose .json files in the script's directory,
    reformats them based on the specified structure,
    and merges them into a single 'generated_presets.json' file.
    """
    output_filename = "generated_presets.json"
    merged_presets = {}
    
    # Find all .json files in the current directory
    json_files = glob.glob('*.json')
    
    print(f"Found files: {json_files}")
    
    for filename in json_files:
        # Skip the output file itself
        if filename == output_filename:
            continue
            
        print(f"Processing {filename}...")
        
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                source_data = json.load(f)
            
            # --- Transformation Logic ---
            
            # Get the main key for the new structure
            root_id = source_data.get("Root")
            
            # Skip if the source file doesn't have a "Root" key
            if not root_id:
                print(f"  ...Skipping {filename}: 'Root' key is missing or empty.")
                continue

            # Create the new formatted dictionary
            # We hardcode "_changeWeaponName" and "_type" as per To.json
            formatted_preset = {
                "_changeWeaponName": False,
                "_id": source_data.get("Id"),
                "_items": source_data.get("Items", []), # Use default if key missing
                "_name": source_data.get("Name"),
                "_parent": source_data.get("Parent"),
                "_type": "Preset"
            }
            
            # Add the newly formatted preset to our main dictionary
            # using the root_id as the key.
            if root_id in merged_presets:
                print(f"  ...Warning: Duplicate Root ID '{root_id}' found in {filename}. Overwriting previous entry.")
            
            merged_presets[root_id] = formatted_preset
            
        except json.JSONDecodeError:
            print(f"  ...Skipping {filename}: Not a valid JSON file.")
        except Exception as e:
            print(f"  ...An error occurred while processing {filename}: {e}")

    # --- Write Output File ---
    
    if not merged_presets:
        print("No valid preset files found. Output file will not be created.")
        return

    try:
        with open(output_filename, 'w', encoding='utf-8') as f:
            # Use indent=4 for pretty-printing, as seen in your example
            json.dump(merged_presets, f, indent=4)
        
        print(f"\nSuccessfully merged {len(merged_presets)} presets into {output_filename}")
        
    except Exception as e:
        print(f"\nAn error occurred while writing output file: {e}")

if __name__ == "__main__":
    # This ensures the script runs when executed directly
    format_and_merge_presets()