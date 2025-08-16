import os
import time
import random
import requests
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

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

def get_html(driver: webdriver.Chrome, url: str) -> str|None:
    try:
        # Navigate to the target URL
        driver.get(url)
        # Get the page source
        page_source = driver.page_source
        print(page_source)
        exit()
        response = requests.get(url, headers={'User-Agent': get_user_agent()})
        return response.text
    except Exception as e:
        print(f"Error fetching HTML: {e}")
    # Failure, if all proxies failed
    return None

def get_next_word(driver: webdriver.Chrome, last_word: str) -> list[str]:
    print(last_word)
    # Encode URL
    url = base_url+last_word
    # Fetch the HTML
    html = get_html(driver, url)
    # Parse the HTML
    soup = BeautifulSoup(html, 'html.parser')
    words_div = soup.find('div', class_='words')
    if words_div is None:
        print(soup)
    # The second link in the div is the next word
    return words_div.find_all('a')[1].contents[0]

def scrape_words(driver: webdriver.Chrome):
    # If the file doesn't exist, then last_word = 'а'
    if not os.path.exists(output_file):
        last_word = 'а'
    # Read the last word from the file
    with open(output_file, 'r', encoding='utf-8') as f:
        last_word = f.readlines()[-1].strip()

    # Scrape the words
    while True:
        # Fetch the next word
        word = get_next_word(driver, last_word)
        # Abort, if the word is not found
        if word is None:
            break
        # Append the word to a .txt file
        with open(output_file, 'a', encoding='utf-8') as f:
            f.write(word + '\n')
        # Move forward
        last_word = word
        # Minor delay
        random_delay = random.uniform(0.5, 3)
        time.sleep(random_delay)

def scrape_words_with_selenium():
    # Set up the Chrome browser
    options = webdriver.ChromeOptions() 
    options.add_argument("start-maximized")
    options.add_argument("--auto-open-devtools-for-tabs")
    # options.add_argument("--no-sandbox")   
    # # options.add_argument('--ignore-certificate-errors')
    # # options.add_argument("--test-type")
    # # options.add_experimental_option("excludeSwitches", ["enable-automation"])
    # options.add_experimental_option('useAutomationExtension', False)
                            
    # Create a new Chrome browser instance
    driver = webdriver.Chrome(options=options)
    # Navigate to the target URL
    driver.get(target_url)
    # Wait for the page to load
    WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".fc-button.fc-cta-consent.fc-primary-button")))
    # Click on Consent = Yes
    btn_cookies_yes = driver.find_elements(By.CSS_SELECTOR, ".fc-button.fc-cta-consent.fc-primary-button")
    btn_cookies_yes[0].click()
    # Click on the search bar
    search_bar = driver.find_element(By.CSS_SELECTOR, "input[id='word']")
    search_bar.send_keys("а")
    # Click on the search button
    btn_search = driver.find_element(By.CSS_SELECTOR, "button[id='submitButton']")
    btn_search.click()
    # Wait for the page to load
    WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[id='wordsList']")))
    # ActionChains(driver).send_keys(Keys.F12).perform()
    words_div = driver.find_element(By.CSS_SELECTOR, "div[id='wordsList']")
    word_hrefs = words_div.find_elements(By.CSS_SELECTOR, "a")
    words = "\n".join([word_href.text for word_href in word_hrefs])
    print(words)
    # Append the words to a file
    with open('data/words.txt', 'a', encoding='utf-8') as f:
        f.write(words)
    # CLick on the last word anchor
    word_hrefs[-1].click()
    time.sleep(3)

    try:
        ad_div = driver.find_element(By.CSS_SELECTOR, "div[id='mys-content']")
        print(ad_div)
        # identify the iframe element
        iframe = driver.find_element(By.ID, "contentFrame")
        # switch to the iframe
        driver.switch_to.frame(iframe)
        btn_close = driver.find_element(By.CSS_SELECTOR, "div[class='closeButton']")
        btn_close.click()
    except:
        print("No close button found")
        pass
    time.sleep(70)
    # ActionChains(driver).send_keys(Keys.F12).perform()
    # Wait for the page to load
    # # Start the scraping
    # scrape_words(driver)
    # release the resources allocated by Selenium and shut down the browser
   # driver.quit()

# Main loop
scrape_words_with_selenium()