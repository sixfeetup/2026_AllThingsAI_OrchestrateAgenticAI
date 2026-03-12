import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# The URL of the page you are viewing
url = "https://www.americanroads.us/dungeons.html"
# The folder where the PDFs will be saved
folder_name = "DnD_Archive"

if not os.path.exists(folder_name):
    os.makedirs(folder_name)

print(f"Connecting to {url}...")
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Find all links ending in .pdf
links = soup.find_all('a', href=True)
pdf_links = [urljoin(url, l['href']) for l in links if l['href'].lower().endswith('.pdf')]

print(f"Found {len(pdf_links)} PDF files. Starting download...")

for link in pdf_links:
    # Use the filename from the URL
    file_name = os.path.join(folder_name, link.split('/')[-1])

    print(f"Downloading: {file_name}")
    try:
        with requests.get(link, stream=True) as r:
            r.raise_for_status()
            with open(file_name, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
    except Exception as e:
        print(f"Failed to download {link}: {e}")

print("\nAll downloads complete!")
