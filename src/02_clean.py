"""cleans raw data & make clean dataset"""
import pandas as pd
import json
import os
import re
import spacy
import inflect

nlp = spacy.load("en_core_web_sm")
p = inflect.engine()

RAW_FILE = 'data/reviews_raw.jsonl'
CLEAN_FILE = 'data/reviews_clean.jsonl'
METADATA_FILE = 'data/dataset_metadata.json'
APP_NAME = "Calm"

def text_cleaning_pipeline(text):
    if not text:
        return ""
    
    # Convert numbers to text
    words = []
    for word in text.split():
        if word.isdigit():
            try:
                words.append(p.number_to_words(word))
            except:
                words.append(word)
        else:
            words.append(word)
    text = " ".join(words)

    # remove emojis and special characters, remove punctuation
    text = re.sub(r'[^a-zA-Z\s]', '', text)

    #To remove stop words and lemmatize (using spacy)
    doc = nlp(text.lower())
    
    cleaned_tokens = [
        token.lemma_ for token in doc 
        if not token.is_stop and not token.is_space and len(token.text) > 1
    ]
    
    return " ".join(cleaned_tokens)

def main():
    if not os.path.exists(RAW_FILE):
        print(f"Error: {RAW_FILE} not found!")
        return

    #Load data
    df = pd.read_json(RAW_FILE, lines=True)
    initial_count = len(df)

    #Remove duplicates and empty entries
    df = df.drop_duplicates(subset=['content'])
    df = df.dropna(subset=['content'])
    print("Starting NLP cleaning (this may take a minute)...")
    df['content_cleaned'] = df['content'].apply(text_cleaning_pipeline)

    #Filter out reviews that are too short after cleaning
    df = df[df['content_cleaned'].str.len() > 3]

    #Save cleaned dataset
    df.to_json(CLEAN_FILE, orient='records', lines=True)

    #Create Metadata File
    metadata = {
        "app_name": APP_NAME,
        "dataset_size": len(df),
        "collection_method": "Scraped from Google Play Store using google-play-scraper",
        "cleaning_decisions": [
            "Removed duplicates and null entries",
            "Filtered out reviews with < 4 characters after processing",
            "Converted numbers to text using inflect",
            "Removed punctuation, special characters, and emojis via Regex",
            "Lowercased all text",
            "Removed stop words and performed lemmatization using spaCy en_core_web_sm"
        ]
    }

    with open(METADATA_FILE, 'w') as f:
        json.dump(metadata, f, indent=4)

    print(f"Processing complete!")
    print(f"- Cleaned {initial_count} down to {len(df)} high-quality reviews.")
    print(f"- Metadata saved to {METADATA_FILE}")

if __name__ == "__main__":
    main()