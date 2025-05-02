import requests
from bs4 import BeautifulSoup
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import re
import time

def clean_text(text):
    # Implement your text cleaning logic here
    return text.strip()

def scrape_dynamic(url):
    try:
        # Set up Selenium
        options = Options()
        options.headless = True
        driver = webdriver.Chrome(options=options)
        driver.get(url)
        time.sleep(3)  # Wait for page to load

        # Parsing dengan BeautifulSoup
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        driver.quit()

        # Cari semua tag img untuk gambar
        images = []
        for img in soup.find_all('img'):
            src = img.get('src') or img.get('data-src', '')
            if src and ('.jpg' in src or '.jpeg' in src or '.png' in src):
                if not src.startswith('data:image'):  # Skip base64 encoded images
                    if src.startswith('http') or src.startswith('//'):
                        # Get image dimensions
                        width = 0
                        height = 0
                        
                        # Check HTML attributes first
                        width_attr = img.get('width')
                        height_attr = img.get('height')
                        
                        if width_attr and width_attr.isdigit():
                            width = int(width_attr)
                        if height_attr and height_attr.isdigit():
                            height = int(height_attr)
                            
                        # If dimensions not in HTML attributes, check style
                        if width == 0 or height == 0:
                            style = img.get('style', '')
                            if style:
                                # Extract width and height from style
                                width_match = re.search(r'width:\s*(\d+)px', style)
                                height_match = re.search(r'height:\s*(\d+)px', style)
                                if width_match:
                                    width = int(width_match.group(1))
                                if height_match:
                                    height = int(height_match.group(1))
                        
                        # Normalize URL
                        if src.startswith('//'):
                            src = 'https:' + src
                            
                        images.append({
                            'src': src,
                            'width': width,
                            'height': height,
                            'area': width * height
                        })

        # Filter to get only large images
        if images:
            # Sort by area (width * height) descending
            images.sort(key=lambda x: x['area'], reverse=True)
            
            # Take the largest image or top few large images
            # You can adjust this threshold as needed
            max_images = 3
            large_images = [img['src'] for img in images[:max_images] if img['area'] > 50000]  # 50000 = ~224x224
            
            # If no images meet the threshold, take the largest one anyway
            if not large_images and images:
                large_images = [images[0]['src']]
        else:
            large_images = []

        return {'images': large_images}

    except Exception as e:
        return {'error': str(e)}

# Contoh penggunaan
if __name__ == "__main__":
    url = "https://www.instagram.com/p/DIWPniWPhkZ/?igsh=MTA3dTE4MG0yODJ2MQ=="  # Ganti dengan URL postingan Instagram
    result = scrape_dynamic(url)  # Gunakan scrape_dynamic untuk Instagram
    print("Images:", result.get('images', []))
    if 'error' in result:
        print("Error:", result['error'])