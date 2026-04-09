"""checks all required files and folders exist individually"""
import os

def validate_repository():
    # List of required folders
    required_folders = [
        "data", "personas", "spec", "metrics", "src", "tests", "reflection", "prompts"
    ]

    # Comprehensive list of all required files
    required_files = [
        "data/reviews_raw.jsonl",
        "data/reviews_clean.jsonl",
        "data/dataset_metadata.json",
        "data/review_groups_manual.json",
        "data/review_groups_auto.json",
        "data/review_groups_hybrid.json",
        "personas/personas_manual.json",
        "personas/personas_auto.json",
        "personas/personas_hybrid.json",
        "spec/spec_manual.md",
        "spec/spec_auto.md",
        "spec/spec_hybrid.md",
        "metrics/metrics_manual.json",
        "metrics/metrics_auto.json",
        "metrics/metrics_hybrid.json",
        "metrics/metrics_summary.json",
        "tests/tests_manual.json",
        "tests/tests_auto.json",
        "tests/tests_hybrid.json",
        "reflection/reflection.md",
        "prompts/prompt_auto.json",
        "README.md",
        "src/run_all.py",
        "src/08_metrics.py",
        "src/00_validate_repo.py"
    ]

    print("Checking repository structure...")

    # Validate Folders
    for folder in required_folders:
        if os.path.isdir(folder):
            print(f"{folder}/ found")
        else:
            print(f"MISSING FOLDER: {folder}")

    # Validate Files
    for file_path in required_files:
        if os.path.isfile(file_path):
            print(f"{file_path} found")
        else:
            print(f"MISSING FILE: {file_path}")

    print("Repository validation complete")

if __name__ == "__main__":
    validate_repository()