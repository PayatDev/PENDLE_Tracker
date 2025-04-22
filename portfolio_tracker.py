import requests
import pandas as pd
from datetime import datetime
import gspread
import json
import os
from google.oauth2.service_account import Credentials

def fetch_pendle_and_save_to_sheet():
    # Service account authentication using GitHub secrets
    credentials_json = json.loads(os.environ.get('GOOGLE_CREDENTIALS'))
    scope = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'
    ]
    
    credentials = Credentials.from_service_account_info(
        credentials_json, 
        scopes=scope
    )
    
    gc = gspread.authorize(credentials)
    
    # Open the Google Sheet
    sheet_id = os.environ.get('SHEET_ID')
    sheet = gc.open_by_key(sheet_id).sheet1
    
    # Fetch data from Pendle API
    wallet_address = os.environ.get('WALLET_ADDRESS')
    url = f"https://api-v2.pendle.finance/core/v1/dashboard/positions/database/{wallet_address}"
    
    response = requests.get(url)
    data = response.json()
    
    # Extract portfolio value
    total_value = 0
    for position in data.get('positions', []):
        for open_position in position.get('openPositions', []):
            total_value += open_position.get('pt', {}).get('valuation', 0)
            total_value += open_position.get('yt', {}).get('valuation', 0)
            total_value += open_position.get('lp', {}).get('valuation', 0)
    
    # Get current date
    current_date = datetime.now().strftime("%Y-%m-%d")
    
    # Append to sheet
    sheet.append_row([current_date, total_value])
    print(f"Updated sheet with portfolio value: ${total_value} on {current_date}")

if __name__ == "__main__":
    fetch_pendle_and_save_to_sheet()
