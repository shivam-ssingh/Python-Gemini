import google.generativeai as genai
import os
from dotenv import find_dotenv,load_dotenv
from bs4 import BeautifulSoup
from requests import get
import pathlib
from xhtml2pdf import pisa             
import requests
import uuid

def scrape(url):
    page = get(url).text
    soup = BeautifulSoup(page, 'html.parser')
    post = soup.find_all('p')
    text = ''
    for line in post:
        text = f'{text} {line.text}'
    return text

def get_pdf_from_url(url,name):
    headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0"
    }
    response = requests.get(url,headers = headers)
    with open(f'C:/Python-Project/Pdf/{name}.pdf', 'wb') as f:
        f.write(response.content)

def ai(query, inputData):
    dotenv = find_dotenv(usecwd=True)
    load_dotenv(dotenv)
    API_KEY = os.getenv("GEMINI_API_KEY")
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content([query, inputData])
    print(response.text)

def aiFile(fileName):
    dotenv = find_dotenv(usecwd=True)
    load_dotenv(dotenv)
    API_KEY = os.getenv("GEMINI_API_KEY")
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel("gemini-1.5-flash")
    sample_pdf = genai.upload_file(f'C:/Python-Project/Pdf/{fileName}.pdf')
    response = model.generate_content(["Explain me this report, highlight the positive and negative aspect of the report, highlight all the technical jargon present in the file along with explanation. Please reply in HTML so that I can convert it to PDF.", sample_pdf])
    convert_html_to_pdf(response.text,f'{fileName}-analysis.pdf')

def convert_html_to_pdf(source_html, output_filename):
    # open output file for writing (truncated binary)
    result_file = open(f'C:/Python-Project/Analysis/{output_filename}', "w+b")
    # convert HTML to PDF
    pisa_status = pisa.CreatePDF(
            source_html,                # the HTML to convert
            dest=result_file)           # file handle to recieve result
    # close output file
    result_file.close()                 # close output file
    # return False on success and True on errors
    return pisa_status.err

def get_user_input():
    userSelection = input('what do you want to do? \n Input 1 to summarize a website page. \n Input 2 to summarize a pdf. \n')
    if(userSelection == '1'):
        urlToSummarize = input('Share the website url. \n')
        #scrape the data.
        websiteData = scrape(urlToSummarize)
        #basic summary query
        query = 'Summarize the content in short to help understand fully'
        #calling our gemini api
        ai(query,websiteData)
    elif(userSelection == '2'):
        urlToSummarize = input('Share the pdf url. \n')
        finalSummaryName = input('Please share the name of the final pdf, where the summary will be present. \n')
        finalSummaryName += '_' + str(uuid.uuid4())
        #downloading and storing the file
        get_pdf_from_url(urlToSummarize,finalSummaryName)
        #passing the question
        aiFile(finalSummaryName)

get_user_input()