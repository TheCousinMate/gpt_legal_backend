# convert_json_to_yaml.py
import json
import yaml
import sys
import os

def convert(json_input_path, yaml_output_path):
    """Converts a JSON file to a YAML file."""
    try:
        with open(json_input_path, 'r', encoding='utf-8') as f:
            json_data = json.load(f)
        
        # Use default_flow_style=False for block style YAML, which is often preferred for readability
        # And allow_unicode=True to handle special characters
        with open(yaml_output_path, 'w', encoding='utf-8') as f:
            yaml.dump(json_data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
        
        print(f"Successfully converted '{json_input_path}' to '{yaml_output_path}'.")
    except FileNotFoundError:
        print(f"Error: Input file not found at '{json_input_path}'.", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in '{json_input_path}'.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred during conversion: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python convert_json_to_yaml.py <input_json_path> <output_yaml_path>", file=sys.stderr)
        sys.exit(1)
    
    input_json_path = sys.argv[1]
    output_yaml_path = sys.argv[2]
    
    convert(input_json_path, output_yaml_path)
