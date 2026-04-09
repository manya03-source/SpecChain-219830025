import json
import os
import time
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from groq import Groq

# --- CONFIGURATION (Based on Project PDF) ---
INPUT_PATH = "data/reviews_clean.jsonl"
GROUPS_PATH = "data/review_groups_auto.json"
PERSONAS_PATH = "personas/personas_auto.json"
PROMPT_PATH = "prompts/prompt_auto.json"
MODEL_NAME = "meta-llama/llama-4-scout-17b-16e-instruct"

# Initialize Groq Client
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def main():
    print("--- Starting Task 4.1: Mathematical Grouping ---")
    
    # 1. Load Cleaned Data [cite: 158]
    reviews_data = []
    with open(INPUT_PATH, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                reviews_data.append(json.loads(line))
    
    docs = [r.get("content_cleaned", "") for r in reviews_data]
    print(f"Loaded {len(docs)} reviews.")

    # 2. Mathematical Grouping (K-Means) [cite: 216]
    vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
    X = vectorizer.fit_transform(docs)
    # Project requires 5 groups representing distinct types [cite: 175, 218]
    kmeans = KMeans(n_clusters=5, random_state=42, n_init=10)
    kmeans.fit(X)

    # 3. Structure the Groups for the LLM
    auto_groups = {}
    for i in range(5):
        auto_groups[i] = {
            "id": f"group_{i+1}",
            "theme": "", # Will be refined by LLM or vectorizer
            "review_ids": [],
            "sample_texts": []
        }

    for idx, label in enumerate(kmeans.labels_):
        auto_groups[label]["review_ids"].append(reviews_data[idx]["reviewId"])
        # SAMPLING: Only take 15 reviews to avoid token limits and API bans
        if len(auto_groups[label]["sample_texts"]) < 15:
            auto_groups[label]["sample_texts"].append(docs[idx])

    # Save Grouping File [cite: 218]
    with open(GROUPS_PATH, "w", encoding="utf-8") as f:
        json.dump(list(auto_groups.values()), f, indent=4)

    print("--- Starting Task 4.2: Automated Persona Generation ---")
    
    final_personas = []
    # Store the prompt for documentation [cite: 220]
    last_full_prompt = {"system": "", "user": ""}

    for i in range(5):
        group = auto_groups[i]
        print(f"Generating persona for {group['id']}...")

        system_msg = "You are a requirements engineer. Create a structured user persona in JSON format based on user reviews."
        
        # This prompt follows your personas_manual.json template 
        user_msg = f"""
        Based on these reviews, create a persona for an app.
        Return ONLY a JSON object following this template:
        {{
          "id": "P{i+1}",
          "name": "[Catchy Name]",
          "description": "[1-sentence summary]",
          "derived_from_group": "{group['id']}",
          "goals": ["goal 1", "goal 2"],
          "pain_points": ["pain 1", "pain 2"],
          "context": ["context 1", "context 2"],
          "constraints": ["constraint 1"],
          "evidence_reviews": {json.dumps(group['review_ids'][:2])}
        }}

        REVIEWS:
        {chr(10).join(group['sample_texts'])}
        """

        try:
            chat_completion = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_msg},
                    {"role": "user", "content": user_msg}
                ],
                model=MODEL_NAME,
                response_format={"type": "json_object"}
            )
            
            persona_json = json.loads(chat_completion.choices[0].message.content)
            final_personas.append(persona_json)
            
            # Record prompts for the prompts/prompt_auto.json file [cite: 220]
            last_full_prompt = {"system": system_msg, "user": user_msg}
            
            # Wait 5 seconds between requests to avoid rate limits
            time.sleep(5) 
            
        except Exception as e:
            print(f"Error processing {group['id']}: {e}")

    # 4. Save Final Outputs
    # Save Personas 
    os.makedirs(os.path.dirname(PERSONAS_PATH), exist_ok=True)
    with open(PERSONAS_PATH, "w", encoding="utf-8") as f:
        json.dump(final_personas, f, indent=4)

    # Save Prompt documentation [cite: 220, 252]
    os.makedirs(os.path.dirname(PROMPT_PATH), exist_ok=True)
    with open(PROMPT_PATH, "w", encoding="utf-8") as f:
        json.dump(last_full_prompt, f, indent=4)

    print(f"Success! Created {len(final_personas)} personas.")

if __name__ == "__main__":
    main()