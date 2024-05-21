import openai
from bs4 import BeautifulSoup
import requests
import pandas as pd
import urllib.parse

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
    searchquery = f"{company} owner"
    
    # Fetch the top search results
    top_results = google_search(searchquery, num_results=10)
    
    # Print the results
    for idx, (title, description) in enumerate(top_results, start=1):
        print(f"Result {idx}:\nTitle: {title}\nDescription: {description}\n")
    
def google_search(query, num_results=10):
    # Construct the Google search URL
    query = urllib.parse.quote_plus(query)
    url = f"https://www.google.com/search?q={query}&num={num_results}"
    
    # Make the request to Google
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    
    # Parse the response HTML
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Extract titles and descriptions from the search results
    results = []
    for g in soup.find_all('div', class_='tF2Cxc'):
        title = g.find('h3').text if g.find('h3') else 'No title'
        description = g.find('span').text if g.find('span') else 'No description'
        results.append((title, description))
    
    return results

#main method
if __name__ == "__main__":

    #read the csv file
    df = pd.read_csv("leadsMain.csv")

    #do this for each unique company in the companies column
    companies = df['name'].unique()
    #do the first 3
    for company in companies[0:5]:
        company_name = company
        address = df.loc[df['name'] == company_name, 'address'].values
        print(address)
        print(company_name)

        messages = pull_google_search(company_name, address)

        #name = get_response(messages, address, company_name) 

        # if name == "n/a":
        #     df.loc[df['name'] == company_name, 'first_name'] = "n/a"
        #     df.loc[df['name'] == company_name, 'last_name'] = "n/a"
        #     continue
        # name_split = name.split(" ")
        # #print(name_split[0])
        # #print(name_split[1])
        # df.loc[df['name'] == company_name, 'first_name'] = name_split[0]
        # df.loc[df['name'] == company_name, 'last_name'] = name_split[1]

    df.to_csv("final9.csv")


        

