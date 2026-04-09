"""generates tests from specs"""
import json
import os
import re
import time
from groq import Groq

# --- CONFIGURATION ---
INPUT_SPEC = "spec/spec_auto.md"
OUTPUT_TESTS = "tests/tests_auto.json"
MODEL_NAME = "meta-llama/llama-4-scout-17b-16e-instruct"

# Initialize Groq Client (Ensure GROQ_API_KEY is set in your environment)
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def parse_requirements(filepath):
    """
    Parses the Markdown specification file to extract Requirement IDs and Descriptions.
    """
    if not os.path.exists(filepath):
        print(f"Error: {filepath} not found.")
        return []

    requirements = []
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Regex to find Requirement ID and the following Description line
    pattern = r"# Requirement ID:\s*(FR_auto_\d+)\n-\s*Description:\s*(.*?)\n"
    matches = re.findall(pattern, content)

    for req_id, desc in matches:
        requirements.append({
            "requirement_id": req_id,
            "description": desc.strip("[] ")
        })
    
    return requirements

def generate_test_scenario(requirement, index):
    """
    Calls Groq API to generate a structured test scenario for a requirement.
    """
    system_msg = "You are a Quality Assurance engineer. Generate structured software validation tests in JSON format."
    
    user_msg = f"""
    Create a validation test scenario for the following system requirement:
    Requirement ID: {requirement['requirement_id']}
    Description: {requirement['description']}

    Return ONLY a JSON object for this single test following this template:
    {{
      "test_id": "T_auto_{index}",
      "requirement_id": "{requirement['requirement_id']}",
      "scenario": "[Short description of the scenario]",
      "steps": [
        "Step 1",
        "Step 2",
        "Step 3"
      ],
      "expected_result": "[What happens if the requirement is met]"
    }}
    """

    try:
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_msg},
                {"role": "user", "content": user_msg}
            ],
            model=MODEL_NAME,
            response_format={"type": "json_object"}
        )
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        print(f"Error generating test for {requirement['requirement_id']}: {e}")
        return None

def main():
    print("--- Starting Task 4.4: Automated Test Generation ---")
    
    requirements = parse_requirements(INPUT_SPEC)
    if not requirements:
        print("No requirements found to process.")
        return

    print(f"Parsed {len(requirements)} requirements. Generating tests...")
    
    test_list = []
    for i, req in enumerate(requirements, start=1):
        print(f"Generating test for {req['requirement_id']}...")
        test_data = generate_test_scenario(req, i)
        if test_data:
            test_list.append(test_data)
        
        # Buffer to respect rate limits and prevent API bans
        time.sleep(3)

    # Save to JSON file in the requested structure
    output_data = {"tests": test_list}
    
    os.makedirs(os.path.dirname(OUTPUT_TESTS), exist_ok=True)
    with open(OUTPUT_TESTS, "w", encoding="utf-8") as f:
        json.dump(output_data, f, indent=4)

    print(f"Success! {len(test_list)} tests saved to {OUTPUT_TESTS}")

if __name__ == "__main__":
    main()