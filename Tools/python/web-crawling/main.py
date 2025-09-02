# Automated web crawling tool developed using
import requests, os, tarfile
from bs4 import BeautifulSoup
from time import sleep
from tqdm import tqdm
from urllib.parse import urljoin, urlparse

# Base url for crawling/downloading
base_url = "https://phrack.org/issues/"
issue_range = range(1, 73)

def download_issues(base_url, issue_range):
# Progress bar
    for issue_num in tqdm(issue_range, desc="Downloading..."):
        issue_url = f"{base_url}{issue_num}/"
        try:
            # Download HTML content
            response = requests.get(issue_url)
            # Parse content and search for links
            soup = BeautifulSoup(response.text, 'html.parser')
            # Find .tar.gz link
            for link in soup.find_all('a', href=True): # Anchor tags
                if link.text.lower().strip() == "get tar.gz":
                    # Get full url
                    tar_url = urljoin(issue_url, link['href'])
                    filename = tar_url.split("/")[-1] # Extract file name from url
                    print(f"Downloading {filename} from {tar_url}")
                    tar_response = requests.get(tar_url) # Download archive
                    with open(filename, 'wb') as f: # Save file locally
                        f.write(tar_response.content)
                        
                    try:
                        with tarfile.open(filename, 'r:gz') as tar:
                            tar.extractall(path=f"phrack_issue_{issue_num}")
                            print(f"Extracted to phrack_issue_{issue_num}")
                    except tarfile.TarError as e:
                        print(f"Failed to extract {filename}: {e}")
                    sleep(2) # Be kind to server !! Wait before next request
        except Exception as e:
            print(f"Failed to process issue {issue_num}: {e}")
            sleep(2) # Polite crawling !!
    
def main():
    download_issues(base_url, issue_range)
    
if __name__ == "__main__":
    main()