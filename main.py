import openai
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import pandas as pd
#wait for the page to load
from selenium.webdriver.support.ui import WebDriverWait

API_KEY = "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"

def get_response(message):
    openai.api_key = API_KEY

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": "find the most relevant owner/ceo of the company. Make sure it is from the given company exactly not a similar named company-just give the name no other information. If it doesn't explicitly say owner or ceo currently then just return with n/a: " + ' '.join(message)},
        ]
    )
    print(response.choices[0].message['content'])

#only pull the first few results from google
def pull_google_search(company):
    # chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_experimental_option("detach", True)

    # driver = webdriver.Chrome(options=chrome_options)

    searchquery = company + " owner "
    # driver.get("https://www.google.com/search?q=" + searchquery)
    soup = BeautifulSoup(requests.get("https://www.google.com/search?q=" + searchquery).text, "html.parser")

    #find tags with the xpath
    #mydivs = soup.find_all("div", xpath='//*[@id="rso"]/div[3]/div/div/div[2]/div/span/text()')
    allLines = []
    neededLines = []
    #find all divs
    for line in soup.find_all('div'):
        allLines.append(line.get_text())

    #get the first 5...50 lines
    for line in range(0, 50):
        neededLines.append(allLines[line])
    return neededLines
    


#main method
if __name__ == "__main__":

    #read the csv file
    df = pd.read_csv("Copy of Wire Coil Framing Nails - Custom Home Builder - PA - leads-data-custom-home-builder_pennsylvania-usa_f2bff4508934c32a02eac9ee7970c129.csv (1).csv")

    #do this for each unique company in the companies column
    companies = df['name'].unique()
    #do the first 3
    for company in companies[5:9]:
        company_name = company

        messages = pull_google_search(company_name)
        #print(messages)
        get_response(messages)

