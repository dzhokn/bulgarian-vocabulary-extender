import os
import dotenv
import requests
from time import sleep

# Load the .env file
dotenv.load_dotenv()
api_key_groq = os.getenv('GROQ_API_KEY')


# Methods for checking words with LLM API calls
def get_drug_names(words:list[str]) -> list[str]:
    # Make API call to Groq API
    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key_groq}",
            "Content-Type": "application/json"
        },
        json={"model": "meta-llama/llama-4-scout-17b-16e-instruct", 
              "messages": [{"role": "user", "content": f"Отговаряш кратко без обяснения. За кои от следните думи си сигурен, че са имена на медикаменти? \n {words}"}]})
    # Parse the content of the response
    json_data = response.json()
    if 'choices' not in json_data:
        print(json_data)
        exit()
    answer = json_data['choices'][0]['message']['content']
    print(answer)

def get_pharmacy_related_words(words:list[str]) -> list[str]:
    # Make API call to Groq API
    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key_groq}",
            "Content-Type": "application/json"
        },
        json={"model": "openai/gpt-oss-120b", 
              "messages": [{"role": "user", "content": f"Ти си български речник. За кои от следните думи си сигурен, че са медицински или фармацевтични термини? \n {words}"}]})
    # Parse the content of the response
    json_data = response.json()
    if 'choices' not in json_data:
        print(json_data)
        exit()
    answer = json_data['choices'][0]['message']['content']
    print(answer)

def get_names(words:list[str]) -> list[str]:
    # Make API call to Groq API
    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key_groq}",
            "Content-Type": "application/json"
        },
        json={"model": "llama-3.3-70b-versatile", 
              "messages": [{"role": "user", "content": f"Отговаряш кратко без обяснения. За кои от следните думи си сигурен, че са наименования? \n {words}"}]})
    # Parse the content of the response
    json_data = response.json()
    if 'choices' not in json_data:
        print(json_data)
        exit()
    answer = json_data['choices'][0]['message']['content']
    print(answer)

def get_invalid_words(words:list[str]) -> list[str]:
    # Make API call to Groq API
    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key_groq}",
            "Content-Type": "application/json"
        },
        json={"model": "meta-llama/llama-4-scout-17b-16e-instruct", "messages": [{"role": "user", "content": f"Ти си български речник. Отговаряш кратко без обяснения. За кои от следните думи си сигурен, че не същестуват или са неправилно изписани? \n {words}"}]})
    # Parse the content of the response
    json_data = response.json()
    if 'choices' not in json_data:
        print(json_data)
        exit()
    answer = json_data['choices'][0]['message']['content']
    print(answer)

def is_valid_word(word:str) -> tuple[bool, str]:
    # Make API call to Groq API
    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key_groq}",
            "Content-Type": "application/json"
        },
        json={"model": "meta-llama/llama-4-scout-17b-16e-instruct", "messages": [{"role": "user", "content": f"Ти си български речник. В теб няма имена (особено на лекарства, хора и химични съединения). Ти включваш само най-ползваните думи от българския речник. Отговаряй с не повече от 30 думи и без абзаци. Съществува ли думата '{word}' в официалния български речник?"}]})
    # Parse the content of the response
    json_data = response.json()
    if 'choices' not in json_data:
        print(json_data)
        exit()
    answer = json_data['choices'][0]['message']['content']
    if answer.startswith('Да'):
        return True, answer
    else:
        return False, answer


# Main function
words = []
answers = {}
for w in words:
    answers[w] = is_valid_word(w)
    txt_to_write = f"{w}\t{answers[w][0]}\t{answers[w][1].replace('\n', ' ').replace('\r', '')}"
    print(txt_to_write)
    with open('groq.txt', 'a', encoding='utf-8') as f:
        f.write(txt_to_write + '\n')
    sleep(2) # Needed cause of the rate limit (30 req/min)