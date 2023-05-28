import csv
import requests
from bs4 import BeautifulSoup

class Scraper:
    def __init__(self, url, tender_listings_csv, corrigendums_csv):
        self.url = url
        self.tender_listings_csv = tender_listings_csv
        self.corrigendums_csv = corrigendums_csv

    def load_data(self):
        response = requests.get(self.url)
        self.html_content = response.content

    def scrape_tender_listings(self):
        soup = BeautifulSoup(self.html_content, 'html.parser')
        table = soup.find('table', id='activeTenders')

        with open(self.tender_listings_csv, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Tender Title', 'Reference No', 'Closing Date', 'Bid Opening Date'])

            rows = table.find_all('tr', class_=lambda x: x != 'list_header')
            for row in rows:
                columns = row.find_all('td')

                tender_title = columns[0].a.text.strip()
                reference_no = columns[1].text.strip()
                closing_date = columns[2].text.strip()
                bid_opening_date = columns[3].text.strip()

                writer.writerow([tender_title, reference_no, closing_date, bid_opening_date])

    def scrape_corrigendums(self):
        soup = BeautifulSoup(self.html_content, 'html.parser')
        table = soup.find('table', id='activeCorrigendums')

        with open(self.corrigendums_csv, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Corrigendum', 'Tender Number', 'Start Date', 'End Date'])

            rows = table.find_all('tr')
            for row in rows:
                columns = row.find_all('td')
                if len(columns) == 4:
                    corrigendum = columns[0].text.strip()
                    tender_number = columns[1].text.strip()
                    start_date = columns[2].text.strip()
                    end_date = columns[3].text.strip()

                    writer.writerow([corrigendum, tender_number, start_date, end_date])

    def run(self):
        self.load_data()
        self.scrape_tender_listings()
        self.scrape_corrigendums()

# URL of the webpage containing the tender listings
tender_listings_url = 'https://etenders.gov.in/eprocure/app'
tender_listings_csv = 'tenders.csv'

# URL of the webpage containing the corrigendums
corrigendums_url = 'https://etenders.gov.in/eprocure/app'
corrigendums_csv = 'corrigendums.csv'

# Create an instance of the scraper for tender listings and run the scraping process
tender_listings_scraper = Scraper(tender_listings_url, tender_listings_csv, corrigendums_csv)
tender_listings_scraper.run()

# Create an instance of the scraper for corrigendums and run the scraping process
corrigendums_scraper = Scraper(corrigendums_url, tender_listings_csv, corrigendums_csv)
corrigendums_scraper.run()

