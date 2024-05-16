import openai
from bs4 import BeautifulSoup
import requests
import pandas as pd
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
             "content": "find the most relevant owner/ceo of the company-"+ company_name +". Make sure it is from the given company not a similar named company-the address of the company I'm looking for is-"+' '.join(address) +". Just give the first name and last name without middle or any prefixes and no other information and prioritize better business bureau/LinkedIn results." + ' '.join(message)},
        ]
    )
    print(response)
    print(response.choices[0].message['content'])
    return response.choices[0].message['content']


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
        address = df.loc[df['name'] == company_name, 'address'].values
        print(address)
        print(company_name)

        messages = pull_google_search(company_name)

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

    df.to_csv("final1.csv")


        

