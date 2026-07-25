import sys
import os

# Ensure root folder is on Python path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

# Run the live Streamlit dashboard
import src.visualization.dashboard
