import sys
import os

# Ensure src modules can be found
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

# Check if running within a Streamlit server runtime
try:
    import streamlit as st
    in_streamlit = st.runtime.exists()
except Exception:
    in_streamlit = False

if in_streamlit:
    # When launched by Streamlit Community Cloud (e.g. streamlit run main.py), run the UI
    import src.visualization.dashboard
else:
    # When launched via command line (e.g. python main.py), run the data collection pipeline
    from src.database.db_manager import init_db
    from src.scrapers.property_scraper import scrape_property_prices
    from src.scrapers.infrastructure_scraper import scrape_infrastructure_news
    from src.scrapers.sqm_scraper import fetch_sqm_indicators

    def main():
        print("Initializing Database...")
        init_db()
        
        print("\n--- Fetching SQM Research Market Indicators ---")
        fetch_sqm_indicators()

        print("\n--- Scraping Property Prices ---")
        scrape_property_prices()
        
        print("\n--- Scraping Infrastructure News ---")
        scrape_infrastructure_news()
        
        print("\nData collection complete.")

    if __name__ == "__main__":
        main()
