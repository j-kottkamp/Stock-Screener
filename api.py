import re
import json
import string
import random
import requests
import datetime
from bs4 import BeautifulSoup

## Basics

def log(text, level="needs to be implemented"): # Implement abilty to have difrent log levels i.a DEBUG PROCESS or whatever get creative also change each call then according to the levels
    if 1 == 0:
        print(text)
    else:
        pass

def generate_random_string(length=8):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

def random_email():
    return f"{generate_random_string()}.{generate_random_string()}@{generate_random_string()}.{generate_random_string()}"

## Web Request Stuff

def get_csrf_token(session, url):
    response = session.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    csrf_token = soup.find('input', {'name': 'csrfmiddlewaretoken'})['value']

    log(f"CSRFT Token: {csrf_token}")
    return csrf_token

def get_new_api_token(email=random_email()):
    post_url = "https://www.alphavantage.co/create_post/"

    crsf_url = "https://www.alphavantage.co/support/#api-key"

    data = {
        "first_text": "deprecated",
        "last_text": "deprecated",
        "occupation_text": "Investor",
        "organization_text": generate_random_string(12),
        "email_text": email
    }
    headers = {
        "Referer": crsf_url,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }

    with requests.Session() as session:
        # Get CSRF
        csrf_token = get_csrf_token(session, crsf_url)
        data['csrfmiddlewaretoken'] = csrf_token

        # Send request
        log(f"Requesting API Key with following data: {data}")

        response = session.post(post_url, data=data, headers=headers)
        if response.status_code == 200:
            log("Request was successful.")
        else:
            log(f"Request failed with status code: {response.status_code}")

        log(("Response content:", response.content))

        response_text = json.loads(response.content.decode("utf-8"))["text"]

        try:
            api_key = re.search(r"is:\s*([A-Z0-9]+)", response_text).group(1)
            log(f"Successfully retrieved API key: {api_key}")

            return api_key
        except AttributeError:
            log(f"Coudnt get key. Proably duplicate email. Response: {response_text}")

            return None

## API Key Management

# Functions to load and save API records from file
def load_from_file():
    try:
        with open('api_keys.json', 'r') as file:
            return json.load(file)
    except: # Not Ideal
        log("Encounterd Error while loading from file returning empty list")
        return []

def save_to_file(api_keys):
    try:
        with open('api_keys.json', 'w') as file:
            json.dump(api_keys, file)
    except: # Not Ideal
        log("Wasnt abel to Save API Keys to file") # Big Problem

# Function for Consistent data Structure / Creating new entries
def convert_to_record(api_key, amount=0):
    record = {
        "api_key": api_key,
        "amount": amount,
        "date": datetime.datetime.now().strftime("%Y-%m-%d")
    }
    log(f"convertet apiKey:|{api_key}| to Record:|{record}|")    
    return record

# Function to get an API key with amount less than 24 on the current day and update data lazyly
# This is a fucntion that can be called by the user if only_key is False the whole record will be returned
def get_api_key(only_key=True):
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    api_keys = load_from_file()
    log(f"Loaded Api Keys: {api_keys}")

    for record in api_keys:
        if record["amount"] > 0 and record["date"] < current_date:
            record["amount"] = 0
            record["date"] = current_date

            save_to_file(api_keys)
            return record["api_key"]

        elif record["amount"] < 24 and record["date"] == current_date:
            record["amount"] = record["amount"] + 1

            save_to_file(api_keys)
            return record["api_key"]


    log("Was not abel to find valid key getting new one...")
    trys = 10 # change this if we have used up too many email adresses

    for i in range(trys):
        api_key = get_new_api_token(random_email())
        if api_key:
            record = convert_to_record(api_key, 1)
            api_keys.append(record)
            save_to_file(api_keys)
            
            log(f"Returning Valid Api Key {record}")
            if only_key:
                return record["api_key"]
            return record
            
        else:
            log(f"API Key was None trying again for the {i}th time..")

    log(f"Wasnt abel to get API Key after {trys} raising Error | maybe try raising 'trys'")
    raise Exception

## API Requests

def geturl(unique):
    url = f"https://www.alphavantage.co/query?function={unique}&apikey={get_api_key()}"
    log(f"Prepared url: {url}")
    return url

def get(unique):
    url = geturl(unique)
    data = requests.get(url).json()   
    log(f"Got data back from API: {data}")
    return data

if __name__ == "__main__":
    try:
        api_key = get_api_key()
        print(f"Obtained API Key: {api_key}")
    except Exception as e:
        print(f"Error: {e}")