"""imports or reads your raw dataset; if you scraped, include scraper here"""

import os
import json
from google_play_scraper import Sort, reviews

APP_ID = 'com.calm.android'
OUTPUT_FILE = 'data/reviews_raw.jsonl'
TARGET_COUNT = 4000  #My app Calm, has 610K reviews online.

def collect_data():
    # This is where raw reviews will be stored
    if not os.path.exists('data'):
        os.makedirs('data')

    print(f"Fetching {TARGET_COUNT} reviews for {APP_ID}...")

    #Data Scraping
    result, _ = reviews(
        APP_ID,
        lang='en',        
        country='us',     
        sort=Sort.NEWEST, 
        count=TARGET_COUNT
    )

    # Task 2 Specification: To store the raw dataset in JSON Lines format (.jsonl)
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        for entry in result:
            entry['at'] = entry['at'].isoformat()
            if 'repliedAt' in entry and entry['repliedAt']:
                entry['repliedAt'] = entry['repliedAt'].isoformat()
            f.write(json.dumps(entry) + '\n')

    print(f"Done! Saved {len(result)} reviews to {OUTPUT_FILE}")

if __name__ == "__main__":
    collect_data()