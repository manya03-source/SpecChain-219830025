"""creates/updates coding table template + instructions"""
import pandas as pd
import json
import os

CLEAN_DATA = 'data/reviews_clean.jsonl'
SAMPLE_OUT = 'data/review_sample_for_analysis.csv'
GROUPS_OUT = 'data/review_groups_manual.json'

def prepare_manual_coding():
    if not os.path.exists(CLEAN_DATA):
        print("Error: Cleaned data not found. Run src/02_clean.py first.")
        return

    #Load cleaned data
    df = pd.read_json(CLEAN_DATA, lines=True)
    
    #Export a sample of 100 reviews (to select themes)
    sample = df.sample(n=min(100, len(df)), random_state=42)
    sample[['reviewId', 'content', 'score']].to_csv(SAMPLE_OUT, index=False)
    
    #Initialize the JSON structure to help identify themes and review IDs for manual coding
    template = {
        "group_1": {"theme": "", "review_ids": []},
        "group_2": {"theme": "", "review_ids": []},
        "group_3": {"theme": "", "review_ids": []},
        "group_4": {"theme": "", "review_ids": []},
        "group_5": {"theme": "", "review_ids": []}
    }
    
    with open(GROUPS_OUT, 'w') as f:
        json.dump(template, f, indent=4)

    print(f"Success!")
if __name__ == "__main__":
    prepare_manual_coding()