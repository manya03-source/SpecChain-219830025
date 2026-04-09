import json
import os
import re

# --- CONFIGURATION ---
FILES = {
    "reviews": "data/reviews_clean.jsonl",
    "personas": "personas/personas_auto.json",
    "specs": "spec/spec_auto.md",
    "tests": "tests/tests_auto.json",
    "groups": "data/review_groups_auto.json"
}
OUTPUT_METRICS = "metrics/metrics_auto.json"

# Ambiguous terms to check for in requirements (as per project guidelines)
AMBIGUOUS_KEYWORDS = [
    "fast", "easy", "better", "user-friendly", "stable", 
    "smooth", "efficient", "intuitive", "robust", 
    "high-quality", "seamless", "flexible"
]

def load_json(path):
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def load_reviews(path):
    reviews = []
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    reviews.append(json.loads(line))
    return reviews

def parse_markdown_specs(path):
    """
    More robustly extracts requirements by splitting the file into blocks 
    based on the Requirement ID header.
    """
    if not os.path.exists(path):
        print(f"File not found: {path}")
        return []
    
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split the file by the main Requirement ID header
    blocks = re.split(r'# Requirement ID:\s*', content)
    requirements = []
    
    for block in blocks:
        if not block.strip():
            continue
            
        # Extract ID (the first word/code after the split)
        id_match = re.match(r'(FR_auto_\d+)', block)
        if not id_match:
            continue
        req_id = id_match.group(1)
        
        # Use more flexible patterns for the other fields
        desc = re.search(r'Description:\s*(.*)', block)
        persona = re.search(r'Source Persona:\s*\[?(.*?)\]?\n', block)
        ac = re.search(r'Acceptance Criteria:\s*(.*)', block)
        
        requirements.append({
            "id": req_id,
            "desc": desc.group(1).strip() if desc else "",
            "persona": persona.group(1).strip() if persona else "None",
            "ac": ac.group(1).strip() if ac else ""
        })
        
    return requirements

def calculate_metrics():
    # 1. Load all artifacts
    reviews = load_reviews(FILES["reviews"])
    personas = load_json(FILES["personas"])
    requirements = parse_markdown_specs(FILES["specs"])
    tests_data = load_json(FILES["tests"])
    tests = tests_data.get("tests", []) if isinstance(tests_data, dict) else []
    groups = load_json(FILES["groups"])

    # 2. Basic Counts
    dataset_size = len(reviews)
    persona_count = len(personas)
    req_count = len(requirements)
    test_count = len(tests)

    # 3. Traceability Links Count
    # Links: Groups->Personas + Personas->Reqs + Reqs->Tests
    links = 0
    links += len(personas) # Each persona links to a group
    links += sum(1 for r in requirements if r['persona']) # Reqs to personas
    links += sum(1 for t in tests if t.get('requirement_id')) # Tests to reqs

    # 4. Review Coverage Ratio
    # In the automated pipeline, all reviews belong to a group. 
    # If all 5 groups are used to create personas, coverage is 1.0.
    covered_review_ids = set()
    for persona in personas:
        evidence = persona.get("evidence_reviews", [])
        covered_review_ids.update(evidence)
    
    # However, if using cluster coverage:
    # All reviews in the 5 groups / total reviews
    total_grouped_reviews = sum(len(g.get("review_ids", [])) for g in groups)
    review_coverage_ratio = round(total_grouped_reviews / dataset_size if dataset_size > 0 else 0, 2)

    # 5. Traceability Ratio
    # Proportion of requirements that trace back to a persona
    traceable_reqs = sum(1 for r in requirements if r['persona'] and r['persona'] != "None")
    traceability_ratio = round(traceable_reqs / req_count if req_count > 0 else 0, 2)

    # 6. Testability Rate
    # Proportion of requirements that have at least one associated test
    tested_req_ids = {t['requirement_id'] for t in tests}
    testability_rate = round(len(tested_req_ids) / req_count if req_count > 0 else 0, 2)

    # 7. Ambiguity Ratio
    # Check descriptions and AC for vague terms
    ambiguous_count = 0
    for r in requirements:
        text_to_check = (r['desc'] + " " + r['ac']).lower()
        if any(word in text_to_check for word in AMBIGUOUS_KEYWORDS):
            ambiguous_count += 1
    ambiguity_ratio = round(ambiguous_count / req_count if req_count > 0 else 0, 2)

    # 8. Compile Results
    results = {
        "dataset_size": dataset_size,
        "persona_count": persona_count,
        "requirements_count": req_count,
        "tests_count": test_count,
        "traceability_links": links,
        "review_coverage_ratio": review_coverage_ratio,
        "traceability_ratio": traceability_ratio,
        "testability_rate": testability_rate,
        "ambiguity_ratio": ambiguity_ratio
    }

    # Save to file
    os.makedirs(os.path.dirname(OUTPUT_METRICS), exist_ok=True)
    with open(OUTPUT_METRICS, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=4)
    
    return results

if __name__ == "__main__":
    print("Computing metrics for automated pipeline...")
    metrics = calculate_metrics()
    for key, value in metrics.items():
        print(f"{key.replace('_', ' ').title()}: {value}")
    print(f"\nResults saved to {OUTPUT_METRICS}")