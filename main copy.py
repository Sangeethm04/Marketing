import openai
from bs4 import BeautifulSoup
import requests
import pandas as pd
#wait for the page to load
import ollama

#pull api from file API_KEY
API_KEY = open("API_KEY").read().strip()

def get_response(message, company_name):
    openai.api_key = API_KEY
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

    searchquery = company + " owner "
    soup = BeautifulSoup(requests.get("https://www.google.com/search?q=" + searchquery).text, "html.parser")

    #find tags with the xpath
    #mydivs = soup.find_all("div", xpath='//*[@id="rso"]/div[3]/div/div/div[2]/div/span/text()')
    divLines = []
    neededLines = []
    #find all divs
    for line in soup.find_all('div'):
        divLines.append(line.get_text())
    
    for line in soup.find_all('h3'):
        neededLines.append(line.get_text())

    #get the first 5...50 lines
    for line in range(0, 50):
        neededLines.append(divLines[line])
    
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


        

