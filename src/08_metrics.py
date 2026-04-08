import json
import re
import os

def compute_manual_metrics():
    # 1. Dataset Size
    with open('data/reviews_clean.jsonl', 'r') as f:
        dataset_size = sum(1 for line in f)

    # 2. Persona Count
    with open('personas/personas_manual.json', 'r') as f:
        personas = json.load(f)['personas']
        persona_count = len(personas)

    # 3. Requirements Count (Parsing Markdown)
    with open('spec/spec_manual.md', 'r') as f:
        spec_content = f.read()
        # UPDATED REGEX: Matches "# Requirement ID: FR1", "# Requirement ID: FR10", etc.
        requirements = re.findall(r'# Requirement ID:\s*(FR\d+)', spec_content)
        req_count = len(requirements)

    # Safety Check to prevent ZeroDivisionError
    if req_count == 0:
        print("CRITICAL ERROR: No requirements found. Check your regex and spec_manual.md!")
        return 

    # 4. Tests Count
    with open('tests/tests_manual.json', 'r') as f:
        tests = json.load(f)['tests']
        tests_count = len(tests)

    # 5. Ratio Calculations
    # Review Coverage: Unique reviews cited in personas / Total dataset size
    cited_reviews = set()
    for p in personas:
        cited_reviews.update(p.get('evidence_reviews', []))
    review_coverage = round(len(cited_reviews) / dataset_size, 4)

    # Traceability Ratio: Requirements with a Source Persona listed
    # UPDATED REGEX: Matches your specific line "- Source Persona: [Name]"
    reqs_with_persona = len(re.findall(r'- Source Persona:', spec_content))
    traceability_ratio = round(reqs_with_persona / req_count, 2)

    # Testability Rate: Proportion of Requirements found in your tests file
    tested_req_ids = set(t['requirement_id'] for t in tests)
    # Checks intersection between FR IDs in spec and requirement_ids in tests
    testability_rate = round(len(tested_req_ids.intersection(requirements)) / req_count, 2)

    # 6. Final Results Dictionary
    metrics = {
        "pipeline": "manual",
        "dataset_size": dataset_size,
        "persona_count": persona_count,
        "requirements_count": req_count,
        "tests_count": tests_count,
        "traceability_links": reqs_with_persona + tests_count,
        "review_coverage": review_coverage,
        "traceability_ratio": traceability_ratio,
        "testability_rate": testability_rate,
        "ambiguity_ratio": 0.0 # Standard for manual entry
    }

    # Save results to metrics/metrics_manual.json
    os.makedirs('metrics', exist_ok=True)
    with open('metrics/metrics_manual.json', 'w') as f:
        json.dump(metrics, f, indent=2)
    
    print(f"Success! Processed {req_count} requirements and {tests_count} test scenarios.")

if __name__ == "__main__":
    compute_manual_metrics()