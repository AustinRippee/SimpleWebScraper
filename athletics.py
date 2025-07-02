import re

import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://www.alltime-athletics.com/m_mileok.htm"

# Show all columns in output
pd.set_option('display.max_columns', None)

# Also useful: show more rows if needed
pd.set_option('display.max_rows', 100)  # or None for unlimited

# If columns are too wide and get truncated, you can adjust:
pd.set_option('display.max_colwidth', None)  # Show full content in columns

try:
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')

    pre_block = soup.find('pre')

    raw_text = pre_block.getText()

    lines = [line for line in raw_text.split('\n') if line.strip()]

    # Print header lines to find where actual data starts
    #for i, line in enumerate(lines[:10]):
    #    print(f"Line {i}: {line}")

    headers = ["Rank", "Time", "Athlete", "Country", "DOB", "Place In Race", "Location", "Date"]
    expected_cols = len(headers)

    data_rows = []
    for line in lines[4:]:  # skip header lines (adjust if needed)
        columns = re.split(r'\s{2,}', line.strip())

        # Normalize length to expected columns by adding empty strings if needed
        if len(columns) < expected_cols:
            columns += [''] * (expected_cols - len(columns))
        elif len(columns) > expected_cols:
            # Sometimes extra splits happen; you can join extra columns back or slice
            columns = columns[:expected_cols]

        data_rows.append(columns)

    df = pd.DataFrame(data_rows, columns=headers)

    df['Date'] = pd.to_datetime(df['Date'], format='%d.%m.%Y', errors='coerce')  # Converts and handles errors

    usaAthletes = df[df['Country'] == 'USA']

    cutoff_date = pd.to_datetime('1965-09-01')
    before_cutoff = df[df['Date'] < cutoff_date]

    usaCutoff = df[(df['Country'] == 'USA') & (df['Date'] < cutoff_date)]


    #print("Number of columns displayed:", usaCutoff.shape[0])

    #print(df)

#=============================================================================================

    def dynamic_filter(df, start_index=0):
        pointer = start_index

        while pointer < len(df):
            reference_date = df.iloc[pointer]['Date']
            print(f"\nPointer at row {pointer}, Date = {reference_date.date()}")

            # Filter rows before this date
            filtered = df[df['Date'] < reference_date]

            if not filtered.empty:
                # Print all filtered rows one by one:
                for idx, row in filtered.iterrows():
                    print(f"Row index {idx}:", row.to_dict())
            else:
                print("No rows before this date.")

            # Move pointer dynamically to next row with date before reference_date
            next_rows = df[(df.index > pointer) & (df['Date'] < reference_date)]

            if next_rows.empty:
                break

            pointer = next_rows.index[0]


    # Call the function starting at row 0
    print(dynamic_filter(df))

except requests.exceptions.RequestException as e:
    print(f"Error fetching the page: {e}")