import json

with open(file="data/notes/en_sg_notes-coordinates.json") as f:
    notes_coords_data = json.load(f)

with open(file="data/notes/en_sg_notes-text_cleaned.json") as f:
    notes_text_data = json.load(f)

merged_data = []

for chapter_verse_note, note_text in notes_text_data.items():
    chapter_verse, note_index = chapter_verse_note.rsplit(":", 1)
    chapter_number, verse_number = map(int, chapter_verse.split(":"))

    note_coords = notes_coords_data.get(chapter_verse, [])
    if len(note_coords) > int(note_index) - 1:
        coords = note_coords[int(note_index) - 1]
    else:
        coords = None

    merged_data.append(
        [chapter_number, verse_number, int(note_index), note_text, coords]
    )

# Write the merged data back out to a new JSON file
with open("data/notes/merged_notes_data.json", "w") as f:
    json.dump(merged_data, f, separators=(",", ":"))
