import openai
from bs4 import BeautifulSoup
import requests
import pandas as pd
from urllib.parse import quote_plus

#wait for the page to load

#pull api from file API_KEY
API_KEY = open("API_KEY").read().strip()

def get_response(message, address, company_name):
    openai.api_key = API_KEY
    print(message)
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0125",
        messages=[
            {"role": "user", 
             "content": "Find the most relevant owner/ceo of the company-"+ company_name +". Prioritize results that are from Better Business Bureau and Linkedin results. ONLY return the first name & last name without middle or any prefixes and do not make up a name not given. If there is no owner/ceo then just return n/a" + ' '.join(message)},
        ]
    )
    print(response)
    print(response.choices[0].message['content'])
    return response.choices[0].message['content']


#only pull the first few results from google
def pull_google_search(company, address):
    # chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_experimental_option("detach", True)

    # driver = webdriver.Chrome(options=chrome_options)

    searchquery = quote_plus(f"{company} owner")
    soup = BeautifulSoup(requests.get("https://www.google.com/search?q=" + searchquery).text, "html.parser")

    #find tags with the xpath
    #mydivs = soup.find_all("div", xpath='//*[@id="rso"]/div[3]/div/div/div[2]/div/span/text()')
    divLines = []
    h3Lines = []
    neededLines = []

    #find all divs
    for line in soup.find_all('div'):
        #grab only unique divs
        if line.get_text() not in divLines:
            divLines.append(line.get_text())

    for line in soup.find_all('h3'):
        h3Lines.append(line.get_text())

    #print first 50 of each list with the index number
    for i in range(100):
        if i < len(h3Lines):
            neededLines.append(h3Lines[i])
        if i < len(divLines):
            neededLines.append(divLines[i])


    return neededLines
    


#main method
if __name__ == "__main__":

    #read the csv file
    df = pd.read_csv("leadsMain.csv")

    #do this for each unique company in the companies column
    companies = df['name'].unique()
    #do the first 3
    for company in companies[0:25]:
        company_name = company
        address = df.loc[df['name'] == company_name, 'address'].values
        print(address)
        print(company_name)

        messages = pull_google_search(company_name, address)
        print(messages)
        name = get_response(messages, address, company_name) 

        if name == "n/a":
            df.loc[df['name'] == company_name, 'first_name'] = "n/a"
            df.loc[df['name'] == company_name, 'last_name'] = "n/a"
            continue
        name_split = name.split(" ")
        #print(name_split[0])
        #print(name_split[1])
        df.loc[df['name'] == company_name, 'first_name'] = name_split[0]
        df.loc[df['name'] == company_name, 'last_name'] = name_split[1]

    df.to_csv("final9.csv")


        

