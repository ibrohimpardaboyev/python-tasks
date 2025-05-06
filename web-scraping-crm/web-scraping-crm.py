import requests
from bs4 import BeautifulSoup
import csv, json
import time
import logging

logging.basicConfig(filename='log.txt', level=logging.INFO)

def retry(func):
    def wrapper(*args, **kwargs):
        for attempt in range(3):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logging.error(f"Error: {e} | Attempt {attempt + 1}")
                time.sleep(1)
        return None
    return wrapper

class Scraper:
    def __init__(self, url):
        self._url = url
        self.data = []

    @retry
    def fetch(self):
        logging.info(f"Start scraping: {self._url}")
        response = requests.get(self._url)
        if response.status_code != 200:
            raise Exception(f"Status code {response.status_code}")
        soup = BeautifulSoup(response.text, 'lxml')
        self.parse(soup)
        logging.info(f"End scraping: {self._url}")

    def parse(self, soup):
        pass  
class NewsScraper(Scraper):
    def parse(self, soup):
        articles = soup.find_all('h2')[:5]
        for a in articles:
            title = a.get_text(strip=True)
            self.data.append({'title': title})

class ProductScraper(Scraper):
    def parse(self, soup):
        products = soup.find_all('span', class_='product-title')[:5]
        for p in products:
            title = p.get_text(strip=True)
            self.data.append({'product': title})

class DataCleaner:
    @staticmethod
    def clean(data):
        return [{'text': d['title'].strip().lower()} for d in data if 'title' in d]

class LeadGenerator:
    @staticmethod
    def generate(data):
        leads = []
        for item in data:
            leads.append({'user_interest': item['text']})
        return leads

def export_to_csv(data, filename='data.csv'):
    with open(filename, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)

def export_to_json(data, filename='data.json'):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)
