import random
import string
import time
import requests
from concurrent.futures import ThreadPoolExecutor

def generate_onion_url():
    return 'http://' + ''.join(random.choices(string.ascii_letters + string.digits, k=56)) + '.onion'

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

import random
import string
import time
import requests
import threading
from concurrent.futures import ThreadPoolExecutor
import argparse

LOCK = threading.Lock()
OUTPUT_FILE = "accessible_onions.txt"


def generate_onion_url():
    # NOTE: truly valid .onion addresses are derived from keys, so
    # random generation will almost never hit a real service.
    return 'http://' + ''.join(random.choices(string.ascii_letters + string.digits, k=56)) + '.onion'


def check_onion_url(url, timeout=10):
    proxies = {
        'http': 'socks5h://127.0.0.1:9050',
        'https': 'socks5h://127.0.0.1:9050'
    }
    try:
        # verify=False because many onion services use self-signed certs (or none)
        response = requests.get(url, proxies=proxies, timeout=timeout, verify=False)
        # Accept any response that is not a client/server error
        if response.status_code < 400:
            return url
    except requests.RequestException:
        return None
    return None


def save_accessible_url(url):
    # Thread-safe append with explicit encoding
    with LOCK:
        with open(OUTPUT_FILE, "a", encoding="utf-8") as file:
            file.write(url + "\n")


def process_url(_index):
    onion_url = generate_onion_url()
    accessible_url = check_onion_url(onion_url)
    if accessible_url:
        save_accessible_url(accessible_url)
        print(f"{accessible_url} is accessible and saved.")
    else:
        # Keep this quiet if you prefer; printing all misses is noisy
        print(f"{onion_url} is not accessible.")


def main():
    parser = argparse.ArgumentParser(description="Check onion urls in parallel (best-effort).")
    parser.add_argument("--limit", type=int, default=100, help="Number of random checks to perform")
    parser.add_argument("--workers", type=int, default=10, help="Number of concurrent worker threads")
    parser.add_argument("--timeout", type=int, default=10, help="Request timeout in seconds")
    args = parser.parse_args()

    total = args.limit
    workers = args.workers
    timeout = args.timeout

    print(f"Starting: total={total}, workers={workers}, timeout={timeout}")

    try:
        # Use executor.map to submit a bounded batch of tasks
        with ThreadPoolExecutor(max_workers=workers) as executor:
            # map will block until all tasks are submitted and completed
            list(executor.map(lambda i: process_url(i), range(total)))
    except KeyboardInterrupt:
        print("Stopped by user")


if __name__ == "__main__":
    main()