# Fortitude Valley Property Tracker

A local Python application to track median sale prices for 1-bedroom apartments in Fortitude Valley and correlate these prices with 2032 Queensland government infrastructure announcements.

## Project Structure
- `data/raw/`: Store raw scraped data.
- `data/processed/`: Store cleaned and combined data.
- `src/scrapers/`: Scripts to fetch property prices and infrastructure news.
- `src/analysis/`: Scripts to calculate correlations.
- `src/visualization/`: Streamlit dashboard to present the findings interactively.

## Setup

1. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

### 1. Fetch Data and Correlate
Run the main script to collect the data and perform the analysis:
```bash
python main.py
```

### 2. View Dashboard
Launch the Streamlit dashboard to view the interactive plots:
```bash
streamlit run src/visualization/dashboard.py
```
