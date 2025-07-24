import os
import pandas as pd
import json
import concurrent.futures
from tqdm import tqdm
from dotenv import load_dotenv  # Import dotenv
import requests

# Load environment variables from the .env file in the parent directory
load_dotenv(dotenv_path="../.env")  #remove ../ when running alone

headers = {
    "Content-Type": "application/json",
    "api-key": os.getenv("AZURE_OPENAI_API_KEY_gpt-4-turbo"),
}
GPT4V_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT_gpt-4-turbo")


def summarize_text(text):
    """Summarizes the given text to under 10 words using GPT-4."""
    payload = {
        "messages": [
            {
                "role": "user",
                "content": f"Summarize this question in under 10 words: {text}",
            }
        ],
        "temperature": 0.0,
        "max_tokens": 1000,
    }
    response = requests.Response

    try:
        response = requests.post(GPT4V_ENDPOINT, headers=headers, json=payload)
        response_data = response.json()

        # Get the assistant's reply and add it to the conversation history
        return response_data["choices"][0]["message"]["content"].strip()

    except Exception as e:
        print(response.status_code if response else "No response")
        print(e)
        return None


def get_overview(file_path: str, save_json_coverage: bool = False):
    class_name = (
        file_path.replace(".csv", "").replace(".xlsx", "").replace(" ", "_").title().replace("_", "")
    )
    class_name = class_name.split('/')[-1]

    # Load csv
    df = pd.read_excel(file_path)

    # Identify base columns as primary questions
    base_columns = [col for col in df.columns if col.lower().endswith("base")]
    assert len(base_columns) > 0, "No base columns found."

    # Group columns by their base question
    question_groups = {col: [] for col in base_columns}
    for col in df.columns:
        for base in base_columns:
            if col.startswith(
                base.rsplit("_", 1)[0]
            ):  # Match with the base column prefix
                question_groups[base].append(col)  # Keep full column name in answers
                break
    assert len(question_groups) > 0, "No questions extracted."
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

    if save_json_coverage:
        # Save as JSON
        json_output_path = "topic_coverage.json"
        with open(json_output_path, "w", encoding="utf-8") as json_file:
            json.dump(structured_data, json_file, ensure_ascii=False, indent=4)
        print(f"JSON saved to {json_output_path}")

    # Save the structured Python class to a file with correct formatting
    output_python_path = f"statista_data/clone/{class_name}_clone.py"

    # Start building the Python script with structured formatting
    python_code = f"""from typing import Optional, Literal\nfrom pydantic import BaseModel, Field\nimport os\n\nclass {class_name}(BaseModel):
    \"\"\"{class_name} Model with structured formatting.\"\"\"  
    """

    # **Parallelize summarization using ThreadPoolExecutor**
    num_questions = len(structured_data)
    print(f"Summarizing {num_questions} questions in parallel...")

    # Use ThreadPoolExecutor for parallel processing
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        summaries = list(
            tqdm(
                executor.map(
                    summarize_text, [entry["question"] for entry in structured_data]
                ),
                total=num_questions,
                desc="Summarizing",
            )
        )

    # Generate class fields dynamically
    for idx, entry in enumerate(structured_data):
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
            literals_str = ",\n".join(f'\t\t\t"{lit}"' for lit in literals)
            field_def = f"""{question_key}: Optional[\n\t\tLiteral[\n{literals_str}
            ]
    ] = Field(default=None, description=\"{entry['question']}\")\n    """
            python_code += field_def

    # Save to file

    if not os.path.exists(output_python_path):
        with open(output_python_path, "w", encoding="utf-8") as file:
            file.write(python_code)

    print(f"Python class saved to {output_python_path}")

if __name__ == "__main__":
    get_overview("statista_data/transformed/Food and Nutrition in Italy 2021 adv.xlsx", False)