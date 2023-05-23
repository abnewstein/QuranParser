import requests
import json
import time
import logging
import argparse

logging.basicConfig(level=logging.INFO)
result_file = "data/notes/en_sg_notes-text.json"


def parse_arguments():
    parser = argparse.ArgumentParser(description="API data collector")
    parser.add_argument(
        "--max-chapter", type=int, default=114, help="maximum chapter to check"
    )
    parser.add_argument(
        "--max-note", type=int, default=20, help="maximum note to check"
    )
    return parser.parse_args()


def load_existing_results():
    results = {}
    try:
        with open(result_file, "r") as f:
            for line in f:
                result = json.loads(line)
                results.update(result)
            logging.info("Loaded existing results from file")
        return results
    except FileNotFoundError:
        logging.info("No existing results file found")
        return {}


def save_results(key, data):
    with open(result_file, "a") as f:
        line = json.dumps({key: data})
        f.write(line + "\n")


def fetch_data(chapter, verse, note):
    url = "https://reader.quranite.com/notes/search"
    response = requests.get(
        url, params={"chapter": chapter, "verse": verse, "note": note}
    )

    if response.status_code != 200:
        logging.error("API request failed with status code %s", response.status_code)
        return None

    return response.json()


def main():
    args = parse_arguments()
    results = load_existing_results()

    with open("data/quran-chapters.json", "r") as f:
        chapters_info = json.load(f)

    for chapter_info in chapters_info:
        chapter = chapter_info["number"]
        max_verse = chapter_info["versesCount"]
        for verse in range(1, max_verse + 1):
            for note in range(1, args.max_note + 1):
                key = f"{chapter}:{verse}:{note}"
                if key not in results:
                    data = fetch_data(chapter, verse, note)
                    if data is None:
                        logging.info(
                            f"No data found for chapter {chapter}, verse {verse}, note {note}"
                        )
                        break

                    logging.info(f"Successfully fetched data for {key}")
                    save_results(key, data)

                # Sleep for rate limiting
                time.sleep(0.1)


if __name__ == "__main__":
    main()
