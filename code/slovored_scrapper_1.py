import os
import time
import random
import dotenv
import requests
from bs4 import BeautifulSoup # Parse HTML
from requests_ip_rotator import ApiGateway # IP Proxy

target_url = "https://slovored.com"
base_url = "https://slovored.com/search/all/"
output_file = 'data/words.txt'

def get_user_agent(k=1) -> str:
    """Returns a random useragent from the latest user agents strings list, weighted"""
    
    agents = [
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.10 Safari/605.1.1',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.3',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.3',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.3',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36 Trailer/93.3.8652.5',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36 Edg/134.0.0.',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 OPR/117.0.0.',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 Edg/132.0.0.',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:136.0) Gecko/20100101 Firefox/136.']
    # Generate a random index
    return agents[random.randint(0, len(agents) - 1)]

def get_html(session: requests.Session, url: str) -> str|None:
    try:
        response = session.get(url=url, headers={'User-Agent': get_user_agent()})
        return response.text
    except Exception as e:
        print(f"Error fetching HTML: {e}")
        # Second try
        time.sleep(1)
        response = session.get(url=url, headers={'User-Agent': get_user_agent()})
        return response.text

def get_next_word(session: requests.Session, last_word: str) -> list[str]:
    print(last_word)
    # Encode URL
    url = base_url+last_word
    # Fetch the HTML
    html = get_html(session, url)
    # Parse the HTML
    soup = BeautifulSoup(html, 'html.parser')
    words_div = soup.find('div', class_='words')
    if words_div is None:
        print(soup)
    # The second link in the div is the next word
    return words_div.find_all('a')[1].contents[0]

def scrape_words(gateway: ApiGateway):
    # If the file doesn't exist, then last_word = 'а'
    if not os.path.exists(output_file):
        last_word = 'а'
    # Read the last word from the file
    with open(output_file, 'r', encoding='utf-8') as f:
        last_word = f.readlines()[-1].strip()

    counter = 0
    session = None

    # Scrape the words
    while True:
        # Recreate the session every 10 requests
        if counter % 1 == 0:
            # Close previous session
            if session is not None:
                session.close()
            # Open a new session
            session = requests.Session()
            session.mount(target_url, gateway)
        counter += 1
        # Fetch the next word
        word = get_next_word(session, last_word)
        # Abort, if the word is not found
        if word is None:
            break
        # Append the word to a .txt file
        with open(output_file, 'a', encoding='utf-8') as f:
            f.write(word + '\n')
        # Move forward
        last_word = word
        # Minor delay
        time.sleep(0.3)

def scrape_words_with_ip_rotation():
    # Load the .env file
    dotenv.load_dotenv()
    while True:
        # Start the API gateway
        with ApiGateway(
            site=target_url,
            regions=["eu-central-1"], #, "eu-west-1", "eu-west-2", "eu-west-3", "eu-north-1"],
            access_key_id=os.getenv('AWS_API_GATEWAY_ACCESS_KEY'),
            access_key_secret=os.getenv('AWS_API_GATEWAY_SECRET_KEY'),
        ) as gateway:
            gateway.start()
        # Scrape the words
        try:
            scrape_words(gateway)
        except Exception as e:
            print(f"Error scraping words: {e}")
            if "find_all" not in str(e):
                gateway.shutdown()
                raise e

# Main loop
scrape_words_with_ip_rotation()