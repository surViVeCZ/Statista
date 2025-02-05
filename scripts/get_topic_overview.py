import pandas as pd
import json
import re

# Load the CSV file
file_path = "digital_lifestyle.csv"
df = pd.read_csv(file_path)

# Identify base columns as primary questions
base_columns = [col for col in df.columns if col.lower().endswith("base")]

# Group columns by their base question
question_groups = {col: [] for col in base_columns}
for col in df.columns:
    for base in base_columns:
        if col.startswith(base.rsplit("_", 1)[0]):  # Match with the base column prefix
            question_groups[base].append(col)  # Keep full column name in answers
            break

# Convert data to structured format with suggested shortcuts
structured_data = []
for base_question, columns in question_groups.items():
    base_prefix = base_question.rsplit("_", 1)[0]  # Extract prefix for shortcut
    structured_data.append(
        {
            "question": base_question,
            "answers": [
                col for col in columns if col.lower() != "base"
            ],  # Keep full column names
            "suggested_shortcut": [
                col.replace(base_prefix + "_", "").lower().replace(" ", "_")
                for col in columns
                if col.lower() != "base"
            ],  # Suggested shortcut
        }
    )
# Save as JSON
json_output_path = "output.json"
with open(json_output_path, "w", encoding="utf-8") as json_file:
    json.dump(structured_data, json_file, ensure_ascii=False, indent=4)

print(f"JSON saved to {json_output_path}")
