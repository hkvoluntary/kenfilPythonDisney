import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL of the page with the table
url = 'https://en.wikipedia.org/wiki/List_of_countries_by_GDP_(nominal)'

# Send a GET request to the page
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the page content
    soup = BeautifulSoup(response.text, 'html.parser')
    #print(soup.prettify())

    # Find the table with GDP data (the table is under the class "wikitable")
    table = soup.find('table', class_='wikitable')
    #print(table)

    # Extract table headers
    headers = []
    headers = [header.text.strip() for header in table.find_all('th')]

    ##
    # ValueError: 10 columns passed, passed data had 7 columns
    ##
    #for header in table.find_all('th'):
    #    colspan = int(header.get('colspan', 1))
    #    if colspan == 1:
    #        headers.append(header.text.strip())

    print("Headers:", headers)


    # Extract table rows
    rows = table.find_all('tr')[1:]  # Skip the header row

    # Initialize lists to hold row data
    data = []
    for row in rows:
        cells = row.find_all('td')
        if len(cells) > 0:
            row_data = [cell.text.strip() for cell in cells]
            print("Row data:", row_data)
            data.append(row_data)
    # Create a DataFrame from the data
    df = pd.DataFrame(data, columns=headers)

    # Print the DataFrame
    print(df.head())

    # Save the DataFrame to a CSV file
    df.to_csv('gdp_data.csv', index=False)

else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")

