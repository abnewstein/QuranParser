import json
from bs4 import BeautifulSoup

inputFile = "data/notes/en_sg_notes-text.json"
outputFile = "data/notes/en_sg_notes-text_cleaned-1.json"
cleaned_data = {}
with open(file=inputFile) as f:
    for i, line in enumerate(f, 1):  # Start enumerating from 1
        try:
            json_line = json.loads(line)
            for k, v in json_line.items():
                soup = BeautifulSoup(v, "html.parser")
                # Remove button and other unnecessary tags
                for tag in soup.find_all(["button", "span"]):
                    tag.decompose()  # This removes the tag
                text = str(soup)  # Get the cleaned text
                cleaned_data[k] = text
        except Exception as e:
            print("Error in line: ", line, e)

        if i % 1000 == 0:  # Print a progress message for every 1000 lines processed
            print(f"Processed {i} lines")

# Write cleaned data back to json
with open(file=outputFile, mode="w") as f:
    json.dump(cleaned_data, f)
