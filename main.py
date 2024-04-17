import openai
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

API_KEY = "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"

def get_response(message):
    openai.api_key = API_KEY

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": "find the most relevant owner/ceo of the company from the given text-just give the name no other information: " + ' '.join(message)},
        ]
    )
    print(response)

#only pull the first few results from google
def pull_google_search(company):
    # chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_experimental_option("detach", True)

    # driver = webdriver.Chrome(options=chrome_options)

    searchquery = company + " owner "
    # driver.get("https://www.google.com/search?q=" + searchquery)
    soup = BeautifulSoup(requests.get("https://www.google.com/search?q=" + searchquery).text, "html.parser")
    #print(soup.prettify())
    #find tags with the xpath
    mydivs = soup.find_all("div", xpath='//*[@id="rso"]/div[3]/div/div/div[2]/div/span/text()')
    allLines = []
    for line in soup.find_all('span'):
        print(line.get_text())
        #store results in variable and return it
        allLines.append(line.get_text())
    return allLines
    


#main method
if __name__ == "__main__":
    
    messages = pull_google_search("Zaveta Custom Homes")
    print(messages)
    get_response(messages)

