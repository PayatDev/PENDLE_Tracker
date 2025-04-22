import requests
import json
import csv
import os
from datetime import datetime

def fetch_pendle_and_save_to_repo():
    # Fetch data from Pendle API
    wallet_address = os.environ.get('WALLET_ADDRESS', '0x7694c57016F7f1E8Aea7EEcf7dF886f138Bc4aC7')
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
    
    # Save raw API response for reference
    with open('latest_data.json', 'w') as f:
        json.dump(data, f, indent=2)
    
    # Append to CSV history file
    csv_file = 'portfolio_history.csv'
    file_exists = os.path.isfile(csv_file)
    
    with open(csv_file, 'a', newline='') as f:
        writer = csv.writer(f)
        # Write header if file doesn't exist
        if not file_exists:
            writer.writerow(['Date', 'Total Value ($)'])
        writer.writerow([current_date, total_value])
    
    # Update summary file
    summary = {
        'last_updated': current_date,
        'total_value': total_value,
        'wallet_address': wallet_address
    }
    
    with open('portfolio_summary.json', 'w') as f:
        json.dump(summary, f, indent=2)
    
    print(f"Updated repository with portfolio value: ${total_value} on {current_date}")

if __name__ == "__main__":
    fetch_pendle_and_save_to_repo()
