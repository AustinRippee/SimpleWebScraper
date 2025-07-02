import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://en.wikipedia.org/wiki/Mile_run_world_record_progression"

try:
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')

    tables = soup.find_all('table')
    target_table = tables[4]

    headers = [th.get_text(strip=True) for th in target_table.find_all('th')]

    # Extract the data from the table
    rows = []
    for row in target_table.find_all('tr')[1:]:  # Skip the first row (headers)
        # Remove all reference numbers (sup tags) before extracting text
        for sup in row.find_all('sup'):
            sup.decompose()

        # Extract cell data
        cells = [cell.get_text(strip=True) for cell in row.find_all('td')]
        if cells:
            rows.append(cells)

    # Convert to a DataFrame for easy analysis
    df = pd.DataFrame(rows, columns=headers[:len(rows[0])])

    selected_columns = ["Time", "Athlete", "Date"]
    filtered_df = df[selected_columns]

    print(filtered_df)  # Print the first few rows for a quick look

except requests.exceptions.RequestException as e:
    print(f"Error fetching the page: {e}")
