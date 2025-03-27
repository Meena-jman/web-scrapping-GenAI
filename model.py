# import os
# import pandas as pd
# import requests
# import google.generativeai as genai

# # Configure Gemini API (Replace with your actual API key)
# genai.configure(api_key="PI")

# # Define questions
# questions = [
#     "What is the company's vision/mission statement or core values?",
#     "What products or services does the company offer?",
#     "When was the company founded, and who were the founders?",
#     "Where is the company's headquarters located?",
#     "Who are the key executives or leadership team members?",
#     "Has the company received any notable awards or recognitions?"
# ]

# # Get the current script directory
# data_dir = os.path.dirname(os.path.abspath(__file__))  # Same directory as model.py
# output_csv = os.path.join(data_dir, "combined_company_info.csv")

# # Prepare list to store results
# results = []

# # Get all text files in the directory
# txt_files = [f for f in os.listdir(data_dir) if f.endswith("_scraped_data.txt")]

# # Function to send scraped data to Gemini LLM
# def send_to_gemini(content):
#     """Send scraped content to Gemini LLM and retrieve structured responses."""
#     prompt = f"""
#     The following data was scraped from a company's website:
    
#     {content}
    
#     Given this information, please answer the following questions:
#     1. {questions[0]}
#     2. {questions[1]}
#     3. {questions[2]}
#     4. {questions[3]}
#     5. {questions[4]}
#     6. {questions[5]}
    
#     Provide concise answers.
#     """

#     # Call Gemini API
#     model = genai.GenerativeModel("gemini-2.0-flash")
#     response = model.generate_content(prompt)

#     return response.text.strip() if response.text else "No information available"
# print("\n\n\ntextfiles",txt_files)
# # Process each scraped text file
# for filename in txt_files:
#     # Extract company name from filename
#     company_name = filename.replace("www_", "").replace("_com_scraped_data.txt", "").replace("_", ".")

#     file_path = os.path.join(data_dir, filename)

#     # Read file content
#     with open(file_path, "r", encoding="utf-8") as file:
#         content = file.read()

#     # Get answers from Gemini LLM
#     answers = send_to_gemini(content).split("\n")  # Split answers by line
#     print("answwrs",answers)
#     print()
#     print()
#     # Ensure we have exactly 6 answers
#     while len(answers) < 6:
#         answers.append("No information available")

#     # Store results
#     results.append([company_name] + answers[:6])  # Ensure only 6 answers are stored
#     print(results)

# # Convert results to DataFrame and save as CSV
# df = pd.DataFrame(results, columns=["Company"] + questions)
# df.to_csv(output_csv, index=False, encoding="utf-8")

# print(f"Results saved to {output_csv}")

import os
import re
import pandas as pd
import google.generativeai as genai

# Configure Gemini API (Replace with your actual API key)
genai.configure(api_key="Apikey")

# Define structured questions
questions = [
    "What is the company's mission statement or core values?",
    "What products or services does the company offer?",
    "When was the company founded, and who were the founders?",
    "Where is the company's headquarters located?",
    "Who are the key executives or leadership team members?",
    "Has the company received any notable awards or recognitions?"
]

# Get current script directory
data_dir = os.path.dirname(os.path.abspath(__file__))  # Directory where model.py is stored
output_csv = os.path.join(data_dir, "combined_company_info.csv")

# Prepare list to store results
results = []

# Get all text files in the directory
txt_files = [f for f in os.listdir(data_dir) if f.endswith("_scraped_data.txt")]

# Function to send scraped data to Gemini LLM
def send_to_gemini(content):
    """Send scraped content to Gemini LLM and retrieve structured responses."""
    prompt = f"""
    The following data was scraped from a company's website:
    
    {content}
    
    Given this information, please answer the following questions concisely:
    1. {questions[0]}
    2. {questions[1]}
    3. {questions[2]}
    4. {questions[3]}
    5. {questions[4]}
    6. {questions[5]}
    
    Provide answers in the exact numbered format, e.g.:
    1. Answer here.
    2. Answer here.
    3. Answer here.
    4. Answer here.
    5. Answer here.
    6. Answer here.
    """

    # Call Gemini API
    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content(prompt)

    return response.text.strip() if response.text else "No information available"

# Function to extract clean answers from LLM response
def extract_answers(response_text):
    """Extracts structured answers from the Gemini response."""
    answers = ["No information available"] * 6  # Default placeholders

    # Regular expression to match numbered answers (1. ..., 2. ..., etc.)
    matches = re.findall(r"(\d+)\.\s(.+?)(?=\n\d+\.|\Z)", response_text, re.DOTALL)

    for num, answer in matches:
        index = int(num) - 1  # Convert to zero-based index
        if 0 <= index < 6:
            answers[index] = answer.strip()

    return answers

# Process each scraped text file
for filename in txt_files:
    # Extract company name from filename
    company_name = filename.replace("www_", "").replace("_com_scraped_data.txt", "").replace("_", ".")

    file_path = os.path.join(data_dir, filename)

    # Read file content
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()

    # Get answers from Gemini LLM
    raw_response = send_to_gemini(content)
    structured_answers = extract_answers(raw_response)

    # Store results
    results.append([company_name] + structured_answers)

# Convert results to DataFrame and save as CSV
df = pd.DataFrame(results, columns=["Company"] + questions)
df.to_csv(output_csv, index=False, encoding="utf-8")

print(f"Successfull {output_csv}")
