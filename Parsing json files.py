#code 1: For parsing 1,2,4,5,6
import json

# File paths
file_path = r"C:\Users\Ali Com\OneDrive\Desktop\vscodenew\json\3.json"
output_file = r"C:\Users\Ali Com\OneDrive\Desktop\vscodenew\json\parsed_data.json"

def recursive_parse(data, prefix="", rows=None):
    """
    Recursively parse a JSON object and collect its contents into a list of dictionaries.
    Each row is a dictionary of flattened JSON key-value pairs.
    """
    if rows is None:
        rows = []

    if isinstance(data, dict):
        row = {}
        for key, value in data.items():
            if isinstance(value, (dict, list)):
                recursive_parse(value, prefix + f"{key}.", rows)
            else:
                row[prefix + key] = value
        if row:  # Only append non-empty rows
            rows.append(row)
    elif isinstance(data, list):
        for i, item in enumerate(data):
            recursive_parse(item, prefix + f"{i}.", rows)
    else:
        rows.append({prefix[:-1]: data})  # Store the value as a single-row dictionary

    return rows

def main():
    try:
        # Read the JSON file
        with open(file_path, 'r') as file:
            raw_content = file.read().strip()

            # Handle callback wrapper if present
            if raw_content.startswith("IMC.TUI.Integration._callback("):
                raw_content = raw_content[len("IMC.TUI.Integration._callback("):-1]

            # Handle multiple JSON objects or extra data
            json_objects = []
            while raw_content:
                try:
                    # Parse the first valid JSON object
                    data, index = json.JSONDecoder().raw_decode(raw_content)
                    json_objects.append(data)
                    raw_content = raw_content[index:].strip()  # Trim processed content
                except json.JSONDecodeError as e:
                    print(f"Skipping invalid content: {e}")
                    break

        # Flatten and collect all rows from each JSON object
        all_rows = []
        for obj in json_objects:
            rows = recursive_parse(obj)
            all_rows.extend(rows)

        # Save the flattened data to a new JSON file
        with open(output_file, 'w') as outfile:
            json.dump(all_rows, outfile, indent=4)

        print(f"All data with rows has been saved to {output_file}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()


#code 2: for parsing 3,7
import json
# File paths
input_file = r"C:\Users\Ali Com\OneDrive\Desktop\vscodenew\smartcredit_2.json"
output_file = r"C:\Users\Ali Com\OneDrive\Desktop\vscodenew\json\parsed_data.json" 

def recursive_parse(data, prefix="", result=None):
    """
    Recursively parse a JSON object and collect its contents into a dictionary.
    :param data: JSON data (dict, list, or other types)
    :param prefix: String prefix for nested keys
    :param result: Dictionary to store flattened JSON data
    :return: Flattened dictionary
    """
    if result is None:
        result = {}

    if isinstance(data, dict):
        for key, value in data.items():
            new_prefix = f"{prefix}{key}." if prefix else f"{key}."
            recursive_parse(value, new_prefix, result)
    elif isinstance(data, list):
        for i, item in enumerate(data):
            new_prefix = f"{prefix}{i}."
            recursive_parse(item, new_prefix, result)
    else:
        result[prefix[:-1]] = data  # Remove trailing dot
    return result

def main():
    try:
        # Read and preprocess the JSON file
        with open(input_file, 'r', encoding='utf-8') as file:
            raw_content = file.read()

            # Remove the callback wrapper
            if raw_content.startswith("JSON_CALLBACK("):
                raw_content = raw_content[len("JSON_CALLBACK("):-1]

            # Parse JSON content
            data = json.loads(raw_content)

        # Flatten the JSON structure
        flattened_data = recursive_parse(data)

        # Save the flattened data to a new JSON file
        with open(output_file, 'w', encoding='utf-8') as outfile:
            json.dump(flattened_data, outfile, indent=4, ensure_ascii=False)

        print(f"Parsed and flattened JSON data saved to {output_file}")

    except Exception as e:
        print(f"Error processing the file: {e}")

if __name__ == "__main__":
    main()
