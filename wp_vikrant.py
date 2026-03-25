import os
import time
import requests
import subprocess
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import urllib3

# Suppress SSL warnings (optional, use cautiously)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Windows User-Agent for smoother scraping
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"

# Directory to save scraped content
VIKRANT_DIR = "VIKRANT"

def setup_directory():
    """Create the VIKRANT directory if it doesn't exist."""
    if not os.path.exists(VIKRANT_DIR):
        os.makedirs(VIKRANT_DIR)

def save_file(content, filepath):
    """Save content to a file in the VIKRANT directory."""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'wb') as f:
        f.write(content)

def curl_request(url):
    """Perform an HTTP request using curl and return the response content."""
    try:
        result = subprocess.run(
            ['curl', '-s', '-L', '-A', USER_AGENT, url],
            capture_output=True,
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error fetching {url} with curl: {e}")
        return None

def scrape_page(url, visited_urls, base_url):
    """Scrape a single page and its assets, saving them to VIKRANT directory."""
    if url in visited_urls:
        return
    visited_urls.add(url)

    print(f"Scraping: {url}")
    try:
        # Use curl to fetch the page
        html_content = curl_request(url)
        if not html_content:
            return

        # Parse URL to create file path
        parsed_url = urlparse(url)
        path = parsed_url.path
        if path == "/" or path == "":
            filepath = os.path.join(VIKRANT_DIR, "index.html")
        elif path.endswith("/"):
            filepath = os.path.join(VIKRANT_DIR, path.lstrip("/"), "index.html")
        else:
            filepath = os.path.join(VIKRANT_DIR, path.lstrip("/"))

        # Save HTML content
        save_file(html_content, filepath)

        # Parse HTML to find assets and links
        soup = BeautifulSoup(html_content, 'html.parser')
        assets = []

        # Find all asset tags (images, CSS, JS, etc.)
        for img in soup.find_all('img', src=True):
            assets.append(urljoin(url, img['src']))
        for link in soup.find_all('link', href=True):
            assets.append(urljoin(url, link['href']))
        for script in soup.find_all('script', src=True):
            assets.append(urljoin(url, script['src']))

        # Download assets
        for asset_url in assets:
            if base_url in asset_url:  # Only download assets from the target site
                download_asset(asset_url, base_url)

        # Find all internal links to scrape recursively
        for a_tag in soup.find_all('a', href=True):
            href = urljoin(url, a_tag['href'])
            if base_url in href and href not in visited_urls:
                time.sleep(1)  # Rate limiting
                scrape_page(href, visited_urls, base_url)

    except Exception as e:
        print(f"Error scraping {url}: {e}")

def download_asset(asset_url, base_url):
    """Download an asset (e.g., CSS, JS, image) using requests and save it to VIKRANT directory."""
    try:
        headers = {'User-Agent': USER_AGENT}
        response = requests.get(asset_url, headers=headers, verify=False, timeout=10)
        if response.status_code == 200:
            parsed_url = urlparse(asset_url)
            path = parsed_url.path
            filepath = os.path.join(VIKRANT_DIR, path.lstrip("/"))
            save_file(response.content, filepath)
            print(f"Downloaded asset: {asset_url}")
    except Exception as e:
        print(f"Error downloading asset {asset_url}: {e}")

def deep_fingerprinting(url):
    """Perform deep fingerprinting to identify WordPress characteristics."""
    try:
        headers = {'User-Agent': USER_AGENT}
        response = requests.get(url, headers=headers, verify=False, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Check for WordPress-specific indicators
        wp_indicators = [
            soup.find('meta', {'name': 'generator', 'content': lambda x: x and 'WordPress' in x}),
            soup.find(lambda tag: tag.name == 'link' and 'wp-content' in tag.get('href', '')),
            soup.find(lambda tag: tag.name == 'script' and 'wp-includes' in tag.get('src', '')),
        ]

        if any(wp_indicators):
            print("WordPress site detected!")
        else:
            print("Warning: This may not be a WordPress site.")

    except Exception as e:
        print(f"Error during fingerprinting: {e}")

def main():
    # Prompt for the site URL
    site_url = input("Enter the WordPress site URL to clone (e.g., https://example.com): ").strip()
    if not site_url.startswith(('http://', 'https://')):
        site_url = 'https://' + site_url

    # Validate URL
    parsed_url = urlparse(site_url)
    if not parsed_url.scheme or not parsed_url.netloc:
        print("Invalid URL. Please include the protocol (http:// or https://).")
        return

    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"

    # Create VIKRANT directory
    setup_directory()

    # Perform deep fingerprinting
    deep_fingerprinting(site_url)

    # Start scraping from the main page
    visited_urls = set()
    scrape_page(site_url, visited_urls, base_url)
    print(f"Scraping completed! Files saved in '{VIKRANT_DIR}' directory.")

if __name__ == "__main__":
    main()
