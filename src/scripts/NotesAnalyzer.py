import os
import json
import re

dir = os.path.dirname(__file__)
notesFile = os.path.join(dir,"../data/notes_en_sam-gerrans.json")
outputFile = os.path.join(dir,"../data/notes_en_sam-gerrans_final.json")

# load the JSON data
# with open(notesFile, 'r', encoding='utf-8') as f:    
#     notes = json.load(f)
with open(outputFile, 'r', encoding='utf-8') as f:    
    notes = json.load(f)
    
def fix_dangling_tags(note_text):
    # pattern matches an anchor tag, a hyphen and a number
    pattern = r"(<a[^>]*>[^<]*)(</a>)-(\d+)"
    fixed_text = re.sub(pattern, r"\1-\3\2", note_text)
    return fixed_text

def fix_anchor_tags():
    notes_with_dangling_tags = []
    
    for note in notes:
        if("</a>-" in note[1]):
            fixed_text = fix_dangling_tags(note[1])
            note[1] = fixed_text  # replacing original note text with fixed text
            notes_with_dangling_tags.append(note)

    print("Fixed notes with dangling tags: ", len(notes_with_dangling_tags))
    
    # Saving the corrected notes back to the file
    with open(outputFile, 'w', encoding='utf-8') as f:
        json.dump(notes, f)

def validate_anchor_tags():
    notes_with_dangling_tags = []
    
    for note in notes:
        if("</a>-" in note[1]):
            notes_with_dangling_tags.append(note)

    print("Notes with dangling tags: ", len(notes_with_dangling_tags))
    print(notes_with_dangling_tags)

if __name__ == "__main__":
    # fix_anchor_tags()
    validate_anchor_tags()
