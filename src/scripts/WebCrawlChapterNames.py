import requests
import json

# Define the API endpoint and parameters
api_url = 'https://api.quran.com/api/v4/chapters'
params = {
    'language': 'en',
    'text_type': 'text',
}

# Send the API request and get the response
response = requests.get(api_url, params=params)
data = response.json()

# Create a list of Quran chapters with the required information
quran_chapters = []
for chapter in data['chapters']:
    quran_chapters.append({
        'number': chapter['id'],
        'name': {
            'arabic': chapter['name_arabic'],
            'transliteration': chapter['name_simple'],
            'english': chapter['translated_name']['name'],
        },
        'verses_count': chapter['verses_count'],
    })

# Output the result to a JSON file
with open('../data/quran-chapters.json', 'w') as f:
    json.dump({'chapters': quran_chapters}, f)
