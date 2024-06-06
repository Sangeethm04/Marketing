import openai
from bs4 import BeautifulSoup
import requests
import pandas as pd
#wait for the page to load
import ollama
from urllib.parse import quote_plus


def get_response(message, company_name):
    #print(message)
    response = ollama.chat(model='llama3', messages=[
   {"role": "user", 
             "content": "find the most relevant owner/ceo of the company-"+ company_name +". Make sure it is from the given company not a similar named company. Prioritize better business bureau results. Return only the first name without any other text. If it doesn't explicitly say owner or ceo then just return with n/a: " + ' '.join(message)},
    ])
    print(response)
    # print(response)
    # print(response.choices[0].message['content'])
    return response['message']['content']


def get_cleaned(message):
    #print(message)
    response = ollama.chat(model='llama3', messages=[
   {"role": "user", 
             "content": "From this: return only the name" + ' '.join(message)},
    ])
    print(response)
    # print(response)
    # print(response.choices[0].message['content'])
    return response['message']['content']

 
#only pull the first few results from google
def pull_google_search(company):
    # chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_experimental_option("detach", True)

    # driver = webdriver.Chrome(options=chrome_options)
    # driver = webdriver.Chrome(options=chrome_options)

    searchquery = quote_plus(f"{company} owner")
    print("https://www.google.com/search?q=" + searchquery)
    soup = BeautifulSoup(requests.get("https://www.google.com/search?q=" + searchquery).text, "html.parser")

    #find tags with the xpath
    divLines = []
    h3Lines = []
    neededLines = []

    #find all divs
    for line in soup.find_all('div'):
        #grab only unique divs
        if line.get_text() not in divLines:
            divLines.append(line.get_text())

    for line in soup.find_all('h3'):
        if line.get_text() not in h3Lines:
            h3Lines.append(line.get_text())

    #print first 50 of each list with the index number
    for i in range(100):
        if i < len(h3Lines):
            neededLines.append(f"h3: #{i} {h3Lines[i]}")
        if i < len(divLines) and i > 15 and i < len(divLines) - 6:
            neededLines.append(f"div: #{i} {divLines[i]}")


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
        print(company_name)

        messages = pull_google_search(company_name)

        nameOG = get_response(messages, company_name) 

        name = get_cleaned(nameOG)

        if name == "n/a":
            df.loc[df['name'] == company_name, 'first_name'] = "n/a"
            df.loc[df['name'] == company_name, 'last_name'] = "n/a"
            continue
        name_split = name.split(" ")
        if name_split[0] != None:
            print(name_split[0])
            df.loc[df['name'] == company_name, 'first_name'] = name_split[0]
        if name_split[1] != None:    
            print(name_split[1])
            df.loc[df['name'] == company_name, 'last_name'] = name_split[1]
        

    df.to_csv("final999.csv")


        

