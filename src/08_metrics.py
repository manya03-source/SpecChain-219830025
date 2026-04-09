import json
import os
import re

FILES = {
    "reviews": "data/reviews_clean.jsonl",
    "personas": "personas/personas_hybrid.json",
    "specs": "spec/spec_hybrid.md",
    "tests": "tests/tests_hybrid.json",
    "groups": "data/review_groups_hybrid.json"
}
OUTPUT_METRICS = "metrics/metrics_hybrid.json"

AMBIGUOUS_KEYWORDS = [
    "fast", "easy", "better", "user-friendly", 
    "smooth", "efficient", "intuitive", "robust", 
    "high-quality", "seamless", "flexible"
] 

def load_json(path):
    if not os.path.exists(path):
        return []
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        # Handle both list format and dict wrapper format
        if isinstance(data, dict):
            if "personas" in data: return data["personas"]
            if "tests" in data: return data["tests"]
            if "groups" in data: return data["groups"]
        return data

def load_reviews(path):
    reviews = []
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    reviews.append(json.loads(line))
    return reviews

def parse_markdown_specs(path):
    """Robustly extracts hybrid requirements."""
    if not os.path.exists(path):
        return []
    
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split by Requirement ID header
    blocks = re.split(r'# Requirement ID:\s*', content)
    requirements = []
    
    for block in blocks:
        if not block.strip():
            continue
            
        # Match hybrid IDs
        id_match = re.match(r'(FR_hybrid_\d+)', block)
        if not id_match:
            continue
        
        req_id = id_match.group(1)
        desc = re.search(r'Description:\s*(.*)', block)
        persona = re.search(r'Source Persona:\s*\[?(.*?)\]?\n', block)
        ac = re.search(r'Acceptance Criteria:\s*\[?(.*?)\]?\n', block)
        
        requirements.append({
            "id": req_id,
            "desc": desc.group(1).strip() if desc else "",
            "persona": persona.group(1).strip() if persona else "None",
            "ac": ac.group(1).strip() if ac else ""
        })
        
    return requirements

def calculate_metrics():
    #Load Hybrid Artifacts
    reviews = load_reviews(FILES["reviews"])
    personas = load_json(FILES["personas"])
    requirements = parse_markdown_specs(FILES["specs"])
    tests = load_json(FILES["tests"])
    groups = load_json(FILES["groups"])

    #Basic Counts
    dataset_size = len(reviews)
    persona_count = len(personas)
    req_count = len(requirements)
    test_count = len(tests)

    #Traceability Links Count
    #Persona
    links = 0
    links += len(personas) 
    links += sum(1 for r in requirements if r['persona'] and r['persona'] != "None")
    links += sum(1 for t in tests if t.get('requirement_id'))

    #Review Coverage Ratio
    # Based on the unique reviews listed in the hybrid groups
    covered_ids = set()
    for g in groups:
        covered_ids.update(g.get("review_ids", []))
    review_coverage_ratio = round(len(covered_ids) / dataset_size if dataset_size > 0 else 0, 4)

    #Traceability Ratio
    traceable_reqs = sum(1 for r in requirements if r['persona'] and r['persona'] != "None")
    traceability_ratio = round(traceable_reqs / req_count if req_count > 0 else 0, 2)

    #Testability Rate
    tested_req_ids = {t['requirement_id'] for t in tests}
    testability_rate = round(len(tested_req_ids) / req_count if req_count > 0 else 0, 2)

    #Ambiguity Ratio
    ambiguous_count = 0
    for r in requirements:
        text = (r['desc'] + " " + r['ac']).lower()
        if any(word in text for word in AMBIGUOUS_KEYWORDS):
            ambiguous_count += 1
    ambiguity_ratio = round(ambiguous_count / req_count if req_count > 0 else 0, 2)

    #Results
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

    os.makedirs(os.path.dirname(OUTPUT_METRICS), exist_ok=True)
    with open(OUTPUT_METRICS, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=4)
    
    return results

if __name__ == "__main__":
    print("Computing metrics for HYBRID pipeline...")
    metrics = calculate_metrics()
    for key, value in metrics.items():
        print(f"{key.replace('_', ' ').title()}: {value}")
    print(f"\nResults saved to {OUTPUT_METRICS}")