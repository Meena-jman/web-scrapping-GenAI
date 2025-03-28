import os
import re
import pandas as pd
import google.generativeai as genai

genai.configure(api_key="AIzaSyDkeb4BiVaPwBWPsav0XBqtp5yilqI2URI")

questions = [
    "What is the company's vision/mission statement or core values?",
    "What products or services does the company offer?",
    "When was the company founded, and who were the founders?",
    "Where is the company's headquarters located?",
    "Who are the key executives or leadership team members?",
    "Has the company received any notable awards or recognitions?"
]

data_dir = os.path.dirname(os.path.abspath(__file__)) 
output_csv = os.path.join(data_dir, "company_output.csv")


results = []

txt_files = [f for f in os.listdir(data_dir) if f.endswith(".txt")]

def send_to_gemini(content):
    prompt = f"""
    The data scraped are:
    
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

    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content(prompt)

    return response.text.strip() if response.text else "No information available"

# To extract clean answers
def extract_answers(response_text):
  
    answers = ["No information available"] * 6 

    matches = re.findall(r"(\d+)\.\s(.+?)(?=\n\d+\.|\Z)", response_text, re.DOTALL)

    for num, answer in matches:
        index = int(num) - 1  
        if 0 <= index < 6:
            answers[index] = answer.strip()

    return answers

for filename in txt_files:
    company_name = filename.replace(".txt", "")

    file_path = os.path.join(data_dir, filename)

    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()

    # Answers 
    raw_response = send_to_gemini(content)
    structured_answers = extract_answers(raw_response)

    results.append([company_name] + structured_answers)

df = pd.DataFrame(results, columns=["Company"] + questions)
df.to_csv(output_csv, index=False, encoding="utf-8")

print(f"Successfull {output_csv}")
