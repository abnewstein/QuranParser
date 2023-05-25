import json
import time
from collections import defaultdict
from bs4 import BeautifulSoup
import os

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.firefox import GeckoDriverManager


def read_progress():
    if os.path.exists("data/notes/en_sg_notes-coordinates.json"):
        with open(file="data/notes/en_sg_notes-coordinates.json", mode="r") as infile:
            quran = json.load(infile)
            last_key = list(quran.keys())[-1]
            chapter, _ = map(int, last_key.split(":"))
            return chapter, quran
    return 1, defaultdict(dict)


def write_progress(quran):
    try:
        with open(file="data/notes/en_sg_notes-coordinates.json", mode="w") as outfile:
            json.dump(quran, outfile)
    except Exception as e:
        print("Failed to write to JSON: ", e)


url = "https://reader.quranite.com/verses/chapters?chapter={0}&page={1}"
driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()))

page = 1
chapter, quran = read_progress()
print(f"Starting from Chapter {chapter}")

while True:
    if chapter > 114:
        break
    try:
        print(f"Processing Chapter {chapter}, Page {page}")
        driver.get(url.format(chapter, page))
        time.sleep(0.5)

        isError = driver.find_elements(By.CSS_SELECTOR, ".error")
        if len(isError) > 0:
            chapter = chapter + 1
            page = 1
            continue

        verses_data = driver.find_elements(By.CSS_SELECTOR, ".post-item")
        for verse in verses_data:
            verseNumber = verse.get_attribute("id")
            verse_html = verse.get_attribute("innerHTML")
            soup = BeautifulSoup(verse_html, "html.parser")
            english_data = soup.select_one(".englishData > p")
            if english_data is None:
                continue
            # Remove the first sup tag (verse number)
            first_sup = english_data.find("sup")
            if first_sup:
                first_sup.replace_with("")
            verse_text = str(english_data.text).strip()
            sup_tags = english_data.find_all("a", class_="showComment")
            if sup_tags:
                for tag in sup_tags:
                    note = tag.text
                    verse_key = f"{chapter}:{verseNumber}"
                    if verse_key not in quran:
                        quran[verse_key] = []  # type: ignore
                    for i in range(len(verse_text)):
                        if verse_text.startswith(note, i):
                            quran[verse_key].append(i)  # type: ignore
                            break  # break the loop after the first match
                    write_progress(quran)

        page = page + 1

    except Exception as e:
        print("Error occurred: ", e)

write_progress(quran)
print("Completed Processing")
