"""runs the full pipeline end-to-end"""

import subprocess
import sys
import os

def run_script(script_path):
    """Executes a python script and handles errors."""
    print(f"\n>>> Executing: {script_path}...")
    try:
        # Run the script and wait for it to finish
        result = subprocess.run([sys.executable, script_path], check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while running {script_path}: {e}")
        return False

def main():
    print("===============================================")
    print("STARTING FULL AUTOMATED REQUIREMENTS PIPELINE")
    print("===============================================")

    #Collecting Raw Dataset
    if not run_script("src/01_collect_or_import.py"): 
        sys.exit(1)

    #Cleaning dataset (removing duplicates, filtering out irrelevant reviews, etc.)
    if not run_script("src/02_clean.py"):
        sys.exit(1)

    #Grouping reviews into themes and generating personas for each theme
    if not run_script("src/05_personas_auto.py"):
        sys.exit(1)

    #Generating specification from the personas and reviews using LLMs
    if not run_script("src/06_spec_generate.py"):
        sys.exit(1)

    #Generating tests from the specification using LLMs
    if not run_script("src/07_tests_generate.py"):
        sys.exit(1)

    #Metrics computation for the generated artifacts
    if not run_script("src/08_metrics.py"):
        sys.exit(1)

    print("\n===============================================")
    print("AUTOMATED PIPELINE COMPLETED SUCCESSFULLY")
    print("All artifacts generated in data/, personas/, spec/, tests/, and metrics/")
    print("===============================================")

if __name__ == "__main__":
    main()