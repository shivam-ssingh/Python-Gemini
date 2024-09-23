import google.generativeai as genai
import os
from dotenv import find_dotenv,load_dotenv
from bs4 import BeautifulSoup
from requests import get

def ai(query, inputData):
    dotenv = find_dotenv(usecwd=True)
    load_dotenv(dotenv)
    API_KEY = os.getenv("GEMINI_API_KEY")
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content([query, inputData])
    print(response.text)


def scrape(url):
    page = get(url).text
    soup = BeautifulSoup(page, 'html.parser')
    post = soup.find_all('p')
    text = ''
    for line in post:
        text = f'{text} {line.text}'
    return text

websiteData = scrape('https://arstechnica.com/science/2024/09/researchers-spot-largest-black-hole-jets-ever-discovered/')
query = 'Summarize the content in short to help understand fully'

ai(query,websiteData)