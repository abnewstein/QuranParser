import json
import os


def read_original_data(file_path):
    with open(file_path, 'r', encoding="utf-8") as file:
        json_data = json.load(file)
    for item in json_data:
        if item["type"] == "table" and item["name"] == "versesimple":
            return item["data"]
    return []


def separate_translations(quran_data):
    english_data = []
    arabic_data = []
    current_id = 1

    for verse in quran_data:
        if int(verse["chapter"]) > 1 and int(verse["verse"]) == 0:
            continue

        english_verse = {"id": current_id, "chapterNumber": int(verse["chapter"]), "verseNumber": int(verse["verse"]),
                         "text": verse["english"]}
        arabic_verse = {"id": current_id, "chapterNumber": int(verse["chapter"]), "verseNumber": int(verse["verse"]),
                        "text": verse["arabic"]}
        english_data.append(english_verse)
        arabic_data.append(arabic_verse)
        current_id += 1

    return english_data, arabic_data


def create_directories(base_path, *directories):
    for directory in directories:
        path = os.path.join(base_path, directory)
        if not os.path.exists(path):
            os.makedirs(path)


def save_translation_data(file_path, data):
    with open(file_path, 'w', encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False)


def main():
    quran_data = read_original_data('data/versesimple.json')
    english_data, arabic_data = separate_translations(quran_data)

    translations_dir = 'data/translations'
    create_directories(translations_dir)

    save_translation_data(os.path.join(translations_dir, 'en_sam_gerrans.json'), english_data)
    save_translation_data(os.path.join(translations_dir, 'ar_original.json'), arabic_data)


if __name__ == '__main__':
    main()
