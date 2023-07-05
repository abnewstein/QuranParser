import json
import os
from bs4 import BeautifulSoup

dir = os.path.dirname(__file__)
inputFile = os.path.join(dir, '../data/notes/en_sg_notes-text_cleaned-1.json')
outputFile = os.path.join(dir, '../data/notes/en_sg_notes-text_final.json')

# Create a dictionary to store note text and its corresponding first key.
first_occurrence = {}
cleaned_data = {}

with open(file=inputFile) as f:
    try:
        json_line = json.loads(f.readline())        
        for k, v in json_line.items():
            soup = BeautifulSoup(v, "html.parser")

            for tag in soup.find_all(["a"]):
                tag.attrs.clear()

            text = str(soup)

            # If this note text has been seen before, store a reference to the
            # first key where it was seen. Otherwise, store the note text.
            if text in first_occurrence:
                cleaned_data[k] = first_occurrence[text]
            else:
                cleaned_data[k] = text
                first_occurrence[text] = k

    except Exception as e:
        print("Error in line: ", e)

# Now we can write the cleaned_data to the output file.
with open(outputFile, 'w') as f:
    # format the output to be array of arrays
    f.write(json.dumps([[k, v] for k, v in cleaned_data.items()]))
    
print("Data cleaning complete.")
