import requests
from bs4 import BeautifulSoup
import time
from google import genai
session=requests.Session()
client = genai.Client(api_key="AIzaSyDkeb4BiVaPwBWPsav0XBqtp5yilqI2URI")

def lenovopg():
    url="https://www.lenovo.com/in/en/about/who-we-are/"


    headers={
        "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36 Edg/134.0.0.0"
    }
    response=session.get(url,headers=headers)
    print(response)
    print("requesting")
    soup=BeautifulSoup(markup=response.text,features="html.parser")

    # print("Connected")
    text_products = soup.get_text(separator="\n", strip=True)
    # print(text_products)

    leaderpg="https://www.lenovo.com/in/en/about/who-we-are/our-leadership/"
    response=session.get(leaderpg,headers=headers)

    soup1=BeautifulSoup(markup=response.text,features="html.parser")

    text_leader=soup1.get_text(separator="\n", strip=True)
    # print(text_leader)

    loc_pg="https://www.lenovo.com/in/en/about/locations/"
    response=session.get(loc_pg,headers=headers)

    soup2=BeautifulSoup(markup=response.text,features="html.parser")

    location=soup2.get_text(separator="\n", strip=True)

    return {
        "about": text_products,
        "leadership": text_leader,
        "location": location
    }
def send_to_gemini(data):
    
    prompt = f"""
    The following data was scraped from the Lenovo website:

    1. About the company:
    {data['about']}

    2. Leadership information:
    {data['leadership']}

    3. Location information:
    {data['location']}

    Given this information, please answer the following questions:
    1. What is the company's vision/mission statement or core values?
    2. What products or services does the company offer?
    3. When was the company founded, and who were the founders?
    4. Where is the company's headquarters located?
    5. Who are the key executives or leadership team members?
    6. Has the company received any notable awards or recognitions?

    Provide concise answers to each of these questions.
    """
    
    response = client.models.generate_content(
        model="gemini-2.0-flash",  
        contents=prompt
    )
    
    return response.text

lenovo_data = lenovopg()

answers = send_to_gemini(lenovo_data)

if answers:
    print("Model's Answers:")
    print(answers)


