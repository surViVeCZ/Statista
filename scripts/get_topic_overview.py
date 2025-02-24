import os
import pandas as pd
import json
import re
import concurrent.futures
from openai import OpenAI
from tqdm import tqdm
from dotenv import load_dotenv  # Import dotenv

# Load environment variables from the .env file in the parent directory
load_dotenv(dotenv_path="../.env")

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def summarize_text(text):
    """Summarizes the given text to under 10 words using GPT-4."""
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "user",
                "content": f"Summarize this question in under 10 words: {text}",
            }
        ],
        temperature=0,
    )
    return response.choices[0].message.content.strip()


# Load the CSV file
file_path = "digital_lifestyle.csv"
class_name = file_path.replace(".csv", "").replace(" ", "_").title().replace("_", "")

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
    formatted_question = (
        base_question.replace("(", "")
        .replace(")", "")
        .replace("__", "_")
        .replace("_base", "")
        .replace("_Base", "")
        .replace("&", "and")
        .replace("/", "or")
        .replace("!", "")
        .replace("?", "")
        .replace("-", "")
        .replace("\xa0", "_")  # Remove non-breaking spaces
        .strip()
    )
    structured_data.append(
        {
            "question": formatted_question,
            "answers": [
                col for col in columns if col.lower() != "base"
            ],  # Keep full column names
            "suggested_shortcut": [
                col.replace(base_prefix + "_", "").lower().replace(" ", "_")
                for col in columns
                if col.lower() != "base" and col.lower() != base_prefix.lower()
            ],  # Exclude "base" and full base prefix
        }
    )

# Save as JSON
json_output_path = "topic_coverage.json"
with open(json_output_path, "w", encoding="utf-8") as json_file:
    json.dump(structured_data, json_file, ensure_ascii=False, indent=4)

print(f"JSON saved to {json_output_path}")

# Save the structured Python class to a file with correct formatting
output_python_path = "topic_suggestion_for_clone.py"

# Load the JSON data
file_path = "topic_coverage.json"
with open(file_path, "r", encoding="utf-8") as file:
    data = json.load(file)

# Start building the Python script with structured formatting
python_code = f"""from typing import Optional, Literal
from pydantic import BaseModel, Field
import os

class {class_name}(BaseModel):
    \"\"\"{class_name} Model with structured formatting.\"\"\"  
"""

# **Parallelize summarization using ThreadPoolExecutor**
num_questions = len(data)
print(f"Summarizing {num_questions} questions in parallel...")

# Use ThreadPoolExecutor for parallel processing
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    summaries = list(
        tqdm(
            executor.map(summarize_text, [entry["question"] for entry in data]),
            total=num_questions,
            desc="Summarizing",
        )
    )

# Generate class fields dynamically
for idx, entry in enumerate(data):
    question_key = summaries[idx].replace(" ", "_").lower()

    # Apply same replacements as before
    question_key = (
        question_key.replace("(", "")
        .replace(")", "")
        .replace("__", "_")
        .replace("_base", "")
        .replace("_Base", "")
        .replace("&", "and")
        .replace("/", "or")
        .replace("!", "")
        .replace("?", "")
        .replace("-", "")
        .replace("'", "")
        .replace(".", "")
        .replace(",", "")
        .replace("\xa0", "_")  # Remove non-breaking spaces
        .strip()
    )

    literals = [lit for lit in entry["suggested_shortcut"] if lit != "base"]
    if literals:
        literals_str = ",\n".join(f'            "{lit}"' for lit in literals)
        field_def = f"""    {question_key}: Optional[
        Literal[
{literals_str}
        ]
    ] = Field(default=None, description=\"{entry['question']}\")\n"""
        python_code += field_def

# Save to file
with open(output_python_path, "w", encoding="utf-8") as file:
    file.write(python_code)

print(f"Python class saved to {output_python_path}")
