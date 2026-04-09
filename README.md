# EECS4312_W26_SpecChain
Name: Manya Khattri
Student Number: 219830025
## instructions:
Please update to include: 
- App name: Calm
- Data collection method: Systematic extraction of user feedback from Google PlayStore
- Original dataset: `data/reviews_raw.jsonl` contains the initial raw feedback.
- Final cleaned dataset: `data/reviews_clean.jsonl`.
- Exact commands to run pipeline: 

# example
Application: [Calm]

Dataset:
- reviews_raw.jsonl contains the collected reviews.
- reviews_clean.jsonl contains the cleaned dataset.
- The cleaned dataset contains 842 reviews.

Repository Structure:
- data/ contains datasets and review groups
- personas/ contains persona files
- spec/ contains specifications
- tests/ contains validation tests
- metrics/ contains all metric files
- src/ contains executable Python scripts
- reflection/ contains the final reflection

How to Run:
Prerequisites:
You must export your Groq API key in your terminal environment to run the automated generation steps:
- Run: `export GROQ_API_KEY='your_api_key_here'`
Paste your API key instead of the words "your_api_key_here"

To validate that all files and folders exist in the repo:
- Run: `python src/00_validate_repo.py`

To run the end to end workflow, (collection -> cleaning -> grouping -> personas -> req spec -> tests):
- Run: `python src/run_all.py`

To see metrics comparison for all three (automated, manual and hybrid):
- Run: `python src/08_metrics.py`

