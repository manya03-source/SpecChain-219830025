import json
import os
import re

# --- CONFIGURATION ---
DATASET_PATH = "data/reviews_clean.jsonl"
OUTPUT_DIR = "metrics"

PIPELINES = {
    "manual": {
        "personas": "personas/personas_manual.json",
        "spec": "spec/spec_manual.md",
        "tests": "tests/tests_manual.json",
        "output": "metrics/metrics_manual.json"
    },
    "auto": {
        "personas": "personas/personas_auto.json",
        "spec": "spec/spec_auto.md",
        "tests": "tests/tests_auto.json",
        "output": "metrics/metrics_auto.json"
    },
    "hybrid": {
        "personas": "personas/personas_hybrid.json",
        "spec": "spec/spec_hybrid.md",
        "tests": "tests/tests_hybrid.json",
        "output": "metrics/metrics_hybrid.json"
    }
}

AMBIGUOUS_KEYWORDS = [
    "fast", "easy", "better", "user-friendly", "stable", 
    "smooth", "efficient", "intuitive", "robust", 
    "high-quality", "seamless", "flexible"
]

def load_reviews():
    reviews = []
    if os.path.exists(DATASET_PATH):
        with open(DATASET_PATH, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    reviews.append(json.loads(line))
    return reviews

def load_json_artifact(path):
    if not os.path.exists(path):
        return []
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        if isinstance(data, dict):
            # Try to find common keys, otherwise return the whole dict as a list item
            for key in ["tests", "personas", "groups", "requirements"]:
                if key in data: return data[key]
        return data if isinstance(data, list) else [data]

def parse_spec_requirements(path):
    """
    Super-flexible parser. Splits by any markdown header (#) and 
    extracts IDs that look like FR1, FR_auto_1, or FR_hybrid_1.
    """
    if not os.path.exists(path):
        return []
    
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split by any markdown header (e.g., # Requirement ID: FR1 or just # FR1)
    blocks = re.split(r'\n(?=#)', content)
    # If the first block doesn't start with #, it might be the title; split carefully
    if not content.startswith('#'):
        blocks = re.split(r'\n(?=#)', content)
    
    requirements = []
    for block in blocks:
        if not block.strip():
            continue
            
        # 1. Extract the ID: Look for FR followed by numbers or underscores
        id_match = re.search(r'(FR(?:_manual|_auto|_hybrid)?_?\d+)', block, re.IGNORECASE)
        if not id_match:
            continue
        req_id = id_match.group(1).strip()
        
        # 2. Extract Description
        desc = re.search(r'Description:\s*(?:\[)?(.*?)(?:\])?(?:\n|$)', block, re.IGNORECASE)
        
        # 3. Extract Persona
        persona = re.search(r'Source\s*Persona:\s*(?:\[)?(.*?)(?:\])?(?:\n|$)', block, re.IGNORECASE)
        
        # 4. Extract Acceptance Criteria
        ac = re.search(r'Acceptance\s*Criteria:\s*(?:\[)?(.*?)(?:\])?(?:\n|$)', block, re.IGNORECASE)
        
        requirements.append({
            "id": req_id,
            "description": desc.group(1).strip() if desc else "",
            "persona": persona.group(1).strip() if persona else "None",
            "acceptance_criteria": ac.group(1).strip() if ac else ""
        })
    return requirements

def compute_metrics(name, config, total_reviews):
    personas = load_json_artifact(config["personas"])
    requirements = parse_spec_requirements(config["spec"])
    tests = load_json_artifact(config["tests"])
    
    # 1. Counts
    dataset_size = len(total_reviews)
    persona_count = len(personas)
    req_count = len(requirements)
    test_count = len(tests)

    # 2. Traceability Links
    # Links: Personas to Evidence + Reqs to Personas + Tests to Reqs
    links = len(personas) 
    links += sum(1 for r in requirements if r["persona"] and r["persona"].lower() != "none")
    links += sum(1 for t in tests if t.get("requirement_id"))

    # 3. Review Coverage
    covered_ids = set()
    for p in personas:
        evidence = p.get("evidence_reviews", [])
        if isinstance(evidence, list):
            covered_ids.update([str(eid) for eid in evidence])
        else:
            covered_ids.add(str(evidence))
    
    review_coverage = round(len(covered_ids) / dataset_size if dataset_size > 0 else 0, 4)

    # 4. Traceability Ratio (Reqs linked to Personas)
    traceable_reqs = sum(1 for r in requirements if r["persona"] and r["persona"].lower() != "none")
    traceability_ratio = round(traceable_reqs / req_count if req_count > 0 else 0, 2)

    # 5. Testability Rate (Reqs with at least one Test)
    # We check how many unique Requirement IDs from the SPEC are mentioned in the TESTS
    spec_req_ids = {r["id"].lower() for r in requirements}
    test_req_ids = {str(t.get("requirement_id", "")).strip("[] ").lower() for t in tests}
    
    # Calculate intersection (how many spec IDs have a matching test ID)
    matched_reqs = spec_req_ids.intersection(test_req_ids)
    testability_rate = round(len(matched_reqs) / req_count if req_count > 0 else 0, 2)

    # 6. Ambiguity Ratio
    ambiguous_count = 0
    for r in requirements:
        text = (r["description"] + " " + r["acceptance_criteria"]).lower()
        if any(word in text for word in AMBIGUOUS_KEYWORDS):
            ambiguous_count += 1
    ambiguity_ratio = round(ambiguous_count / req_count if req_count > 0 else 0, 2)

    return {
        "dataset_size": dataset_size,
        "persona_count": persona_count,
        "requirements_count": req_count,
        "tests_count": test_count,
        "traceability_links": links,
        "review_coverage": review_coverage,
        "traceability_ratio": traceability_ratio,
        "testability_rate": testability_rate,
        "ambiguity_ratio": ambiguity_ratio
    }

def main():
    reviews = load_reviews()
    if not reviews:
        print("Error: data/reviews_clean.jsonl is missing.")
        return

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    for pipe_name, config in PIPELINES.items():
        print(f"Computing {pipe_name} metrics...")
        try:
            results = compute_metrics(pipe_name, config, reviews)
            with open(config["output"], 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=4)
        except Exception as e:
            print(f"  Error processing {pipe_name}: {e}")

if __name__ == "__main__":
    main()