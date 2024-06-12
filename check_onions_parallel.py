import random
import string
import time
import requests
from concurrent.futures import ThreadPoolExecutor

def generate_onion_url():
    return 'https://' + ''.join(random.choices(string.ascii_letters + string.digits, k=56)) + '.onion'

def check_onion_url(url):
    proxies = {
        'http': 'socks5h://127.0.0.1:9050',
        'https': 'socks5h://127.0.0.1:9050'
    }
    try:
        response = requests.get(url, proxies=proxies, timeout=10)
        return url if response.status_code == 200 else None
    except requests.RequestException:
        return None

def save_accessible_url(url):
    with open("accessible_onions.txt", "a") as file:
        file.write(url + "\n")

def process_url(_):
    onion_url = generate_onion_url()
    accessible_url = check_onion_url(onion_url)
    if accessible_url:
        save_accessible_url(accessible_url)
        print(f"{accessible_url} is accessible and saved.")
    else:
        print(f"{onion_url} is not accessible.")

def main():
    try:
        with ThreadPoolExecutor(max_workers=10) as executor:
            while True:
                executor.submit(process_url, None)
                time.sleep(0.1)
    except KeyboardInterrupt:
        print("Stopped by user")

if __name__ == "__main__":
    main()
