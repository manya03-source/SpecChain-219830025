"""generates structured specs from personas"""
import json
import os
import time
from groq import Groq

# --- CONFIGURATION ---
INPUT_PERSONAS = "personas/personas_auto.json"
OUTPUT_SPEC = "spec/spec_auto.md"
MODEL_NAME = "meta-llama/llama-4-scout-17b-16e-instruct"

# Initialize Groq Client
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def load_personas():
    if not os.path.exists(INPUT_PERSONAS):
        print(f"Error: {INPUT_PERSONAS} not found.")
        return []
    with open(INPUT_PERSONAS, "r", encoding="utf-8") as f:
        return json.load(f)

def generate_requirements(persona):
    """
    Uses the Groq API to derive structured requirements from a persona.
    """
    system_msg = "You are a senior requirements engineer. Convert user personas into technical system specifications."
    
    user_msg = f"""
    Based on the following persona, generate 2-3 detailed functional requirements.
    
    PERSONA:
    - Name: {persona['name']}
    - Description: {persona['description']}
    - Goals: {', '.join(persona['goals'])}
    - Pain Points: {', '.join(persona['pain_points'])}
    - Derived from: {persona['derived_from_group']}

    For EACH requirement, follow this EXACT Markdown format:
    
    # Requirement ID: FR_auto_[Number]
    - Description: [The system shall...]
    - Source Persona: [{persona['name']}]
    - Traceability: [Derived from review group {persona['derived_from_group']}]
    - Acceptance Criteria: [Given..., When..., Then...]

    Return ONLY the markdown requirements.
    """

    try:
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_msg},
                {"role": "user", "content": user_msg}
            ],
            model=MODEL_NAME,
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error generating specs for {persona['name']}: {e}")
        return ""

def main():
    print("--- Starting Task 4.3: Automated Specification Generation ---")
    
    personas = load_personas()
    if not personas:
        return

    all_specs = []
    for persona in personas:
        print(f"Deriving requirements from persona: {persona['name']}...")
        spec_text = generate_requirements(persona)
        if spec_text:
            all_specs.append(spec_text)
        
        # Buffer to avoid API rate limits/bans as experienced in Task 4.2
        time.sleep(3)

    # Save to Markdown file
    os.makedirs(os.path.dirname(OUTPUT_SPEC), exist_ok=True)
    with open(OUTPUT_SPEC, "w", encoding="utf-8") as f:
        f.write("# Automated Software Specifications\n\n")
        f.write("\n\n".join(all_specs))

    print(f"Success! Specifications saved to {OUTPUT_SPEC}")

if __name__ == "__main__":
    main()