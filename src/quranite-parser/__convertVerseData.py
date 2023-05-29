import json
import os


def read_original_data(file_path):
    with open(file_path, 'r', encoding="utf-8") as file:
        json_data = json.load(file)
    for item in json_data:
        if item["type"] == "table" and item["name"] == "versesimple":
            return item["data"]
    return []

def separate_translations(quran_data, language):
    translations = []

    for verse in quran_data:
        if int(verse["chapter"]) > 1 and int(verse["verse"]) == 0:
            continue

        translation = [int(verse["chapter"]), int(verse["verse"]), verse[language]]
        translations.append(translation)

    return translations

def save_translation_data(file_path, data):
    with open(file_path, 'w', encoding="utf-8") as file:
        # Compact JSON output by eliminating white space
        json.dump(data, file, separators=(',', ':'), ensure_ascii=False)

def create_directories(base_path, *directories):
    for directory in directories:
        path = os.path.join(base_path, directory)
        if not os.path.exists(path):
            os.makedirs(path)

def main():
    quran_data = read_original_data('data/versesimple.json')
    english_translations = separate_translations(quran_data, 'english')
    arabic_translations = separate_translations(quran_data, 'arabic')

    translations_dir = 'data/translations'
    create_directories(translations_dir)

    save_translation_data(os.path.join(translations_dir, 'en_sam_gerrans.json'), english_translations)
    save_translation_data(os.path.join(translations_dir, 'ar_original.json'), arabic_translations)

if __name__ == '__main__':
    main()