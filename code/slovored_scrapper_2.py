from itertools import cycle
import os
import time
import random
import requests
import pandas as pd
from bs4 import BeautifulSoup # Parse HTML

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

def get_html(proxies: list[str], url: str) -> str|None:
    proxy_pool = cycle(proxies)
    for _ in range(1, len(proxies)):
        proxy = next(proxy_pool)
        print(proxy)
        try:
            response = requests.get(url, proxies={"http": proxy, "https": proxy}, headers={'User-Agent': get_user_agent()})
            return response.text
        except Exception as e:                                
            print('Rotated IP %s failed (%s)' % (proxy, str(e)))
    # Failure, if all proxies failed
    return None

def get_next_word(proxies: list[str], last_word: str) -> list[str]:
    print(last_word)
    # Encode URL
    url = base_url+last_word
    # Fetch the HTML
    html = get_html(proxies, url)
    # Parse the HTML
    soup = BeautifulSoup(html, 'html.parser')
    words_div = soup.find('div', class_='words')
    if words_div is None:
        print(soup)
    # The second link in the div is the next word
    return words_div.find_all('a')[1].contents[0]

def scrape_words(proxies: list[str]):
    # If the file doesn't exist, then last_word = 'а'
    if not os.path.exists(output_file):
        last_word = 'а'
    # Read the last word from the file
    with open(output_file, 'r', encoding='utf-8') as f:
        last_word = f.readlines()[-1].strip()

    # Scrape the words
    while True:
        # Fetch the next word
        word = get_next_word(proxies, last_word)
        # Abort, if the word is not found
        if word is None:
            break
        # Append the word to a .txt file
        with open(output_file, 'a', encoding='utf-8') as f:
            f.write(word + '\n')
        # Move forward
        last_word = word
        # Minor delay
        time.sleep(1)

def scrape_words_with_ip_rotation():
    # Get the proxies
    response = requests.get('https://free-proxy-list.net/') 
    df = pd.read_html(response.text)[0]
    proxies = df[df['Https'] == 'yes']['IP Address'].tolist()
    # Scrape the words
    scrape_words(proxies)

# Main loop
scrape_words_with_ip_rotation()