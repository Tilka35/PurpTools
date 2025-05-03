""" Scanner to brute force (enumerate) subdomains of a domain, kinda inspired by go/dirbuster, takes user input and user-provided list of subdomains as a list.
Idea from thepythoncode.com
Goal is to enumerate subdomains, taking user input. Work in progress.
"requests" library package must be installed.
"""

# Imports
import requests
from threading import Thread, Lock
from queue import Queue
from urllib.parse import urlparse

# Global variables
list_lock = Lock() # Lock object
discovered_subdomains = [] # List of discovered subdomains

# Enumerate Subdomains
def enum_subd(domain, q):
    
    while not q.empty():
        subdomain = q.get()
    
        # URL to send - Scan subdomain
        url = f"http://{subdomain}.{domain}"
        try:
            # If encounters an error - domain does NOT exist
            response = requests.get(url, timeout=5, headers={"User-Agent": "Mozilla/5.0"})
            if response.status_code == 200:
                print("[+] Discovered Subdomain: ", url)
                with list_lock:
                    discovered_subdomains.append(url)
        except requests.ConnectionError:
            # If subdomain does not exist, continue and do nothing
            pass

        q.task_done()
        
# Ensure valid URL
def is_valid_url(domain):
    parsed_url = urlparse(f"http://{domain}")
    return bool(parsed_url.netloc) # Ensure valid URL
                    
def main(domain, subdomains, n_threads):
    if not is_valid_url(domain):
      print("Error: Invalid Domain Format.")
      return
  
    q = Queue()
    for subdomain in subdomains:
        q.put(subdomain)
        
    threads = []
    for t in range(n_threads):
        worker = Thread(target=enum_subd, args=(domain, q))
        worker.daemon = True
        worker.start()
        threads.append(worker)
    
    q.join()
    for t in threads:
        t.join()
    
if __name__ == "__main__":
    import argparse
    
    # Command line input for domain and wordlist instead of code run input
    parser = argparse.ArgumentParser(description="Fast Subdomain Scanner using Threads")
    parser.add_argument("domain", help="Domain to Scan for Subdomains (without protocol e.g without 'http:\\')")
    parser.add_argument("-w", "--wordlist", help="Provide a Wordlist that contains all of the Subdomains to Scan for.")
    parser.add_argument("-t", "--num-threads", help="Number of Threads to use to Scan the Domain. Default is 10. Add more if your system is beefy.", default=10, type=int)
    parser.add_argument("-o", "--output-file", help="Specify the Output file to write the discovered subdomains", default="discovered_subdomains.txt")
    
    args = parser.parse_args()
    domain = args.domain
    wordlist = args.wordlist
    num_threads = args.num_threads
    output_file = args.output_file
    
    try:
        with open(wordlist, "r", encoding="utf-8") as file:
            subdomains = file.read().splitlines()
    except FileNotFoundError:
        print("Error: File not Found. Please check the filepath")
        exit(1)
    
    main(domain, subdomains, num_threads)
    
    # Save results to file
    if discovered_subdomains:
        
        with open(output_file, "w") as f:
            for url in discovered_subdomains:
                print(url, file=f)