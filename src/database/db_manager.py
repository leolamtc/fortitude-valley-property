import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "data", "processed", "fortitude_valley.db")

def get_db_connection():
    """Establish a connection to the SQLite database."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize the database schema."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Table for property prices
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS property_prices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            address TEXT,
            suburb TEXT NOT NULL,
            property_type TEXT NOT NULL,
            bedrooms INTEGER NOT NULL,
            car_spaces INTEGER NOT NULL DEFAULT 0,
            median_price REAL NOT NULL,
            date_scraped TEXT NOT NULL,
            source_url TEXT
        )
    """)
    
    # Table for infrastructure announcements
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS infrastructure_announcements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            date_announced TEXT NOT NULL,
            summary TEXT,
            url TEXT,
            date_scraped TEXT NOT NULL
        )
    """)
    
    conn.commit()
    conn.close()

def save_property_price(address, suburb, property_type, bedrooms, car_spaces, median_price, date_scraped, source_url):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO property_prices (address, suburb, property_type, bedrooms, car_spaces, median_price, date_scraped, source_url)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (address, suburb, property_type, bedrooms, car_spaces, median_price, date_scraped, source_url))
    conn.commit()
    conn.close()

def save_infrastructure_announcement(title, date_announced, summary, url, date_scraped):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO infrastructure_announcements (title, date_announced, summary, url, date_scraped)
        VALUES (?, ?, ?, ?, ?)
    """, (title, date_announced, summary, url, date_scraped))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("Database initialized successfully.")
