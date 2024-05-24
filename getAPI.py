import requests
from bs4 import BeautifulSoup
import random
import string

def generate_random_email():
    domains = ["gmail.com", "yahoo.com", "outlook.com", "example.com"]
    name = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
    domain = random.choice(domains)
    return f"{name}@{domain}"

def get_api_key():
    url = "https://www.alphavantage.co/support/#api-key"
    session = requests.Session()

    # Step 1: Get the form page
    response = session.get(url)
    if response.status_code != 200:
        raise Exception(f"Failed to load page: {response.status_code}")
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Step 2: Find the form action URL and required fields
    form = soup.find('form')
    if not form:
        raise Exception("No form found on the page")
    
    form_action = form['action']
    form_url = f"https://www.alphavantage.co{form_action}"
    
    email = generate_random_email()
    
    # Step 3: Fill the form data
    form_data = {
        'email': email,
        'agreement': 'on'
    }
    
    # Include any other hidden fields required by the form
    for hidden_input in form.find_all('input', type='hidden'):
        form_data[hidden_input['name']] = hidden_input['value']
    
    # Step 4: Submit the form
    response = session.post(form_url, data=form_data)
    if response.status_code != 200:
        raise Exception(f"Form submission failed: {response.status_code}")
    
    # Step 5: Parse the response to extract the API key
    # This step will vary depending on the response format
    soup = BeautifulSoup(response.content, 'html.parser')
    api_key = soup.find('div', class_='api-key').text.strip()
    
    return api_key

def api_key(): # a function that can be called in main.py to get an api key. this function checks when key expires and the gets a new one and returns
    api_key = open("api_key.txt") # other storage can be impelmentet
    if vaild_api_key(api_key):
        return api_key
    return get_api_key()


def valid_api_key(api_key): # Implemt logic for cheking validity of key here
    if Vaild:
        return True
    return False



if __name__ == "__main__":
    try:
        api_key = get_api_key()
        print(f"Obtained API Key: {api_key}")
    except Exception as e:
        print(f"Error: {e}")
