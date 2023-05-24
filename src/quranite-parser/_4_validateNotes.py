import json

# Load the JSON data
with open("data/notes/en_sg_notes-text_cleaned.json") as f:
    notes_text = json.load(f)

with open("data/notes/en_sg_notes-coordinates.json") as f:
    notes_coordinates = json.load(f)

# Convert the keys in notes_coordinates to match the format in notes_text
notes_coordinates_keys = []
for key in notes_coordinates.keys():
    chapter, verse = key.split(":")
    noteLength = len(notes_coordinates[key])
    for i in range(noteLength):
        notes_coordinates_keys.append(f"{chapter}:{verse}:{i + 1}")

# Compare the data
for key in notes_text.keys():
    if key not in notes_coordinates_keys:
        print(
            f"Key {key} from en_sg_notes-text_cleaned.json not found in en_sg_notes-coordinates.json"
        )

for key in notes_coordinates_keys:
    if key not in notes_text:
        print(
            f"Key {key} from en_sg_notes-coordinates.json not found in en_sg_notes-text_cleaned.json"
        )
