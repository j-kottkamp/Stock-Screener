import re
import json
import string
import random
import requests
import datetime
from bs4 import BeautifulSoup

# Basics
def log(text):
    if 1 == 0:
        print(text)
    else:
        pass

def generate_random_string(length=8):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

def random_email():
    return f"{generate_random_string()}.{generate_random_string()}@{generate_random_string()}.{generate_random_string()}"

# Web Request Stuff
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
        "organization_text": "-",
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

# API Key Management

# Function to load existing records from file
def load_api_keys():
    try:
        with open('api_keys.json', 'r') as file:
            return json.load(file)
    except: # Not Ideal
        return []

# Function to save records to a JSON file
def save_to_file(api_keys):
    with open('api_keys.json', 'w') as file:
        json.dump(api_keys, file)


# Function to get an API key with amount less than 24 on the current day
def get_api_key():
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    api_keys = load_api_keys()

    for record in api_keys:
        if record["amount"] > 0 and record["date"] < current_date:
            record["amount"] = 0
            record["date"] = current_date
            save_to_file(api_keys)
            return record["api_key"]

        if record["amount"] < 24 and record["date"] == current_date:
            record["amount"] += record["amount"]
            return record["api_key"]

    
    record = save_api_key(api_keys, get_new_api_token())
    return record["api_key"]




# Example usage:
# Function to save API key record
def save_api_key(api_keys, api_key, amount=0):
    record = {
        "api_key": api_key,
        "amount": amount,
        "date": datetime.datetime.now().strftime("%Y-%m-%d")
    }
    api_keys.append(record)
    save_to_file(api_keys)
    return record


# Retrieving an API key with amount less than 24 on the current day
api_key = get_api_key()
if api_key:
    print(f"Got API key: {api_key}")
else:
    print("No available API keys with amount less than 24 on the current day.")





#print(get_new_api_token(random_email))
