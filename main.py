import os
import sys

# Ensure src modules can be found
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from src.database.db_manager import init_db
from src.scrapers.property_scraper import scrape_property_prices
from src.scrapers.infrastructure_scraper import scrape_infrastructure_news

def main():
    print("Initializing Database...")
    init_db()
    
    print("\n--- Scraping Property Prices ---")
    scrape_property_prices()
    
    print("\n--- Scraping Infrastructure News ---")
    scrape_infrastructure_news()
    
    print("\nData collection complete.")

if __name__ == "__main__":
    main()
