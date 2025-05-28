import pandas as pd
import requests
import json
import csv
from config import URL
from bs4 import BeautifulSoup

# Fetch the url page
url=URL
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")

# Find the first sortable table
table = soup.find("table", attrs={"class": "sortable"})
trs = table.find_all("tr")

# Extract and clean column headers
columns = [th.text.strip() for th in trs[0].find_all("th")]
columns[-1] = "Link"  # Rename 'Ref.' to 'Link'
if len(columns) >= 7:
    columns[6] = "AttendanceMode"  # Rename the 7th column

# Function to extract a row of data
def extract_row(tr):
    row_soup_list = tr.find_all("td")
    row = [td.text.strip() for td in row_soup_list]

    # Ensure the row has the same length as headers
    while len(row) < len(columns):
        row.append("")

    # Extract the second link in the second <td> if available
    try:
        link_tag = row_soup_list[1].find_all('a')[1]
        href = link_tag["href"].lstrip('/')
        row[-1] = f"https://en.wikipedia.org/{href}"
    except (IndexError, KeyError, AttributeError):
        row[-1] = ""

    return row

# Extract all data rows
data = [extract_row(tr) for tr in trs[1:] if tr.find_all("td")]

# Save to CSV
with open("universities.csv", "w", newline='', encoding='utf-8') as f:
    csvwriter = csv.writer(f)
    csvwriter.writerow(columns)
    csvwriter.writerows(data)

# Save to JSON
with open("universities.json", "w", encoding='utf-8') as f:
    json.dump(data, f, indent=4, ensure_ascii=False)

print("Data extracted successfully from the website")