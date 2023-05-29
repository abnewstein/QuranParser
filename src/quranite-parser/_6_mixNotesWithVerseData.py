import json
import os
import re

def load_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

def write_json_file(file_path, data):
    with open(file_path, 'w') as f:
        json.dump(data, f, separators=(',', ':'))

def get_insert_position(verse_text, note_index, adjustment):
    insert_position = note_index + adjustment
    sub_verse_text = verse_text[:insert_position]
    
    while True:
        num_i_o_tags = sub_verse_text.count('<i>') 
        num_i_c_tags = sub_verse_text.count('</i>')
        incomplete_tags = sub_verse_text.count('<') - sub_verse_text.count('>')
        
        if incomplete_tags > 0:
            insert_position += 1
        elif num_i_o_tags > 0 or num_i_c_tags > 0:
            insert_position += 3 * num_i_o_tags
            insert_position += 4 * num_i_c_tags
        else:
            break

        sub_verse_text = verse_text[:insert_position]
        sub_verse_text = re.sub(r'<i>|</i>', '', sub_verse_text)

    return insert_position

def main():
    dir = os.path.dirname(__file__)
    notesFile = os.path.join(dir, '../data/notes/notes_en_sam-gerrans.json')
    versesFile = os.path.join(dir, '../data/translations/en_sam-gerrans.json')
    outputFile = os.path.join(dir, '../data/translations/en_sam-gerrans_with-notes.json')

    notes_data = load_json_file(notesFile)
    verses_data = load_json_file(versesFile)

    notes_dict = {(chapter_num, verse_num): [] for chapter_num, verse_num, _, _, _ in notes_data}

    for chapter_num, verse_num, note_num, note_content, note_index in notes_data:
        notes_dict[(chapter_num, verse_num)].append((note_num, note_content, note_index))

    notes_dict = {k: sorted(v, key=lambda x: x[2]) for k, v in notes_dict.items()}

    merged_data = []

    for chapter_num, verse_num, verse_text in verses_data:
        verse_notes = notes_dict.get((chapter_num, verse_num), [])

        adjustment = 0
        for note_num, note_content, note_index in verse_notes:        
            insert_position = get_insert_position(verse_text, note_index, adjustment)

            # Compute the superscript to be inserted and insert it
            superscript = f"<sup>{note_num}</sup>"
            verse_text = verse_text[:insert_position] + superscript + verse_text[insert_position:]        
            adjustment += len(superscript)

        merged_data.append([chapter_num, verse_num, verse_text])            

    write_json_file(outputFile, merged_data)

if __name__ == "__main__":
    main()
