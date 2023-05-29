import json
import os
import re
import sys

def load_json_file(file_path):
    try:
        print(f"Loading file: {file_path}", end='\r')
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"File {file_path} loaded successfully!")
        return data
    except FileNotFoundError:
        print(f"File {file_path} not found. Exiting...")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error decoding JSON from file {file_path}. Exiting...")
        sys.exit(1)

def write_json_file(file_path, data):
    try:
        print(f"Writing file: {file_path}", end='\r')
        with open(file_path, 'w') as f:
            json.dump(data, f, separators=(',', ':'))
        print(f"File {file_path} written successfully!")
    except Exception as e:
        print(f"Error writing to file {file_path}. Exception: {e}")
        sys.exit(1)

def get_insert_position(verse_text, note_index, adjustment):
    insert_position = note_index + adjustment
    sub_verse_text = verse_text[:insert_position]
    search_end = insert_position
    while True:
        num_i_o_tags = sub_verse_text.count('<i>') 
        num_i_c_tags = sub_verse_text.count('</i>')
        incomplete_tags = abs(num_i_c_tags - num_i_o_tags)
        dangling_tags = abs(sub_verse_text.count('<') - sub_verse_text.count('>'))
        search_end += 1
        if incomplete_tags > 0 or dangling_tags > 0:
            search_end += 1
        elif incomplete_tags == 0 and dangling_tags == 0:
            insert_position += 3 * num_i_o_tags
            insert_position += 4 * num_i_c_tags
            sub_verse_text = re.sub(r'<i>(.*?)</i>', r'\1', sub_verse_text)
            break
        else:
            search_end += 1
        
        sub_verse_text = verse_text[:search_end]
    return insert_position

def main():
    try:
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
        total_verses = len(verses_data)

        for i, (chapter_num, verse_num, verse_text) in enumerate(verses_data):        
            verse_notes = notes_dict.get((chapter_num, verse_num), [])
            adjustment = 0
            for note_num, note_content, note_index in verse_notes:        
                insert_position = get_insert_position(verse_text, note_index, adjustment)
                superscript = f"<sup>{note_num}</sup>"
                verse_text = verse_text[:insert_position] + superscript + verse_text[insert_position:]        
                adjustment += 11
            merged_data.append([chapter_num, verse_num, verse_text])        
            print(f"Processed {i+1}/{total_verses} verses", end='\r')

        write_json_file(outputFile, merged_data)
        print("\nProcessing completed successfully!")

    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
