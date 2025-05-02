import requests
from bs4 import BeautifulSoup
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

# Fungsi untuk membersihkan teks dari tag HTML dan karakter berlebih
def clean_text(text):
    return ' '.join(text.strip().split())

# Fungsi untuk scraping menggunakan requests (untuk halaman statis)
def scrape_static(url):
    try:
        # Kirim permintaan HTTP
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Cari semua tag img untuk gambar
        images = []
        for img in soup.find_all('img'):
            src = img.get('src', '')
            if src and ('.jpg' in src or '.png' in src):  # Filter URL gambar
                if src.startswith('http'):
                    images.append(src)

        # Cari deskripsi (misalnya, dalam tag h1 atau div dengan kelas tertentu)
        description = ''
        # Cari elemen h1 dengan kelas yang relevan
        desc_element = soup.find('h1', class_=re.compile('_ap3a|_aaco|_aacu|_aacx|_aad7|_aade'))
        if desc_element:
            description = clean_text(desc_element.get_text())
        else:
            # Jika tidak ada h1, cari div atau span dengan teks panjang
            for div in soup.find_all(['div', 'span'], class_=re.compile('_aaco|_aacx|_aad7|_aade')):
                text = div.get_text()
                if len(text) > 50:  # Asumsi deskripsi panjang
                    description = clean_text(text)
                    break

        return {'images': images, 'description': description}

    except Exception as e:
        return {'error': str(e)}

# Fungsi untuk scraping menggunakan selenium (untuk halaman dinamis)
def scrape_dynamic(url):
    try:
        # Set up Selenium
        options = Options()
        options.headless = True
        driver = webdriver.Chrome(options=options)
        driver.get(url)
        time.sleep(3)  # Tunggu halaman dimuat

        # Parsing dengan BeautifulSoup
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        driver.quit()

        # Cari semua tag img untuk gambar
        images = []
        for img in soup.find_all('img'):
            src = img.get('src', '')
            if src and ('.jpg' in src or '.png' in src):  # Filter URL gambar
                if src.startswith('http'):
                    images.append(src)

        # Cari deskripsi
        description = ''
        desc_element = soup.find('h1', class_=re.compile('_ap3a|_aaco|_aacu|_aacx|_aad7|_aade'))
        if desc_element:
            description = clean_text(desc_element.get_text())
        else:
            for div in soup.find_all(['div', 'span'], class_=re.compile('_aaco|_aacx|_aad7|_aade')):
                text = div.get_text()
                if len(text) > 50:
                    description = clean_text(text)
                    break

        return {'images': images, 'description': description}

    except Exception as e:
        return {'error': str(e)}

# Contoh penggunaan
if __name__ == "__main__":
    url = "https://www.instagram.com/p/DIsWMxbvx-9/?utm_source=ig_web_copy_link&igsh=MzRlODBiNWFlZA%3D%3D"  # Ganti dengan URL postingan Instagram
    result = scrape_dynamic(url)  # Gunakan scrape_dynamic untuk Instagram
    print("Images:", result.get('images', []))
    print("Description:", result.get('description', ''))
    if 'error' in result:
        print("Error:", result['error'])